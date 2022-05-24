\i schema_drop.sql;

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NOT NULL,
    password varchar(120) NOT NULL,
    email varchar(64) NOT NULL,
    address varchar(64) NOT NULL,
    role varchar(64) NOT NULL CHECK ( role in ('student', 'parent', 'teacher') )
);

CREATE TABLE IF NOT EXISTS groups (
    group_id SERIAL PRIMARY KEY,
    name varchar(64) NOT NULL UNIQUE,
    leaveable boolean DEFAULT TRUE,
    parents_can_post boolean DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS threads (
    thread_id SERIAL PRIMARY KEY,
    title varchar(64) NOT NULL,
    group_id integer REFERENCES groups(group_id),
    creator_id integer REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY,
    content text NOT NULL,
    thread_id integer REFERENCES threads(thread_id),
    author_id integer REFERENCES users(user_id),
    created_date timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    group_id integer REFERENCES groups(group_id),
    author_id integer REFERENCES users(user_id),
    title varchar(64) NOT NULL,
    content text NOT NULL,
    created_date timestamp NOT NULL DEFAULT now()
);

-- Relationships
CREATE TABLE IF NOT EXISTS users_threads (
    user_id integer REFERENCES users(user_id),
    thread_id integer REFERENCES threads(thread_id),
    PRIMARY KEY (user_id, thread_id)
);

CREATE TABLE IF NOT EXISTS users_groups (
    user_id integer REFERENCES users(user_id),
    group_id integer REFERENCES groups(group_id),
    PRIMARY KEY (user_id, group_id)
);