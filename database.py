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

    def getRestRating(self):
        query = "SELECT R.rname, R.restid, round(avg(CR.rating), 2) FROM restaurant R, cust_review CR WHERE CR.restid = R.restid GROUP BY R.restid, R.rname"
        cur = self.cursor.execute(query)
        ratingCur = list(cur)

        query = "SELECT rname, restid, round(0) FROM restaurant WHERE restid not in (SELECT restid FROM cust_review)"
        cur = self.cursor.execute(query)
        noRatingCur = list(cur)

        curList = ratingCur + noRatingCur

        return curList

    def getRestaurantMenu(self, rid):
        query = "SELECT * FROM menu WHERE restid = :rid"
        cur = self.cursor.execute(query,rid=rid)
        return list(cur)

    def writeReview(self, rid, rating, cust_comment, email):
        print(rid)
        print(rating)
        print(cust_comment)
        print(email)
        #insert into CUST_REVIEW VALUES(Customer_ReviewId_Seq.nextval,'john@restaurantadvisor.com',1003,'Gross','Horrible',sysdate + interval '1' minute,2);
        query = "INSERT INTO cust_review (reviewid, custemail, restid, reviewdescr, rating) VALUES (Customer_ReviewId_Seq.nextval, :email, :rid, :cust_comment, :rating)"

        try:
            cur = self.cursor.execute(query, rid=rid, rating=rating, cust_comment=cust_comment, email=email)
            self.con.commit()
            return True
        except Exception as e:
            return False

    def close(self):
        print("Closing connection")
        self.con.close()