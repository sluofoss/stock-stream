from awslamdba import get_symbols_data_multi, check_symbols_info_multi
from source import Source

import os, yaml

if __name__ == '__main__':
    curr_path = os.path.abspath(os.path.dirname(__file__))
    #with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
    #    symbols = yaml.safe_load(file)
    #    symbols = symbols['asx200']
    import pandas as pd
    df = pd.read_csv("./ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv") 
    #print(df)   
    symbols = [x+'.AX' for x in df['ASX code']]

    if False:
        for s in symbols: 
            if len(s)> 6:
                print(s)
    import time
    if True:
        print("Test Info fetch speed")
        for max_worker in [20,30,50]:
            print("---------------------", flush=True)
            print("number of thread:", max_worker, flush=True)
            s = time.time()
            check_symbols_info_multi(symbols, max_worker=max_worker, print_data=True)
            #get_symbols_data_multi(symbols, max_worker=max_worker, print_data=True)
            e = time.time()
            print("time:", e-s, flush=True)
        
    if False:
        for max_worker in [1,10,20,30,50]:
            print("---------------------", flush=True)
            print("number of thread:", max_worker, flush=True)
            s = time.time()
            check_symbol_info_multi(max_worker=max_worker)
            e = time.time()
            print("time:",e-s, flush=True)
        
        print("---------------------")
        print("no thread only loop", flush=True)
        s = time.time()    
        check_symbol_info_loop()
        e = time.time()
        print("time:", e-s, flush=True)