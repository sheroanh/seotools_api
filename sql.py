import mysql.connector
import bcrypt
import util

mydb = mysql.connector.connect(
  host="localhost",
  user="kane",
  password="kane",
  database="testdata"
)

mycursor = mydb.cursor()

def createDatabase(dbName):
    global mycursor
    mycursor.execute("SHOW DATABASES")

def createTableCustomer():
    global mycursor
    tbName = "customer"
    query = """CREATE TABLE {} (
        email VARCHAR(255) PRIMARY KEY,
        name TEXT,
        company TEXT,
        salt TEXT,
        hashed TEXT
    )""".format(tbName)
    mycursor.execute(query)

def dropTable(tbName):
    global mycursor
    mycursor.execute("drop table {}".format(tbName))

def showAllTables():
    global mycursor
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x[0])

def findUserByEmail(email):
    global mycursor
    sql = "SELECT * FROM customer WHERE email ='{}'".format(email)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return None
    return myresult[0]

def addUser(email, name, company, salt, hashed):
    global mycursor
    global mydb
    sql = "INSERT INTO customer (email, name, company, salt, hashed) VALUES (%s, %s, %s, %s, %s)"
    val = (email, name, company, salt, hashed)
    mycursor.execute(sql, val)
    mydb.commit()

def deleteUser(email):
    global mycursor
    sql = "DELETE FROM customer WHERE email ='{}'".format(email)
    mycursor.execute(sql)
    mydb.commit()

def getAllUsers():
    global mycursor
    mycursor.execute("SELECT * FROM customer")
    return [x for x in mycursor]

def changeUserInfo(email, name, newValue):
    global mycursor
    if name == "password":
        salt = bcrypt.gensalt().decode()
        hashed = util.getPasswordHash(salt, newValue)
        query = "UPDATE customer SET salt = '{}' WHERE email = '{}';".format(salt, email)
        mycursor.execute(query)
        mydb.commit()
        query = "UPDATE customer SET hashed = '{}' WHERE email = '{}';".format(hashed, email)
        mycursor.execute(query)
        mydb.commit()
    if name == "name":
        query = "UPDATE customer SET name = '{}' WHERE email = '{}';".format(newValue, email)
        mycursor.execute(query)
        mydb.commit()
        
    if name == "company":
        query = "UPDATE customer SET company = '{}' WHERE email = '{}';".format(newValue, email)
        mycursor.execute(query)
        mydb.commit()
        

# createTableCustomer()
# dropTable("customer")
# deleteUser("anhthi2103@gmail.com")
# print(findUserByEmail("anhthi2103@gmail.com"))
# showAllTables()
