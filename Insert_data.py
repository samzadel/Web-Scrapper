import pymongo
from pymongo import MongoClient
import csv
import os


def import_data():
    # DB connectivity
    client = MongoClient('localhost',27017)

    #create the database and the collection if doesn't exist
    mydb = client['crawler']
    mycoll = mydb['firmware']

    # Insert the cvs file in the collection
    with open('./csv_file.csv',"r") as f:
        reader = csv.reader(f,delimiter="|")
        for row in reader:
            if mycoll.find_one({"Name_device": row[0]}) == None:
                mydict = {"Name_device": row[0], "Version": row[1], "Last_modified": row[2]}
                mycoll.insert_one(mydict)
            elif mycoll.find_one({"Name_device": row[0]})['Last_modified'] != row[2]:
                mycoll.replace_one({"Name_device": row[0]}, {"Name_device": row[0],"Version": row[1], "Last_modified": row[2]})
    os.remove('./csv_file.csv')
    print("Insertion of firmwares metadata completed")

