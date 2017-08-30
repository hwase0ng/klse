#!/usr/bin/python
# Coded by Daniel Fernandez
# mechanicalForex.com, asirikuy.com 2015

import struct
from time import sleep
import time
import pandas as pd
import datetime
import argparse

HEADER_SIZE = 148
OLD_FILE_STRUCTURE_SIZE = 44
NEW_FILE_STRUCTURE_SIZE = 60

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    parser.add_argument('-ty', '--filetype')
    args = parser.parse_args()

    filename = args.filename
    filetype = args.filetype
    
    if filename == None:
        print "Enter a valid filename (-f)"
        quit()
        
    if filetype != "new" and filetype != "old":
        print "Enter a valid filetype (valid options are old and new)"
        quit()

    read = 0
    openTime = []
    openPrice = []
    lowPrice = []
    highPrice = []
    closePrice = []
    volume = []

    with open(filename, 'rb') as f:
        while True:
            
            if read >= HEADER_SIZE:
            
                if filetype == "old":
                    buf = f.read(OLD_FILE_STRUCTURE_SIZE)
                    read += OLD_FILE_STRUCTURE_SIZE        
                         
                if filetype == "new":
                    buf = f.read(NEW_FILE_STRUCTURE_SIZE)
                    read += NEW_FILE_STRUCTURE_SIZE
                    
                if not buf:
                    break
                    
                if filetype == "old":
                    bar = struct.unpack("<iddddd", buf)
                    openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
                    openPrice.append(bar[1])
                    highPrice.append(bar[3])
                    lowPrice.append(bar[2])
                    closePrice.append(bar[4])
                    volume.append(bar[5])  
                if filetype == "new":
                    bar = struct.unpack("<Qddddqiq", buf)
                    openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
                    openPrice.append(bar[1])
                    highPrice.append(bar[2])
                    lowPrice.append(bar[3])
                    closePrice.append(bar[4])
                    volume.append(bar[5])  
                                              
            else:           
                buf = f.read(HEADER_SIZE)
                read += HEADER_SIZE
                
    data = {'0_openTime':openTime, '1_open':openPrice,'2_high':highPrice,'3_low':lowPrice,'4_close':closePrice,'5_volume':volume}
     
    result = pd.DataFrame.from_dict(data)
    result = result.set_index('0_openTime')
    print result
     
    result.to_csv(filename+'_.csv', header = False)   
        
        
##################################
###           MAIN           ####
##################################

if __name__ == "__main__": main()