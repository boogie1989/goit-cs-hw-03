import psycopg2
import os


def create_conn():
    return psycopg2.connect(
        dbname="goit",
        user="goit",
        password="goit",
        host="localhost",
        port="5432"
    )


def create_db():
    conn = create_conn()
    cur = conn.cursor()

    with open(os.path.abspath("create_db.sql"), "r") as f:
        sql = f.read()
    try:
        cur.execute(sql)
        conn.commit()
    except psycopg2.Error as e:
        print("Error tables creation:", e)
        conn.rollback()

    return conn, cur
