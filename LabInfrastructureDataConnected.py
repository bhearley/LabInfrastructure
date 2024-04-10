# Import Modules
import streamlit as st

import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

db = client['testdb']
# Access the 'example_collection' collection
collection = db['example_collection']

# Query for documents with age greater than 25
query = {'name': 'John Doe'}
results = collection.find(query)
# Print the matching documents
for result in results:
    st.markdown(result['name'])
