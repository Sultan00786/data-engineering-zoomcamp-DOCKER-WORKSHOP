#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

pg_user = 'root'
pg_pass = 'root'
pg_host = "localhost"
pg_port = 5432
pg_db = 'ny_taxi'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
year = 2021
month = 1

# Read a sample of the data

url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)

engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')


# we want to create schema like this for 'yellow_taxi_data'
print("Schema for 'yellow_taxi_data' table")
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
df.head(0).to_sql(
    name='yellow_taxi_data', 
    con=engine,
    if_exists='replace' # if something is there then it gonna drop and replace with this empty value schema
)



df = pd.read_csv(
    url,
)
print(f'NO. of row in csv file: {len(df)}')


# csv file have 1.36M rows, 
# so we reading this csv file in 100k cunks of row
# so we are iterating as 100k window cunks
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)
for df_i in df_iter:
    print(len(df_i))



# Now load 100K cunks wise data in postgresql
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)
for df_i in tqdm(df_iter):
    df_i.to_sql(
         name='yellow_taxi_data', 
        con=engine,
        if_exists='append' # if something is there then it gonna append rows
    )


