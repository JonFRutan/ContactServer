#jfr
import vobject, psycopg2, requests, uuid
from PythonScripts.utils import DB, RAD

#export vcards into a single file, for use in payload.
def export_vcards(cards, filepath):
    count = 0
    with open(filepath, 'w', encoding='utf-8') as o:
        for card in cards:
            o.write(f"{card.serialize()}\nEND:VCARD\n")
            count += 1
    print(f"{filepath} created with {count} vCards.")

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

        uid_field = vcard.add('uid')
        uid_field.value = str(uuid.uuid4())

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

    #print("Exporting vcards to output.vcf")
    #export_vcards(cards)
    return cards

#ugly parameters and function name
def upload_card_to_radicale(session, radicale_url, username, addressbook, vcard):
    vcard_file = f"{vcard.uid.value}.vcf"
    contact_url = f"{radicale_url}/{username}/{addressbook}/{vcard_file}"
    headers = {
        "Content-Type": "text/vcard"
    }
    vcard_content = vcard.serialize()
    try:
        response = session.put(contact_url, headers=headers, data=vcard_content)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error uploading: {e}")

def upload_group_to_book(group, addressbook):
    pass
    # The idea here is that provided an addressbook and a group, we can select all the contacts pertaining to that group
    # using the join table group_contacts and push them into a specified addressbook.
    # these addressbooks for now are manually created on the Radicale interface, like 'super'.

# this must be replaced, it's too statically written for it's own good.
# change the .env variables into arguments. 
def upload_all_to_radicale():
    with requests.Session() as session:
        session.auth = (RAD.user, RAD.password)
        cards = generate_vcards()
        if not cards:
            print("Error at contact card creation")
            return
        for card in cards:
            upload_card_to_radicale(session, RAD.url, RAD.password, RAD.addressbook, card) # This is no good

       
if __name__ == "__main__":
    upload_all_to_radicale()
