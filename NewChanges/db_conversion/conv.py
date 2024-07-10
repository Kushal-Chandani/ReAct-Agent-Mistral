import sqlite3
import pandas as pd

# Define the CSV file path and database path
csv_file_path = 'db_conversion\Transactions.csv'
db_path = 'db_conversion\chatbotupdate.db'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Connect to the existing SQLite database
conn = sqlite3.connect(db_path)

# Create a new table name (e.g., 'csv_data')
table_name = 'Finalchatbot'

# Write the DataFrame to a new table in the database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print(f"CSV data has been successfully imported into the '{table_name}' table in the database.")
