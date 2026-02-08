import sqlite3

#Global Variables
db = "Accounts.db"

#to Execute Single Value with single value
def Execute(query:str):
    connect = sqlite3.connect(db)
    cur = connect.cursor()
    cur.execute(query)
    connect.commit()
    connect.close()
    print(f"Query Executed : {query}")

#to Execute query with multiple values
def ExecuteMany(query:str,setValue):
    connect = sqlite3.connect(db)
    cur = connect.cursor()
    cur.executemany(query,setValue)
    connect.commit()
    connect.close()
    print(f"Query Executed : {query}")


#to Create DataBase if its Existed Before
def createDataBase():
    try:
        query = """CREATE TABLE Accounts(
            Email TEXT,
            Passowrd TEXT
            )"""
        Execute(query)
        return True
    except sqlite3.OperationalError:
         print("DataBase Already Exists")
         return False

#to add single value
def AddValue(email,password):
     Query = """INSERT INTO Accounts VALUES (?,?)"""
     ExecuteMany(Query,(email,password))


#to add multiple value
def AddValueMany(li):
     query =  """INSERT INTO Accounts VALUES (?,?)"""
     ExecuteMany(query,li)


#to view the values 
def show():
    connect = sqlite3.connect(db)
    cur = connect.cursor()
    cur.execute("select rowid,* from Accounts")
    connect.commit()
    values = cur.fetchall()
    for value in values:
         print(f"{value}\n")
    connect.close()


def getinput ():
     email = str(input("Enter Your EmailID: "))
     password = str(input("Enter Your PassWord: "))
                    
     return (email,password)


if __name__ == "__main__":
        createDataBase()
        li = [
             ('test@mail.com','password'),
             ('test1@mail.com','password')
        ]
        AddValueMany(li)
        show()
        




