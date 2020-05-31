#!/usr/bin/python3

import bua_parser as bua

if __name__ == '__main__':
    
    bl = bua.create_bua_list()
    print("BUAs Loaded.")
    print("Processing...")
    for b in bl:
        b.process()
    print("BUAs Processed.")
    bua.to_csv(bl)
