from bs4 import BeautifulSoup
import requests
import os
import re
import csv

def download(start_url):

    if not os.path.exists('./firmwares'):
        os.makedirs('./firmwares')
    number_page='firmware-downloads'

    # Pass in all pages
    while True:
        r = requests.get(start_url + number_page)
        soup_pages = BeautifulSoup(r.text, 'lxml')
        link_download = soup_pages.findAll("td", {"class":"views-field views-field-title"})

        # Pass in all links
        for link in link_download:
            url = start_url+link.find('a')['href']
            new_url = url.replace('\\','/')
            r = requests.get(new_url)
            soup = BeautifulSoup(r.text, 'lxml')
            name_device = soup.find("div",{"class":"field field-name-title field-type-ds field-label-hidden"}).h2.text
            name_d= re.sub(r"[/*|\":<>?\\]","",name_device)

            # Find the download link
            downloads = soup.find("span",{"class":"file"})
            if downloads == None :
                downloads = soup.find("div",{"class":"field field-name-field-firmware-image-download field-type-text field-label-above"})
                if downloads == None :
                    continue

            # Download
            if not os.path.exists('./firmwares/'+ name_d +'.zip'):
                print("Downloading... " + name_d +'.zip')
                req = requests.get(downloads.find('a')['href'])
                with open('./firmwares/'+ name_d +'.zip','wb') as f:
                    f.write(req.content)
            
        try:
            next_div=soup_pages.find("li", {"class": "pager-next last"})
            number_page = next_div.find('a')['href']
        except Exception as e:
            break