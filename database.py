import cx_Oracle

class Database:

    def __init__(self):
        self.con = cx_Oracle.connect('miller/005842514@dataserv.mscs.mu.edu:1521/ORCL')
        self.cursor = self.con.cursor()
        print(self.con.version)

    def getUsers(self, username, password):
        cur = self.cursor.execute("""SELECT email, password FROM restaurant_customer""")

        for cust_email, cust_password in cur:
            if cust_email == username and cust_password == password:
                return cust_email

        return None

    def close(self):
        print("Closing connection")
        self.con.close()