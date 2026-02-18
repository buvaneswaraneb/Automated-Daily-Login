import sqlite3
from datetime import date
#Global Variables

class AccountDateBase:
    def __init__(self):
        self.db = "../DataBase/Accounts.db"
        self.table = "Accounts"

    #to Execute Single Value with single value
    def Execute(self,query:str):
        connect = sqlite3.connect(self.db)
        cur = connect.cursor()
        cur.execute(query)
        connect.commit()
        connect.close()
        print(f"Query Executed : {query}")
    
    def ExecuteM(self,query:str,tup):
        connect = sqlite3.connect(self.db)
        cur = connect.cursor()
        cur.execute(query,tup)
        connect.commit()
        connect.close()
        print(f"Query Executed : {query}")

    #to Execute query with multiple values
    def ExecuteMany(query:str,setValue,self):
        connect = sqlite3.connect(self.db)
        cur = connect.cursor()
        cur.executemany(query,setValue)
        connect.commit()
        connect.close()
        print(f"Query Executed : {query}")


    #to Create DataBase if its Existed Before
    def createTable(self):
        try:
            query = f"""CREATE TABLE {self.table}(
                Email TEXT PRIMARY KEY,
                Passowrd TEXT
                )"""
            self.Execute(query)
            return True
        except sqlite3.OperationalError:
            print("DataBase Already Exists")
            return False

    #to add single value
    def AddValue(self,email,password):
        Query = f"""INSERT INTO {self.table} VALUES (?,?)"""
        self.ExecuteMany(Query,(email,password))


    #to add multiple value
    def AddValueMany(self):
        query =  f"""INSERT {self.table} INTO  VALUES (?,?)"""
        li = self.getManyInputs()
        self.ExecuteMany(query,li)


    #to view the values 
    def show(self):
        connect = sqlite3.connect(self.db)
        cur = connect.cursor()
        cur.execute(f"select rowid,* from {self.table}")
        connect.commit()
        values = cur.fetchall()
        for value in values:
            print(f"{value}\n")
        connect.close()


    def getManyInputs(self):
        previous = 0
        account_array=[]
        n:int = int(input("Enter the Number of Accounts : "))
        for i in range(0,n):
            email = input("Enter the Email: \n")
            password = input("Enter the Password or use Previous Password (p): \n")
            print("Email validation: ",self.validEmail(email))
            if(password=="p"):
                password = previous
            else:
                previous = password     
            account_array.append((email,password))
        return account_array

    def validEmail(email):
        pass
        # regex = "^[^@]+@[^@]+\.[^@]+$"
        # pattern = re.compile(regex)
        # return bool(pattern.match(email))



class Date(AccountDateBase):
    def __init__(self):
        super().__init__()
        self.db = "src/DataBase/date.db"
        self.table = "Claim"

    def createTable(self):
        query = f"""CREATE TABLE Claim(
        day DATE ,
        email TEXT,
        status TEXT
        )"""
        self.Execute(query)
    
    def AddValue(self,EMAIL):
        query = f"""INSERT INTO Claim VALUES (date('now'),?,?)"""
        self.ExecuteM(query,(EMAIL,"Claimmed"))

    #debug
    def AddValueMany(self):
        n:int = int(input("Enter the Number Of Elements: "))
        for i in range(n):
            email = input("Enter the Email: ")
            self.AddValue(email)
    #test 
    def testExecution(self):
        conn = sqlite3.connect("src/DataBase/date.db")
        curr = conn.cursor()
        curr.execute("""INSERT INTO Claim VALUES (date('now'),'Test@mail.com','claimmed')""")
        conn.commit()
        conn.close()
    
    def getclaimed(self):
        conn = sqlite3.connect(self.db)
        curr = conn.cursor()
        query = """SELECT email FROM Claim WHERE day = date('now')"""
        curr.execute(query)
        conn.commit()
        val = curr.fetchall()
        li = []
        for i in val:
            li.append(i[0])
        return li
        conn.close()
    


if __name__ == "__main__":
    date = Date()
    print(date.getclaimed())    
        



    



