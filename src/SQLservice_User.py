import mysql.connector as db
import os

DATABASE = "accounts_info"
MYSQL_IP = os.environ['LC_MYSQL_IP']

class SQL_User_db:
    def __init__(self):
        # self.conn = db.connect(host="54.244.217.119", user="root", db=DATABASE)
        # self.conn = db.connect(host="localhost", user="root", db=DATABASE)
        self.conn = db.connect(host=MYSQL_IP, user="root", db=DATABASE)

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
        except Exception as e:
            print('duplicate username')
            print(e)
            return False
        return True

    def get_usr_info(self, username):
        cursor = self.conn.cursor()
        cursor.execute("select id,password,isadmin from accounts where username = (%(username)s)", {"username": username})
        res = cursor.fetchall()
        if res == []:
            return "fake_username", "fake_user_hash_password", None
        return res[0]

if __name__ == "__main__":
    import hashlib
    print(SQL_User_db().add_user('Jiankun',hashlib.md5('123456'.encode('utf-8')).hexdigest()))
    # print(SQL_User_db().describe())
# print(SQL_User_db().get_password('test4'))
