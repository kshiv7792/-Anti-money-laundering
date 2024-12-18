import gspread
import mysql.connector

# Authenticate without OAuth (works only if the sheet is public)
client = gspread.authorize(None)

# Open the Google Sheet using its public URL
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1mKFEPsbtZpwlUWLWOUHU2P1sQMuBKMjWqrXdHEimW_g/edit?usp=sharing")
sheet = spreadsheet.sheet1  # Access the first sheet

# Fetch all records from the sheet
data = sheet.get_all_records()

# Connect to MySQL
db = mysql.connector.connect(
  host="localhost",
  user="root",  # Use your MySQL username
  password="1234",  # Use your MySQL password
  database="techpay"
)


cursor = db.cursor()

# Prepare the column names and values to insert into MySQL
columns = ', '.join(data[0].keys())  # Column names from the first record
values = [tuple(row.values()) for row in data]  # Values from each row

# Create the MySQL table if it doesn't exist
create_table_query = f"""
CREATE TABLE IF NOT EXISTS google_sheet_data (
    {', '.join([f'{key} VARCHAR(255)' for key in data[0].keys()])}
);
"""
cursor.execute(create_table_query)

# Insert the data into the MySQL table
insert_query = f"""
INSERT INTO google_sheet_data ({columns})
VALUES ({', '.join(['%s'] * len(data[0]))})
"""
cursor.executemany(insert_query, values)
db.commit()

print("Data successfully inserted into MySQL database!")

# Close MySQL connection
cursor.close()
db.close()
