import pandas as pd
from sqlalchemy import create_engine, URL

# 1. Read the cleaned CSV
df = pd.read_csv('cleaned_social_media_posts.csv')
print(f"Rows found in CSV: {len(df)}")

# 2. Build a safe connection URL (handles special characters in passwords)
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Sai@9486",  
    host="localhost",
    port=3306,
    database="social_media_db",
    query={"charset": "utf8mb4"}
)

engine = create_engine(connection_url)

# 3. Upload directly to the 'posts' table
df.to_sql(name='posts', con=engine, if_exists='replace', index=False)

print(f"Successfully imported {len(df)} records into MySQL table 'posts'!")