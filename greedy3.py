from greedy1 import greedy1_cardinalities, greedy1
from prepared_data import get_queries_names
import random

def greedy3():

    original_cardinalities = greedy1_cardinalities()
    join_orderings = {}

    for query in original_cardinalities:
        # At max 1 join (less than 3 relations)
        if len(original_cardinalities[query]) < 3:
            join_orderings[query] = greedy1()[query]

        # More than 1 join 
        else:
            while len(original_cardinalities[query]) != 0:
                # Get starting relation of current query
                for relation in original_cardinalities[query]:
                    relations_left = original_cardinalities[query].copy()
                    best_order = relation
                    current_cost = original_cardinalities[query][relation]
                    relations_left.pop(best_order)
                    print("STARTING RELATION IS", relation)
                    print("RELATIONS LEFT:", relations_left)
                    
                    while len(relations_left) != 0:
                        current_options = {}
                        for table in relations_left:                    
                            new_key = best_order + ',' + table
                            current_options[new_key] = random.randint(0, current_cost * relations_left[table])

                        best_order = min(current_options, key=current_options.get)
                        current_options.pop(best_order)
                        last_added_relation = best_order.split(',')[-1]
                        relations_left.pop(last_added_relation)


    return




if __name__ == "__main__":
    greedy3()