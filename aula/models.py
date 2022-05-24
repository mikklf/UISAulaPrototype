# write all your SQL queries in this file.
from aula import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    schema = 'users'
    _id = 'user_id'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(_id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        User(cur.fetchone())
    else:
        return None

#
# Models
#
class Group(tuple):
    def __init__(self, group_data):
        self.group_id = group_data[0]
        self.name = group_data[1]
        self.leaveable = group_data[2]
        self.parents_can_post = group_data[3]

class Message(tuple):
    def __init__(self, message_data):
        self.message_id = message_data[0]
        self.content = message_data[1]
        self.thread_id = message_data[2]
        self.author_id = message_data[3]
        self.created_date = message_data[4]

class Post(tuple):
    def __init__(self, post_data):
        self.post_id = post_data[0]
        self.group_id = post_data[1]
        self.author_id = post_data[2]
        self.title = post_data[3]
        self.content = post_data[4]
        self.created_date = post_data[5]

class Thread(tuple):
    def __init__(self, thread_data):
        self.thread_id = thread_data[0]
        self.title = thread_data[1]
        self.group_id = thread_data[2]
        self.creator_id = thread_data[3]

class User(tuple, UserMixin):
    def __init__(self, user_data):
        self.user_id = user_data[0]
        self.first_name = user_data[1]
        self.last_name = user_data[2]
        self.password = user_data[3]
        self.email = user_data[4]
        self.address = user_data[5]
        self.role = user_data[6]

def insert_users(user_id, first_name, last_name, password, email, adresse, role):
    cur = conn.cursor()
    sql_call = """
    INSERT INTO Customers(user_id, first_name, last_name, password, email, adresse, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql_call, (user_id, first_name, last_name, password, email, adresse, role))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_users(user_id):
    cur = conn.cursor()
    sql_call = """
    SELECT * FROM users
    WHERE user_id = %s
    """
    cur.execute(sql_call, (user_id,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user
