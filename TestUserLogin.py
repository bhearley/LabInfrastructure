#==================================================================================================================================================================
#   NASA GRC Lab Infrastructure Data Collection Tool
#   Brandon Hearley - LMS
#   4/11/2024
#
#   PURPOSE: Create a web app (using streamlit) to collect data on the GRC Lab Infrastructure. The data collected is 
#            stored in a Mongo Database.
#
#==================================================================================================================================================================
# SETUP
# Import the necessary modules to run the app

# Import Modules
# -- see requirements.txt for any specified versions need
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi
import datetime
import time
from PIL import Image
import io

#==================================================================================================================================================================
# GENERAL INFORMATION
# Set the web app general information not edited by the user

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
            '  - An asset is defined as a unique equipment that is segregable from the facility. An asset may be composed of multiple components. ' + 
            '(i.e. a Scanning Electron Microscope). Consider only assets associated with the infrastructure of the lab and not the facility. \n\n' + 
            '  - For each laboratory enter assets with a value over $50K or assets at lower values that are extremely critical or different to replace. \n\n \n'+
           'For questions regarding the data collection tool, please contact Brandon Hearley (LMS) at brandon.l.hearley@nasa.gov')

#==================================================================================================================================================================
# LOGIN
# Access Username/Login Info in Database
@st.cache_resource
def init_connection():
    uri = "mongodb+srv://nasagrc:" + st.secrets['mongo1']['password'] + "@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
    return MongoClient(uri, tlsCAFile=certifi.where())

# Create the Database Client
client = init_connection()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Read the Database
@st.cache_data(ttl=6000)
def get_user_data():
    db = client['LabData']
    items = db['UserInfo'].find()
    items = list(items)  # make hashable for st.cache_data
    return items

# Get All Data in Database
all_users = get_user_data()

# Default access to False
access = 'No'
password = ''

# Set Home Screen Options
home_screen = 1
def create_home_screen(home_screen):
    if home_screen == 1:
        # Create input for password
        grid_pass = st.columns([0.5,0.5])
        with grid_pass[0]:
            user_place = st.empty()
            username = user_place.text_input('Username',value = '', key="user_key")
                    
            pass_place = st.empty()
            password = pass_place.text_input('Password',value = '', type="password", key="pwd_key")
        
        # Check if Username Exists
        if username != '':
            user_flag = 0
            for k in range(len(all_users)):
                if all_users[k]['Username'] == username:
                    real_pass = all_users[k]['Password']
                    user_flag = 1
            if user_flag == 0:
                st.error('Username not found.')
            else:
                if password != "":
                    if password == real_pass:
                        access = 'Yes'
                        # Delete Widgets
                        user_place.empty()
                        pass_place.empty()
                    else:
                        st.error('The password entered is incorrect.')
        
        grid_user = st.columns([0.1,0.2,0.2,0.5])
        with grid_user[0]:
            login_btn = st.empty()
        with grid_user[1]:
            sign_up_btn = st.empty()
        
        new_user = st.empty()
        new_pass1 = st.empty()
        new_pass2 = st.empty()
        new_access_code = st.empty()
        sign_up_btn2 = st.empty()
        
        
        login_btn.button('Login', key='login_btn') 
        sign_up_btn.button('Sign Up with Access Code', key='sign_up_btn_1') 
        
        if st.session_state['sign_up_btn_1']:
            user_place.empty()
            pass_place.empty()
            login_btn.empty()
            sign_up_btn.empty()

    
    elif homescreen == 2:
        new_user.text_input('Enter Your Username',value='',key='new_user')
        new_pass1.text_input('Enter Your Pasword',value='', type='password',key='new_pass1')
        new_pass2.text_input('Re-enter Your Pasword',value='', type='password', key='new_pass2')
        new_access_code.text_input('Enter The Access Code',value='',key='new_access_code')
    
        if sign_up_btn2.button('Sign Up'):
            st.write(st.session_state['new_user'])
            # Check Username
            if st.session_state['new_user'] == '':
                st.error('Username cannot by empty')
            else:
                user_flag = 0
                for k in range(len(all_users)):
                    if all_users[k]['Username'] == st.session_state['new_user']:
                        user_flag = 1
                if user_flag == 1:
                    st.error('Username is unavailable. If you have an accout, please enter your password.')

if "user_key" not in st.session_state:
    st.write('test')
    create_home_screen(1)
else:
    st.write(st.session_state['sign_up_btn_1'])

if access == 'Yes':
    #==================================================================================================================================================================
    # DATA POPULATION
    # Set up the database connection and define functions to populate data fields in the web app

    # Connect to the Database
    @st.cache_resource
    def init_connection():
        uri = "mongodb+srv://nasagrc:" + st.secrets['mongo1']['password'] + "@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
        return MongoClient(uri, tlsCAFile=certifi.where())
    
    # Create the Database Client
    client = init_connection()
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    # Read the Database
    @st.cache_data(ttl=6000)
    def get_data():
        db = client['LabData']
        collection = db['LabData']
        query = {'Username': st.session_state["user_key"]}
        items = collection.find(query)
        items = list(items)  # make hashable for st.cache_data
        return items
    
    # Get All Data in Database
    all_data = get_data()
    all_labs = [''] #Initialize list of labs to display to user
    for k in range(len(all_data)):
        all_labs.append(all_data[k]["Laboratory/Capability Name"])
    all_labs.sort() #Sort the list of labs alphabetically
    
    # Load Data Function
    # -- Set the values in the web app from the database when an existing lab is chosen
    def load_data():
        # Populate the data fields in the web app if an lab is selected
        if st.session_state['selection_lab'] != '':
            # Get the database
            db = client['LabData']
            # Query the database for the record and get results
            query = {'Laboratory/Capability Name': st.session_state['selection_lab']}
            results = db['LabData'].find(query)
            for result in results:
                st.session_state['name'] = result['Laboratory/Capability Name']
                st.session_state['poc'] = result['Point of Contact']
                st.session_state['branch'] = result['Branch']
                st.session_state['desc'] = result['Laboratory/Capability Description']
                st.session_state['link'] = result['Laboratory/Capability Website']
                st.session_state['chal'] = result['Challenges in sustaining this laboratory/capability']
                st.session_state['lab_age'] = result['Age (yrs)']
                st.session_state['cond'] = result['Condition']
                st.session_state['asset_num'] = result['Number of Assets']
                for m in range(int(result['Number of Assets'])):
                    st.session_state[f'input_cola{m}'] = result['T1-Asset Name'][m]
                    st.session_state[f'input_colb{m}'] = result['T1-Location (Bldg/Rm)'][m]
                    st.session_state[f'input_colc{m}'] = result['T1-Age (yrs)'][m]
                    st.session_state[f'input_cold{m}'] = result['T1-Acquisition Year'][m]
                    st.session_state[f'input_cole{m}'] = result['T1-Expected Year of Obsolescence'][m]
                    st.session_state[f'input_colf{m}'] = result['T1-Asset Condition'][m]
                    st.session_state[f'input_colg{m}'] = result['T1-Replacement Cost ($)'][m]
                    st.session_state[f'input_colh{m}'] = result['T1-Impact to Capability if Lost'][m]
                    st.session_state[f'input_coli{m}'] = result['T1-Associated Software'][m]
                    st.session_state[f'input_colj{m}'] = result['T1-Inlcudes IT Hardware?'][m]
                    st.session_state[f'input_colk{m}'] = result['T1-Replacement'][m]
    
                # -- Never Replace Images (until I figure out loading/unloading images in streamlit/mongo)
                if 'Lab Images' in list(result.keys()):
                    lab_images_old = result['Lab Images']
                else:
                    lab_images_old = []
                #st.session_state['asset_img'] = result['Number of Asset Images']
                #for m in range(int(result['Number of Asset Images'])):
                #    st.session_state[f'input_colimga{m}'] = result['T2-Asset'][m]
                st.session_state['asset_img'] = 0
                
                st.session_state['sust'] = result['Sustainment Funding Source']
                st.session_state['fund_num'] = result['Number of Funding Sources']
                for m in range(int(result['Number of Funding Sources'])):
                    st.session_state[f'input_coll{m}'] = result['T3-Funding Source'][m]
                    date1 = result['T3-Funding Start Date'][m].split('-')
                    st.session_state[f'input_colm{m}'] = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
                    date2 = result['T3-Funding End Date'][m].split('-')
                    st.session_state[f'input_coln{m}'] = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))
                    st.session_state[f'input_colo{m}'] = result['T3-Funding Amount per Year ($)'][m]
                            
                st.session_state['proj_num'] = result['Number of Projects']
                for m in range(int(result['Number of Projects'])):
                    st.session_state[f'input_colp{m}'] = result['T4-Mission/Project Name'][m]
                    st.session_state[f'input_colq{m}'] = result['T4-WBS Number'][m]
                    st.session_state[f'input_colr{m}'] = result['T4-Project Use (%)'][m]
                    st.session_state[f'input_cols{m}'] = result['T4-Risk to Project'][m]
                    st.session_state[f'input_colt{m}'] = result['T4-Impact if Laboratory/Capability is Lost'][m]
                st.session_state['hist'] = result['History of capability utilization']
                st.session_state['impact'] = result['Major impact and contributions this capability has made possible']
                st.session_state['tot_imp'] = result['Overall impact of laboratory/capability is lost']
                st.session_state['dt_num'] = result['Number of Failures']
                for m in range(int(result['Number of Failures'])):
                    st.session_state[f'input_colu{m}'] = result['T5-Asset'][m]
                    date1 = result['T5-Start Date'][m].split('-')
                    st.session_state[f'input_colv{m}'] = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
                    st.session_state[f'input_colw{m}'] = result['T5-Time Down'][m]
                    st.session_state[f'input_colx{m}'] = result['T5-Unit'][m]
                    st.session_state[f'input_coly{m}'] = result['T5-Additional Notes'][m]
                    st.session_state[f'input_colyy{m}'] = result['T5-Impact'][m]
                st.session_state['cost_rep'] = result['Estimated Cost to Replace Entire Laboratory/Capability ($)']
                st.session_state['cost_serv'] = result['Cost of Service Contracts ($)']
                st.session_state['cost_ann'] = result['Annual Cost to Operate and Sustain the Lab ($/yr)']
                st.session_state['cost_inc'] = result['Incurred Cost For Downtime ($/yr)']
                st.session_state['labor_num'] = result['Number of Divisions (Labor Costs)']
                for m in range(int(result['Number of Divisions (Labor Costs)'])):
                    st.session_state[f'input_colz{m}'] = result['T6-Directorate'][m]
                    st.session_state[f'input_colaa{m}'] = result['T6-Labor Cost (%)'][m]
                st.session_state['status'] = result['Status']
    
    # Clear all fields
    if st.button('Clear All Fields'):
        # Clear Data
        st.session_state['name'] = ''
        st.session_state['poc'] = ''
        st.session_state['branch'] = ''
        st.session_state['desc'] = ''
        st.session_state['link'] = ''
        st.session_state['chal'] = ''
        st.session_state['lab_age'] = None
        st.session_state['cond'] = ''
        st.session_state['asset_num'] = 0
        st.session_state['asset_img'] = 0
        st.session_state['sust'] = ''
        st.session_state['fund_num'] = 0
        st.session_state['proj_num'] = 0
        st.session_state['hist'] = ''
        st.session_state['impact'] = ''
        st.session_state['tot_imp'] = ''
        st.session_state['dt_num'] = 0
        st.session_state['cost_rep'] = None
        st.session_state['cost_serv'] = None
        st.session_state['cost_ann'] = None
        st.session_state['cost_inc'] = None
        st.session_state['labor_num'] = 0
        st.session_state['status'] = 'Draft'
    
    # Load Data from Database
    if st.button('Load From Database'):
        selection_lab = st.selectbox('Select the Lab:',all_labs, on_change = load_data, key = 'selection_lab')
    #==================================================================================================================================================================
    # GENERAL LAB INFORMATION
    # Create inputs to collect general lab information
    
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
    lab_age = st.number_input("Age (yrs):", min_value=0, max_value=None, value=None, help="The age of the laboratory/capability (i.e., how long we've had this capability at NASA GRC)",key='lab_age')
    
    # Create Input for Condition
    cond_opts = ['','Excellent','Good','Fair','Poor']
    lab_condition = st.selectbox('Condition:',cond_opts,key='cond')
    
    # Create Input for Assets
    asset_rows = st.number_input('Number of Assets:', min_value=0, max_value=None, key='asset_num')
    grid_asset = st.columns([0.125,0.070,0.060,0.065,0.09,0.08,0.07,0.11,0.115,0.07,0.1])
    asset_name = [] #Store the asset name
    asset_loc = []  #Store the asset location
    asset_age = [] #Store the asset age
    asset_date_in = [] #Store the asset date of entry
    asset_date_out = [] #Store the asset date of obsolescence
    asset_cond = [] #Store the asset condition
    asset_cost = [] #Store the asset cost of replacement
    asset_imp = [] #Store the asset impact description
    asset_software = [] #Store the asset associated software
    asset_itrep = [] #Store if an IT/Hardware replacement is needed
    asset_repdesc = [] #Store the description on IT/Hardware replacement
    
    # Add rows to asset table
    def add_row_asset(row):
        # -- Asset Name
        with grid_asset[0]:
            while len(asset_name) < row+1:
                asset_name.append(None)
            if row == 0:
                asset_name[row]=st.text_input('Asset \n \n Name', key=f'input_cola{row}')
            else:
                asset_name[row]=st.text_input('Temp', key=f'input_cola{row}',label_visibility = "collapsed")
        # -- Asset Location    
        with grid_asset[1]:
            while len(asset_loc) < row+1:
                asset_loc.append(None)
            if row == 0:
                asset_loc[row]=st.text_input('Location  \n \n (Bldg/Rm)', key=f'input_colb{row}')
            else:
                asset_loc[row]=st.text_input('Temp', key=f'input_colb{row}',label_visibility = "collapsed")
        # -- Asset Age
        with grid_asset[2]:
            while len(asset_age) < row+1:
                asset_age.append(None)
            if row == 0:
                asset_age[row]=st.number_input('Age  \n \n  (yrs)', step=0.5, value = None, key=f'input_colc{row}')
            else:
                asset_age[row]=st.number_input('Temp', step=0.5, value = None, key=f'input_colc{row}',label_visibility = "collapsed")
        # -- Asset Year of Entry
        with grid_asset[3]:
            while len(asset_date_in) < row+1:
                asset_date_in.append(None)
            if row == 0:
                asset_date_in[row]=st.number_input('Acquistion  \n \n Year', step = 1, min_value = 0, max_value = 3000, value = None, help = 'The year the asset was acquired.', key=f'input_cold{row}')
            else:
                asset_date_in[row]=st.number_input('Temp', step = 1, min_value = 0, max_value = 3000, value = None, key=f'input_cold{row}',label_visibility = "collapsed")
        # -- Asset Date of Obsolescence
        with grid_asset[4]:
            while len(asset_date_out) < row+1:
                asset_date_out.append(None)
            if row == 0:
                asset_date_out[row]=st.number_input('Expected Year of Obsolescence', step = 1, min_value = 0, max_value = 3000, value = None, help = 'Expected year of obsolescence includes both the asset itself becoming obsolete and the inability to obtain a service contract for the asset.', key=f'input_cole{row}')
            else:
                asset_date_out[row]=st.number_input('Temp', step = 1, min_value = 0, max_value = 3000, key=f'input_cole{row}', value = None, label_visibility = "collapsed")
        # -- Asset Condition
        with grid_asset[5]:
            while len(asset_cond) < row+1:
                asset_cond.append(None)
            if row == 0:
                asset_cond[row]=st.selectbox('Asset  \n \n  Condition',  ('','Excellent', 'Good', 'Fair', 'Poor'), help="Excellent - No current issues with the asset. \n \n \n " +
                                                                                           "Good - Only minor issues with the asset that can be easily fixed. \n \n \n " +
                                                                                           "Fair - Asset is still in a working condition, but is near end of life. \n \n \n " +
                                                                                           "Poor - Asset has many issues/doesn't operate properly ", key=f'input_colf{row}')
            else:
                asset_cond[row]=st.selectbox('Temp', ('','Excellent', 'Good', 'Fair', 'Poor'),key=f'input_colf{row}',label_visibility = "collapsed")
        # -- Asset Cost of Replacement
        with grid_asset[6]:
            while len(asset_cost) < row+1:
                asset_cost.append(None)
            if row == 0:
                asset_cost[row]=st.number_input('Replacement \n \n  Cost ($)', step=1000, value= None, key=f'input_colg{row}')
            else:
                asset_cost[row]=st.number_input('Temp', step=1000, key=f'input_colg{row}', value = None, label_visibility = "collapsed")
        # -- Asset Impact if Lost
        with grid_asset[7]:
            while len(asset_imp) < row+1:
                asset_imp.append(None)
            if row == 0:
                asset_imp[row]=st.text_input('Impact to Capability \n \n  if Lost', key=f'input_colh{row}')
            else:
                asset_imp[row]=st.text_input('Temp', key=f'input_colh{row}',label_visibility = "collapsed")
        # -- Associated Software
        with grid_asset[8]:
            while len(asset_software) < row+1:
                asset_software.append(None)
            if row == 0:
                asset_software[row]=st.text_input('Associated Software / \n \n  Required OS', help = "List any assoicated software or required operating systems, separated by commas, necessary for the asset to operate", key=f'input_coli{row}')
            else:
                asset_software[row]=st.text_input('Temp', key=f'input_coli{row}',label_visibility = "collapsed")
        # -- IT/computer hardware repalcement
        with grid_asset[9]:
            while len(asset_itrep) < row+1:
                asset_itrep.append(None)
            if row == 0:
                asset_itrep[row]=st.selectbox('Inlcudes IT \n \n  Hardware?', ('','Yes','No'), help = 'Does the replacement of this asset require and IT Hardware replacement as well?', key=f'input_colj{row}')
            else:
                asset_itrep[row]=st.selectbox('Temp', ('','Yes','No'),key=f'input_colj{row}',label_visibility = "collapsed")
        # -- Parts vs Full Replacement
        with grid_asset[10]:
            while len(asset_repdesc) < row+1:
                asset_repdesc.append(None)
            if row == 0:
                asset_repdesc[row]=st.text_input('Replacement Parts \n \n Available?', help = 'Are replacement components available or would a full replacement be needed if asset is lost?', key=f'input_colk{row}')
            else:
                asset_repdesc[row]=st.text_input('Temp', key=f'input_colk{row}',label_visibility = "collapsed")
    
    # Add rows for each asset
    for r in range(int(st.session_state['asset_num'])):
        add_row_asset(r)
    
    # Create Input for Asset Images
    asset_imgs_lab = [] #Store the asset images label
    asset_imgs = [] #Store the asset images
    asset_imgs_notes = [] #Store the asset image notes
    asset_imgs_keep = [] #Store the asset image status
    asset_imgs_num = st.number_input('Number of NEW Asset Images:', min_value=0, max_value=None, key='asset_img')

    # Add row to asset image table
    def add_row_img(row):
        # -- Create the grid for each row
        grid_img = st.columns([0.25,0.3,0.3,0.15])
         # -- Set the Options
        options_dt = []
        for k in range(len(asset_name)):
            options_dt.append(asset_name[k])
            
        # -- Asset
        with grid_img[0]:
            while len(asset_imgs_lab) < row+1:
                asset_imgs_lab.append(None)
            if row == 0:
                asset_imgs_lab[row]=st.selectbox('Asset', options_dt, key=f'input_colimga{row}')  
            else:
                asset_imgs_lab[row]=st.selectbox('Temp', options_dt, key=f'input_colimga{row}',label_visibility = "collapsed")
    
        # -- Asset image   
        with grid_img[1]:
            while len(asset_imgs) < row+1:
                asset_imgs.append(None)
            if row == 0:
                asset_imgs[row]=st.file_uploader('Images', accept_multiple_files=False, key=f'input_colimgb{row}')
            else:
                asset_imgs[row]=st.file_uploader('Temp', accept_multiple_files=False, key=f'input_colimgb{row}',label_visibility = "collapsed")
        # -- Asset Notes
        with grid_img[2]:
            while len(asset_imgs_notes) < row+1:
                asset_imgs_notes.append(None)
            if row == 0:
                asset_imgs_notes[row]=st.text_area('Notes', value='', key=f'input_colimgc{row}')  
            else:
                asset_imgs_notes[row]=st.text_area('Temp', value='', key=f'input_colimgc{row}',label_visibility = "collapsed")
    
    # Add rows for number of images
    for r in range(int(st.session_state['asset_img'])):
        add_row_img(r)

    # Dispaly Existing Files for this record
    st.markdown(' ')
    with st.expander("View/Edit Existing Asset Images in the Database"):
        # -- Find list of existing values
        db = client['LabData']
        collection = db['LabData']
        query = {'Laboratory/Capability Name': st.session_state['name']}
        results = collection.find(query)
        curr_asset_imgs = []
        curr_asset_labels = []
        curr_asset_notes = []
        for result in results:
            if 'T7-Asset Image' in list(result.keys()):
                curr_asset_imgs = result['T7-Asset Image']
                curr_asset_labels = result['T7-Asset Image Label']
                curr_asset_notes = result['T7-Asset Image Notes']

        # -- Create Grid for Current Images
        if len(curr_asset_imgs) != 0:
            for k in range(len(curr_asset_imgs)):
                # Create The Grid
                col1_asset_img, col2_asset_img, col3_asset_img, col4_asset_img = st.columns([0.25,0.3,0.3,0.15])
    
                # Get the list of assets and the index
                options_dt = []
                idx = None
                for kk in range(len(asset_name)):
                    options_dt.append(asset_name[kk])
                    if asset_name[kk] == curr_asset_labels[k]:
                        idx = kk
    
                
                # Populate Existing Asset Images
                col1_asset_img.selectbox('Temp', options_dt, index = idx, key=f'input_colba{k}',label_visibility = "collapsed")
                col2_asset_img.image(curr_asset_imgs[k])
                col3_asset_img.text_area('Temp',value = curr_asset_notes[k], key=f'input_colbb{k}',label_visibility = "collapsed")
                col4_asset_img.selectbox('Temp', ('Keep','Remove'),key=f'input_colbc{k}',label_visibility = "collapsed")
    
    # Create Input for Sustainment Funding Source
    sust_funding = st.text_area("Sustainment Funding Source:",value='',key='sust')
    
    # Additional Information on Funding
    fund_rows = st.number_input('Number of Funding Sources:', min_value=0, max_value=None,key='fund_num')
    grid_fund = st.columns(4)
    fund_src = [] #Store funding source
    start_fund = [] #Store the start date of funding
    end_fund = [] #Store the end date of funding
    fund_amt = [] #Store the funding amount
    
    # Add row to funding table
    def add_row_fund(row):
        # -- Funding Source
        with grid_fund[0]:
            while len(fund_src) < row+1:
                fund_src.append(None)
            if row == 0:
                fund_src[row]=st.text_input('Funding Source', value='',key=f'input_coll{row}')
            else:
                fund_src[row]=st.text_input('Temp', value='',key=f'input_coll{row}',label_visibility = "collapsed")
        # -- Start Date of Funding
        with grid_fund[1]:
            while len(start_fund) < row+1:
                start_fund.append(None)
            if row == 0:
                start_fund[row]=st.date_input('Funding Start Date', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY",value = None, key=f'input_colm{row}')
            else:
                start_fund[row]=st.date_input('Temp', min_value = datetime.date(1950, 1, 1),  format="MM/DD/YYYY",  value = None, key=f'input_colm{row}',label_visibility = "collapsed")
        # -- End Date of Funding
        with grid_fund[2]:
            while len(end_fund) < row+1:
                end_fund.append(None)
            if row == 0:
                end_fund[row]=st.date_input('Funding End Date', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY", value = None,  key=f'input_coln{row}')
            else:
                end_fund[row]=st.date_input('Temp', min_value = datetime.date(1950, 1, 1),  format="MM/DD/YYYY", value = None, key=f'input_coln{row}',label_visibility = "collapsed")
        # -- Funding Amount
        with grid_fund[3]:
            while len(fund_amt) < row+1:
                fund_amt.append(None)
            if row == 0:
                fund_amt[row]=st.number_input("Funding Amount per Year ($)",min_value=0,max_value=None,step=1000,value=None, key=f'input_colo{row}')
            else:
                fund_amt[row]=st.number_input('Temp',min_value=0,max_value=None,step=1000,value=None, key=f'input_colo{row}',label_visibility = "collapsed")
    
    # Add rows for number of funding sources
    for r in range(int(st.session_state['fund_num'])):
        add_row_fund(r)
    
    # Create File Uploader
    uploaded_files = st.file_uploader("Upload New Laboratory Images:", accept_multiple_files=True, type =  ['png', 'jpg'], key='lab_imgs')

    # Dispaly Existing Files for this record
    with st.expander("View/Edit Existing Laboratory Images"):      
        # -- Find list of existing values
        db = client['LabData']
        collection = db['LabData']
        query = {'Laboratory/Capability Name': st.session_state['name']}
        results = collection.find(query)
        curr_imgs = []
        for result in results:
            if 'Lab Images' in list(result.keys()):
                curr_imgs = result['Lab Images']

        # -- Create Grid for Current Images
        if len(curr_imgs) != 0:
            for k in range(len(curr_imgs)):
                col1_img, col2_img, col3_img = st.columns(3)
                col1_img.image(curr_imgs[k])
                col2_img.selectbox('Temp', ('Keep','Remove'),key=f'input_colab{k}',label_visibility = "collapsed")


    #Create Divider for Name and Description
    st.subheader('Current Mission/Project Utilization')
    # Create Input for Project Utilization and Risk
    proj_rows = st.number_input('Number of Projects', min_value=0, max_value=None, key = 'proj_num')
    grid_proj = st.columns(5)
    proj_util = [] #Store the projects
    wbs_util = [] #Store the project WBS
    use_util = [] #Store the use for each project
    risk = [] #Store the risk
    impact_util = [] #Store the use for each project
    
    # Add row to project table
    def add_row_proj(row):
        # -- Project Name
        with grid_proj[0]:
            while len(proj_util) < row+1:
                proj_util.append(None)
            if row == 0:
                proj_util[row]=st.text_input('Mission/Project Name', key=f'input_colp{row}')
            else:
                proj_util[row]=st.text_input('Temp', key=f'input_colp{row}',label_visibility = "collapsed")
        # -- WBS Number
        with grid_proj[1]:
            while len(wbs_util) < row+1:
                wbs_util.append(None)
            if row == 0:
                wbs_util[row]=st.text_input('WBS Number', help = 'Enter the 6 Digit WBS Number', key=f'input_colq{row}')
            else:
                wbs_util[row]=st.text_input('Temp', key=f'input_colq{row}',label_visibility = "collapsed")
        # -- Project Use
        with grid_proj[2]:
            while len(use_util) < row+1:
                use_util.append(None)
            if row == 0:
                use_util[row]=st.number_input('Project Use (%)', min_value=0.0, max_value=100.0, step=0.5, value = None, key=f'input_colr{row}')
            else:
                use_util[row]=st.number_input('Tmp', min_value=0.0, max_value=100.0, step=0.5, value = None, key=f'input_colr{row}',label_visibility = "collapsed")
        # -- Risk to Project
        with grid_proj[3]:
            while len(risk) < row+1:
                risk.append(None)
            if row == 0:
                risk[row]=st.selectbox('Risk to Project', ('','High', 'Moderate', 'Low'),help='High -  Capability cannot be replicated elsewhere and replacement has high cost/lead time. \n \n \n ' +
                                                                                           'Moderate - Capability cannot be replicated elsewhere and replacement has low cost/lead time. \n \n \n ' +
                                                                                           'Low - Capability can be replicated elsewhere for low cost/lead time.',key=f'input_cols{row}')
            else:
                risk[row]=st.selectbox('Temp', ('','High', 'Moderate', 'Low'),key=f'input_cols{row}',label_visibility = "collapsed")
        # -- Impact to Project
        with grid_proj[4]:
            while len(impact_util) < row+1:
                impact_util.append(None)
            if row == 0:
                impact_util[row]=st.text_input('Impact if Laboratory/Capability is Lost', key=f'input_colt{row}')
            else:
                impact_util[row]=st.text_input('Temp', key=f'input_colt{row}',label_visibility = "collapsed")
    
    # Add rows for each project
    for r in range(int(st.session_state['proj_num'])):
        add_row_proj(r)
    
    # Create Divider for Name and Description
    st.subheader('Utilization History and Impact')
    
    # Create Input for History of Capability Utilization
    hist = st.text_area("History of capability utilization:",value='',key='hist')
    
    # Create Input for Major Impact and Contributions
    impact = st.text_area("Major impact and contributions this capability has made possible:",value='',key='impact')
    
    # Create Input for Impact if total Capability is Lost
    tot_imp = st.text_area("Overall impact of laboratory/capability is lost:",value='',key='tot_imp')
    
    #Create Divider for Down Time History
    st.subheader('History of Down Time Due to Maintenance or Failure')
    
    # Create Input for Downtime History
    down_rows = st.number_input('Number of Rows:', min_value=0, max_value=None, help='Enter the down time history for the entire lab or individual assets relevant to the failure of the lab infrastructure. Consider only failures in the last 5 years.', key = 'dt_num')
    grid_down = st.columns(6)
    asset_dt = [] #Store the associated Asset
    date_dt = [] #Store date the asset went down
    time_dt = [] #Store the time down
    unit_dt = [] #Store the unit for time down
    imp_dt = [] #Store a description for the time down
    desc_dt = [] #Store a description for the time down
    
    # Add row to down time table
    def add_row_down(row):
        # -- Set the Options
        options_dt = ['Entire Lab/Capability']
        for k in range(len(asset_name)):
            options_dt.append(asset_name[k])
            
        # -- Asset that went down
        with grid_down[0]:
            while len(asset_dt) < row+1:
                asset_dt.append(None)
            if row == 0:
                asset_dt[row]=st.selectbox('Asset', options_dt, key=f'input_colu{row}')
            else:
                asset_dt[row]=st.selectbox('Temp', options_dt, key=f'input_colu{row}',label_visibility = "collapsed")
        # -- Start Date for Time Down
        with grid_down[1]:
            while len(date_dt) < row+1:
                date_dt.append(None)
            if row == 0:
                date_dt[row]=st.date_input('Start Date', min_value=datetime.date(2019, 1, 1),  format="MM/DD/YYYY", value = None,  key=f'input_colv{row}')
            else:
                date_dt[row]=st.date_input('Tepm', min_value = datetime.date(2019, 1, 1), format="MM/DD/YYYY", value = None,  key=f'input_colv{row}',label_visibility = "collapsed")
        # -- Time Down
        with grid_down[2]:
            while len(time_dt) < row+1:
                time_dt.append(None)
            if row == 0:
                time_dt[row]=st.number_input('Time Down', step=0.5, value = None, key=f'input_colw{row}')
            else:
                time_dt[row]=st.number_input('Temp', step=0.5, value = None, key=f'input_colw{row}',label_visibility = "collapsed")
        # -- Unit of Time Down
        with grid_down[3]:
            while len(unit_dt) < row+1:
                unit_dt.append(None)
            if row == 0:
                unit_dt[row]=st.selectbox('Unit', ('','Days', 'Weeks', 'Months','Years'),key=f'input_colx{row}')
            else:
                unit_dt[row]=st.selectbox('Temp', ('','Days', 'Weeks', 'Months','Years'),key=f'input_colx{row}',label_visibility = "collapsed")
        # -- Impact due to down time
        with grid_down[4]:
            while len(imp_dt) < row+1:
                imp_dt.append(None)
            if row == 0:
                imp_dt[row]=st.text_input('Impact on Mission/Project', value='',key=f'input_colyy{row}')
            else:
                imp_dt[row]=st.text_input('Temp', value='',key=f'input_colyy{row}',label_visibility = "collapsed")
        # -- Additonal Notes for Time Down
        with grid_down[5]:
            while len(desc_dt) < row+1:
                desc_dt.append(None)
            if row == 0:
                desc_dt[row]=st.text_input('Additional Notes', value='',key=f'input_coly{row}')
            else:
                desc_dt[row]=st.text_input('Temp', value='',key=f'input_coly{row}',label_visibility = "collapsed")
                        
    for r in range(int(st.session_state['dt_num'])):
        add_row_down(r)
    
    #Create Divider for Down Time History
    st.subheader('Cost')
    
    # Create Input for Cost of Replacement
    cost_rep = st.number_input("Estimated Cost to Replace Entire Laboratory/Capability ($):",min_value=0,max_value=None,step=1000,value=None,key='cost_rep')
    
    # Create Input for Cost of Service Contracts
    cost_serv = st.number_input("Cost of Service Contracts ($):",min_value=0,max_value=None,step=1000,value=None,key='cost_serv')
    
    # Create Input for Annual Expenses to operate and sustain the lab
    cost_ann = st.number_input("Annual Cost to Operate and Sustain the Lab ($/yr):",min_value=0,max_value=None,step=1000,value=None,key='cost_ann')
    
    # Create Input for Incurred Cost Due to Downtown
    cost_inc = st.number_input("Incurred Cost For Downtime ($/yr):",min_value=0,max_value=None,step=1000,value=None,key='cost_inc')
    
    # Create Input for Labor Division
    labor_rows = st.number_input('Number of Divisions (Labor Costs):', min_value=0, max_value=None,key = 'labor_num')
    grid_labor = st.columns([0.3,0.3,0.4])
    division = [] #Store division
    labor_pct = [] #Store the labor percentrate
    
    # Add row to labor cost table
    def add_row_labor(row):
        # -- Start Date for Time Down
        with grid_labor[0]:
            while len(division) < row+1:
                division.append(None)
            if row == 0:
                division[row]=st.selectbox('Directorate', ('Code F','Code L'), key=f'input_colz{row}')
            else:
                division[row]=st.selectbox('Temp', ('Code F','Code L'), key=f'input_colz{row}',label_visibility = "collapsed")
        # -- Time Down
        with grid_labor[1]:
            while len(labor_pct) < row+1:
                labor_pct.append(None)
            if row == 0:
                labor_pct[row]=st.number_input('Labor Cost (%)', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colaa{row}')
            else:
                labor_pct[row]=st.number_input('Temp', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colaa{row}',label_visibility = "collapsed")
    
    # Add row for each labor cost
    for r in range(int(st.session_state['labor_num'])):
        add_row_labor(r)
    
    # Add Drop Down for Status
    status = st.selectbox('Completion Status', ('Draft','Final'),key='status')
    
    # Initialize Data Validation
    err_flag = 0  # Flag to check errors - 0 = no errors, 1 = errors (messages will show in app)
    err_msgs = [] # Store list of error messages 
    
    # Create buttons to interact with database
    grid_db = st.columns([0.115,0.135,0.75])
    with grid_db[0]:
        # Save Data to Database
        if st.button('Save To Database'):                
            # Data Validation - Check specific attributes are properly added before writing
            # -- Laboratory/Capability Name Must Be Populated
            if st.session_state['name'] == '':
                err_msgs.append('Laboratory/Capability Name Must Be Populated')
                err_flag = 1
    
            # -- Branch must be 3 letters
            if st.session_state['branch'] == '':
                err_msgs.append('Branch Must Be Populated')
                err_flag = 1
            elif len(st.session_state['branch']) != 3:
                err_msgs.append('Enter the 3 letter code for the Branch (e.g., LMS)')
                err_flag = 1
                
            # Write To Database If No Errors
            if err_flag == 0:
                # Create New Document
                new_data = {}
                        
                # Write New Data
                new_data['Laboratory/Capability Name'] = st.session_state['name']
                new_data['Point of Contact'] = st.session_state['poc']
                new_data['Branch'] = st.session_state['branch']
                new_data['Laboratory/Capability Description'] = st.session_state['desc']
                new_data['Laboratory/Capability Website'] = st.session_state['link']
                new_data['Challenges in sustaining this laboratory/capability'] = st.session_state['chal']
                new_data['Age (yrs)'] = st.session_state['lab_age']
                new_data['Condition'] = st.session_state['cond']
                new_data['Number of Assets'] = st.session_state['asset_num']
                new_data['T1-Asset Name'] = []
                new_data['T1-Location (Bldg/Rm)'] = []
                new_data['T1-Age (yrs)'] = []
                new_data['T1-Acquisition Year'] = []
                new_data['T1-Expected Year of Obsolescence'] = []
                new_data['T1-Asset Condition'] = []
                new_data['T1-Replacement Cost ($)'] = []
                new_data['T1-Impact to Capability if Lost'] = []
                new_data['T1-Associated Software'] = []
                new_data['T1-Inlcudes IT Hardware?'] = []
                new_data['T1-Replacement'] = []
                for m in range(int(st.session_state['asset_num'])):
                    new_data['T1-Asset Name'].append(st.session_state[f'input_cola{m}']) 
                    new_data['T1-Location (Bldg/Rm)'].append(st.session_state[f'input_colb{m}'])
                    new_data['T1-Age (yrs)'].append(st.session_state[f'input_colc{m}'])
                    new_data['T1-Acquisition Year'].append(st.session_state[f'input_cold{m}'])
                    new_data['T1-Expected Year of Obsolescence'].append(st.session_state[f'input_cole{m}'])
                    new_data['T1-Asset Condition'].append(st.session_state[f'input_colf{m}'])
                    new_data['T1-Replacement Cost ($)'].append(st.session_state[f'input_colg{m}'])
                    new_data['T1-Impact to Capability if Lost'].append(st.session_state[f'input_colh{m}'])
                    new_data['T1-Associated Software'].append(st.session_state[f'input_coli{m}'])
                    new_data['T1-Inlcudes IT Hardware?'].append(st.session_state[f'input_colj{m}'])
                    new_data['T1-Replacement'].append(st.session_state[f'input_colk{m}'])
                new_data['Number of Asset Images'] = st.session_state['asset_img']
                new_data['Sustainment Funding Source'] = st.session_state['sust']
                new_data['Number of Funding Sources'] = st.session_state['fund_num'] 
                new_data['T3-Funding Source'] = []
                new_data['T3-Funding Start Date'] = []
                new_data['T3-Funding End Date'] = []
                new_data['T3-Funding Amount per Year ($)'] = []
                for m in range(int(st.session_state['fund_num'] )):
                    new_data['T3-Funding Source'].append(st.session_state[f'input_coll{m}'])
                    new_data['T3-Funding Start Date'].append(str(st.session_state[f'input_colm{m}']))
                    new_data['T3-Funding End Date'].append(str(st.session_state[f'input_coln{m}']))
                    new_data['T3-Funding Amount per Year ($)'].append(st.session_state[f'input_colo{m}'])
                new_data['Number of Projects'] = st.session_state['proj_num']
                new_data['T4-Mission/Project Name'] = []
                new_data['T4-WBS Number'] = []
                new_data['T4-Project Use (%)'] = []
                new_data['T4-Risk to Project'] = []
                new_data['T4-Impact if Laboratory/Capability is Lost'] = []
                for m in range(int(st.session_state['proj_num'])):
                    new_data['T4-Mission/Project Name'].append(st.session_state[f'input_colp{m}'])
                    new_data['T4-WBS Number'].append(st.session_state[f'input_colq{m}'])
                    new_data['T4-Project Use (%)'].append(st.session_state[f'input_colr{m}'])
                    new_data['T4-Risk to Project'].append(st.session_state[f'input_cols{m}'])
                    new_data['T4-Impact if Laboratory/Capability is Lost'].append(st.session_state[f'input_colt{m}'])
                new_data['History of capability utilization'] = st.session_state['hist'] 
                new_data['Major impact and contributions this capability has made possible'] = st.session_state['impact']
                new_data['Overall impact of laboratory/capability is lost'] = st.session_state['tot_imp']
                new_data['Number of Failures'] = st.session_state['dt_num']
                new_data['T5-Asset'] = []
                new_data['T5-Start Date'] = []
                new_data['T5-Time Down'] = []
                new_data['T5-Unit'] = []
                new_data['T5-Additional Notes'] = []
                new_data['T5-Impact'] = []
                for m in range(int(st.session_state['dt_num'])):
                    new_data['T5-Asset'].append(st.session_state[f'input_colu{m}'])
                    new_data['T5-Start Date'].append(str(st.session_state[f'input_colv{m}']))
                    new_data['T5-Time Down'].append(st.session_state[f'input_colw{m}'])
                    new_data['T5-Unit'].append(st.session_state[f'input_colx{m}'])
                    new_data['T5-Additional Notes'].append(st.session_state[f'input_coly{m}'])
                    new_data['T5-Impact'].append(st.session_state[f'input_colyy{m}'])
                new_data['Estimated Cost to Replace Entire Laboratory/Capability ($)']= st.session_state['cost_rep']
                new_data['Cost of Service Contracts ($)'] = st.session_state['cost_serv']
                new_data['Annual Cost to Operate and Sustain the Lab ($/yr)'] = st.session_state['cost_ann']
                new_data['Incurred Cost For Downtime ($/yr)'] = st.session_state['cost_inc']
                new_data['Number of Divisions (Labor Costs)'] = st.session_state['labor_num']
                new_data['T6-Directorate'] = []
                new_data['T6-Labor Cost (%)'] = []
                for m in range(int(st.session_state['labor_num'])):
                    new_data['T6-Directorate'].append(st.session_state[f'input_colz{m}'])
                    new_data['T6-Labor Cost (%)'].append(st.session_state[f'input_colaa{m}'])
                new_data['Status'] = st.session_state['status']

                # Check Lab Images
                new_data['Lab Images'] = []
                new_data['T7-Asset Image'] = []
                new_data['T7-Asset Image Label'] = []
                new_data['T7-Asset Image Notes'] = []
                # -- Find list of existing values
                # Load the Current Database
                db = client['LabData']
                collection = db['LabData']
                query = {'Laboratory/Capability Name': st.session_state['name']}
                results = collection.find(query)
                for result in results:
                    # -- Overall Lab Images
                    if 'Lab Images' in list(result.keys()):
                        curr_img_write = result['Lab Images']
                    else:
                        curr_img_write = []

                    # -- Asset Images
                    if 'T7-Asset Image' in list(result.keys()):
                        asset_img_write = result['T7-Asset Image']
                        asset_img_label_write = result['T7-Asset Image Label']
                        asset_img_notes_write = result['T7-Asset Image Notes']
                    else:
                        asset_img_write = []
                        asset_img_label_write = []
                        asset_img_notes_write = []

                # -- Populate List of Existing Images
                for kk in range(len(curr_img_write)):
                    if st.session_state[f'input_colab{kk}'] == 'Keep':
                        new_data['Lab Images'].append(curr_img_write[kk])
                for iii in range(len(uploaded_files)):
                    new_data['Lab Images'].append(uploaded_files[iii].getvalue())

                # -- Populate List of Existing Asset Images
                for kk in range(len(asset_img_write)):
                    if st.session_state[f'input_colbc{kk}'] == 'Keep':
                        new_data['T7-Asset Image'].append(asset_img_write[kk])
                        new_data['T7-Asset Image Label'].append(st.session_state[f'input_colba{kk}'])
                        new_data['T7-Asset Image Notes'].append(st.session_state[f'input_colbb{kk}'])
                for iii in range(st.session_state['asset_img']):
                    new_data['T7-Asset Image'].append(st.session_state[f'input_colimgb{iii}'].getvalue())
                    new_data['T7-Asset Image Label'].append(st.session_state[f'input_colimga{iii}'])
                    new_data['T7-Asset Image Notes'].append(st.session_state[f'input_colimgc{iii}'])
            
                # Delete the existing entry if it exists
                db = client['LabData']
                collection = db['LabData']
                myquery = { "Laboratory/Capability Name": st.session_state["name"]}
                collection.delete_one(myquery)
            
                # Write the Data the the Mongo DB
                new_entry = collection.insert_one(new_data)
    
                # Refetch Data
                st.cache_data.clear()
    
                # Create Popup for Save
                st.markdown( 'Saved to Database!')


                
                        
    with grid_db[1]:
        # Delete Entry from Database
        if st.button('Delete From Database'):
            # Delete the existing entry if it exists
            db = client['LabData']
            collection = db['LabData']
            myquery = { "Laboratory/Capability Name": st.session_state["name"]}
            collection.delete_one(myquery)
    
            # Refetch Data
            st.cache_data.clear()
    
    
    # Write Error Messages
    if err_flag == 1:
        for k in range(len(err_msgs)):
            st.error(err_msgs[k])
