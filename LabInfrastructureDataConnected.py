import streamlit as st
import pymongo


client = pymongo.MongoClient("mongodb+srv://nasagrc:{st.secrets['MONGODB_PASSWORD']}@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest")
try:
    client.admin.command('ping')
    st.markdown("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.markdown(e)

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
#def get_data():
#    db = client.testdb
#    items = db.mycollection.find()
#    items = list(items)  # make hashable for st.cache_data
#    return items

#items = get_data()

# Print results.
#for item in items:
#    st.write(item["name"])
