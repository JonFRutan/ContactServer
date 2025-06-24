#jfr
import vobject, psycopg2, os, requests
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

RAD_URLS=os.getenv('RAD_URLS')
RAD_USER=os.getenv('RAD_USER')
RAD_PASS=os.getenv('RAD_PASS')
RAD_ADDR=os.getenv('RAD_ADDR')

DB = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST
}

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

    print("Exporting vcards to output.vcf")
    export_vcards(cards)
    return cards

def radicale_vcf_import():
    temp_file = "temp_radicale.vcf"
    vcards = generate_vcards()
    if not vcards:
        print("No contacts returned from generate")
        return
    print(f"Generating combined VCF file: {temp_file}")
    export_vcards(vcards, temp_file)
    radicale_upload = f"{RAD_URLS}/{RAD_USER}/"
    auth = (RAD_USER, RAD_PASS)
    try:
        with open(temp_file, 'rb') as vcf:
            files = {'uploadfile': (os.path.basename(vcf.name), vcf, 'text/vcard')}
            data = {'href': RAD_ADDR}
            print(f"Uploading {temp_file} to Radicale as {RAD_ADDR}")
            response = requests.post(
                radicale_upload,
                auth=auth,
                files=files,
                data=data
            )
            response.raise_for_status()
            print(f"Address Book {RAD_ADDR} created.")
    except requests.exceptions.RequestException as e:
        print(f"Error uploading VCF into Radicale: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"Temp file cleaned {temp_file}")

if __name__ == "__main__":
    print(DB)
