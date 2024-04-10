# Import Modues
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi

# Connect to the Database
uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
client = MongoClient(uri, tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Get List of Existing Records
db = client['LabData']
collection = db['LabData']
cursor = collection.find({})
Rec_Exist = {}
for document in cursor:
    # Get the current list of all branches
    cur_branch = list(Rec_Exist.keys())
    # -- Add branch if new
    if document["Branch"] not in cur_branch:
        Rec_Exist[document["Branch"]] = []

    # Add record to branch list
    Rec_Exist[document['Branch']].append(document["Laboratory/Capability Name"])

    # Initialize Lists
    selection_branch_list  =list(Rec_Exist.keys())
    selection_lab_list = Rec_Exist[selection_branch_list[0]]
    
    # Create the Function to get the list of branches
    def get_selection_lab():
        selection_lab_list = Rec_Exist[selection_branch]
        
    
    if st.button('Load previous Entry from Database'):
        selection_grid = st.columns(2)
        with selection_grid[0]:
            selection_branch = st.selectbox('Select the Branch:',selection_branch_list,on_change = get_selection_lab, key = 'selection_branch') 
        with selection_grid[1]:
            selection_lab = st.selectbox('Select the Branch:',selection_lab_list, key = 'selection_lab') 












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

