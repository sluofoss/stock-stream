from awslamdba import get_symbols_data_multi
from source import Source

import os, yaml

if __name__ == '__main__':
    curr_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
        symbols = yaml.safe_load(file)
    print(symbols['asx200'])
    import time
    if True:
        print("Test data fetch speed")
        for max_worker in [20,30,50]:
            print("---------------------", flush=True)
            print("number of thread:", max_worker, flush=True)
            s = time.time()
            get_symbols_data_multi(symbols['asx200'], max_worker=max_worker)
            e = time.time()
            print("time:",e-s, flush=True)
        
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