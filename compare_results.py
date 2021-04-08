from greedy1 import greedy1
from greedy2 import greedy2
from greedy3 import greedy3
from dynamic_programming import dynamic_programming

g1 = greedy1()
g2 = greedy2()
g3 = greedy3()
dp = dynamic_programming()

def greedy1_compare():

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

def greedy2_compare():

    g2_match_g3 = 0
    g2_match_dp = 0
    
    for query in g2:
        if g2[query] == g3[query]:
            g2_match_g3 += 1

        if g2[query] == dp[query]:
            g2_match_dp += 1

    return g2_match_g3/len(g2), g2_match_dp/len(g2)

def greedy3_compare():

    g3_match_dp = 0
    
    for query in g3:
        if g3[query] == dp[query]:
            g3_match_dp += 1

    return g3_match_dp/len(g3)

if __name__ == "__main__":
    print("MATCH PERCENTAGE - GREEDY1 VS GREEDY2:", greedy1_compare()[0])
    print("MATCH PERCENTAGE - GREEDY1 VS GREEDY3:", greedy1_compare()[1])
    print("MATCH PERCENTAGE - GREEDY1 VS DP:", greedy1_compare()[2])
    print()
    print("MATCH PERCENTAGE - GREEDY2 VS GREEDY3:", greedy2_compare()[0])
    print("MATCH PERCENTAGE - GREEDY2 VS DP:", greedy2_compare()[1])
    print()
    print("MATCH PERCENTAGE - GREEDY3 VS DP", greedy3_compare())

