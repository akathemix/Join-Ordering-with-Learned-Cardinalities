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

    '''
    greedy1_vs_greedy2 = []
    greedy1_vs_greedy3 = []
    greedy1_vs_dp = []
    greedy2_vs_greedy3 = []
    greedy2_vs_dp = []
    greedy3_vs_dp = []
    '''

    greedy1_dicts = []
    greedy1_dicts_no_baseline = []

    '''
    greedy2_dicts = []
    greedy3_dicts = []
    dp_dicts = []
    '''

    for i in range(1, 11):
        greedy1_dicts.append(greedy1(i))
        greedy1_dicts_no_baseline.append(greedy1(i,baseline=False))
        '''
        greedy2_dicts.append(greedy2(i))
        greedy3_dicts.append(greedy3(i))
        dp_dicts.append(dynamic_programming(i))
        '''

    
    results = []
    for i in range(len(greedy1_dicts)):
        no_baseline_match = 0
        for query in greedy1_dicts[i]:
            if greedy1_dicts[i][query] == greedy1_dicts_no_baseline[i][query]:
                no_baseline_match += 1

        results.append(no_baseline_match/len(greedy1_dicts[i]))

    print("GREEDY 1 WITH 50% MODIFIED BY 25%")
    print(results)
    print()
    print("AVERAGE MATCH:", sum(results)/len(results))

    

    '''
    # Seeds 1-10
    for i in range(1, 11):
        greedy1_vs_greedy2.append(greedy1_compare(i)[0])
        greedy1_vs_greedy3.append(greedy1_compare(i)[1])
        greedy1_vs_dp.append(greedy1_compare(i)[2])
        greedy2_vs_greedy3.append(greedy2_compare(i)[0])
        greedy2_vs_dp.append(greedy2_compare(i)[1])
        greedy3_vs_dp.append(greedy3_compare(i))

    print("AVERAGE MATCH - GREEDY1 VS GREEDY2:", sum(greedy1_vs_greedy2) / len(greedy1_vs_greedy2))
    print("AVERAGE MATCH - GREEDY1 VS GREEDY3:", sum(greedy1_vs_greedy3) / len(greedy1_vs_greedy3))
    print("AVERAGE MATCH - GREEDY1 VS DP:", sum(greedy1_vs_dp) / len(greedy1_vs_dp))
    print("AVERAGE MATCH - GREEDY2 VS GREEDY3:", sum(greedy2_vs_greedy3) / len(greedy2_vs_greedy3))
    print("AVERAGE MATCH - GREEDY2 VS DP:", sum(greedy2_vs_dp) / len(greedy2_vs_dp))
    print("AVERAGE MATCH - GREEDY3 VS DP:", sum(greedy3_vs_dp) / len(greedy3_vs_dp))
    print()

    print("MAX/MIN - GREEDY1 VS GREEDY2:", max(greedy1_vs_greedy2), min(greedy1_vs_greedy2))
    print("MAX/MIN - GREEDY1 VS GREEDY3:", max(greedy1_vs_greedy3), min(greedy1_vs_greedy3))
    print("MAX/MIN - GREEDY1 VS DP:", max(greedy1_vs_dp), min(greedy1_vs_dp))
    print("MAX/MIN - GREEDY2 VS GREEDY3:", max(greedy2_vs_greedy3), min(greedy2_vs_greedy3))
    print("MAX/MIN - GREEDY2 VS DP:", max(greedy2_vs_dp), min(greedy2_vs_dp))
    print("MAX/MIN - GREEDY3 VS DP:", max(greedy2_vs_dp), min(greedy3_vs_dp))
    print()
    
    print("MATCH PERCENTAGE - GREEDY1 VS GREEDY2:", greedy1_vs_greedy2)
    print("MATCH PERCENTAGE - GREEDY1 VS GREEDY3:", greedy1_vs_greedy3)
    print("MATCH PERCENTAGE - GREEDY1 VS DP:", greedy1_vs_dp)
    print("MATCH PERCENTAGE - GREEDY2 VS GREEDY3:", greedy2_vs_greedy3)
    print("MATCH PERCENTAGE - GREEDY2 VS DP:", greedy2_vs_dp)
    print("MATCH PERCENTAGE - GREEDY3 VS DP:", greedy3_vs_dp)
    '''
    


    
    
    

