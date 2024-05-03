from faker import Faker
import random

faker = Faker()


def create_users(cur, n):
    for _ in range(n):
        fullname = faker.name()
        email = faker.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))


def create_status(cur, statuses):
    for status in statuses:
        cur.execute("INSERT INTO status (status_name) VALUES (%s)", (status,))


def create_tasks(cur, n):
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    for _ in range(n):
        title = faker.sentence(nb_words=6)
        description = faker.text(max_nb_chars=200)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )


def seed_db(cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM users LIMIT 1);")
    users_empty = not cur.fetchone()[0]

    cur.execute("SELECT EXISTS(SELECT 1 FROM status LIMIT 1);")
    status_empty = not cur.fetchone()[0]

    cur.execute("SELECT EXISTS(SELECT 1 FROM tasks LIMIT 1);")
    tasks_empty = not cur.fetchone()[0]

    if not users_empty and not status_empty and not tasks_empty:
        return

    number_of_users = 10
    number_of_tasks = 30
    statuses = ['Todo', 'InProgress', 'Completed']

    create_users(cur, number_of_users)
    create_status(cur, statuses)
    create_tasks(cur, number_of_tasks)

    print("Data seeding completed successfully!")
