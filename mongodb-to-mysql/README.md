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
- Jupyter Notebook: http://localhost:8888
- Spark UI: http://localhost:4040

## Generate Fake Data
We will use `fake_data.py` to generate 1 million sample data.
```bash
# Create virtual environment
virtualenv venv --python=3.8
# Install python dependencies
pip install -r requirements.txt
# Generate data and insert to MongoDB
python fake_data.py
```

## Run Notebook
Open http://127.0.0.1:8888/notebooks/work/notebooks/telkom_demo.ipynb and run.

## Destroy Containers
```bash
docker-compose down -v
```