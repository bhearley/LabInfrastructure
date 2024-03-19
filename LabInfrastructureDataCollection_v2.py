#----------------------------------------------------------------
#   LabInfrastructureDataCollection
#   Brandon Hearley - LMS
#   12/19/2023
#
#   PURPOSE: Create a web app (using streamlit) to collect data 
#            on the GRC Lab Infrastructure
#
#----------------------------------------------------------------
#   SETUP
#   Import Modules and Set Paths


# Import Modules
import glob
import os
import pandas as pd
import pickle
import streamlit as st
#from streamlit_gsheets import GSheetsConnection
from git import Repo
import datetime

# Set Paths
home = os.getcwd()
existing_files = "/mount/src/labinfrastructure/NewFiles/"

# Get the names of the existing files
os.chdir(existing_files)
files = glob.glob('*.txt')
files_disp = ['New']
for j in range(len(files)):
    with open(files[j]) as f:
        lines = f.readlines()
    idx = lines[0].find(':')
    files_disp.append(lines[0][idx+1:])
os.chdir(home)

# Create Function to Read the Data
def read_data():
    # Set Flag
    flag =0

    # Find the File
    if st.session_state.load != 'New':
        for i in range(len(files_disp)):
            if st.session_state.load == files_disp[i]:
                file_read = files[i-1]
                flag = 1
            
    if flag == 0:
        st.session_state.name = ''
        st.session_state.poc = ''
        st.session_state.branch = ''
        st.session_state.desc = ''
        st.session_state.link = ''
        st.session_state.chal = ''
        st.session_state.lab_age_k = 0
        st.session_state.cond = 'Excellent'
        st.session_state.sust = ''
        st.session_state.hist = ''
        st.session_state.impact = ''
        st.session_state.tot_imp = ''
        st.session_state.cost_rep = 0
        st.session_state.cost_serv = 0
        st.session_state.cost_ann = 0
        st.session_state.cost_inc = 0
        st.session_state.labor_num = 0
        st.session_state.asset_num = 0
        st.session_state.fund_num = 0
        st.session_state.proj_num = 0
        st.session_state.dt_num = 0
    else:
    
        # Read the file
        with open(os.path.join(existing_files,file_read)) as f:
            lines = f.readlines()
    
        # Parse Data
        # -- Laboratory/Capability Name
        key = 'Laboratory/Capability Name:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.name = val
        
        # -- Point of Contact
        key = 'Point of Contact:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.poc = val

        # -- Branch
        key = 'Branch:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.branch = val
        
        # -- Laboratory/Capability Description
        key = 'Laboratory/Capability Description:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.desc  = val
        
        # -- Laboratory/Capability Website
        key = 'Laboratory/Capability Website:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.link = val
        
        # -- Challenges in sustaining this laboratory/capability
        key = 'Challenges in sustaining this laboratory/capability:'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
        st.session_state.chal = val
        
        # -- Age (yrs):
        key = 'Age (yrs):'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.lab_age_k = int(val)
        
        # -- Condition:
        key = 'Condition:'
        fag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.cond  = val
        
        # -- Sustainment Funding Source:
        key = 'Sustainment Funding Source:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.sust  = val
        
        # -- History of capability utilization:
        key = 'History of capability utilization:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.hist  = val
        
        # -- Major impact and contributions this capability has made possible:
        key = 'Major impact and contributions this capability has made possible:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.impact  = val

        # -- Overall impact of laboratory/capability is lost::
        key = 'Overall impact of laboratory/capability is lost:'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.tot_imp  = val
        
        # -- Estimated Cost to Replace Entire Laboratory/Capability ($):
        key = 'Estimated Cost to Replace Entire Laboratory/Capability ($):'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.cost_rep  = int(val)
        
        # -- Cost of Service Contracts ($):
        key = 'Cost of Service Contracts ($):'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.cost_serv  = int(val)
        
        # -- Cost of Service Contracts ($):
        key = 'Annual Cost to Operate and Sustain the Lab ($/yr):'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
        st.session_state.cost_ann  = int(val)
        
        # -- Cost of Service Contracts ($):
        key = 'Incurred Cost For Downtime ($/yr):'
        flag = 0
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                flag = 1
        if flag == 1:
            st.session_state.cost_inc  = int(val)

        # -- Asset Table
        key = 'Number of Assets:'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                line_num = i
        num_assets  = int(val)
        st.session_state.asset_num = num_assets
        
        data = ''
        for k in range(line_num+2,line_num+2+num_assets):
            data = data + lines[k]
        data= data.split('\n')
        data_all = []
        for k in range(num_assets):
            data_line = data[k]
            data_line = data_line.split('\t')
            data_line[2] = float(data_line[2])
            data_line[6] = int(data_line[6])
            data_all.append(data_line)

        for k in range(num_assets):
            st.session_state[f'input_cola{k}'] = data_all[k][0]
            st.session_state[f'input_colb{k}'] = data_all[k][1]
            st.session_state[f'input_colc{k}'] = data_all[k][2]
            date1 = data_all[k][3].split('-')
            date2 = data_all[k][4].split('-')
            st.session_state[f'input_cold{k}'] = int(date1[0])
            st.session_state[f'input_cole{k}'] = int(date2[0])
            st.session_state[f'input_colf{k}'] = data_all[k][5]
            st.session_state[f'input_colg{k}'] = data_all[k][6]
            st.session_state[f'input_colh{k}'] = data_all[k][7]
            st.session_state[f'input_coli{k}'] = data_all[k][8]
            st.session_state[f'input_colj{k}'] = data_all[k][9]
            st.session_state[f'input_colk{k}'] = data_all[k][10]

        # -- Read Funding Table
        key = 'Number of Funding Sources:'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                line_num = i
        num_fund  = int(val)
        st.session_state.fund_num  = num_fund
        
        data = ''
        for k in range(line_num+2,line_num+2+num_fund):
            data = data + lines[k]
        data= data.split('\n')
        data_all = []
        for k in range(num_fund):
            data_line = data[k]
            data_line = data_line.split('\t')
            data_line[3] = float(data_line[3])
            data_all.append(data_line)

        for k in range(num_fund):
            st.session_state[f'input_coll{k}'] = data_all[k][0]
            date1 = data_all[k][1].split('-')
            st.session_state[f'input_colm{k}'] = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
            date2 = data_all[k][2].split('-')
            st.session_state[f'input_coln{k}'] = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))
            st.session_state[f'input_colo{k}'] = data_all[k][3]
        
        # -- Read Project Table
        key = 'Number of Projects:'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                line_num = i
        num_proj  = int(val)
        st.session_state.proj_num = num_proj
        
        data = ''
        for k in range(line_num+2,line_num+2+num_proj):
            data = data + lines[k]
        data= data.split('\n')
        data_all = []
        for k in range(num_proj):
            data_line = data[k]
            data_line = data_line.split('\t')
            data_line[2] = float(data_line[2])
            data_all.append(data_line)

        for k in range(num_proj):
            st.session_state[f'input_colp{k}'] = data_all[k][0]
            st.session_state[f'input_colq{k}'] = data_all[k][1]
            st.session_state[f'input_colr{k}'] = data_all[k][2]
            st.session_state[f'input_cols{k}'] = data_all[k][3]
            st.session_state[f'input_colt{k}'] = data_all[k][4]

        # -- Read Down Time Table
        key = 'Number of Failures:'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                line_num = i
        num_dt  = int(val)
        st.session_state.dt_num = num_dt
        
        data = ''
        for k in range(line_num+2,line_num+2+num_dt):
            data = data + lines[k]
        data= data.split('\n')
        data_all = []
        for k in range(num_dt):
            data_line = data[k]
            data_line = data_line.split('\t')
            data_line[2] = float(data_line[2])
            data_all.append(data_line)

        for k in range(num_dt):
            st.session_state[f'input_colu{k}'] = data_all[k][0]
            date1 = data_all[k][1].split('-')
            st.session_state[f'input_colv{k}'] = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
            st.session_state[f'input_colw{k}'] = data_all[k][2]
            st.session_state[f'input_colx{k}'] = data_all[k][3]
            st.session_state[f'input_colyy{k}'] = data_all[k][4]
            if len(data_all[k]) > 5:
                st.session_state[f'input_coly{k}'] = data_all[k][5]
        
        # -- Read Divisons Table
        key = 'Number of Divisions (Labor Costs):'
        for i in range(len(lines)):
            if key in lines[i]:
                val  = lines[i][len(key)+1:len(lines[i])-1]
                line_num = i
        num_div  = int(val)
        st.session_state.labor_num = num_div
        
        data = ''
        for k in range(line_num+2,line_num+2+num_div):
            data = data + lines[k]
        data= data.split('\n')
        data_all = []
        for k in range(num_div):
            data_line = data[k]
            data_line = data_line.split('\t')
            data_line[1] = float(data_line[1])
            data_all.append(data_line)

        for k in range(num_div):
            st.session_state[f'input_colz{k}'] = data_all[k][0]
            st.session_state[f'input_colaa{k}'] = data_all[k][1]


#----------------------------------------------------------------
#   CREATE THE APP
#   Create the streamlit app for data collection

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

# Create Save State Option                 
lab_load = st.selectbox('Create New Entry or Load Previous:',files_disp,on_change = read_data, key = 'load') 

#----------------------------------------------------------------------------------
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
            s = f"<p style='font-size:1px;'>{'test'}</p>"
            st.markdown(s, unsafe_allow_html=True) 
        else:
            asset_imgs_lab[row]=st.selectbox('', options_dt, key=f'input_colimg1{row}')

    # -- Asset image   
    with grid_img[1]:
        while len(asset_imgs) < row+1:
            asset_imgs.append(None)
        if row == 0:
            asset_imgs[row]=st.file_uploader('Images', accept_multiple_files=True, key=f'input_colimg2{row}')
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
        else:
            asset_imgs[row]=st.file_uploader('', accept_multiple_files=True, key=f'input_colimg2{row}')

for r in range(asset_imgs_num):
    add_row_img(r)

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

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Current Mission/Project Utilization')
# Create Input for Project Utilization and Risk
proj_rows = st.number_input('Number of Projects', min_value=0, max_value=None, key = 'proj_num')
grid3 = st.columns(5)
proj_util = [] #Store the projects
wbs_util = [] #Store the project WBS
use_util = [] #Store the use for each project
risk = [] #Store the risk
impact_util = [] #Store the use for each project
def add_row3(row):
    # -- Project Name
    with grid3[0]:
        while len(proj_util) < row+1:
            proj_util.append(None)
        if row == 0:
            proj_util[row]=st.text_input('Mission/Project Name', key=f'input_colp{row}')
        else:
            proj_util[row]=st.text_input('', key=f'input_colp{row}')
    # -- WBS Number
    with grid3[1]:
        while len(wbs_util) < row+1:
            wbs_util.append(None)
        if row == 0:
            wbs_util[row]=st.text_input('WBS Number', help = 'Enter the 6 Digit WBS Number', key=f'input_colq{row}')
        else:
            wbs_util[row]=st.text_input('', key=f'input_colq{row}')
    # -- Project Use
    with grid3[2]:
        while len(use_util) < row+1:
            use_util.append(None)
        if row == 0:
            use_util[row]=st.number_input('Project Use (%)', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colr{row}')
        else:
            use_util[row]=st.number_input('', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colr{row}')
    # -- Risk to Project
    with grid3[3]:
        while len(risk) < row+1:
            risk.append(None)
        if row == 0:
            risk[row]=st.selectbox('Risk to Project', ('High', 'Moderate', 'Low'),help='High -  Capability cannot be replicated elsewhere and replacement has high cost/lead time. \n \n \n ' +
                                                                                       'Moderate - Capability cannot be replicated elsewhere and replacement has low cost/lead time. \n \n \n ' +
                                                                                       'Low - Capability can be replicated elsewhere for low cost/lead time.',key=f'input_cols{row}')
        else:
            risk[row]=st.selectbox('', ('High', 'Moderate', 'Low'),key=f'input_cols{row}')
    # -- Impact to Project
    with grid3[4]:
        while len(impact_util) < row+1:
            impact_util.append(None)
        if row == 0:
            impact_util[row]=st.text_input('Impact if Laboratory/Capability is Lost', key=f'input_colt{row}')
        else:
            impact_util[row]=st.text_input('', key=f'input_colt{row}')
for r in range(proj_rows):
    add_row3(r)

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Utilization History and Impact')
# Create Input for History of Capability Utilization
hist = st.text_area("History of capability utilization:",value='',key='hist')

# Create Input for Major Impact and Contributions
impact = st.text_area("Major impact and contributions this capability has made possible:",value='',key='impact')

# Create Input for Impact if total Capability is Lost
tot_imp = st.text_area("Overall impact of laboratory/capability is lost:",value='',key='tot_imp')

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('History of Down Time Due to Maintenance or Failure')
# Create Input for Downtime History
down_rows = st.number_input('Number of Rows:', min_value=0, max_value=None, help='Enter the down time history for the entire lab or individual assets relevant to the failure of the lab infrastructure. Consider only failures in the last 5 years.', key = 'dt_num')
grid4 = st.columns(6)
asset_dt = [] #Store the associated Asset
date_dt = [] #Store date the asset went down
time_dt = [] #Store the time down
unit_dt = [] #Store the unit for time down
imp_dt = [] #Store a description for the time down
desc_dt = [] #Store a description for the time down

def add_row4(row):
    # -- Set the Options
    options_dt = ['Entire Lab/Capability']
    for k in range(len(asset_name)):
        options_dt.append(asset_name[k])
        
    # -- Asset that went down
    with grid4[0]:
        while len(asset_dt) < row+1:
            asset_dt.append(None)
        if row == 0:
            asset_dt[row]=st.selectbox('Asset', options_dt, key=f'input_colu{row}')
        else:
            asset_dt[row]=st.selectbox('', options_dt, key=f'input_colu{row}')
    # -- Start Date for Time Down
    with grid4[1]:
        while len(date_dt) < row+1:
            date_dt.append(None)
        if row == 0:
            date_dt[row]=st.date_input('Start Date', min_value=datetime.date(2019, 1, 1),  format="MM/DD/YYYY",  key=f'input_colv{row}')
        else:
            date_dt[row]=st.date_input('', min_value = datetime.date(2019, 1, 1), format="MM/DD/YYYY",  key=f'input_colv{row}')
    # -- Time Down
    with grid4[2]:
        while len(time_dt) < row+1:
            time_dt.append(None)
        if row == 0:
            time_dt[row]=st.number_input('Time Down', step=0.5, key=f'input_colw{row}')
        else:
            time_dt[row]=st.number_input('', step=0.5, key=f'input_colw{row}')
    # -- Unit of Time Down
    with grid4[3]:
        while len(unit_dt) < row+1:
            unit_dt.append(None)
        if row == 0:
            unit_dt[row]=st.selectbox('Unit', ('Days', 'Weeks', 'Months','Years'),key=f'input_colx{row}')
        else:
            unit_dt[row]=st.selectbox('', ('Days', 'Weeks', 'Months','Years'),key=f'input_colx{row}')
    # -- Additonal Notes for Time Down
    with grid4[4]:
        while len(imp_dt) < row+1:
            imp_dt.append(None)
        if row == 0:
            imp_dt[row]=st.text_input('Impact on Mission/Project', value='',key=f'input_colyy{row}')
        else:
            imp_dt[row]=st.text_input('', value='',key=f'input_colyy{row}')
    with grid4[5]:
        while len(desc_dt) < row+1:
            desc_dt.append(None)
        if row == 0:
            desc_dt[row]=st.text_input('Additional Notes', value='',key=f'input_coly{row}')
        else:
            desc_dt[row]=st.text_input('', value='',key=f'input_coly{row}')
for r in range(down_rows):
    add_row4(r)

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('Cost')
# Create Input for Cost of Replacement
cost_rep = st.number_input("Estimated Cost to Replace Entire Laboratory/Capability ($):",min_value=0,max_value=None,step=1000,value=0,key='cost_rep')

# Create Input for Cost of Service Contracts
cost_serv = st.number_input("Cost of Service Contracts ($):",min_value=0,max_value=None,step=1000,value=0,key='cost_serv')

# Create Input for Annual Expenses to operate and sustain the lab
cost_ann = st.number_input("Annual Cost to Operate and Sustain the Lab ($/yr):",min_value=0,max_value=None,step=1000,value=0,key='cost_ann')

# Create Input for Incurred Cost Due to Downtown
cost_inc = st.number_input("Incurred Cost For Downtime ($/yr):",min_value=0,max_value=None,step=1000,value=0,key='cost_inc')

# Create Input for Labor Division
labor_rows = st.number_input('Number of Divisions (Labor Costs):', min_value=0, max_value=None,key = 'labor_num')
grid5 = st.columns([0.3,0.3,0.4])
division = [] #Store division
labor_pct = [] #Store the labor percentrate

def add_row5(row):
    # -- Start Date for Time Down
    with grid5[0]:
        while len(division) < row+1:
            division.append(None)
        if row == 0:
            division[row]=st.selectbox('Directorate', ('Code F','Code L'), key=f'input_colz{row}')
        else:
            division[row]=st.selectbox('', ('Code F','Code L'), key=f'input_colz{row}')
    # -- Time Down
    with grid5[1]:
        while len(labor_pct) < row+1:
            labor_pct.append(None)
        if row == 0:
            labor_pct[row]=st.number_input('Labor Cost (%)', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colaa{row}')
        else:
            labor_pct[row]=st.number_input('', min_value=0.0, max_value=100.0, step=0.5, key=f'input_colaa{row}')
for r in range(labor_rows):
    add_row5(r)

#----------------------------------------------------------------------------------
# Submit Button
st.markdown('Press "Submit" to generate the output Text File. Download the *.txt file and upload to: https://nasagov.app.box.com/f/dcb7f4527bb345998aec063aa8d33109')
st.subheader('')
# Create SUBMIT Button
if st.button('Submit'):
    

    # Write the Text File
    # -- Laboratory/Capability Information
    data_out = 'Laboratory/Capability Name: ' + lab_name + '\n'
    data_out = data_out + 'Point of Contact: ' + poc + '\n'
    data_out = data_out + 'Branch: ' + branch + '\n'
    data_out = data_out + 'Laboratory/Capability Description: ' + lab_desc + '\n'
    data_out = data_out + 'Laboratory/Capability Website: ' + lab_link + '\n'
    data_out = data_out + 'Challenges in sustaining this laboratory/capability: ' + lab_chal + '\n'
    data_out = data_out + 'Age (yrs): ' + str(lab_age) + '\n'
    data_out = data_out + 'Condition: ' + lab_condition + '\n'
    data_out = data_out + '\n'

    # -- Asset Information
    data_out = data_out + 'Number of Assets: ' + str(asset_rows) + '\n'
    if asset_rows > 0:
        data_out = data_out + 'Asset Name \t Location (Bldg/Rm) \t Age (yrs) \t Date of Entry \t Expected Date of Obsolescence \t ' + \
                              'Asset Condition \t Replacement Cost ($) \t Impact to Capability if Lost \t Associated Software \t ' + \
                              'IT Hardware Repalcement? \t Part or Full Replacement? \n'
        for w in range(asset_rows):
            data_out = data_out + asset_name[w] +'\t' + asset_loc[w] + '\t' +  str(asset_age[w]) + '\t' + str(asset_date_in[w])  + '\t' + \
                       str(asset_date_out[w]) + '\t' +  asset_cond[w] + '\t' + str(asset_cost[w]) + '\t' +  asset_imp[w] + '\t' + \
                       asset_software[w] + '\t' + asset_itrep[w] + '\t' + asset_repdesc[w] +'\n' 
        data_out = data_out + '\n'
        
    # -- Funding Information
    data_out = data_out + 'Sustainment Funding Source: ' + sust_funding + ' \n'
    data_out = data_out + 'Number of Funding Sources: ' + str(fund_rows) + '\n'
    if fund_rows > 0:
        data_out = data_out + 'Funding Source \t Funding Start Date \t Funding End Date \t Funding Amount per Year ($) \n'
        for w in range(fund_rows):
            data_out = data_out + fund_src[w] +'\t' + str(start_fund[w]) +'\t' + str(end_fund[w]) +'\t' + str(fund_amt[w]) + '\n'
        data_out = data_out + '\n'
        
    # -- Projects
    data_out = data_out + 'Number of Projects: ' + str(proj_rows) + '\n'
    if proj_rows > 0:
        data_out = data_out + 'Mission/Project Name \t WBS Number \t Project Use (%) \t Risk to Project \t Impact if Laboratory/Capability is Lost \n'
        for w in range(proj_rows):
            data_out = data_out + proj_util[w] + '\t' + wbs_util[w] + '\t' + str(use_util[w]) + '\t' + risk[w] + '\t' + impact_util[w] + '\n'
        data_out = data_out + '\n'

    # -- Utilization History and Impact
    data_out = data_out + 'History of capability utilization: ' + hist + '\n'
    data_out = data_out + 'Major impact and contributions this capability has made possible: ' + impact + '\n'

    # -- History of Down Time
    data_out = data_out + 'Number of Failures: ' + str(down_rows) + '\n'
    if down_rows > 0:
        data_out = data_out + 'Asset \t Start Date \t Time Down \t Unit \t Additional Notes \n'
        for w in range(down_rows):
            data_out = data_out + asset_dt[w] + '\t' + str(date_dt[w]) + '\t' + str(time_dt[w]) + '\t' + unit_dt[w] + '\t' + desc_dt[w] +'\n'
        data_out = data_out + '\n'

    # -- Cost
    data_out = data_out + 'Estimated Cost to Replace Entire Laboratory/Capability ($): ' + str(cost_rep) + '\n'
    data_out = data_out + 'Cost of Service Contracts ($): ' + str(cost_serv) + '\n'
    data_out = data_out + 'Annual Cost to Operate and Sustain the Lab ($/yr): ' + str(cost_ann) + '\n'
    data_out = data_out + 'Incurred Cost For Downtime ($/yr): ' + str(cost_inc) + '\n'
    data_out = data_out + 'Number of Divisions (Labor Costs): ' + str(labor_rows) + '\n'
    if labor_rows > 0:
        data_out = data_out + 'Directorate \t Labor Cost (%) \n'
        for w in range(labor_rows):
            data_out = data_out + division[w] + '\t' + str(labor_pct[w]) + '\n'
        data_out = data_out + '\n'
    
    st.download_button('Download Data File (Temporary)', data_out, file_name = lab_name + '.txt')
    
