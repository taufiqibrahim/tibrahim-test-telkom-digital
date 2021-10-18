from datetime import timedelta
import pytz
import random
from faker import Faker
from pymongo import MongoClient

fake = Faker()

RANGE = 1000000
TZ_INFO = pytz.timezone('Asia/Jakarta')
MONGO_HOST = "mongodb://root:example@localhost:27017"
MONGO_DB = "local"
MONGO_COLLECTION = "vaccination"
client = MongoClient(MONGO_HOST)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


for _ in range(RANGE):
    gender = 'M' if random.randint(0, 1) else 'F'

    full_name = fake.name_male() if gender == 'M' else fake.name_female()

    created_at = fake.date_time_between(start_date='-4d', end_date='-1d', tzinfo=TZ_INFO)
    # created_at = fake.date_time_between(start_date='2021-10-11 00:00:00', end_date='2021-10-13 00:00:00', tzinfo=TZ_INFO)
    updated_at = created_at + timedelta(days=random.randint(0, 2))

    data = {
        # "_id": "5ffdf9f4f90ec3ce06b11892",
        "vaccinePatient": {
            "profession": "teacher",
            "fullName": full_name,
            "gender": gender,
            "bornDate": "1990-09-13",
            "mobileNumber": "089912345671",
            "nik": "1105095309901232"
        },
        "channel": random.choice(['loket', 'umb', ]),
        "createdAt": created_at,
        "updatedAt": updated_at,
        "vaccination": {
            "vaccineDate": "2021-01-13",
            "vaccineLocation": {
                "name": "KLINIK SETIA",
                "faskesCode": "CC23456"
            },
            "vaccineCode": "W-87654321",
            "vaccineStatus": "2",
            "type": "second"
        }
    }
    # print(data)
    collection.insert_one(data)

print(f"{RANGE} has been inserted to MongoDB")
