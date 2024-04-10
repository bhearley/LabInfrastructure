import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi

uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
# Create a new client and connect to the server
#client = MongoClient(uri)

#client = MongoClient(**st.secrets["mongo2"])
client = MongoClient(uri, tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.markdown("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.markdown(e)

if st.button('View Data'):
    db = client['testdb']
    # Access the 'example_collection' collection
    collection = db['example_collection']
    
    # Query for documents with age greater than 25
    cursor = collection.find({})
    for document in cursor:
        st.markdown(document)
name = st.text_input("Name:",value='')
age = st.number_input("Age:",value=0)
email = st.text_input("Email:", value = '')

if st.button('Add Data'):
    db = client['testdb']
    # Access the 'example_collection' collection
    collection = db['example_collection']

    new_doc = {
    'name': name,
    'age': age,
    'email': email
    }

    new_entry = collection.insert_one(new_doc)

if st.button('Delete Data'):
    db = client['testdb']
    # Access the 'example_collection' collection
    collection = db['example_collection']
    myquery = { "name": name }

    collection.delete_one(myquery)

