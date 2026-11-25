import pandas as pd
import numpy as np

# 1. Load raw data
df = pd.read_csv('social_media_posts.csv')

# 2. Trim extra spaces in text columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# 3. Remove commas from numbers and convert data types
df['Views'] = pd.to_numeric(df['Views'].astype(str).str.replace(',', '', regex=False), errors='coerce').astype('Int64')
df['Likes'] = pd.to_numeric(df['Likes'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).astype('int64')
df['Comments'] = pd.to_numeric(df['Comments'], errors='coerce').fillna(0).astype('int64')

# 4. Standardize casing & domain categories
df['Kind'] = df['Kind'].str.lower()
df['Content_Type'] = df['Content type'].str.lower()
df['Content_Category'] = df['Content category'].str.lower()

domain_map = {
    'Cyber Security': 'Cybersecurity',
    'Cybersecurity': 'Cybersecurity',
    'Cybersecurity & Cloud Security': 'Cybersecurity & Cloud',
    'AIML': 'AI & Machine Learning',
    'AI & Machine Learning': 'AI & Machine Learning',
    'Generative AI': 'AI & Machine Learning',
    'Artificial Intelligence': 'AI & Machine Learning',
    'AI & Generative AI': 'AI & Machine Learning',
    'Cloud': 'Cloud Computing',
    'Cloud Computing': 'Cloud Computing',
    'Cloud Computing & FinOps': 'Cloud Computing',
    'Other': 'Other'
}
df['Domain'] = df['domain'].map(domain_map).fillna(df['domain'])

# 5. Clean URLs & remove duplicate posts (keep latest snapshot)
df['Published_dt'] = pd.to_datetime(df['Published'], utc=True)
df['Post_URL'] = df['Link'].str.split('&utm_', regex=False).str[0].str.split('?utm_', regex=False).str[0]
df = df.sort_values(['Published_dt', 'Views'], ascending=[False, False]).drop_duplicates(subset=['Post_URL'], keep='first')

# 6. Recalculate Interactions & Engagement Rate
df['Total_Interactions'] = df['Likes'] + df['Comments']
df['Engagement_Rate_Pct'] = np.where(
    df['Views'].notna() & (df['Views'] > 0),
    np.round((df['Total_Interactions'] / df['Views']) * 100, 4),
    np.nan
)

# 7. Add Date/Time helper columns & Post_ID
df['Published_Timestamp'] = df['Published_dt'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['Published_Date'] = df['Published_dt'].dt.strftime('%Y-%m-%d')
df['Day_of_Week'] = df['Published_dt'].dt.day_name()
df['Published_Hour'] = df['Published_dt'].dt.hour
df['Hashtag_Count'] = df['Hashtags'].apply(lambda x: 0 if pd.isna(x) or str(x).strip() == '' else len([t.strip() for t in str(x).split(',') if t.strip()]))

df = df.sort_values('Published_dt').reset_index(drop=True)
df.insert(0, 'Post_ID', range(1, len(df) + 1))

final_cols = [
    'Post_ID', 'Platform', 'Kind', 'Post_URL', 'Views', 'Likes', 'Comments',
    'Total_Interactions', 'Engagement_Rate_Pct', 'Published_Timestamp',
    'Published_Date', 'Day_of_Week', 'Published_Hour',
    'Content_Type', 'Content_Category', 'Domain', 'Hashtags', 'Hashtag_Count'
]
df[final_cols].to_csv('cleaned_social_media_posts.csv', index=False)
print("Saved cleaned_social_media_posts.csv successfully!")