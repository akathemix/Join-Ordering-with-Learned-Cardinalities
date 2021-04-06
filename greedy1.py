from prepared_data import read_write_to_csv, get_queries_names
import random

# Cardinalities from https://github.com/andreaskipf/learnedcardinalities/blob/master/data/column_min_max_vals.csv
column_cardinalities = {
        't.id': 2528312,
        't.kind_id': 2528312,
        't.production_year': 2528312,
        'mc.id': 2609129,
        'mc.company_id': 2609129,
        'mc.movie_id': 2609129,
        'mc.company_type_id': 2609129,
        'ci.id': 36244344,
        'ci.movie_id': 36244344,
        'ci.person_id': 36244344,
        'ci.role_id': 36244344,
        'mi.id': 14835720,
        'mi.movie_id': 14835720,
        'mi.info_type_id': 14835720,
        'mi_idx.id': 1380035,
        'mi_idx.movie_id': 1380035,
        'mi_idx.info_type_id': 1380035,
        'mk.id': 4523930,
        'mk.movie_id': 4523930,
        'mk.keyword_id': 4523930
    }

column_unique_values = {
        't.id': 2528312,
        't.kind_id': 6,
        't.production_year': 133,
        'mc.id': 2609129,
        'mc.company_id': 234997,
        'mc.movie_id': 1087236,
        'mc.company_type_id': 2,
        'ci.id': 36244344,
        'ci.movie_id': 2331601,
        'ci.person_id': 4051810,
        'ci.role_id': 11,
        'mi.id': 14835720,
        'mi.movie_id': 2468825,
        'mi.info_type_id': 71,
        'mi_idx.id': 1380035,
        'mi_idx.movie_id': 459925,
        'mi_idx.info_type_id': 5,
        'mk.id': 4523930,
        'mk.movie_id': 476794,
        'mk.keyword_id': 134170
    }

# Based on http://resources.mpi-inf.mpg.de/departments/d5/teaching/ss09/queryoptimization/lecture5.pdf
# Slide 13
def greedy1_cardinalities():

    greedy1_cardinalities = {}
    random.seed(1)

    # If there is a predicate for a table, the predicate is applied on the table first
    seen_tables = {}
    predicate_idx = 0

    for predicate in read_write_to_csv('scale')[2]:
        predicate_idx += 1
        
        if len(predicate) != 0 and len(predicate) % 3 == 0:
            for i in range(0, len(predicate), 3):
                # If predicate is one of the relations where each entry is different
                if predicate[i] in ['t.id', 'mc.id', 'ci.id', 'mi.id', 'mi_idx.id', 'mk.id']:
                    # Then if operator is =, output table will only have 1 entry
                    if predicate[i+1] == '=':
                        table_cardinality = 1
                    # Then if operator is < or >
                    else:
                        table_cardinality = column_cardinalities[predicate[i]] - int(predicate[2]) - 1
                else:
                    table_cardinality = random.randint(0, column_cardinalities[predicate[i]] - column_unique_values[predicate[i]] + 1)
                
                # For each predicate, we keep the cardinality of filtering that table
                table = predicate[i].split('.')[0]

                if predicate_idx not in seen_tables:
                    seen_tables[predicate_idx] = {table:[table_cardinality]}
                elif table not in seen_tables[predicate_idx]:
                    seen_tables[predicate_idx][table] = [table_cardinality]
                elif table in seen_tables[predicate_idx]:
                    seen_tables[predicate_idx][table].append(table_cardinality)
    
    join_idx = 0
    for joins in read_write_to_csv('scale')[1]:
        join_idx += 1
        for join in joins:
            # Joins > 0
            if join != '':
                j = join.split("=")
                # If left table has predicate(s), use its max filtered cardinality
                left_table = j[0].split('.')[0]
                right_table = j[1].split('.')[0]

                if join_idx not in seen_tables:
                    greedy1_cardinalities[join_idx] = {left_table: column_cardinalities[j[0]], right_table: column_cardinalities[j[1]]}
                elif join_idx not in greedy1_cardinalities:
                    left_table_cardinality =  max(seen_tables[join_idx][left_table]) if left_table in seen_tables[join_idx] else column_cardinalities[j[0]]
                    greedy1_cardinalities[join_idx] = {left_table:left_table_cardinality}
                
                elif left_table in seen_tables[join_idx]:
                    greedy1_cardinalities[join_idx][left_table] = max(seen_tables[join_idx][left_table])
                else:
                    greedy1_cardinalities[join_idx][left_table] = column_cardinalities[j[0]]
                
                # If right table has predicate(s), use its max filtered cardinality
                if join_idx in seen_tables:
                    if right_table in seen_tables[join_idx]:
                        greedy1_cardinalities[join_idx][right_table] = max(seen_tables[join_idx][right_table])
                    else:
                        greedy1_cardinalities[join_idx][right_table] = column_cardinalities[j[1]]

            # JOINs = 0
            else:
                if join_idx not in greedy1_cardinalities:
                    greedy1_cardinalities[join_idx] = {}
                    for t in seen_tables[join_idx]:
                        if t not in greedy1_cardinalities[join_idx]:
                            greedy1_cardinalities[join_idx][t] = max(seen_tables[join_idx][t])
    
    '''
    # Normalize cardinalities between 0 and 100
    top = 1380035
    bottom = 36244344
    for key in greedy1_cardinalities:
        for key2 in greedy1_cardinalities[key]:
            if greedy1_cardinalities[key][key2] < bottom:
                bottom = greedy1_cardinalities[key][key2]
                min_key = key
            elif greedy1_cardinalities[key][key2] > top:
                top = greedy1_cardinalities[key][key2]
                max_key = key

    
    print("MIN KEY:", min_key, "WITH VAL:", bottom, "IN", greedy1_cardinalities[min_key])
    print("MAX KEY:", max_key, "WITH VAL:", top, "IN", greedy1_cardinalities[max_key])
    
    for key in greedy1_cardinalities:
        for key2 in greedy1_cardinalities[key]:
            greedy1_cardinalities[key][key2] = ((greedy1_cardinalities[key][key2] - bottom) / (top - bottom)) * 100
    
    '''

    return greedy1_cardinalities

'''
def get_joins_per_query():

    joins = read_write_to_csv('scale')[1]
    relations_per_query = {}

    for i in range(len(get_queries_names('scale'))):
        current_query = set()

        for join in joins[i]:
            if join != '':
                j = join.split("=")
                current_query.add(j[0])
                current_query.add(j[1])

        relations_per_query[i+1] = current_query

    return relations_per_query
'''

def greedy1():

    cardinalities = greedy1_cardinalities()
    query_names = get_queries_names('scale')
    join_orderings = {}

    for query in cardinalities:
        relations_of_interest = cardinalities[query].copy()
        join_order = []
                
        #print("QUERY", query)
        #print(query_names[query])
        #print()
        #print("RELATIONS OF INTEREST ARE:", relations_of_interest)
        
        while len(relations_of_interest) != 0:
            least_costly_relation = min(relations_of_interest, key=relations_of_interest.get)
            join_order.append(least_costly_relation)
            relations_of_interest.pop(least_costly_relation)
            # print("REMOVED", least_costly_relation, " --- CURRENT JOIN ORDER:", join_order)

        join_orderings[query] = join_order
        #print(join_orderings[query])
        #print("-------------------------------------------")

    return join_orderings
            
if __name__ == "__main__":
    (greedy1())