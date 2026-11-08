import sys      # sys = system-related functionality.
import pandas as pd
# print(r'System args ',sys.argv)
month = sys.argv[1]
df = pd.DataFrame({"id": [1, 2], "day": [3, 4]})
df.loc[:,'month'] = month
df.to_parquet(f'output_month_{month}.parquet')
print(f'{df}')