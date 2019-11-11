import mysql.connector as db

DATABASE = "accounts_info"

class SQL_User_db:
    def __init__(self):
        self.conn = db.connect(host="localhost", user="root", db=DATABASE)

    def describe(self):
        cursor = self.conn.cursor()
        cursor.execute("desc accounts")
        res = cursor.fetchall()
        return res

    def add_user(self, username, password, isadmin=0):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""INSERT INTO accounts(username,password,isadmin) VALUES(%(username)s,%(password)s,%(isadmin)s);""",
                           {"username": username, "password": password, "isadmin":isadmin})
            self.conn.commit()
        except:
            print('duplicate username')
            return False
        return True

    # Added an encrypted function to protect the password
    def get_password(self, username):
        cursor = self.conn.cursor()
        cursor.execute("select password from accounts where username = (%(username)s)", {"username": username})
        res = cursor.fetchall()
        if res == []:
            return False
        return res[0][0]

    def get_usr_id(self, username):
        cursor = self.conn.cursor()
        cursor.execute("select id from accounts where username = (%(username)s)", {"username": username})
        res = cursor.fetchall()
        if res == []:
            return False
        return res[0][0]

if __name__ == "__main__":
    import hashlib
    print(SQL_User_db().add_user('Jiankun',hashlib.md5('123456'.encode('utf-8')).hexdigest()))
    # print(SQL_User_db().describe())
# print(SQL_User_db().get_password('test4'))
