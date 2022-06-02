# write all your SQL queries in this file.
from datetime import datetime, timedelta
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
        self.mandatory = group_data[2]
        super().__init__()

    def get_posts(self):
        cur = conn.cursor()
        sql_call = """
        SELECT post_id, title, content, created_date, g.group_id, g.name, g.mandatory, u.user_id, u.first_name, u.last_name, u.email, u.address, u.role FROM posts as p
            INNER JOIN groups g on g.group_id = p.group_id
            INNER JOIN users u on u.user_id = p.author_id
        WHERE p.group_id = %s
        ORDER BY created_date DESC;
        """
        cur.execute(sql_call, (self.group_id,))
        Posts = cur.fetchall()
        result = []
        for post_data in Posts:
            result.append(Post(post_data))
        cur.close()
        return result

    def get_threads(self):
        cur = conn.cursor()
        sql_call = """
        SELECT thread_id, title, g.group_id, g.name, g.mandatory FROM threads
        INNER JOIN groups g on g.group_id = threads.group_id
        WHERE threads.group_id = %s
        """
        cur.execute(sql_call, (self.group_id,))
        threads = cur.fetchall()
        result = []
        for thread_data in threads:
            result.append(Thread(thread_data))
        cur.close()
        return result

class Message(tuple):
    def __init__(self, message_data):
        self.message_id = message_data[0]
        self.content = message_data[1]
        self.thread_id = message_data[2]
        self._created_date = message_data[3]
        self.author = {
            "user_id": message_data[4],
            "first_name": message_data[5],
            "last_name": message_data[6],
            "role": message_data[7],
        }
        super().__init__()

    @property
    def created_date(self):
        now = datetime.now()
        if now.date() == self._created_date.date():
            return self._created_date.strftime("Idag %X")
        elif now.date() == self._created_date.date() + timedelta(days=1):
            return self._created_date.strftime("Igår %X")
        elif now < self._created_date + timedelta(days=7):
            dag = [
                "Mandag",
                "Tirsdag",
                "Onsdag",
                "Torsdag",
                "Fredag",
                "Lørdag",
                "Søndag",
            ][int(self._created_date.strftime("%w"))]
            return self._created_date.strftime(f"{dag} %X")
        elif now.strftime("%y") == self._created_date.strftime("%y"):
            return self._created_date.strftime("%d/%m %X")
        else:
            return self._created_date.strftime("%d/%m/%y %X")

class Post(tuple):
    def __init__(self, post_data):
        self.post_id = post_data[0]
        self.title = post_data[1]
        self.content = post_data[2]
        self.created_date = post_data[3]
        self.group = {
            'group_id': post_data[4],
            'name': post_data[5],
            'mandatory': post_data[6],
        }
        self.author = {
            'user_id': post_data[7],
            'first_name': post_data[8],
            'last_name': post_data[9],
            'email': post_data[10],
            'address': post_data[11],
            'role': post_data[12],
        }
        super().__init__()

class Thread(tuple):
    def __init__(self, thread_data):
        self.thread_id = thread_data[0]
        self.title = thread_data[1]
        self.group = {
            "group_id": thread_data[2],
            "name": thread_data[3],
            "mandatory": thread_data[4]
        }
        self.group_id = thread_data[2]
        if len(thread_data) == 6:
            self.last_message_date = thread_data[5]
        super().__init__()

    def get_messages(self):
        cur = conn.cursor()
        sql_call = """
        SELECT message_id, content, thread_id, created_date ,u.user_id, u.first_name, u.last_name, u.role FROM messages
            INNER JOIN users u on u.user_id = messages.author_id
        WHERE messages.thread_id = %s;
        """
        cur.execute(sql_call, (self.thread_id,))
        messages = cur.fetchall()
        result = []
        for message_data in messages:
            result.append(Message(message_data))
        cur.close()
        return result
        

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

    def is_member_of_group(self, group_id):
        cur = conn.cursor()
        sql_call = """
        SELECT * FROM users_groups WHERE user_id = %s AND group_id = %s
        """
        cur.execute(sql_call, (self.user_id, group_id))
        result = cur.fetchone()
        return cur.rowcount > 0


    def get_groups_joinable(self):
        cur = conn.cursor()
        sql_call = """
        SELECT groups.* FROM groups INNER JOIN users_groups ON groups.group_id = users_groups.group_id WHERE users_groups.user_id = %s 
        UNION
        SELECT groups.* FROM groups WHERE groups.mandatory = FALSE
        ORDER BY mandatory ASC, name DESC
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

    def get_threads(self):
        cur = conn.cursor()
        sql_call = """
        SELECT threads.thread_id, title, g.group_id, g.name, g.mandatory, lm.last_message_date FROM threads
            INNER JOIN
                groups g
                ON g.group_id = threads.group_id
            LEFT JOIN
                (SELECT thread_id, MAX(created_date) as last_message_date FROM messages GROUP BY thread_id) lm
                ON threads.thread_id = lm.thread_id
            WHERE g.group_id IN
            (
                SELECT group_id FROM users_groups
                WHERE user_id = %s
            )
        ORDER BY last_message_date DESC NULLS LAST;
        """
        cur.execute(sql_call, (self.user_id,))
        threads = cur.fetchall()
        result = []
        for thread_data in threads:
            result.append(Thread(thread_data))
        cur.close()
        return result

    def in_thread(self, thread_id):
        cur = conn.cursor()
        sql_call = """
        SELECT * FROM users_threads WHERE
        user_id = %s AND
        thread_id = %s
        """
        cur.execute(sql_call, (self.user_id, thread_id))
        return cur.rowcount > 0

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
    SELECT post_id, title, content, created_date, g.group_id, g.name, g.mandatory, u.user_id, u.first_name, u.last_name, u.email, u.address, u.role FROM posts as p
    INNER JOIN groups g on g.group_id = p.group_id
    INNER JOIN users u on u.user_id = p.author_id
    WHERE g.group_id in (
        SELECT g.group_id FROM users_groups
        WHERE user_id = %s
    )
    ORDER BY created_date DESC
    """
    cur.execute(sql_call, (user_id,))
    user = [Post(i) for i in cur.fetchmany(50)] if cur.rowcount > 0 else []
    cur.close()
    return user

def get_group(group_id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM groups
    WHERE group_id = %s
    """
    cur.execute(sql, (group_id,))
    group = Group(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return group

def get_thread(thread_id):
    cur = conn.cursor()
    sql = """
    SELECT thread_id, title, g.group_id, g.name, g.mandatory FROM threads
    INNER JOIN groups g on g.group_id = threads.group_id
    WHERE thread_id = %s
    """
    cur.execute(sql, (thread_id,))
    thread = Thread(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return thread

def insert_thread(group_id, title):
    cur = conn.cursor()
    sql = """
    INSERT INTO threads(group_id, title) VALUES (%s, %s)
    """ 
    cur.execute(sql, (group_id, title))
    conn.commit()
    cur.close()

def group_exist(name):
    cur = conn.cursor()
    sql = """
    SELECT COUNT(*) FROM groups WHERE name = %s
    """
    cur.execute(sql, (name,))
    return cur.fetchone()[0] > 0

def insert_group(name, mandatory):
    cur = conn.cursor()
    sql = """
    INSERT INTO groups(name, mandatory) VALUES (%s, %s) RETURNING *
    """ 
    cur.execute(sql, (name, mandatory))

    result = Group(cur.fetchone()) if cur.rowcount > 0 else None
    
    conn.commit()
    cur.close()
    return result

def insert_post(group_id, author_id, title, content):
    cur = conn.cursor()
    sql = """
    INSERT INTO posts(group_id, author_id, title, content) VALUES (%s, %s, %s, %s)
    """ 
    cur.execute(sql, (group_id, author_id, title, content))
    conn.commit()
    cur.close()

def insert_message(content, thread_id, author_id):
    cur = conn.cursor()
    sql_call = """
    INSERT INTO messages(content, thread_id, author_id, created_date)
    VALUES (%s, %s, %s, NOW())
    """
    cur.execute(sql_call, (content, thread_id, author_id))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()
