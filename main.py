from bs4 import BeautifulSoup
import requests
import os
import sys
import download
import fetch_metadata
import multiprocessing

#start_url='https://www.rockchipfirmware.com/'
start_url=sys.argv[1]
if __name__ == "__main__": 
    # creating processes 
    p1 = multiprocessing.Process(target=fetch_metadata.fetch_metadata, args=(start_url,))
    p2 = multiprocessing.Process(target=download.download, args=(start_url,)) 
    
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
   
    # both processes finished 
    print("Done!") 