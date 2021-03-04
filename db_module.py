import sqlite3
import os
from datetime import datetime as dt
import hashlib
import host_info

crawlerDB = "Crawler_DB-test.db"

def db_init():
    """Verifies if there is database for crawler. If there is none, new database with appropriate tables is created"""

    if not os.path.exists(crawlerDB):
        print("Error:\tCrawler database not found, creating new database...")

    global db
    db = sqlite3.connect(crawlerDB)
    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS files
                (file_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                file_name TEXT,
                path TEXT UNIQUE,
                parent_dir INTEGER,
                last_backed_up DATETIME,   
                created DATETIME,
                file_hash TEXT,
                size INTEGER,
                file_type TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS directories
                   (dir_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                   file_name TEXT,
                   path TEXT UNIQUE,
                   parent_dir INTEGER,
                   last_backed_up DATETIME,   
                   created DATETIME,
                   size INTEGER)''')
    db.commit()
    db.close()


def new_db_entry(crawled_path):
    db = sqlite3.connect(crawlerDB)
    cur = db.cursor()
    properties = new_file_properties(crawled_path)
    properties["last_backed_up"]= dt.now()
    cur.execute("INSERT INTO files(file_hash, file_name, path, parent_dir, created, size, file_type, last_backed_up) "
                "VALUES (:file_hash, :file_name, :path, :parent_dir, :created, :size, :file_type, :last_backed_up)", properties)

    db.commit()
    db.close()

def update_db_entry(crawled_path):

    path = crawled_path
    db = sqlite3.connect(crawlerDB)
    cur = db.cursor()
    properties = new_file_properties(crawled_path)
    cur.execute("UPDATE files SET file_hash = :file_hash,"
                "file_name = :file_name,"
                "parent_dir= :parent_dir,"
                "created = :created,"
                "size = :size,"
                "file_type = :file_type "
                "WHERE path = :path", properties)
    db.commit()
    db.close()


def new_file_properties(file_path):
    try:
        f_hash = file_hash(file_path)
        f_path = file_path

        delimiter = host_info.system_compatibility_check(delimiter=True)
        parent_dir = f_path.rsplit(delimiter,1)[-2]

        age = os.path.getctime(file_path)
        created = dt.fromtimestamp(age).strftime('%Y-%m-%d %H:%M:%S')

        size = os.path.getsize(file_path)
        file_type = file_path.rsplit(".")[-1]
        file_name = file_path.rsplit(".")[-2]

        properties = {"file_hash": f_hash,
                      "file_name": file_name,
                      "path": f_path,
                      "parent_dir": parent_dir,
                      "created": created,
                      "size": size,
                      "file_type": file_type}


        return properties
    except:
        print(f_hash, f_path, parent_dir, created, size, file_type)
        quit()


def file_hash(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break

            h.update(chunk)
    return h.hexdigest()


db_init()

update_db_entry(r"D:\Coding\Local\PycharmProjects\dirCrawler\test.txt")
# new_db_entry(r"D:\Coding\Local\PycharmProjects\dirCrawler\test.txt")

# print(file_hash("C:\\Users\\Mike\\Downloads\\pycharm-community-2020.2.3.exe"))
