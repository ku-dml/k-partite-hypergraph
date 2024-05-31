import pandas as pd
import sys, time, warnings, argparse, json, itertools, functools

from collections import deque

import hypergraph    # import the code

warnings.simplefilter('ignore')

def main(fname):
    csv_filename = fname   # fname: file name of csv; e.g., "celltissue.csv"   
                           # theta_list: thresholds of sizes,
                           # the ordering is supposed to be the same as the input file
                           # i.e.,  "sex", "tissue", "celltype" for celltissue.csv

    ################
    # 1. Construct a hypergraph object
    # To construct a hypergraph, the data is required to be a pandas.DataFrame type object

    # Notice: the code is written in the way that the csv file has the same format as "celltissue.csv" 
    #         (no row indices, and the first line is column indices)
    hyperedge_list = pd.read_csv(csv_filename) # An example
    H = hypergraph.Hypergraph()
    H.create_from_DataFrame(hyperedge_list)    # (create a hypergraph object from a pd.DataFrame object)

    # 2. Construct an instance object to solve the problem
    instance = hypergraph.Hyperclique_Instance()
    theta_list = [2]*H.k
    instance.set_instance(hypergraph=H, theta_list=theta_list)  
        # (a hypergraph obejct H, and a list of theta (the thresholds) is necessary)

    # 3. Solve
    maximal_solutions_list = instance.find_maximal_solutions()
    # the result is in "maximal_clqiue_list", which will be a list of list of tuples 
    # (i.e. a maximal solution will be in the format of a list of tuples)

    return maximal_solutions_list
    ################

    

if __name__ == "__main__":
    # try:
    time_start = time.time()
    solutions = main(sys.argv[1])
    time_end = time.time()
    for c in solutions:
        for _c in c:
            print(_c)
        print()
    print(f"{len(solutions)} maximal solutions have been found.")
    print(f"Time: {time_end - time_start} sec.")
    # except:
    #     sys.stderr.write("usage: {} (filename.csv)\n".format(sys.argv[0]))
        
