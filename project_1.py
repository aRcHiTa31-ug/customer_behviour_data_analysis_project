#import numpy as np
import pandas as pd
df=pd.read_csv("customer_shopping_behavior.csv") # read the csv data
df.columns = df.columns.str.lower().str.replace(' ', '_')
print(df.head()) # gives the top 5 rows
print(df.info()) # gives all type of information regarding table
print(df.describe()) # gives summary statistics of numerical column
print(df.describe(include='all')) # give summary statistics of both numerical & categorical column
print(df.isnull().sum()) # tells the all missing values in each rows

# to fill the missing values, we choose median over mean because median os robust to outliers, while mean is
# highly effected. basically mean is sensitive to extreme values.

# Fill missing Review Rating values using the median rating of each Category.
# transform() is used so the computed median is repeated for every row in the group,
# keeping the original DataFrame shape and allowing safe assignment.

df['review_rating']=df.groupby('category')['review_rating'].transform(lambda x:x.fillna(x.median()))
print(df['review_rating'])
print(df.isnull().sum()) # to check filling isss done
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns) # to check the changes

# create a column og age_group
labels=['young adults','adults','middle-age','senior']
df['age_group']=pd.qcut(df['age'], q=4, labels=labels) # 'labels=labels' maps my custom label
                                                           # list to the qcut labels parameter
print(df[['age','age_group']]) # outer []-> data frame selection
                               # inner[] -> list of column names, bcz pandas except one col name not multiple

# for better analysis
# create column purchase_frequency_days
print(df['frequency_of_purchases'])
frequency_mapping={'Fortnightly':14,
                   'Weekly':7,
                   'Bi-Weekly':14,
                'Quarterly': 90,
                   'Annually':365,
                   'Every 3 month':90,
                   'Monthly':30
                   }
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases','purchase_frequency_days']].head(10)) # to see 10 columns

# clean sum data
print(df[['discount_applied', 'promo_code_used']].head(10))
print((df['discount_applied']==df['promo_code_used']).all()) # True is the output so both are same then we will
                                                                # keep only one column
df=df.drop('promo_code_used',axis=1) # axia=1 shows column, we need to specify it coz by default it select rows
print(df.columns)

import pandas as pd
from sqlalchemy import create_engine

# 1. Setup the connection details
# Replace 'root' and 'password' with your actual MySQL credentials
user = 'root'
password = 'Pihu%4012345'
host = 'localhost'
port = '3306'
database = 'customer_shopping_behavior'

# 2. Create the connection engine
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# 3. Upload the DataFrame
try:
    df.to_sql(name='cleaned_data', con=engine, if_exists='replace', index=False)
    print("Data uploaded successfully to MySQL!")
except Exception as e:
    print(f"Error: {e}")