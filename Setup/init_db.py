#jfr
#script for connect to psql and intiating db schema
import psycopg2
from psycopg2 import sql, errors

DB_NAME = "contacts_db"
DB_USER = "contacts_admin"
DB_PASSWORD = "test"

def run():
    try:
        #sees if postgres user exists and if database exists, creates them if they dont
        db_connection = psycopg2.connect(dbname="postgres", user="postgres", host="localhost")
        db_connection.autocommit = True
        db_cursor = db_connection.cursor()

        db_cursor.execute("select 1 from pg_roles where rolname = %s", (DB_USER,))
        if not db_cursor.fetchone():
            db_cursor.execute("create user {} with password %s").format(sql.Identifier(DB_USER), [DB_PASSWORD])
            print(f"User {DB_USER} was created.")
        else:
            print(f"User {DB_USER} exists.")
        
        db_cursor("select 1 from pg_database where datname = %s", (DB_NAME,))
        if not db_cursor.fetchone():
            db_cursor.execute(sql.SQL("create database {} owner {}").format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER)))
            print(f"Database {DB_NAME} was created.")
        else:
            print(f"Database {DB_NAME} exists.")

        db_cursor.close()
        db_connection.close()

        schema_connection = psycopg2.connect(dbname=DB_NAME, user="postgres", host="localhost")
        schema_cursor = schema_connection.cursor()
        schema_cursor.execute("""
        create table if not exists users (
            id serial primary key,
            username text unique not null,
            display_name text,
            email text,
            phone text,
            assigned_tags text[] default '{}'
            );
        
        create table if not exists groups (
            id serial primary key,
            name text unique not null
        );
                              
        create table if not exists contacts (
            id serial primary key,
            full_name text,
            email text,
            phone text,
            title text
        );
                              
        create table if not exists group_contacts (
            group_id integer references groups(id) on delete cascade,
            contact_id integer references contacts(id) on delete cascade,
            primary key (group_id, contact_id)
        );
        """)
        schema_connection.commit()
        schema_cursor.close()
        schema_connection.close()
        print("Schema imported.")
    except Exception as e:
        print("Exception: ", e)

if __name__ == "__main__":
    run()