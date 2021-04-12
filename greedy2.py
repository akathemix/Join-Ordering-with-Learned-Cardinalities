from greedy1 import get_cardinalities, greedy1
from prepared_data import get_queries_names
import random

def greedy2(seed, baseline=True, num_modifications=1, modification=1):

    #random.seed(2)
    
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
            '''
            print("NO OPERATIONS NEEDED:", join_orderings[query])
            print("---------------------------------------")
            '''

        # More than 1 join 
        else:
            # Get starting relation
            best_order = min(original_cardinalities[query], key=original_cardinalities[query].get)
            current_cost = original_cardinalities[query][best_order]
            original_cardinalities[query].pop(best_order)
            
            '''
            #print("STARTING RELATION IS", best_order)
            #print("REMAINING RELATIONS", original_cardinalities[query])
            '''
            
            while len(original_cardinalities[query]) != 0:
                current_options = {}
                for table in original_cardinalities[query]:                    
                    new_key = best_order + ',' + table
                    if not baseline and query % num_modifications == 0:
                        current_options[new_key] = random.randint(0, round(modification * current_cost * original_cardinalities[query][table]))
                    elif not baseline and num_modifications < 2 and float(query) % num_modifications != 0.0:
                        current_options[new_key] = random.randint(0, round(modification * current_cost * original_cardinalities[query][table]))
                    else:
                        current_options[new_key] = random.randint(0, current_cost * original_cardinalities[query][table])
                
                '''
                #print("CURRENT OPTIONS ARE", current_options)
                '''

                best_order = min(current_options, key=current_options.get)
                current_cost = current_options[best_order]
                current_options.pop(best_order)
                last_added_relation = best_order.split(',')[-1]
                original_cardinalities[query].pop(last_added_relation)
                
                '''
                #print("BEST ORDER IS", best_order)
                #print("REMAINING RELATIONS", original_cardinalities[query])
                '''

            join_orderings[query] = best_order.split(',')

        '''
        print(join_orderings[query])
        print("---------------------------------------------------")
        '''
        
    return join_orderings


                
if __name__ == "__main__":
    (greedy2())