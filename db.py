from sqlalchemy import *

DB_USER = "ys3593"
DB_PASSWORD = "0316"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_SERVER + "/proj1part2"


def getEngine():
    return create_engine(DATABASEURI)
