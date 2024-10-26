import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="admin101",
    password="Giri12345@",
    database="work_management"
)

def connet():
    return mydb.cursor()

def commit_all():
    mydb.commit()
        