from bs4 import BeautifulSoup
import requests
import os
import csv

def page_download(url):
    new_url = url.replace('\\','/')
    r = requests.get(new_url)
    soup = BeautifulSoup(r.text, 'lxml')

    #Place the metadata in a cvs file
    name_device = soup.find("div",{"class":"field field-name-title field-type-ds field-label-hidden"}).h2.text
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
    with open('./csv_file.csv','a+',newline='') as f:
        csv_writer = csv.writer(f, delimiter="|")
        csv_writer.writerow([name_device , version ,last_modified])

    #Download the firmwares

    if not os.path.exists('./firmwares'):
        os.makedirs('./firmwares')
    if not os.path.exists('./firmwares/'+ name_device +'.zip'):
        downloads = soup.find("span",{"class":"file"})
        if downloads == None :
            downloads = soup.find("div",{"class":"field field-name-field-firmware-image-download field-type-text field-label-above"})
            if downloads == None :
                return
        print(downloads)
        req = requests.get(downloads.find('a')['href'])
        with open('./firmwares/'+ name_device +'.zip','wb') as f:
            f.write(req.content)


        