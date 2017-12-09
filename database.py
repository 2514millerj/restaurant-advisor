import cx_Oracle

class Database:

    def __init__(self):
        self.con = cx_Oracle.connect('miller/005842514@dataserv.mscs.mu.edu:1521/ORCL')
        self.cursor = self.con.cursor()
        print(self.con.version)

    def authenticateUser(self, username, password):
        cur = self.cursor.execute("""SELECT email, password FROM restaurant_customer""")

        for cust_email, cust_password in cur:
            if cust_email == username and cust_password == password:
                return True

        return False

    def getUserName(self, username):
        query = "SELECT fname FROM restaurant_customer WHERE email = :username"
        cur = self.cursor.execute(query, username=username)

        userNames = list(cur)
        return userNames[0][0]

    def getRestaurants(self):
        query = "SELECT * FROM restaurant"
        cur = self.cursor.execute(query)
        return list(cur)

    def getRestaurantNames(self):
        query = "SELECT rname, restid FROM restaurant"
        cur = self.cursor.execute(query)
        return list(cur)

    def getRestIdFromName(self, restaurant):
        query = "SELECT restid FROM restaurant where rname = :restName"
        cur = self.cursor.execute(query, restName=restaurant)
        rid = list(cur)
        return rid[0][0]

    def getRestRating(self, restaurant):
        #select
        #R.rname, R.restid, round(avg(CR.rating), 2)
        #from restaurant R, cust_review
        #CR
        #where
        #CR.restid = R.restid
        #group
        #by
        #R.restid, R.rname
        query = "SELECT R.rname, R.restid, round(avg(CR.rating), 2) FROM restaurant R, cust_review CR WHERE "

    def getRestaurantMenu(self, restaurant):
        rid = self.getRestIdFromName(restaurant)
        query = "SELECT * FROM menu WHERE restid = :rid"
        cur = self.cursor.execute(query,rid=rid)
        return list(cur)

    def close(self):
        print("Closing connection")
        self.con.close()