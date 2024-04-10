import streamlit as st
import pymongo


#write data in a file.

temp_file = 

file1 = open(temp_file, "w")
L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
 
# \n is placed to indicate EOL (End of Line)
file1.write("Hello \n")
file1.writelines(L)
file1.close()  # to change file access modes

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])


