import mysql.connector
import os
import fnmatch
import json
import datetime


user = 'silopete117' #getuser()

# Connect to MySQL DB.
mydb = mysql.connector.connect(
  username=user,
  password="Rk&ajXN1HlEy2hW5X!34",
  host=f"{user}.mysql.pythonanywhere-services.com",
  database=f"{user}$rarity_distributions"
)

# Loop through folder and insert JSON metadata into MySQL DB Table.
def insert_metadata_to_db(path):
    # Get subfolders in folder.
    folders = os.listdir(path)
    for i in len(folders):

        # Get files in folder.
        folderpath = os.path.join(path, folders[i])
        files = fnmatch.filter(os.listdir(folderpath), "*.json")

        # Get Collection Address!
        address = ''

        # Get Date.
        date = datetime.now()

        for file in files:
            # Get json, build and submit mysql record.
            json_data = json.load(file)
            mycursor = mydb.cursor()
            sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
            val = (address, file.name, json_data, date)
            mycursor.execute(sql, val)
            #mycursor.executemany(sql, val)
            mydb.commit()
        
        print("collection ", folders[i], " inserted.")
    print("all collections inserted.")
