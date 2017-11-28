from database import Database

db = Database()
user = db.getUsers("justin@restaurantadvisor.com", "jmiller789")

print(user)