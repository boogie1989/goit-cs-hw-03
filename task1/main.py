from create_db import create_db
from seed_db import seed_db
from queries import run_and_log_all_queries


def main():
    conn, cur = create_db()
    seed_db(cur)
    run_and_log_all_queries(cur)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
