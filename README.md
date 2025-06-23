# Contact Server  
Contact management system that doesn't rely on WebDAV or a CardDAV server.  
I've tried many CardDAV systems and none of them have fully suited our use case or worked properly for implementation. My solution is to create a vertically integrated system that suits our specific use case:  
1. Export user contact info from sources (Azure, Outlook, Database, etc).  
2. Import into a local database on our machine using PostgreSQL.  
3. Export info as Jamf payloads to mobile device management and contact syncing.  
This avoids the overhead of an all-inclusive service like NextCloud or Mailcow, and allows us to also circumvent the limitations and setup complexity of tools like Baikal or SOGo.  

## Requirements  
- **Python**  
- **PostgreSQL**  
Python libraries will be managed using a virtual environment.  

## Setup  
In the project root type `make` and the Makefile will set up the virtual environment, install requirements, and run the database initialization script.  
Within your server you will need to create a contacts_db admin user, remember to give it privileges to your contacts database using the psql command: `grant all privileges on all tables in schema public to contacts_admin`  
Fill out a local .env file with the needed database and login information.  
