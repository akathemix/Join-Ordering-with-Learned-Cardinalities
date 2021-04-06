from itertools import permutations
import csv

# Load queries
def read_write_to_csv(file_name):

    tables = []
    joins = []
    predicates = []
    label = []
    ops = []

    with open("workloads/" + file_name + ".csv", 'rU') as f:
        data_raw = list(list(rec) for rec in csv.reader(f, delimiter='#'))
        for row in data_raw:
            tables.append(row[0].split(','))

            # First n-1 tables
            if len(row[0].split(',')) > 1:
                ta = row[0].split(',')[:-1]

            # Nth table
            tb = row[0].split(',')[-1] + '#'
            
            joins.append(row[1].split(','))

            # 1st join which will be concatenated with tb
            ja = row[1].split(',')[0]
            result = ta + [tb + ja]            

            if len(row[1].split(',')) == 1:
                result[-1] += '#'
            else:
                for i in range(1, len(row[1].split(','))):
                    # Reached last element
                    if i == len(row[1].split(',')) - 1:
                        jlast = row[1].split(',')[i] + '#'
                        result += [jlast]
                    else:
                        result += [row[1].split(',')[i]]

            predicates.append(row[2].split(','))

            # 1st predicate which will be concatenated with result
            pa = row[2].split(',')[0]
            result[-1] += pa    

            if len(row[2].split(',')) == 1:
                result[-1] += '#'
            else:
                for i in range(1, len(row[2].split(','))):
                    # Reached last element
                    if i == len(row[2].split(',')) - 1:
                        plast = row[2].split(',')[i] + '#'
                        result += [plast]
                    else:
                        result += [row[2].split(',')[i]]

            if int(row[3]) < 1:
                print("Queries must have non-zero cardinalities")
                exit(1)
            label.append(row[3])
            
            # Add label to result
            result[-1] += row[3]

            ops.append(result)

    '''
    with open("test_writing2.csv", 'w', newline='') as tw:
        writer = csv.writer(tw, delimiter=',')
        for op in ops:
            writer.writerow(op)
    '''
    '''
    for op in ops:
        print(op)
    #print("Loaded queries")
    '''
    return tables, joins, predicates, label

####################################################################
####################################################################
####################################################################

def prepare_predicates(predicates):
    prepared_predicates = []

    for pred in predicates:
        if len(pred) % 3 != 0:
            continue
        current_predicate = []

        for i in range(0, len(pred), 3):
            current_predicate.append(''.join(pred[i:i+3]))

        prepared_predicates.append(current_predicate)

    return prepared_predicates

####################################################################
####################################################################
####################################################################

# First example of job light
# ops = ['t.id=mc.movie_id', 't.id=mi_idx.movie_id', 'mi_idx.info_type_id=112', 'mc.company_type_id=2']

def generate_permutations(joins, labels):
    
    ops = []

    for i in range(len(joins)):
        ops.append(joins[i])
        #ops.append(joins[i] + predicates[i])

    
    # Dictionary to keep track of each query's subqueries
    perms = {}

    # My own labelling
    label = 1
    subqueries_to_call = {}
    # Iterate through entire list of operations
    p = open("permutations_joins_only.txt", 'w')

    for i in range(len(ops)):
        #print(ops[i])
        p.write("LOOKING AT THE FOLLOWING OPERATIONS FROM QUERY " + labels[i] + '\n')
        if labels[i] not in subqueries_to_call:
            subqueries_to_call[labels[i]] = {}
        
        # Iterate through each query
        if len(ops[i]) == 1:
            p.write("%s\n" % ops[i])
            p.write("SUBQUERIES OF SIZE " + str(1) + '\n')
            # Generate subsets of all possible sizes for current operation
            for subset in permutations(ops[i], 1):
                if 1 not in subqueries_to_call[labels[i]]:
                    subqueries_to_call[labels[i]][1] = set()

                # Key format: label--length
                key = ','.join(list(subset))
                #print(key)
                if key not in perms.keys():
                    perms[key] = label
                    label += 1
                
                subqueries_to_call[labels[i]][1].add(perms[key])
                p.write("LABEL: " + str(perms[key]) + " -------  " + key + '\n')

            p.write('\n')

        else:


            for j in range(1, len(ops[i])):
                
                p.write("%s\n" % ops[i])
                p.write("SUBQUERIES OF SIZE " + str(j) + '\n')
                #print("JOIN ORDERINGS OF SIZE", j)

                # Generate subsets of all possible sizes for current operation
                for subset in permutations(ops[i], j):
                    if j not in subqueries_to_call[labels[i]]:
                        subqueries_to_call[labels[i]][j] = set()

                    
                    # Key format: label--length
                    key = ','.join(list(subset))
                    #print(key)
                    if key not in perms.keys():
                        perms[key] = label
                        label += 1
                    
                    subqueries_to_call[labels[i]][j].add(perms[key])
                    p.write("LABEL: " + str(perms[key]) + " -------  " + key + '\n')

                p.write('\n')

    p.close()
    #print(subqueries_to_call['3243247'])
    '''  
    print("--------------------------------")
    print("--------------------------------")
                
    print(len(perms), "TOTAL JOIN ORDERING SEQUENCES")
    print("--------------------------------")
    print("--------------------------------")
    '''

    return perms

####################################################################
####################################################################
####################################################################


def find_tables(perms):

    relations_dict = {'t':'title t', 'mk':'movie_keyword mk', 'mc':'movie_companies mc', 'mi':'movie_info mi', 'mi_idx':'movie_info_idx mi_idx', 'ci':'cast_info ci'}
    generated_tables = {}

    # Iterate through all keys
    for key in perms:
        if key not in generated_tables:
            generated_tables[key] = []
        # Iterate through all subqueries
        #print("KEY IS", key)
        # Iterate through elements left and right of '='
        for elem in key.split('='):
            #print(elem)
            # FIND INDEX OF '.'
            if not elem.isdigit():
                full_stop_idx = elem.index('.')
                if relations_dict[elem[:full_stop_idx]] not in generated_tables:
                    generated_tables[key].append(relations_dict[elem[:full_stop_idx]])

    return generated_tables

def put_everything_together():

    file_name = 'job-light'
    # JOINS FORMAT --- ['t.id=mc.movie_id', 't.id=mi_idx.movie_id']
    joins = read_write_to_csv(file_name)[1]

    # LABEL FORMAT --- 715
    labels = read_write_to_csv(file_name)[3]

    perms = generate_permutations(joins, labels)
    tables = find_tables(perms)

    rows = []

    for p in perms:
        current_label = '##' + str(perms[p])
        current_tables = tables[p]
        current_tables[-1] += '#'

        if ',' in p:
            p_split = p.split(',')
            current_tables[-1] += p_split[0]
            p_split = p_split[1:]
            p_split[-1] += current_label
            row = current_tables + p_split
        else:
            current_tables[-1] += p + current_label
            row = current_tables

        rows.append(row)
        print(row)

    return rows
    
def final_writing(rows):

    with open("final_writing.csv", 'w', newline='') as tw:
        writer = csv.writer(tw, delimiter=',')
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":

    file_name = 'scale'
    tables, joins, predicates, labels = read_write_to_csv(file_name)

    for i in range(len(tables)):
       print(i+1, "---", (joins[i]))

        
        