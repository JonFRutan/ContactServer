#jfr
import vobject, psycopg2

DB = {
    "dbname": "contacts_db",
    "user": "contacts_admin",
    "password": "test",
    "host": "localhost"
}

#takes all the records found in the contacts table and generates vcards out of them.
def generate_vcards():
    cards = []
    db_connection = psycopg2.connect(**DB)
    db_cursor = db_connection.cursor()

    db_cursor.execute("""select full_name, email, phone, title from contacts;""")
    #the cursor object is iterable, so we can iterate through retrieved records.
    for full_name, email, phone, title in db_cursor:
        vcard = vobject.vCard()

        vcard.add('fn') # full name - 'fn' attribute is required by vobject
        vcard.fn.value = full_name

        vcard.add('n')  # username
        vcard.n.value = vobject.vcard.Name(family='', given=full_name)

        email_field = vcard.add('email')
        email_field.value = email
        email_field.type_param = 'INTERNET'

        tel_field = vcard.add('tel')
        tel_field.value = phone
        tel_field.type_param='WORK'

        if title:
            title_field = vcard.add('title')
            title_field.value = title

        cards.append(vcard)
        vcard.serialize()
        vcard.prettyPrint()

    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    return cards


