from greedy1 import get_cardinalities, greedy1
from prepared_data import get_queries_names
import random

def greedy3(seed, baseline=True, num_modifications=1, modification=1):

    #random.seed(1)

    original_cardinalities = get_cardinalities(seed)
    join_orderings = {}
    queries = get_queries_names('scale')

    # Queries with 1 join or less will be the same as greedy1
    basic_joins = greedy1(seed)

    for query in original_cardinalities:
        
        '''
        print("QUERY", query)
        print(queries[query])
        print()
        '''

        # At max 1 join (less than 3 relations)
        if len(original_cardinalities[query]) < 3:
            join_orderings[query] = basic_joins[query]

        # More than 1 join 
        else:
            current_query_orderings = {}

            # Use each relation in query as starting one
            for relation in original_cardinalities[query]:
                relations_left = original_cardinalities[query].copy()
                best_order = relation
                current_cost = original_cardinalities[query][relation]
                relations_left.pop(best_order)
                #print("STARTING RELATION IS", relation)
                #print("RELATIONS LEFT:", relations_left)
                
                # Use all relations in query
                while len(relations_left) != 0:
                    current_options = {}

                    # Assign a cost to possible next options
                    for table in relations_left:                    
                        new_key = best_order + ',' + table
                        if not baseline and query % num_modifications == 0:
                            current_options[new_key] = random.randint(0, round(modification * current_cost * original_cardinalities[query][table]))
                        elif not baseline and num_modifications < 2 and float(query) % num_modifications != 0.0:
                            current_options[new_key] = random.randint(0, round(modification * current_cost * original_cardinalities[query][table]))
                        else:
                            current_options[new_key] = random.randint(0, current_cost * relations_left[table])
                    
                    #print("CURRENT OPTIONS ARE:", current_options)

                    # Choose best option available
                    best_order = min(current_options, key=current_options.get)
                    current_cost = current_options[best_order]
                    current_options.pop(best_order)
                    last_added_relation = best_order.split(',')[-1]
                    relations_left.pop(last_added_relation)
                    
                    #print("BEST COST IS", current_cost, "WITH ORDER", best_order)
                    #print("RELATIONS LEFT", relations_left)

                current_query_orderings[best_order] = current_cost
            
            join_orderings[query] = min(current_query_orderings, key=current_query_orderings.get).split(',')
        
        '''
        print(join_orderings[query])   
        print("----------------------------------")
        '''

    return join_orderings


if __name__ == "__main__":
    print(greedy3())