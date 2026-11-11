#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'
url


# In[4]:


df = pd.read_csv(
    url,
    nrows=100
)


# In[5]:


df.info()


# In[6]:


df.head()


# In[7]:


 # we need to specify the types:
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


# In[8]:


df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[9]:


df.head()


# In[10]:


df.info()


# In[12]:


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')


# In[13]:


engine


# In[14]:


# we want to create schema like this for 'yellow_taxi_data'
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[25]:


df.head(0)


# In[26]:


df.head(0).info()


# In[15]:


# Now create only schema as we see with zero values
df.head(0).to_sql(
    name='yellow_taxi_data', 
    con=engine,
    if_exists='replace' # if something is there then it gonna drop and replace with this empty value schema
)


# In[17]:


df = pd.read_csv(
    url,
)


# In[18]:


len(df)


# In[28]:


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


# In[32]:


from tqdm.auto import tqdm
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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




