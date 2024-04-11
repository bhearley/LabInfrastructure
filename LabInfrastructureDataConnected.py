# Import Modues
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi
import datetime

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
def init_connection():
    uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
    return MongoClient(uri, tlsCAFile=certifi.where())

client = init_connection()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_data():
    db = client['LabData']
    items = db['LabData'].find()
    items = list(items)  # make hashable for st.cache_data
    return items

# Get All Data in Database
all_data = get_data()
all_labs = ['']
for k in range(len(all_data)):
    all_labs.append(all_data[k]["Laboratory/Capability Name"])

# Sort List
all_labs.sort()

# Load Data Function
def load_data():
    if st.session_state['selection_lab'] != '':
        db = client['LabData']
        # Query the database for the record
        query = {'Laboratory/Capability Name': st.session_state['selection_lab']}
        results = db['LabData'].find(query)

        # Write Data
        for result in results:
            #st.write(result)
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
            #st.session_state['asset_img'] = result['Number of Asset Images']
            #for m in range(int(result['Number of Asset Images'])):
            #    st.session_state[f'input_colimg1{m}'] = result['T2-Asset'][m]
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

            
            st.session_state['test_area'] = '--' + result['Condition'].strip() + '--'
    else:
        st.session_state['name'] = ''
        st.session_state['poc'] = ''
        st.session_state['branch'] = ''
        st.session_state['desc'] = ''
        st.session_state['link'] = ''
        st.session_state['chal'] = ''
        st.session_state['lab_age'] = None
        st.session_state['cond'] = 'Excellent'
        st.session_state['asset_num'] = 0
        st.session_state['asset_img'] = 0
        st.session_state['sust'] = ''
        st.session_state['fund_num'] = 0

#--------------------------------------------------------------------------------------------------------------------------------
# Create Data Entries
#

# Select Lab
selection_lab = st.selectbox('Select the Lab:',all_labs, on_change = load_data, key = 'selection_lab')

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
lab_age = st.number_input("Age (yrs):",min_value=0,max_value=None,help="The age of the laboratory/capability (i.e., how long we've had this capability at NASA GRC)",key='lab_age')

# Create Input for Condition
cond_opts = ['Excellent','Good','Fair','Poor']
lab_condition = st.selectbox('Condition:',cond_opts,key='cond')

# Create Input for Assets
asset_rows = st.number_input('Number of Assets:', min_value=0, max_value=None, key='asset_num')
grid = st.columns([0.125,0.075,0.05,0.08,0.09,0.08,0.07,0.11,0.115,0.07,0.1])
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

def add_row_asset(row):
    # -- Asset Name
    with grid[0]:
        while len(asset_name) < row+1:
            asset_name.append(None)
        if row == 0:
            asset_name[row]=st.text_input('Asset \n \n Name', key=f'input_cola{row}')
        else:
            asset_name[row]=st.text_input('', key=f'input_cola{row}')
    # -- Asset Location    
    with grid[1]:
        while len(asset_loc) < row+1:
            asset_loc.append(None)
        if row == 0:
            asset_loc[row]=st.text_input('Location  \n \n (Bldg/Rm)', key=f'input_colb{row}')
        else:
            asset_loc[row]=st.text_input('', key=f'input_colb{row}')
    # -- Asset Age
    with grid[2]:
        while len(asset_age) < row+1:
            asset_age.append(None)
        if row == 0:
            asset_age[row]=st.number_input('Age  \n \n  (yrs)', step=0.5, key=f'input_colc{row}')
        else:
            asset_age[row]=st.number_input('', step=0.5, key=f'input_colc{row}')
    # -- Asset Date of Entry
    with grid[3]:
        while len(asset_date_in) < row+1:
            asset_date_in.append(None)
        if row == 0:
            #asset_date_in[row]=st.date_input('Acquistion  \n \n Year', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY", help = 'The date the asset was acquired.', key=f'input_cold{row}')
            asset_date_in[row]=st.number_input('Acquistion  \n \n Year', step = 1, min_value = 0, max_value = 3000, help = 'The year the asset was acquired.', key=f'input_cold{row}')
        else:
            #asset_date_in[row]=st.date_input('', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY", key=f'input_cold{row}')
            asset_date_in[row]=st.number_input('', step = 1, min_value = 0, max_value = 3000,  key=f'input_cold{row}')
    # -- Asset Date of Obsolescence
    with grid[4]:
        while len(asset_date_out) < row+1:
            asset_date_out.append(None)
        if row == 0:
            #asset_date_out[row]=st.date_input('Expected Year of Obsolescence', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY", help = 'Expected year of obsolescence includes both the asset itself becoming obsolete and the inability to obtain a service contract for the asset.', key=f'input_cole{row}')
            asset_date_out[row]=st.number_input('Expected Year of Obsolescence', step = 1, min_value = 0, max_value = 3000, help = 'Expected year of obsolescence includes both the asset itself becoming obsolete and the inability to obtain a service contract for the asset.', key=f'input_cole{row}')
        else:
            #asset_date_out[row]=st.date_input('', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY", key=f'input_cole{row}')
            asset_date_out[row]=st.number_input('', step = 1, min_value = 0, max_value = 3000, key=f'input_cole{row}')
    # -- Asset Condition
    with grid[5]:
        while len(asset_cond) < row+1:
            asset_cond.append(None)
        if row == 0:
            asset_cond[row]=st.selectbox('Asset  \n \n  Condition',  ('Excellent', 'Good', 'Fair', 'Poor'), help="Excellent - No current issues with the asset. \n \n \n " +
                                                                                       "Good - Only minor issues with the asset that can be easily fixed. \n \n \n " +
                                                                                       "Fair - Asset is still in a working condition, but is near end of life. \n \n \n " +
                                                                                       "Poor - Asset has many issues/doesn't operate properly ", key=f'input_colf{row}')
        else:
            asset_cond[row]=st.selectbox('', ('Excellent', 'Good', 'Fair', 'Poor'),key=f'input_colf{row}')
    # -- Asset Cost of Replacement
    with grid[6]:
        while len(asset_cost) < row+1:
            asset_cost.append(None)
        if row == 0:
            asset_cost[row]=st.number_input('Replacement \n \n  Cost ($)', step=1000, key=f'input_colg{row}')
        else:
            asset_cost[row]=st.number_input('', step=1000, key=f'input_colg{row}')
    # -- Asset Impact if Lost
    with grid[7]:
        while len(asset_imp) < row+1:
            asset_imp.append(None)
        if row == 0:
            asset_imp[row]=st.text_input('Impact to Capability \n \n  if Lost', key=f'input_colh{row}')
        else:
            asset_imp[row]=st.text_input('', key=f'input_colh{row}')
    # -- Associated Software
    with grid[8]:
        while len(asset_software) < row+1:
            asset_software.append(None)
        if row == 0:
            asset_software[row]=st.text_input('Associated Software / \n \n  Required OS', help = "List any assoicated software or required operating systems, separated by commas, necessary for the asset to operate", key=f'input_coli{row}')
        else:
            asset_software[row]=st.text_input('', key=f'input_coli{row}')
    # -- IT/computer hardware repalcement
    with grid[9]:
        while len(asset_itrep) < row+1:
            asset_itrep.append(None)
        if row == 0:
            asset_itrep[row]=st.selectbox('Inlcudes IT \n \n  Hardware?', ('Yes','No'), help = 'Does the replacement of this asset require and IT Hardware replacement as well?', key=f'input_colj{row}')
        else:
            asset_itrep[row]=st.selectbox('', ('Yes','No'),key=f'input_colj{row}')
    with grid[10]:
        while len(asset_repdesc) < row+1:
            asset_repdesc.append(None)
        if row == 0:
            asset_repdesc[row]=st.text_input('Replacement Parts \n \n Available?', help = 'Are replacement components available or would a full replacement be needed if asset is lost?', key=f'input_colk{row}')
        else:
            asset_repdesc[row]=st.text_input('', key=f'input_colk{row}')

for r in range(asset_rows):
    add_row_asset(r)

# Create Input for Asset Images
asset_imgs_lab = [] #Store the asset images label
asset_imgs = [] #Store the asset images

asset_imgs_num = st.number_input('Number of Asset Images:', min_value=0, max_value=None, key='asset_img')
grid_img = st.columns(2)

def add_row_img(row):
     # -- Set the Options
    options_dt = []
    for k in range(len(asset_name)):
        options_dt.append(asset_name[k])
        
    # -- Asset
    with grid_img[0]:
        while len(asset_imgs_lab) < row+1:
            asset_imgs_lab.append(None)
        if row == 0:
            asset_imgs_lab[row]=st.selectbox('Asset', options_dt, key=f'input_colimg1{row}')  
            #s = f"<p style='font-size:.01px;'>{'test'}</p>"
            #st.markdown(s, unsafe_allow_html=True) 
        else:
            asset_imgs_lab[row]=st.selectbox('', options_dt, key=f'input_colimg1{row}',label_visibility = "collapsed")

    # -- Asset image   
    with grid_img[1]:
        while len(asset_imgs) < row+1:
            asset_imgs.append(None)
        if row == 0:
            asset_imgs[row]=st.file_uploader('Images', accept_multiple_files=True, key=f'input_colimg2{row}')

        else:
            asset_imgs[row]=st.file_uploader('', accept_multiple_files=True, key=f'input_colimg2{row}',label_visibility = "collapsed")

for r in range(asset_imgs_num):
    add_row_img(r)
css = '''
<style>
    [data-testid='stFileUploader'] {
        width: max-content;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: left;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: right;
        padding-top: 0;
    }

</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Create Input for Sustainment Funding Source
sust_funding = st.text_area("Sustainment Funding Source:",value='',key='sust')

# Additional Information on Funding
fund_rows = st.number_input('Number of Funding Sources:', min_value=0, max_value=None,key='fund_num')
grid2 = st.columns(4)
fund_src = [] #Store funding source
start_fund = [] #Store the start date of funding
end_fund = [] #Store the end date of funding
fund_amt = [] #Store the funding amount
def add_row2(row):
    # -- Funding Source
    with grid2[0]:
        while len(fund_src) < row+1:
            fund_src.append(None)
        if row == 0:
            fund_src[row]=st.text_input('Funding Source', value='',key=f'input_coll{row}')
        else:
            fund_src[row]=st.text_input('', value='',key=f'input_coll{row}')
    # -- Start Date of Funding
    with grid2[1]:
        while len(start_fund) < row+1:
            start_fund.append(None)
        if row == 0:
            start_fund[row]=st.date_input('Funding Start Date', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY",  key=f'input_colm{row}')
        else:
            start_fund[row]=st.date_input('', min_value = datetime.date(1950, 1, 1),  format="MM/DD/YYYY",  key=f'input_colm{row}')
    # -- End Date of Funding
    with grid2[2]:
        while len(end_fund) < row+1:
            end_fund.append(None)
        if row == 0:
            end_fund[row]=st.date_input('Funding End Date', min_value=datetime.date(1950, 1, 1), format="MM/DD/YYYY",  key=f'input_coln{row}')
        else:
            end_fund[row]=st.date_input('', min_value = datetime.date(1950, 1, 1),  format="MM/DD/YYYY",  key=f'input_coln{row}')
    # -- Funding Amount
    with grid2[3]:
        while len(fund_amt) < row+1:
            fund_amt.append(None)
        if row == 0:
            fund_amt[row]=st.number_input("Funding Amount per Year ($)",min_value=0,max_value=None,step=1000,value=0, key=f'input_colo{row}')
        else:
            fund_amt[row]=st.number_input("",min_value=0,max_value=None,step=1000,value=0, key=f'input_colo{row}')
for r in range(fund_rows):
    add_row2(r)

# Create File Uploader
uploaded_files = st.file_uploader("Upload Documents/Images:", accept_multiple_files=True)

test_text = st.text_area("For Testing",value = '', key='test_area')


if st.button('Save Data'):
    if st.session_state['selection_lab'] != '':
        # Get a copy of the data structure 
        new_data = all_data[0]
    else:
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
    for m in range(int(st.session_state['asset_img'])):
        new_data['T2-Asset'].append(st.session_state[f'input_colimg1{m}'])
        new_data['T2-Image'].append(st.session_state[f'input_colimg2{m}'])
    new_data['Sustainment Funding Source'] = st.session_state['sust']
    new_data['Number of Funding Sources'] = st.session_state['fund_num'] 
    result['T3-Funding Source'] = []
    result['T3-T3-Funding Start Date'] = []
    result['T3-T3-Funding End Date'] = []
    result['T3-Funding Amount per Year ($)'] = []
    for m in range(int(result['Number of Funding Sources'])):
        new_data['T3-Funding Source'].append(st.session_state[f'input_coll{m}'])
        new_data['T3-Funding Start Date'].append(str(st.session_state[f'input_colm{m}']))
        new_data['T3-Funding End Date'].append(str(st.session_state[f'input_coln{m}']))
        new_data['T3-Funding Amount per Year ($)'].append(st.session_state[f'input_colo{m}'])

    # Delete the existing entry if it exists
    db = client['LabData']
    collection = db['LabData']
    myquery = { "Laboratory/Capability Name": st.session_state["name"]}
    collection.delete_one(myquery)

    # Write the Data the the Mongo DB
    new_entry = collection.insert_one(new_data)
