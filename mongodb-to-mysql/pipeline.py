import pymysql
import pytz
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

MONGO_HOST = "mongodb://root:example@localhost:27017"
MONGO_DB = "local"
MONGO_COLLECTION = "vaccination"
INGEST_DATE = '2021-10-15'
INGEST_DATE_START = datetime.strptime(INGEST_DATE, '%Y-%m-%d')
INGEST_DATE_START = INGEST_DATE_START.replace(
    tzinfo=pytz.timezone('Asia/Jakarta'))
INGEST_DATE_END = INGEST_DATE_START + timedelta(days=1)

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'example'
MYSQL_DB = 'example'


def default_filters():
    return {
        "$or": [
            {'createdAt': {"$gte": INGEST_DATE_START, "$lt": INGEST_DATE_END}},
            {'updatedAt': {"$gte": INGEST_DATE_START, "$lt": INGEST_DATE_END}}
        ],
    }


def default_transformer(doc):
    return doc


def get_mongo_docs_by_date(db, collection, filters, transformer=default_transformer):
    client = MongoClient(MONGO_HOST)
    db = client[db]
    collection = db[collection]

    docs = list()

    for doc in collection.find(filters):
        docs.append(transformer(doc))

    return docs


def vaccination_doc_transformer(doc):
    transformed = {
        "_id": doc.get('_id'),
        "channel": doc.get('channel'),
        "createdAt": doc.get('createdAt'),
        "updatedAt": doc.get('updatedAt'),
        "vaccination_type": doc.get('vaccination', {}).get('type'),
        "vaccination_vaccineCode": doc.get('vaccination', {}).get('vaccineCode'),
        "vaccination_vaccineDate": doc.get('vaccination', {}).get('vaccineDate'),
        "vaccination_vaccineLocation_faskesCode": doc.get('vaccination', {}).get('vaccineLocation', {}).get('faskesCode', {}),
        "vaccination_vaccineLocation_name": doc.get('vaccination', {}).get('vaccineLocation', {}).get('name', {}),
        "vaccination_vaccineStatus": doc.get('vaccination', {}).get('vaccineStatus'),
        "vaccinePatient_bornDate": doc.get('vaccinePatient', {}).get('bornDate'),
        "vaccinePatient_fullName": doc.get('vaccinePatient', {}).get('fullName'),
        "vaccinePatient_gender": doc.get('vaccinePatient', {}).get('gender'),
        "vaccinePatient_mobileNumber": doc.get('vaccinePatient', {}).get('mobileNumber'),
        "vaccinePatient_nik": doc.get('vaccinePatient', {}).get('nik'),
        "vaccinePatient_profession": doc.get('vaccinePatient', {}).get('profession'),
        "_ingestion_ts": datetime.utcnow(),
    }
    return transformed


def upsert_to_db(table_name, fields, key, docs):
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 database=MYSQL_DB,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    into_fields = ','.join([f"`{f}`" for f in fields])
    placeholders = ','.join(["%s" for field in fields])
    assignments = ','.join(
        ["`{f}` = VALUES(`{f}`)".format(f=f) for f in fields])
    sql = f"""
    INSERT INTO {table_name}
    ({into_fields})
    VALUES
    ({placeholders})
    ON DUPLICATE KEY UPDATE {assignments}
    """

    with connection:
        with connection.cursor() as cursor:
            data = [tuple(doc.values()) for doc in docs]
            cursor.executemany(sql, data)
            connection.commit()


# pipeline
docs = get_mongo_docs_by_date(
    db=MONGO_DB,
    collection=MONGO_COLLECTION,
    filters=default_filters(),
    transformer=vaccination_doc_transformer,
)

upsert_to_db(
    table_name='vaccinations',
    fields=[
        "_id",
        "channel",
        "createdAt",
        "updatedAt",
        "vaccination_type",
        "vaccination_vaccineCode",
        "vaccination_vaccineDate",
        "vaccination_vaccineLocation_faskesCode",
        "vaccination_vaccineLocation_name",
        "vaccination_vaccineStatus",
        "vaccinePatient_bornDate",
        "vaccinePatient_fullName",
        "vaccinePatient_gender",
        "vaccinePatient_mobileNumber",
        "vaccinePatient_nik",
        "vaccinePatient_profession",
        "_ingestion_ts",
    ], key=[], docs=docs)
