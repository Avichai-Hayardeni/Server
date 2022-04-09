import sqlite3

# cursor = self.conn.cursor()
#         sql_to_execute = ""
#         record = ()
#         cursor.execute(sql_to_execute, record)
#         self.conn.commit()


class Database:

    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name, check_same_thread=False)
        self.messages_table()
        self.users_table()
        self.init_user()
        self.init_message()

    def users_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS user_list
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        date_joined TEXT NOT NULL,
        birthdate TEXT NOT NULL)
        ''')
        # name: nickname
        # date_joined: year-month-day hour:minute:second
        # birthdate: year-month-day hour:minute:second

    def messages_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS message_list
        (message_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        addressee_id INTEGER NOT NULL,      
        is_pending INTEGER NOT NULL,
        type INTEGER NOT NULL,
        data TEXT NOT NULL)
        ''')

    def init_user(self):
        cursor = self.conn.cursor()
        sql1_to_execute = "SELECT * FROM user_list WHERE user_id = 0"
        cursor.execute(sql1_to_execute)
        if not len(cursor.fetchall()) > 0:
            sql2_to_execute = "INSERT INTO user_list(user_id, name, date_joined, birthdate) VALUES(?,?,?,?)"
            record = (0, "Dohnny", "2022-03-31 19:57:51", "2004-09-15 00:00:00")
            cursor.execute(sql2_to_execute, record)
            self.conn.commit()

    def init_message(self):
        cursor = self.conn.cursor()
        sql1_to_execute = "SELECT * FROM message_list WHERE message_id = 0"
        cursor.execute(sql1_to_execute)
        if not len(cursor.fetchall()) > 0:
            sql2_to_execute = "INSERT INTO message_list(message_id, date, author_id, addressee_id, is_pending, type, data) VALUES(?,?,?,?,?,?,?)"
            record = (0, "2004-09-15 00:00:00", 0, 0, 0, 0, "hello")
            cursor.execute(sql2_to_execute, record)
            self.conn.commit()

    def add_user(self, name, date_joined, birthdate):
        user_id = self.create_new_id("user_list") + 1
        user_name = name

        cursor = self.conn.cursor()
        sql_to_execute = "INSERT INTO user_list(user_id, name, date_joined, birthdate) VALUES(?,?,?,?)"
        record = (user_id, user_name, date_joined, birthdate)
        cursor.execute(sql_to_execute, record)
        self.conn.commit()

    def create_new_id(self, list_type):
        cursor = self.conn.cursor()
        sql_to_execute = "SELECT * FROM sqlite_sequence where name = ?"
        cursor.execute(sql_to_execute, (list_type, ))
        current_id = cursor.fetchall()[0][1]
        return current_id

    def add_message(self, date, author_id, addressee_id, type, data):
        message_id = self.create_new_id("message_list") + 1

        cursor = self.conn.cursor()
        sql_to_execute = "INSERT INTO message_list(message_id, date, author_id, addressee_id, is_pending, type, data) VALUES(?,?,?,?,?,?,?)"
        record = (message_id, date, author_id, addressee_id, 1, type, data)
        cursor.execute(sql_to_execute, record)
        self.conn.commit()

    def remove_user(self, given_user_id):
        cursor = self.conn.cursor()
        sql_to_execute = "DELETE FROM user_list WHERE user_id = ?"
        record = ((given_user_id, ))
        cursor.execute(sql_to_execute, record)
        self.conn.commit()

    def clear_user_list(self):
        cursor = self.conn.cursor()
        sql_to_execute = "DELETE FROM user_list"
        cursor.execute(sql_to_execute)
        self.conn.commit()
        self.update_sqlite_sequence("user_list")
        self.init_user()

    def clear_message_list(self):
        cursor = self.conn.cursor()
        sql_to_execute = "DELETE FROM message_list"
        cursor.execute(sql_to_execute)
        self.conn.commit()
        self.update_sqlite_sequence("message_list")
        self.init_message()

    def update_sqlite_sequence(self, list_type):
        cursor = self.conn.cursor()
        sql_to_execute = f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{list_type}'"
        cursor.execute(sql_to_execute)
        self.conn.commit()

    def get_pending_messages(self, given_user_id):
        cursor = self.conn.cursor()
        sql_to_execute = f"Select * FROM message_list WHERE addressee_id = {given_user_id} AND is_pending = 1"
        cursor.execute(sql_to_execute)
        message_list = cursor.fetchall()
        message_dict = {}
        for message in message_list:
            message_dict[message[0]] = f"{message[1]} {message[2]} {message[5]} {message[6]}"
        self.set_messages_not_pending(given_user_id)
        return message_dict

    def set_messages_not_pending(self, given_user_id):
        cursor = self.conn.cursor()
        sql_to_execute = f"UPDATE message_list SET is_pending = 0 WHERE addressee_id = {given_user_id}"
        cursor.execute(sql_to_execute)
        self.conn.commit()

