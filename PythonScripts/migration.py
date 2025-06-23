#jfr
#(hopefully) one time use, for splitting the multiple tags of a user into a join table group_users
import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

DB = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST
}

def migrate():
    print("beginning migration...")
    db_connection = psycopg2.connect(**DB)
    db_cursor = db_connection.cursor()

    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_users (
            group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            PRIMARY KEY (group_id, user_id)
        );
    """)
    db_connection.commit()

    db_cursor.execute("select id, assigned_tags from users")
    users = db_cursor.fetchall()

    for user_id, tags, in users:
        if not tags:
            continue
        for tag in tags:
            tag = tag.strip()
            if not tag:
                continue
            db_cursor.execute("insert into groups (name) values (%s) on conflict do nothing", (tag,))
            db_cursor.execute("select id from groups where name = %s", (tag,))
            group_id = db_cursor.fetchone()[0]
            db_cursor.execute("""
                insert into group_users (group_id, user_id)
                values (%s, %s)
                on conflict do nothing
            """, (group_id, user_id))

    db_connection.commit()

    DROP_TAGS_COLUMN = True
    if DROP_TAGS_COLUMN:
        db_cursor.execute("alter table users drop column assigned_tags")
        db_connection.commit()
    
    db_cursor.close()
    db_connection.close()
    print("migrated.")

if __name__ == "__main__":
    migrate()