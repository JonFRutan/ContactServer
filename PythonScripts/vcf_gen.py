#jfr
import vobject, psycopg2

DB = {
    "dbname": "contacts_db",
    "user": "contacts_admin",
    "password": "test",
    "host": "localhost"
}

#currently generates based on users table, when it should generate based on contacts table
def generate_vcards():
    cards = []
    db_connection = psycopg2.connect(**DB)
    db_cursor = db_connection.cursor()

    db_cursor.execute("""select * from users;""")
    #the cursor object is iterable, so we can iterate through retrieved records.
    #[0] for ID, [1] for username, [2] for full name, [3] for email, [4] for phone
    for record in db_cursor:
        username, display_name, email, phone = record[1], record[2], record[3], record[4]
        vcard = vobject.vCard()

        vcard.add('fn') # full name - 'fn' attribute is required by vobject
        vcard.fn.value = display_name

        vcard.add('n')  # username
        vcard.n.value = vobject.vcard.Name(family='', given=username)

        email_field = vcard.add('email')
        email_field.value = email
        email_field.type_param = 'INTERNET'

        tel_field = vcard.add('tel')
        tel_field.value = phone
        tel_field.type_param='WORK'

        cards.append(vcard)
        vcard.serialize()
        vcard.prettyPrint()
    return cards

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

