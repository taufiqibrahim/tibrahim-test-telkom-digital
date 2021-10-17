# MongoDB to MySQL

## Prepare mongo-seed/seed.json

We need to change the date fields from string into Extended JSON using JQ.
```bash
cd mongo-seed
jq -f fix_dates.jq seed.orig.json > seed.json
cd ..
```

## Initialize Sandbox Containers

Run using `docker-compose`
```bash
docker-compose up -d
```

- MySQL
    - Host: localhost
    - Port: 3306
    - Database: example
    - User: root
    - Password: example
- MongoDB
    - Mongo Express: http://localhost:8081

