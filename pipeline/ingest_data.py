
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')


def run (pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
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
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # csv file have 1.36M rows, 
    # so we reading this csv file in 100k cunks of row
    # so we are iterating as 100k window cunks

    # Now load 100K cunks wise data in postgresql
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )
    first = True
    
    for df_i in tqdm(df_iter):
        if first:
            # for first iterate, we want to create schema like this for 'yellow_taxi_data'
            df_i.head(0).to_sql(
                name='yellow_taxi_data', 
                con=engine,
                # if something is there then it gonna drop and replace with this empty value schema
                if_exists='replace' 
            )
            table_schema = pd.io.sql.get_schema(
                df_i, 
                name=target_table, 
                con=engine
            )
            print(f'Table Created \n{table_schema}')
            first = False
        df_i.to_sql(
            name='yellow_taxi_data', 
            con=engine,
            # if something is there then it gonna append rows
            if_exists='append' 
        )
        print(len(df_i))

# Only run the code if this file directly executed in the terminal.
if __name__ == '__main__': 
    run()