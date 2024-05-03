-- Drop tables if they exist in reverse order of dependency
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    CONSTRAINT users_email_unique UNIQUE (email)
);

-- Create status table
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    CONSTRAINT name_unique UNIQUE (name)
);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    CONSTRAINT fk_tasks_status FOREIGN KEY (status_id)
        REFERENCES status(id) ON DELETE CASCADE,
    CONSTRAINT fk_tasks_users FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);