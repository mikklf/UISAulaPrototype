# write all your SQL queries in this file.
from flask_login import UserMixin

from aula import conn, login_manager

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    user_sql = """
    SELECT * FROM users
    WHERE user_id = %s
    """

    cur.execute(user_sql, (user_id,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user

#
# Models
#
class Group(tuple):
    def __init__(self, group_data):
        self.group_id = group_data[0]
        self.name = group_data[1]
        self.leaveable = group_data[2]
        self.parents_can_post = group_data[3]
        super().__init__()

    def get_posts(self):
        cur = conn.cursor()
        sql_call = """
        SELECT * FROM posts
        WHERE group_id = %s
        """
        cur.execute(sql_call, (self.group_id,))
        Posts = Posts(cur.fetchall()) if cur.rowcount > 0 else None
        result = []
        for post_data in Posts:
            result.append(Post(post_data))
        cur.close()
        return result

class Message(tuple):
    def __init__(self, message_data):
        self.message_id = message_data[0]
        self.content = message_data[1]
        self.thread_id = message_data[2]
        self.author_id = message_data[3]
        self.created_date = message_data[4]
        super().__init__()

class Post(tuple):
    def __init__(self, post_data):
        self.post_id = post_data[0]
        self.group_id = post_data[1]
        self.author_id = post_data[2]
        self.author = ""
        self.title = post_data[3]
        self.content = post_data[4]
        self.created_date = post_data[5]
        self._get_author_name()
        super().__init__()

    def _get_author_name(self):
        cur = conn.cursor()
        sql_call = """
        SELECT first_name, last_name FROM users WHERE user_id = %s
        """
        cur.execute(sql_call, (self.author_id,))
        self.author = ' '.join(cur.fetchone())

class Thread(tuple):
    def __init__(self, thread_data):
        self.thread_id = thread_data[0]
        self.title = thread_data[1]
        self.group_id = thread_data[2]
        self.creator_id = thread_data[3]
        super().__init__()

class User(tuple, UserMixin):
    def __init__(self, user_data):
        self.user_id = user_data[0]
        self.first_name = user_data[1]
        self.last_name = user_data[2]
        self.password = user_data[3]
        self.email = user_data[4]
        self.address = user_data[5]
        self.role = user_data[6]
        super().__init__()

    def get_id(self):
        return self.user_id

    def get_groups(self):
        cur = conn.cursor()
        sql_call = """
        SELECT groups.* FROM users_groups JOIN groups ON users_groups.group_id = groups.group_id WHERE users_groups.user_id = %s
        """
        cur.execute(sql_call, (self.user_id,))
        groups = cur.fetchall()
        result = []
        for group_data in groups:
            result.append(Group(group_data))
        cur.close()
        return result

    def get_groups_joinable(self):
        cur = conn.cursor()
        sql_call = """
        SELECT groups.* FROM groups INNER JOIN users_groups ON groups.group_id = users_groups.group_id WHERE users_groups.user_id = %s 
        UNION
        SELECT groups.* FROM groups WHERE groups.leaveable = TRUE
        ORDER BY leaveable DESC, name DESC
        """
        cur.execute(sql_call, (self.user_id,))
        groups = cur.fetchall()
        result = []
        for group_data in groups:
            result.append(Group(group_data))
        cur.close()
        return result

    def leave_group(self, group_id):
        # TODO: Tjek om brugeren må forlade gruppen
        cur = conn.cursor()
        sql_call = """
        DELETE FROM users_groups WHERE user_id = %s AND group_id = %s
        """
        cur.execute(sql_call, (self.user_id, group_id))
        conn.commit()
        cur.close()

    def join_group(self, group_id):
        cur = conn.cursor()
        sql_call = """
        INSERT INTO users_groups VALUES (%s, %s)
        """
        cur.execute(sql_call, (self.user_id, group_id))
        conn.commit()
        cur.close()
    



def insert_users(user_id, first_name, last_name, password, email, adresse, role):
    cur = conn.cursor()
    sql_call = """
    INSERT INTO users(user_id, first_name, last_name, password, email, adresse, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql_call, (user_id, first_name, last_name, password, email, adresse, role))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_users_by_id(user_id):
    cur = conn.cursor()
    sql_call = """
    SELECT * FROM users
    WHERE user_id = %s
    """
    cur.execute(sql_call, (user_id,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user

def select_users_by_email(email):
    cur = conn.cursor()
    sql_call = """
    SELECT * FROM users
    WHERE email = %s
    """
    cur.execute(sql_call, (email,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user

def get_posts_for_user(user_id):
    cur = conn.cursor()
    sql_call = """
    SELECT * FROM posts
    WHERE group_id in (
        SELECT group_id FROM users_groups
        WHERE user_id = %s
    )
    """
    cur.execute(sql_call, (user_id,))
    user = [Post(i) for i in cur.fetchmany(50)] if cur.rowcount > 0 else []
    cur.close()
    return user

