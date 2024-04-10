# Import Modules
import streamlit as st
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['testdb']
# Access the 'example_collection' collection
collection = db['example_collection']

# Prepare a document to insert
#document = {
#    'name': 'John Doe',
#    'age': 30,
#    'email': 'john@example.com'
#}

# Query for documents with age greater than 25
query = {'name': 'John Doe'}
results = collection.find(query)
for result in results:
    st.markdown(results)
