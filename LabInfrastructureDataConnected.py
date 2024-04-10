# Import Modues
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi

# Set the page configuration
st.set_page_config(layout="wide")

# Create the Title
st.title("NASA GRC Laboratory Infrastructure Data Collection")

# Create Instructions
st.markdown('The NASA GRC Laboratory Infrastructure Data Collection Tool will capture the current state of GRC capabilities. ' +
            'This information is necessary to assess the overall state of our infrastructure and assets and will be used to develop ' +
            'strategic plans for laboratory investment. \n \n \n' 
            'Please complete each of the fields below for Laboratory assets.  \n\n' +
            '  - A Laboratory is defined as a dedicated facility, or dedicated infrastructure, for performing a specific type of testing, ' +
            'research, or development. A laboratory may encompass a unique capability, and may include multiple high values assets such as ' +
            'test or analytical equipment. (i.e. The Structural Dynamics Laboratory) \n\n' 
            '  - An asset is defined as a unique equipment that is segregable from the facility. An asset may be composed of multiple components. (i.e. a Scanning Electron Microscope). Consider only assets associated with the infrastructure of the lab and not the facility. \n\n' + 
            '  - For each laboratory enter assets with a value over $50K or assets at lower values that are extremely critical or different to replace. \n\n \n'+
           'For questions regarding the data collection tool, please contact Brandon Hearley (LMS) at brandon.l.hearley@nasa.gov')

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
        
    
    if st.button('Load Previous Entry from Database'):
        selection_grid = st.columns(2)
        with selection_grid[0]:
            selection_branch = st.selectbox('Select the Branch:',selection_branch_list,on_change = get_selection_lab, key = 'selection_branch') 
        with selection_grid[1]:
            selection_lab = st.selectbox('Select the Branch:',selection_lab_list, key = 'selection_lab')

        if st.button('Load Data'):
            # Query the database for the record
            query = {'Laboratory/Capability Name': selection_lab}
            results = collection.find(query)
            # Print the matching documents
            for result in results:
                        st.session_state.name = result['Laboratory/Capability Name']
                    

#Create Divider for Name and Description
st.subheader('Laboratory Information')

# Create Input for Asset Name
lab_name = st.text_input("Laboratory Name:",value='',key='name')

# Create Input for Point of Contact
poc = st.text_input("Point of Contact:",value='', key = 'poc')

# Create Input for Branch
branch = st.text_input("Branch:",value='', key = 'branch')

# Create Input for Asset Description
lab_desc = st.text_area("Laboratory/Capability Description:",value='',key='desc')

# Create Input for Asset Website
lab_link = st.text_input("Laboratory/Capability Website:",value='',key='link')

# Create Input for Describing Challegne in Sustaining
lab_chal = st.text_area("Challenges in sustaining this laboratory/capability:",value='',key='chal')

# Create Input for Age
lab_age = st.number_input("Age (yrs):",min_value=0,max_value=None,value=0,help="The age of the laboratory/capability (i.e., how long we've had this capability at NASA GRC)",key='lab_age_k')

# Create Input for Condition
cond_opts = ['Excellent','Good','Fair','Poor']
lab_condition = st.selectbox('Condition:',cond_opts,key='cond')










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

