import random
import csv

# Load queries from csv
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
    
    for op in ops:
        print(op)
    
    print("Loaded queries")
    '''

    return tables, joins, predicates, label

# Names of queries (in SQL format)
def get_queries_names(file_name):

    tables, joins, predicates, labels = read_write_to_csv(file_name)
    queries = {}

    for i in range(len(tables)):

        # TABLES ADDED TO QUERY
        t = ','.join(tables[i])

        query = "SELECT FROM " + t + " WHERE "

        # JOINS ADDED TO QUERY
        if len(joins[i]) == 1 and joins[i][0] != '':
            query += ''.join(joins[i])
        elif len(joins[i]) == 1:
            query += ''
        elif len(joins[i]) > 1:
            query += ' AND '.join(joins[i])

        # PREDICATES ADDED TO QUERY
        if joins[i][0] == '':
            query += ''.join(predicates[i])
        elif len(predicates[i]) != 0 and len(predicates[i]) % 3 == 0:
            for j in range(0, len((predicates[i])), 3):
                current_pred = ''.join(predicates[i][j:j+3])
                query += ' AND ' + current_pred

        queries[i+1] = query

    return queries

  

if __name__ == "__main__":
    file_name = "scale"   
    print(len(get_queries_names(file_name)))