import cx_Oracle

class Database:

    def __init__(self):
        self.con = cx_Oracle.connect('miller/005842514@dataserv.mscs.mu.edu:1521/ORCL')
        print(self.con.version)

    def close(self):
        print("Closing connection")
        self.con.close()