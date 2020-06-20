from bs4 import BeautifulSoup
import requests
import os
import sys
import scrapper
import Insert_data

#Remove the cvs file if already exist
if os.path.isfile('./csv_file.csv'):
    os.remove('./csv_file.csv')

#Pass in all link in all page

# start_url='https://www.rockchipfirmware.com/'
start_url= sys.argv[1]
number_page='firmware-downloads'
nextpage= True
while nextpage:
    r = requests.get(start_url + number_page)
    soup = BeautifulSoup(r.text, 'lxml')

    link_download = soup.findAll("td", {"class":"views-field views-field-title"})
    for link in link_download:
        scrapper.page_download(start_url + link.find('a')['href'])
    print(start_url+number_page)
        
    try:
        next_div=soup.find("li", {"class": "pager-next last"})
        number_page = next_div.find('a')['href']
    except Exception as e:
        break
    

#Import data in MongoDB
Insert_data.import_data()

