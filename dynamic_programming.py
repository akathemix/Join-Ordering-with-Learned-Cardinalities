from greedy1 import get_cardinalities, greedy1
from prepared_data import get_queries_names
from itertools import permutations
import random

def dynamic_programming(seed):
    
    #random.seed(1)

    basic_cardinalities = get_cardinalities(seed)
    join_orderings = {}
    queries = get_queries_names('scale')
    
    # Queries with 1 join or less will be the same as greedy1
    basic_joins = greedy1(seed)

    for query in basic_cardinalities:
        final_join = ','.join(sorted(list(basic_cardinalities[query].keys())))

        '''
        print("QUERY", query)
        print(queries[query])
        print()
        
        print("RELATIONS OF INTEREST ARE", basic_cardinalities[query])
        print()
        '''
        
        # At max 1 join (less than 3 relations)
        if len(basic_cardinalities[query]) < 3:
            join_orderings[query] = basic_joins[query]

        # More than 1 join 
        else:
            cardinalities_of_interest = {}

            # Joins of length 2
            for relation in basic_cardinalities[query]:
                cardinalities = basic_cardinalities[query].copy()
                cardinalities.pop(relation)
                for r in cardinalities:
                    key = relation + ',' + r
                    key_as_list = key.split(',')
                    sorted_key = sorted(key_as_list)

                    if ','.join(sorted_key) not in cardinalities_of_interest:
                        # (cost, bestorder)
                        cardinalities_of_interest[','.join(sorted_key)] = (random.randint(0, basic_cardinalities[query][relation]*basic_cardinalities[query][r]), ','.join(sorted_key))
            
            seen_subsets = set()
            
            '''
            print("BUILD ON:", cardinalities_of_interest)
            '''

            for i in range(3, len(cardinalities)+2):

                for relation in cardinalities_of_interest.copy():
                    
                    relations_left = basic_cardinalities[query].copy()
                    
                    # Find which relations are left to append
                    for used_relation in relation.split(','):
                        relations_left.pop(used_relation)
                    
                    for unused_relation in relations_left:
                        key = relation + ',' + unused_relation
                        key_as_list = key.split(',')
                        if ','.join(sorted(key_as_list)) in seen_subsets:
                            continue
                        
                        '''
                        print("RELATION TO BUILD ON:", relation)
                        print("RELATIONS TO ADD", list(relations_left.keys()))
                        print("RELATIONS CONSIDERED", key, "WITH SORTED KEY", ','.join(sorted(key_as_list)))
                        print()
                        '''

                        # Want to find least-expensive i-1 subset
                        subset_found = False
                        left_outs = {}
                        for permutation in permutations(key_as_list, i-1):
                            subset = ','.join(list(permutation))
                            if subset in cardinalities_of_interest:
                                left_out = [table for table in key_as_list if table not in list(permutation)][0]
                                left_outs[subset] = left_out
                                
                                '''
                                print("POSSIBLE MIN SUBSET FOR SUBSET", subset, "IS", cardinalities_of_interest[subset])
                                print("LEAVING OUT", left_out)
                                '''

                                if not subset_found:
                                    min_subset = cardinalities_of_interest[subset]
                                    subset_found = True
                                else:
                                    if cardinalities_of_interest[subset] < min_subset:
                                        min_subset = cardinalities_of_interest[subset]
                        
                        sorted_min_subset = ','.join(sorted(min_subset[1].split(',')))
                        cardinalities_of_interest[','.join(sorted(key_as_list))] = (random.randint(0, min_subset[0]*basic_cardinalities[query][left_outs[sorted_min_subset]]), min_subset[1] + ',' + left_outs[sorted_min_subset])
                        seen_subsets.add(','.join(sorted(key_as_list)))
                        
                        '''
                        print("BEST ORDER:", min_subset[1] + ',' + left_outs[sorted_min_subset], "WITH COST", min_subset[0])
                        print("CARDINALITIES OF INTEREST", cardinalities_of_interest)
                        print("SEEN SUBSETS", seen_subsets)
                        print()
                        '''
                        
                # When you've examined all orders of length i, remove those of i-1
                for order in list(cardinalities_of_interest.keys()):
                    if len(order.split(',')) == i-1:
                        cardinalities_of_interest.pop(order)
                        
                        
            join_orderings[query] = cardinalities_of_interest[final_join][1].split(',')
        
        '''
        # Print best order for query
        print(join_orderings[query])
        print("COST", cardinalities_of_interest[final_join][0])
        print("-------------------------------")
        '''

    return join_orderings

if __name__ == "__main__":
    print(dynamic_programming())

