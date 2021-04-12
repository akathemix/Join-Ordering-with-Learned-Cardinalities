from greedy1 import greedy1
from greedy2 import greedy2
from greedy3 import greedy3
from dynamic_programming import dynamic_programming

def greedy1_compare(seed):

    g1 = greedy1(seed)
    g2 = greedy2(seed)
    g3 = greedy3(seed)
    dp = dynamic_programming(seed)

    g1_match_g2 = 0
    g1_match_g3 = 0
    g1_match_dp = 0
    
    for query in g1:
        if g1[query] == g2[query]:
            g1_match_g2 += 1

        if g1[query] == g3[query]:
            g1_match_g3 += 1

        if g1[query] == dp[query]:
            g1_match_dp += 1

    return g1_match_g2/len(g1), g1_match_g3/len(g1), g1_match_dp/len(g1)

def greedy2_compare(seed):

    g1 = greedy1(seed)
    g2 = greedy2(seed)
    g3 = greedy3(seed)
    dp = dynamic_programming(seed)

    g2_match_g3 = 0
    g2_match_dp = 0
    
    for query in g2:
        if g2[query] == g3[query]:
            g2_match_g3 += 1

        if g2[query] == dp[query]:
            g2_match_dp += 1

    return g2_match_g3/len(g2), g2_match_dp/len(g2)

def greedy3_compare(seed):

    g1 = greedy1(seed)
    g2 = greedy2(seed)
    g3 = greedy3(seed)
    dp = dynamic_programming(seed)

    g3_match_dp = 0
    
    for query in g3:
        if g3[query] == dp[query]:
            g3_match_dp += 1

    return g3_match_dp/len(g3)

if __name__ == "__main__":

    baseline_results = {}
    no_baseline_results = {}
    dp_results = {}

    num_of_modifications = [4/3, 3/2, 2,3,4,5,10]
    modifications = [0.25,0.5,0.75,1.25,1.5,2,10]
    
    for i in range(1, 11):
        baseline_results[i] = greedy3(i)
        dp_results[i] = dynamic_programming(i)
        for nm in num_of_modifications:
            for mod in modifications:
                key = "% OF MODS: " + str(round(100/nm)) + " --- MOD: x" + str(mod)
                #print(str(nm), "--", str(mod))
                if i not in no_baseline_results:
                    no_baseline_results[i] = {}
                elif key not in baseline_results[i]:
                    no_baseline_results[i][key] = greedy3(i, baseline=False, num_modifications=nm, modification=mod)
     
    greedy2_self_average = {}
    dp_average = {}
    
    # Through seeds
    for i in range(1, len(baseline_results)+1):
        for key in no_baseline_results[i]:
            no_baseline_match = 0
            dp_match = 0
            for j in range(1, len(no_baseline_results[i][key]) + 1):
                if baseline_results[i][j] == no_baseline_results[i][key][j]:
                    no_baseline_match += 1

                if dp_results[i][j] == no_baseline_results[i][key][j]:
                    dp_match += 1

                
            greedy2_self_average[key] = no_baseline_match / len(baseline_results[i])
            dp_average[key] = dp_match / len(baseline_results[i])

            print(key)
            ###################### Change below
            print("AVERAGE MATCH --", greedy2_self_average[key])
            print()

    print("----------------------------")
    print("----------------------------")
    print("----------------------------")
    print()

    average_difference = 0

    '''
    for key in greedy2_self_average:
        average_difference += greedy2_self_average[key]

    print("AVERAGE MATCH BETWEEN GREEDY2 AND GREEDY2 MODIFIED PLANS:", average_difference / len(greedy2_self_average))

    '''
    for key in dp_average:
        average_difference += dp_average[key]

    print("AVERAGE MATCH BETWEEN DP AND GREEDY2 MODIFIED PLANS:", average_difference / len(dp_average))