import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote

# MySQL connection details
user = 'root'  # your MySQL username
pw = '1234'  # your MySQL password
db = 'techpay'  # your MySQL database name
engine = create_engine(f"mysql+pymysql://{user}:%s@localhost/{db}" % quote(f'{pw}'))

# Title of the app
st.title('Funnel Data Input Form and Dashboard')

# Create the form to collect input data
with st.form(key='funnel_form'):
    opportunity_name = st.text_input('Opportunity Name')
    work = st.text_input('Work')
    stage = st.text_input('Stage')
    est_value = st.number_input('Estimated Value', min_value=0, step=1)
    relationship_owner = st.text_input('Relationship Owner')
    probability = st.number_input('Probability', min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
    notes = st.text_area('Notes')
    no_of_projects = st.number_input('No of Projects', min_value=1, step=1)

    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Handle form submission
if submit_button:
    # Validation: Check if all required fields are filled
    if not opportunity_name or not work or not stage or not relationship_owner:
        st.error("Please fill in all required fields.")
    else:
        # Create a DataFrame with the collected data
        data = {
            'Opportunity': opportunity_name,
            'Name': opportunity_name,
            'Work': work,
            'Stage': stage,
            'Est. value': est_value,
            'Relationship owner': relationship_owner,
            'Probability': probability,
            'Notes': notes,
            'No of Projects': no_of_projects
        }

        df = pd.DataFrame([data])

        # Insert the data into MySQL
        try:
            df.to_sql('funnel', con=engine, if_exists='append', index=False, chunksize=1000)
            st.success("Data submitted successfully!")
        except Exception as e:
            st.error(f"Error while submitting data: {str(e)}")

# Display live data from MySQL
st.subheader('Live Funnel Data')

try:
    # Query the MySQL database to get the data
    query = "SELECT * FROM funnel"
    live_data = pd.read_sql(query, con=engine)

    # Display the data in Streamlit as a dataframe
    if live_data.empty:
        st.write("No data available.")
    else:
        st.dataframe(live_data)
except Exception as e:
    st.error(f"Error while fetching data: {str(e)}")
