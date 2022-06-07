\i schema_drop.sql;

CREATE TABLE IF NOT EXISTS users (
    cpr_num INTEGER PRIMARY KEY,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NOT NULL,
    password varchar(120) NOT NULL,
    role varchar(64) NOT NULL CHECK ( role in ('student', 'parent', 'teacher') )
);

CREATE TABLE IF NOT EXISTS groups (
    group_id SERIAL PRIMARY KEY,
    name varchar(64) NOT NULL UNIQUE,
    mandatory boolean DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS threads (
    thread_id SERIAL PRIMARY KEY,
    title varchar(64) NOT NULL,
    group_id integer REFERENCES groups(group_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY,
    content text NOT NULL,
    thread_id integer REFERENCES threads(thread_id) NOT NULL,
    author_cpr_num integer REFERENCES users(cpr_num) NOT NULL,
    created_date timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    group_id integer REFERENCES groups(group_id) NOT NULL,
    author_cpr_num integer REFERENCES users(cpr_num) NOt NULL,
    title varchar(64) NOT NULL,
    content text NOT NULL,
    created_date timestamp NOT NULL DEFAULT now()
);

-- Relationships
CREATE TABLE IF NOT EXISTS users_in_groups (
    cpr_num integer REFERENCES users(cpr_num) NOT NULL,
    group_id integer REFERENCES groups(group_id) NOT NULL,
    PRIMARY KEY (cpr_num, group_id)
);

\i schema_ins.sql;