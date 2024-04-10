import streamlit as st
from pymongo.mongo_client import MongoClient
import dns

uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
# Create a new client and connect to the server
#client = MongoClient(uri)

client = MongoClient(**st.secrets["mongo"])
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.markdown("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.markdown(e)
