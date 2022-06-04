# write all your SQL queries in this file.
from datetime import datetime, timedelta
from flask_login import UserMixin

from aula import conn, login_manager

@login_manager.user_loader
def load_user(cpr_num):
    cur = conn.cursor()

    user_sql = """
    SELECT * FROM users
    WHERE cpr_num = %s
    """

    cur.execute(user_sql, (cpr_num,))
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
        SELECT post_id, title, content, created_date, g.group_id, g.name, g.mandatory, u.cpr_num, u.first_name, u.last_name, u.role FROM posts as p
            INNER JOIN groups g on g.group_id = p.group_id
            INNER JOIN users u on u.cpr_num = p.author_cpr_num
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
            "cpr_num": message_data[4],
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
            'cpr_num': post_data[7],
            'first_name': post_data[8],
            'last_name': post_data[9],
            'role': post_data[10],
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
        SELECT message_id, content, thread_id, created_date ,u.cpr_num, u.first_name, u.last_name, u.role FROM messages
            INNER JOIN users u on u.cpr_num = messages.author_cpr_num
        WHERE messages.thread_id = %s
        ORDER BY created_date DESC;
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
        self.cpr_num = user_data[0]
        self.first_name = user_data[1]
        self.last_name = user_data[2]
        self.password = user_data[3]
        self.role = user_data[4]
        super().__init__()

    def get_id(self):
        return self.cpr_num

    def get_groups(self):
        cur = conn.cursor()
        sql_call = """
        SELECT groups.* FROM users_in_groups JOIN groups ON users_in_groups.group_id = groups.group_id WHERE users_in_groups.cpr_num = %s
        """
        cur.execute(sql_call, (self.cpr_num,))
        groups = cur.fetchall()
        result = []
        for group_data in groups:
            result.append(Group(group_data))
        cur.close()
        return result

    def is_member_of_group(self, group_id):
        cur = conn.cursor()
        sql_call = """
        SELECT * FROM users_in_groups WHERE cpr_num = %s AND group_id = %s
        """
        cur.execute(sql_call, (self.cpr_num, group_id))
        return cur.rowcount > 0


    def get_groups_joinable(self):
        cur = conn.cursor()
        sql_call = """
        SELECT groups.* FROM groups INNER JOIN users_in_groups ON groups.group_id = users_in_groups.group_id WHERE users_in_groups.cpr_num = %s 
        UNION
        SELECT groups.* FROM groups WHERE groups.mandatory = FALSE
        ORDER BY mandatory ASC, name DESC
        """
        cur.execute(sql_call, (self.cpr_num,))
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
        DELETE FROM users_in_groups WHERE cpr_num = %s AND group_id = %s
        """
        cur.execute(sql_call, (self.cpr_num, group_id))
        conn.commit()
        cur.close()

    def join_group(self, group_id):
        cur = conn.cursor()
        sql_call = """
        INSERT INTO users_in_groups VALUES (%s, %s)
        """
        cur.execute(sql_call, (self.cpr_num, group_id))
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
                SELECT group_id FROM users_in_groups
                WHERE cpr_num = %s
            )
        ORDER BY last_message_date DESC NULLS LAST;
        """
        cur.execute(sql_call, (self.cpr_num,))
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
        cpr_num = %s AND
        thread_id = %s
        """
        cur.execute(sql_call, (self.cpr_num, thread_id))
        return cur.rowcount > 0

def insert_users(cpr_num, first_name, last_name, password, email, adresse, role):
    cur = conn.cursor()
    sql_call = """
    INSERT INTO users(cpr_num, first_name, last_name, password, email, adresse, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql_call, (cpr_num, first_name, last_name, password, email, adresse, role))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_users_by_cpr(cpr_num):
    cur = conn.cursor()
    sql_call = """
    SELECT * FROM users
    WHERE cpr_num = %s
    """
    cur.execute(sql_call, (cpr_num,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return user

def get_posts_for_user(cpr_num):
    cur = conn.cursor()
    sql_call = """
    SELECT post_id, title, content, created_date, g.group_id, g.name, g.mandatory, u.cpr_num, u.first_name, u.last_name, u.role FROM posts as p
    INNER JOIN groups g on g.group_id = p.group_id
    INNER JOIN users u on u.cpr_num = p.author_cpr_num
    WHERE g.group_id in (
        SELECT g.group_id FROM users_in_groups
        WHERE cpr_num = %s
    )
    ORDER BY created_date DESC
    """
    cur.execute(sql_call, (cpr_num,))
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

def insert_post(group_id, author_cpr_num, title, content):
    cur = conn.cursor()
    sql = """
    INSERT INTO posts(group_id, author_cpr_num, title, content) VALUES (%s, %s, %s, %s)
    """ 
    cur.execute(sql, (group_id, author_cpr_num, title, content))
    conn.commit()
    cur.close()

def insert_message(content, thread_id, author_cpr_num):
    cur = conn.cursor()
    sql_call = """
    INSERT INTO messages(content, thread_id, author_cpr_num, created_date)
    VALUES (%s, %s, %s, NOW())
    """
    cur.execute(sql_call, (content, thread_id, author_cpr_num))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()
