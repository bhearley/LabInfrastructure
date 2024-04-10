import streamlit as st
from pymongo.mongo_client import MongoClient
import dns

uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
# Create a new client and connect to the server
#client = MongoClient(uri)

client = MongoClient(**st.secrets["mongo1"])
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.markdown("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.markdown(e)

db = client['testdb']
# Access the 'example_collection' collection
collection = db['example_collection']

# Query for documents with age greater than 25
query = {'name': 'John Doe'}
results = collection.find(query)
# Print the matching documents
for result in results:
    st.markdown(result)


