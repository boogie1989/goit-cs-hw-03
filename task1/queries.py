import psycopg2


def execute_query(cursor, query, params=None):
    """Execute a SQL query with optional parameters and fetch all results."""
    cursor.execute(query, params or ())
    return cursor.fetchall()


def execute_action(cursor, action, params):
    """Execute a SQL action (like update or insert) that requires commit/rollback."""
    try:
        cursor.execute(action, params)
        cursor.connection.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        cursor.connection.rollback()


def get_tasks_by_user(cursor, user_id):
    """Fetch all tasks for a specified user ID."""
    query = "SELECT * FROM tasks WHERE user_id = %s"
    return execute_query(cursor, query, (user_id,))


def get_tasks_by_status(cursor, name):
    """Fetch all tasks with a specified status."""
    query = """
    SELECT * FROM tasks WHERE status_id = (
        SELECT id FROM status WHERE name = %s
    )"""
    return execute_query(cursor, query, (name,))


def update_task_status(cursor, task_id, new_name):
    """Update the status of a task by task ID and new status name."""
    action = """
    UPDATE tasks SET status_id = (
        SELECT id FROM status WHERE name = %s
    ) WHERE id = %s"""
    execute_action(cursor, action, (new_name, task_id))


def get_users_without_tasks(cursor):
    """Fetch users who do not have any tasks."""
    query = "SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)"
    return execute_query(cursor, query)


def add_task(cursor, title, description, status_id, user_id):
    """Add a new task for a user."""
    action = "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)"
    execute_action(cursor, action, (title, description, status_id, user_id))


def get_incomplete_tasks(cursor):
    """Fetch tasks that have not been marked as completed."""
    query = "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'Completed')"
    return execute_query(cursor, query)


def delete_task(cursor, task_id):
    """Delete a task by its ID."""
    action = "DELETE FROM tasks WHERE id = %s"
    execute_action(cursor, action, (task_id,))


def find_users_by_email(cursor, email_domain):
    """Find users by their email domain."""
    query = "SELECT * FROM users WHERE email LIKE %s"
    return execute_query(cursor, query, (f"%@{email_domain}",))


def update_user_name(cursor, user_id, new_name):
    """Update a user's name by their user ID."""
    action = "UPDATE users SET fullname = %s WHERE id = %s"
    execute_action(cursor, action, (new_name, user_id))


def count_tasks_by_status(cursor):
    """Count tasks grouped by their statuses."""
    query = "SELECT name, COUNT(*) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY name"
    return execute_query(cursor, query)


def get_tasks_by_email_domain(cursor, email_domain):
    """Fetch tasks assigned to users with a specific email domain."""
    query = "SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s"
    return execute_query(cursor, query, (f"%@{email_domain}",))


def get_tasks_without_description(cursor):
    """Fetch tasks that lack a description."""
    query = "SELECT * FROM tasks WHERE description IS NULL OR description = ''"
    return execute_query(cursor, query)


def get_users_and_tasks(cursor, status):
    """Fetch users and their tasks that are currently in a specific status."""
    query = """
    SELECT users.*, tasks.*, status.name FROM users
    INNER JOIN tasks ON users.id = tasks.user_id
    INNER JOIN status ON tasks.status_id = status.id
    WHERE status.name = %s"""
    return execute_query(cursor, query, (status,))


def get_users_with_task_counts(cursor):
    """Fetch users along with the count of their tasks."""
    query = """
    SELECT users.id, users.fullname, COUNT(tasks.id) FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.id, users.fullname"""
    return execute_query(cursor, query)


def run_and_log_all_queries(cur):

    # 1. Get tasks by user
    print("Getting tasks by user...")
    tasks_by_user = get_tasks_by_user(cur, user_id=1)
    print(f"Tasks by user: {tasks_by_user}")

    # 2. Get tasks by status
    print("Getting tasks by status...")
    tasks_by_status = get_tasks_by_status(cur, name="Todo")
    print(f"Tasks by status: {tasks_by_status}")

    # 3. Update task status
    print("Updating task status...")
    update_task_status(cur, task_id=1, new_name="Completed")

    # 4. Get users without tasks
    print("Getting users without tasks...")
    users_without_tasks = get_users_without_tasks(cur)
    print(f"Users without tasks: {users_without_tasks}")

    # 5. Add task
    print("Adding a new task...")
    add_task(cur, title="New Task",
             description="Description here", status_id=1, user_id=1)

    # 6. Get incomplete tasks
    print("Getting incomplete tasks...")
    incomplete_tasks = get_incomplete_tasks(cur)
    print(f"Incomplete tasks: {incomplete_tasks}")

    # 7. Delete task
    print("Deleting a task...")
    delete_task(cur, task_id=2)

    # 8. Find users by email
    print("Finding users by email...")
    users_by_email = find_users_by_email(cur, email_domain="example.com")
    print(f"Users by email: {users_by_email}")

    # 9. Update user name
    print("Updating user name...")
    update_user_name(cur, user_id=1, new_name="John Doe")

    # 10. Count tasks by status
    print("Counting tasks by status...")
    task_counts = count_tasks_by_status(cur)
    print(f"Task counts by status: {task_counts}")

    # 11. Get tasks by email domain
    print("Getting tasks by email domain...")
    tasks_by_email_domain = get_tasks_by_email_domain(
        cur, email_domain="example.com")
    print(f"Tasks by email domain: {tasks_by_email_domain}")

    # 12. Get tasks without description
    print("Getting tasks without description...")
    tasks_without_description = get_tasks_without_description(cur)
    print(f"Tasks without description: {tasks_without_description}")

    # 13. Get users and tasks by status
    print("Getting users and tasks by status 'InProgress'...")
    users_and_tasks = get_users_and_tasks(cur, status="InProgress")
    print(f"Users and tasks by status: {users_and_tasks}")

    # 14. Get users with task counts
    print("Getting users with task counts...")
    users_with_task_counts = get_users_with_task_counts(cur)
    print(f"Users with task counts: {users_with_task_counts}")
