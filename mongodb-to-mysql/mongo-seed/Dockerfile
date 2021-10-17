FROM mongo

COPY seed.json /seed.json
COPY seed_types.txt /seed_types.txt
RUN sleep 20
CMD mongoimport --host mongo --db local --collection vaccination --drop --type json \
    --file /seed.json --jsonArray \
    --authenticationDatabase admin --username root --password example
