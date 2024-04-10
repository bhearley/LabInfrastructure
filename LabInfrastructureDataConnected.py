import streamlit as st
import pymongo


st.markdown(st.secrets["mongo"]["host"])
st.markdown(st.secrets["mongo"]["port"])
st.markdown(st.secrets["mongo"]["username"])
st.markdown(st.secrets["mongo"]["password"])

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

#@st.cache_resource
#def init_connection():
#    connection_string = st.secrets["mongo"]["connection_string"]
#    return pymongo.MongoClient(connection_string)

#client = init_connection()
try:
    client.admin.command('ping')
    st.markdown("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.markdown(e)
