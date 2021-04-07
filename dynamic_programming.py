from greedy1 import greedy1_cardinalities, greedy1
from prepared_data import get_queries_names
from itertools import permutations
import random

# Use example in http://www.mathcs.emory.edu/~cheung/Courses/554/Syllabus/5-query-opt/dyn-prog-join3.html


basic_cardinalities = {'R':1000, 'S':1000, 'T':1000, 'U':1000}
final_join = ','.join(sorted(list(basic_cardinalities.keys())))

def dynamic_programming():
    
    random.seed(1)

    cardinalities_of_interest = {}

    # Joins of length 2
    for relation in basic_cardinalities:
        cardinalities = basic_cardinalities.copy()
        cardinalities.pop(relation)
        for r in cardinalities:
            key = relation + ',' + r
            key_as_list = key.split(',')
            sorted_key = sorted(key_as_list)
            if ','.join(sorted_key) not in cardinalities_of_interest:
                # (cost, bestorder)
                cardinalities_of_interest[key] = (random.randint(0, basic_cardinalities[relation]*basic_cardinalities[r]), key)
    
    #print("STARTING CARDINALITIES", cardinalities_of_interest)

    seen_subsets = set()

    for i in range(3, len(cardinalities)+2):

        for relation in cardinalities_of_interest.copy():
            #print("RELATION TO BUILD ON:", relation)
            relations_left = basic_cardinalities.copy()
            
            # Find which relations are left to append
            for used_relation in relation.split(','):
                relations_left.pop(used_relation)
            
            #print("RELATIONS TO ADD", list(relations_left.keys()))
            #print()
            for unused_relation in relations_left:
                key = relation + ',' + unused_relation
                key_as_list = key.split(',')
                if ','.join(sorted(key_as_list)) in seen_subsets:
                    continue
                
                print("RELATION CONSIDERED", key)
                
                # Want to find least-expensive i-1 subset
                subset_found = False
                left_outs = {}
                for permutation in permutations(key_as_list, i-1):
                    subset = ','.join(list(permutation))
                    if subset in cardinalities_of_interest:
                        print("POSSIBLE MIN SUBSET", cardinalities_of_interest[subset])
                        left_out = [table for table in key_as_list if table not in list(permutation)][0]
                        left_outs[subset] = left_out
                        print("LEAVING OUT", left_out)
                        if not subset_found:
                            min_subset = cardinalities_of_interest[subset]
                            subset_found = True
                        else:
                            if cardinalities_of_interest[subset] < min_subset:
                                min_subset = cardinalities_of_interest[subset]
                
                cardinalities_of_interest[key] = (random.randint(0, min_subset[0]*basic_cardinalities[left_outs[min_subset[1]]]), min_subset[1] + ',' + left_outs[min_subset[1]])
                seen_subsets.add(key)
                print("MIN SUBSET", min_subset)
                print("BEST ORDER:", min_subset[1] + ',' + left_outs[min_subset[1]])
                print("CARDINALITIES OF INTEREST", cardinalities_of_interest)
                
                
                print("-------------------------------")

        # When you've examined all orders of length i, remove those of i-1
        for order in list(cardinalities_of_interest.keys()):
            if len(order.split(',')) == i-1:
                cardinalities_of_interest.pop(order)
                
                
    print("FINAL ORDERING", cardinalities_of_interest)
    print("BEST ORDER IS", cardinalities_of_interest[final_join][1], "WITH COST", cardinalities_of_interest[final_join][0])
    
    '''
    FINAL ORDERING {'R,S,T,U': (14815451299, 'R,S,U,T')}
    BEST ORDER IS R,S,U,T WITH COST 14815451299
    '''

if __name__ == "__main__":
    dynamic_programming()

