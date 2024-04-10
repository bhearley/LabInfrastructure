import streamlit as st
import pymongo


#write data in a file.

temp_file = "/mount/src/labinfrastructure/TestData.txt'

file1 = open(temp_file, "w")
content = file1.read()

st.markdown(content)


L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
# \n is placed to indicate EOL (End of Line)
file1.write("Hello \n")
file1.writelines(L)
file1.close()  # to change file access modes

file1 = open(temp_file, "w")

st.markdown(content)

#@st.cache_resource
#def init_connection():
#    return pymongo.MongoClient(**st.secrets["mongo"])


