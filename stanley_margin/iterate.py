
import time
import datetime
import argparse
import copy
import itertools

# variables
time = [5, 15, 30, 120, 240]
fast = [3, 5, 8, 12, 15]
mid = [1.5,2,3,5,10]
slow = [2,3,4,6]


#fast,mid,slow,time
# functions
def count_test(fast,mid,slow,time):
    count = len(fast)*len(mid)*len(slow)*len(time)
    return count

def generate_fmst(f,m,s,t):
    print(str(f))
    fmst = [f,f*m,f*m*s,t]
    return fmst

def generate_fmst_test(test):
    #print(str(f))
    fmst = [test[0],test[0]*test[1],test[0]*test[1]*test[2],test[3]]
    return fmst

def calc_profit(fmst):
    profit = fmst[0] + fmst[1] + fmst[2] + fmst[3]
    print("Profit: " + str(profit))
    return profit

def explicit(l):
    max_val = max(l)
    max_idx = l.index(max_val)
    return max_idx, max_val

def generate_test(fast,mid,slow,time):
    test = itertools.product(fast,mid,slow,time)
    return test


# main
if __name__ == "__main__":
    i = 0
    fmst = []
    test = generate_test(fast,mid,slow,time)

    test_count = len(list(test))
    profit = [0]*test_count

    print('--------------')
    current_time = datetime.datetime.now()
    print("Date Time:%s  " % (current_time))
    print("Test count:%s  " % (test_count))
    #print("Test:%s  " % (test.head()))

    fmst = generate_fmst(2,3,4,5)
    print("Test:%s  " % (test))

    while i < 3 :
        print("i :%s  " % (i))

        for x in test:
            print(x)
            fmst = generate_fmst(x[0],x[1],x[2],x[3])
            print(fmst)
            profit[i] = calc_profit(fmst)

        i=i+1

    max_idx, max_val = explicit(profit)
    print("Max idx: " + str(max_idx))
    print("Max val: " + str(max_val))


    print('--------------')
