#pip install gspread oauth2client mysql-connector-python


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector

# Set up the scope and credentials for accessing Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Shiv\Downloads\funneldata12152024-feeeae67b648.json', scope)

client = gspread.authorize(credentials)

# Open the Google Sheet by name (or you can use the sheet URL)
sheet = client.open("Untitled spreadsheet").sheet1  # Or use .get_worksheet(index)

# Fetch all data from the sheet
data = sheet.get_all_records()  # Returns a list of dictionaries, one for each row

# Connect to MySQL
mydb = mysql.connector.connect(
  host="your-mysql-host",
  user="root",  # Use your MySQL username
  password="1234",  # Use your MySQL password
  database="techpay"
)

mycursor = mydb.cursor()

# Create a query to insert data into the MySQL table
insert_query = """INSERT INTO your_table (column1, column2, column3)
                  VALUES (%s, %s, %s)"""

# Loop through the Google Sheets data and insert it into MySQL
for row in data:
    values = (row['column1'], row['column2'], row['column3'])  # Change based on your sheet columns
    mycursor.execute(insert_query, values)

# Commit the changes and close the connection
mydb.commit()
mycursor.close()
mydb.close()

print("Data successfully inserted into MySQL!")
