from sqlalchemy import *

DB_USER = "YOUR_DB_USERNAME_HERE"
DB_PASSWORD = "YOUR_DB_PASSWORD_HERE"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"

engine = create_engine(DATABASEURI)
