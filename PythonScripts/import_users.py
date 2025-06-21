#jfr
import psycopg2, csv, sys

DB = {
    "dbname": "contacts_db",
    "user": "contacts_admin",
    "password": "test",
    "host": "localhost"
}

def import_from_csv(file_path):
    db_connection = psycopg2.connect(**DB)
    db_cursor = db_connection.cursor()

    with open(file_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        import_count = 0;
        for row in reader:
            tags = [t.strip() for t in row['tags'].split(',')] if row['tags'] else []
            db_cursor.execute("""
                insert into users (username, display_name, email, phone, assigned_tags)
                values (%s, %s, %s, %s, %s)
                on conflict (username) do update set
                    display_name = excluded.display_name,
                    email = excluded.email,
                    phone = excluded.phone,
                    assigned_tags = excluded.assigned_tags
            """, (row['username'], row['display_name'], row['email'], row['phone'], tags))
            import_count += 1;
        
        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        print(f"{import_count} users added to database.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Provide a filepath to a CSV file as an argument.")
        print("Usage: python import_users.py ./files/sample.csv")
        exit(1)
    import_from_csv(sys.argv[1])
