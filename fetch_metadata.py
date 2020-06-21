from bs4 import BeautifulSoup
import requests
import os
import re
import insert_data
import csv


def fetch_metadata(start_url):

    if not os.path.exists('./firmwares'):
        os.makedirs('./firmwares')
    number_page='firmware-downloads'
    nextpage=True
    # Pass in all pages
    while nextpage:
        r = requests.get(start_url + number_page)
        soup_pages = BeautifulSoup(r.text, 'lxml')
        link_download = soup_pages.findAll("td", {"class":"views-field views-field-title"})

        # Pass in all links
        for link in link_download:
            url = start_url+link.find('a')['href']
            new_url = url.replace('\\','/')
            r = requests.get(new_url)
            soup = BeautifulSoup(r.text, 'lxml')

            # Find the metadata
            name_device = soup.find("div",{"class":"field field-name-title field-type-ds field-label-hidden"}).h2.text
            name_d= re.sub(r"[/*|\":<>?\\]","",name_device)
            try:
                version = soup.find("div",{"class":"field field-name-field-android-version2 field-type-taxonomy-term-reference field-label-inline clearfix"}).find("div",{"class":"field-item even"}).text
            except Exception as e:
                try:
                    version = soup.find("div",{"class":"field field-name-field-android-version2 field-type-taxonomy-term-reference field-label-above"}).find("div",{"class":"field-item even"}).text
                except Exception as e:
                    version ="no version specified"
            try:
                last_modified = soup.find("div",{"class":"field field-name-changed-date field-type-ds field-label-inline clearfix"}).find("div",{"class":"field-item even"}).text
            except Exception as e:
                last_modified = soup.find("div",{"class":"field field-name-changed-date field-type-ds field-label-hidden"}).text

            # Write the metadata into csv file
            with open('./csv_file.csv','a+',newline='') as f:
                csv_writer = csv.writer(f, delimiter="|")
                csv_writer.writerow([name_d , version ,last_modified])
                        
        try:
            next_div=soup_pages.find("li", {"class": "pager-next last"})
            number_page = next_div.find('a')['href']
        except Exception as e:
            break
    # Import the cvs file to mongoDB
    insert_data.import_data()

