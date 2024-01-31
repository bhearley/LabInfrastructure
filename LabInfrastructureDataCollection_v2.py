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
data_template = "/mount/src/labinfrastructure/Template/DataTemplate.pkl"
# data_template= os.path.join(home,'Template','DataTemplate.pkl')

#----------------------------------------------------------------
#   CREATE THE APP
#   Create the streamlit app for data collection

# Set the page configuration
st.set_page_config(layout="wide")

# Create the Title
st.title("NASA GRC Laboratory Infrastructure Data Collection")

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Laboratory/Capability Information')

# Create Input for Asset Name
asset_name = st.text_input("Laboratory/Capability Name:",value="")

# Create Input for Asset Description
asset_desc = st.text_area("Laboratory/Capability Description:",value="")

# Create Input for Asset Name
asset_link = st.text_input("Laboratory/Capability Website:",value="")

# Create Input for Describing Challegne in Sustaining
challenge_desc = st.text_area("Challenges in sustaining this laboratory/capability:",value="")

# Create Input for Age
age = st.number_input("Age (yrs):",min_value=0,max_value=None,value=0)

# Create Input for Condition
condition = st.selectbox('Condition:',
    ('Excellent', 'Good', 'Fair','Poor')) #Options

# Create Input for Assets
asset_rows = st.number_input('Number of Assets:', min_value=0, max_value=50)
#grid = st.columns([0.075,0.05,0.05,0.08,0.125,0.085,0.11,0.075,0.1,0.125,0.125])
grid = st.columns([0.125,0.075,0.05,0.08,0.08,0.09,0.07,0.125,0.1,0.07,0.1])
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
            asset_name[row]=st.text_input('Asset \n \n Name', key=f'input_col1{row}')
        else:
            asset_name[row]=st.text_input('', key=f'input_col1{row}')
    # -- Asset Location    
    with grid[1]:
        while len(asset_loc) < row+1:
            asset_loc.append(None)
        if row == 0:
            asset_loc[row]=st.text_input('Location  \n \n (Bldg/Rm)', key=f'input_col2{row}')
        else:
            asset_loc[row]=st.text_input('', key=f'input_col2{row}')
    # -- Asset Age
    with grid[2]:
        while len(asset_age) < row+1:
            asset_age.append(None)
        if row == 0:
            asset_age[row]=st.number_input('Age  \n \n  (yrs)', step=0.5, key=f'input_col3{row}')
        else:
            asset_age[row]=st.number_input('', step=0.5, key=f'input_col3{row}')
    # -- Asset Date of Entry
    with grid[3]:
        while len(asset_date_in) < row+1:
            asset_date_in.append(None)
        if row == 0:
            asset_date_in[row]=st.date_input('Date of  \n \n  Entry', min_value=datetime.date(1950, 1, 1), key=f'input_col4{row}')
        else:
            asset_date_in[row]=st.date_input('', min_value=datetime.date(1950, 1, 1), key=f'input_col4{row}')
    # -- Asset Date of Obsolescence
    with grid[4]:
        while len(asset_date_out) < row+1:
            asset_date_out.append(None)
        if row == 0:
            asset_date_out[row]=st.date_input('Expected Date of Obsolescence', min_value=datetime.date(1950, 1, 1), key=f'input_col5{row}')
        else:
            asset_date_out[row]=st.date_input('', min_value=datetime.date(1950, 1, 1), key=f'input_col5{row}')
    # -- Asset Condition
    with grid[5]:
        while len(asset_cond) < row+1:
            asset_cond.append(None)
        if row == 0:
            asset_cond[row]=st.selectbox('Asset  \n \n  Condition', ('Excellent', 'Good', 'Fair', 'Poor'),key=f'input_col6{row}')
        else:
            asset_cond[row]=st.selectbox('', ('Excellent', 'Good', 'Fair', 'Poor'),key=f'input_col6{row}')
    # -- Asset Cost of Replacement
    with grid[6]:
        while len(asset_cost) < row+1:
            asset_cost.append(None)
        if row == 0:
            asset_cost[row]=st.number_input('Replacement \n \n  Cost ($)', step=1000, key=f'input_col7{row}')
        else:
            asset_cost[row]=st.number_input('', step=1000, key=f'input_col7{row}')
    # -- Asset Impact if Lost
    with grid[7]:
        while len(asset_imp) < row+1:
            asset_imp.append(None)
        if row == 0:
            asset_imp[row]=st.text_input('Impact to Capability \n \n  if Lost', key=f'input_col8{row}')
        else:
            asset_imp[row]=st.text_input('', key=f'input_col8{row}')
    # -- Associated Software
    with grid[8]:
        while len(asset_software) < row+1:
            asset_software.append(None)
        if row == 0:
            asset_software[row]=st.text_input('Associated \n \n Software', key=f'input_col9{row}')
        else:
            asset_software[row]=st.text_input('', key=f'input_col9{row}')
    # -- IT/computer hardware repalcement
    with grid[9]:
        while len(asset_itrep) < row+1:
            asset_itrep.append(None)
        if row == 0:
            asset_itrep[row]=st.selectbox('IT Hardware \n \n  Repalcement?', ('Yes','No'),key=f'input_col10{row}')
        else:
            asset_itrep[row]=st.selectbox('', ('Yes','No'),key=f'input_col10{row}')
    with grid[10]:
        while len(asset_repdesc) < row+1:
            asset_repdesc.append(None)
        if row == 0:
            asset_repdesc[row]=st.text_input('Part or Full \n \n Replacement?', key=f'input_col11{row}')
        else:
            asset_repdesc[row]=st.text_input('', key=f'input_col11{row}')
for r in range(asset_rows):
    add_row_asset(r)

# Create Input for Sustainment Funding Source
sust_funding = st.text_area("Sustainment Funding Source:",value="")

# Additional Information on Funding
fund_rows = st.number_input('Number of Rows:', min_value=0, max_value=50)
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
            fund_src[row]=st.text_input('Funding Source', value='',key=f'input_col12{row}')
        else:
            fund_src[row]=st.text_input('', value='',key=f'input_col12{row}')
    # -- Start Date of Funding
    with grid2[1]:
        while len(start_fund) < row+1:
            start_fund.append(None)
        if row == 0:
            start_fund[row]=st.date_input('Funding Start Date', min_value=datetime.date(1950, 1, 1), key=f'input_col13{row}')
        else:
            start_fund[row]=st.date_input('', min_value = datetime.date(1950, 1, 1), key=f'input_col13{row}')
    # -- End Date of Funding
    with grid2[2]:
        while len(end_fund) < row+1:
            end_fund.append(None)
        if row == 0:
            end_fund[row]=st.date_input('Funding End Date', min_value=datetime.date(1950, 1, 1), key=f'input_col13{row}')
        else:
            end_fund[row]=st.date_input('', min_value = datetime.date(1950, 1, 1), key=f'input_col13{row}')
    # -- Funding Amount
    with grid2[3]:
        while len(fund_amt) < row+1:
            fund_amt.append(None)
        if row == 0:
            fund_amt[row]=st.number_input("Funding Amount per Year ($)",min_value=0,max_value=None,step=1000,value=0, key=f'input_col14{row}')
        else:
            fund_amt[row]=st.number_input("",min_value=0,max_value=None,step=1000,value=0, key=f'input_col14{row}')
for r in range(fund_rows):
    add_row2(r)

# Create File Uploader
uploaded_files = st.file_uploader("Upload Documents/Images:", accept_multiple_files=True)

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Current Mission/Project Utilization')
# Create Input for Project Utilization and Risk
proj_rows = st.number_input('Number of Projects', min_value=0, max_value=50)
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
            proj_util[row]=st.text_input('Mission/Project Name', key=f'input_col12{row}')
        else:
            proj_util[row]=st.text_input('', key=f'input_col12{row}')
    # -- WBS Number
    with grid3[1]:
        while len(wbs_util) < row+1:
            wbs_util.append(None)
        if row == 0:
            wbs_util[row]=st.text_input('WBS Number', key=f'input_col13{row}')
        else:
            wbs_util[row]=st.text_input('', key=f'input_co13{row}')
    # -- Project Use
    with grid3[2]:
        while len(use_util) < row+1:
            use_util.append(None)
        if row == 0:
            use_util[row]=st.number_input('Project Use (%)', min_value=0.0, max_value=100.0, step=0.5, key=f'input_col14{row}')
        else:
            use_util[row]=st.number_input('', min_value=0.0, max_value=100.0, step=0.5, key=f'input_col14{row}')
    # -- Risk to Project
    with grid3[3]:
        while len(risk) < row+1:
            risk.append(None)
        if row == 0:
            risk[row]=st.selectbox('Risk to Project', ('High', 'Moderate', 'Low'),help='High -  Capability cannot be replicated elsewhere and replacement has high cost/lead time. \n \n \n ' +
                                                                                       'Moderate - Capability cannot be replicated elsewhere and replacement has low cost/lead time. \n \n \n ' +
                                                                                       'Low - Capability can be replicated elsewhere for low cost/lead time.',key=f'input_col15{row}')
        else:
            risk[row]=st.selectbox('', ('High', 'Moderate', 'Low'),key=f'input_col15{row}')
    # -- Impact to Project
    with grid3[4]:
        while len(impact_util) < row+1:
            impact_util.append(None)
        if row == 0:
            impact_util[row]=st.text_input('Impact if Laboratory/Capability is Lost', key=f'input_col16{row}')
        else:
            impact_util[row]=st.text_input('', key=f'input_col16{row}')
for r in range(proj_rows):
    add_row3(r)

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Utilization History and Impact')
# Create Input for History of Capability Utilization
hist = st.text_area("History of capability utilization:",value="")

# Create Input for Major Impact and Contributions
impact = st.text_area("Major impact and contributions this capability has made possible:",value="")

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('History of Down Time Due to Maintenance or Failure')
# Create Input for Downtime History
down_rows = st.number_input('Number of Rows:', min_value=0, max_value=50)
grid4 = st.columns(4)
date_dt = [] #Store date the asset went down
time_dt = [] #Store the time down
unit_dt = [] #Store the unit for time down
desc_dt = [] #Store a description for the time down
def add_row4(row):
    # -- Start Date for Time Down
    with grid4[0]:
        while len(date_dt) < row+1:
            date_dt.append(None)
        if row == 0:
            date_dt[row]=st.date_input('Start Date', min_value=datetime.date(1950, 1, 1), key=f'input_col17{row}')
        else:
            date_dt[row]=st.date_input('', min_value = datetime.date(1950, 1, 1), key=f'input_col17{row}')
    # -- Time Down
    with grid4[1]:
        while len(time_dt) < row+1:
            time_dt.append(None)
        if row == 0:
            time_dt[row]=st.number_input('Time Down', step=0.5, key=f'input_col18{row}')
        else:
            time_dt[row]=st.number_input('', step=0.5, key=f'input_col18{row}')
    # -- Unit of Time Down
    with grid4[2]:
        while len(unit_dt) < row+1:
            unit_dt.append(None)
        if row == 0:
            unit_dt[row]=st.selectbox('Unit', ('Days', 'Weeks', 'Months','Years'),key=f'input_col19{row}')
        else:
            unit_dt[row]=st.selectbox('', ('Days', 'Weeks', 'Months','Years'),key=f'input_col19{row}')
    # -- Additonal Notes for Time Down
    with grid4[3]:
        while len(desc_dt) < row+1:
            desc_dt.append(None)
        if row == 0:
            desc_dt[row]=st.text_input('Additional Notes', value='',key=f'input_col20{row}')
        else:
            desc_dt[row]=st.text_input('', value='',key=f'input_col20{row}')
for r in range(down_rows):
    add_row4(r)

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('Cost')
# Create Input for Cost of Replacement
cost_rep = st.number_input("Estimated Cost to Replace Entire Laboratory/Capability ($):",min_value=0,max_value=None,step=1000,value=0)

# Create Input for Cost of Service Contracts
cost_serv = st.number_input("Cost of Service Contracts ($):",min_value=0,max_value=None,step=1000,value=0)

# Create Input for Annual Expenses to operate and sustain the lab
cost_ann = st.number_input("Annual Cost to Operate and Sustain the Lab ($/yr):",min_value=0,max_value=None,step=1000,value=0)

# Create Input for Incurred Cost Due to Downtown
cost_inc = st.number_input("Incurred Cost For Downtime ($/yr):",min_value=0,max_value=None,step=1000,value=0)

# Create Input for Labor Division
labor_rows = st.number_input('Number of Divisions (Labor Costs):', min_value=0, max_value=50)
grid5 = st.columns(2)
division = [] #Store division
labor_pct = [] #Store the labor percentrate

def add_row5(row):
    # -- Start Date for Time Down
    with grid5[0]:
        while len(division) < row+1:
            division.append(None)
        if row == 0:
            division[row]=st.selectbox('Directorate', ('Code F','Code L'), key=f'input_col21{row}')
        else:
            division[row]=st.date_input('', ('Code F','Code L'), key=f'input_col21{row}')
    # -- Time Down
    with grid5[1]:
        while len(labor_pct) < row+1:
            labor_pct.append(None)
        if row == 0:
            labor_pct[row]=st.number_input('Labor Cost (%)', min_value=0.0, max_value=100.0, step=0.5, key=f'input_col22{row}')
        else:
            labor_pct[row]=st.number_input('', min_value=0.0, max_value=100.0, step=0.5, key=f'input_col22{row}')
for r in range(labor_rows):
    add_row5(r)

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('')
# Create SUBMIT Button
if st.button('Submit'):
    #Load the template
    with open("/mount/src/labinfrastructure/Template/DataTemplate.pkl", 'rb') as handle:
        Data = pickle.load(handle)

    
#----------------------------------------------------------------------------------
    # DATA VALIDATION
    # Ensure Data is correct before writing

    # Set the error flag
    err_flag = 0 #Only write data if error flag is 0 after validation

    # Required Text Attributes
    req_txt = [asset_name,
               asset_desc,
               challenge_desc,
               hist,
               impact]
    req_txt_d = ['Laboratory/Capability Name:',
                'Laboratory/Capability Description:',
                'Challenge in sustaining this capablity:',
                'History of capability utilization:',
                'Major impact and contributions this capability has made possible:'
                ]

    for j in range(len(req_txt)):
        if req_txt[j] == '':
            st.error(req_txt_d[j] + ' is required.')
            err_flag=1

    # Required Point Attributes
    req_pnt = [age,
               cost_rep,
               cost_serv,
               cost_ann]
    req_pnt_d = ['Age (years)',
                 'Cost of Replacement ($):',
                 'Cost of Service Contracts ($):',
                 'Annual Cost to Operate and Sustain the Lab ($/yr):'
                 ]
    for j in range(len(req_pnt)):
        if req_pnt[j] == 0:
            st.error(req_pnt_d[j] + ' is required.')
            err_flag=1
    

    # Write the Data
    if err_flag == 0:
        #-- Populate the Data
        Data['Name'] = asset_name
        Data['Description'] = asset_desc
        Data['Challenge'] = challenge_desc
        Data['Age'] = age
        Data['Condition'] = condition

        proj_write = []
        util_write = []
        risk_write = []
        for k in range(proj_rows):
            proj_write.append(proj_util[k])
            util_write.append(use_util[k])
            risk_write.append(risk[k])

        Data['Projects'] = proj_write
        Data['Utilization'] = util_write
        Data['Risk'] = risk_write

        Data['History'] = hist
        Data['Impact'] = asset_desc

        date_write = []
        time_write = []
        unit_write = []
        desc_write = []
        for k in range(down_rows):
            date_write.append(date_dt[k])
            time_write.append(time_dt[k])
            unit_write.append(unit_dt[k])
            desc_write.append(desc_dt[k])


        Data['DownTimeDates'] = date_write
        Data['DownTimeTimes'] = time_dt
        Data['DownTimeUnits'] = unit_write
        Data['DownTimeDescs'] = desc_write

        Data['ReplacementCost'] = cost_rep
        Data['ServiceContractCost'] = cost_serv
        Data['AnnualExpenseCost'] = cost_ann

        #--Get the new file name
        os.chdir("/mount/src/labinfrastructure/NewFiles/")
        files_all = glob.glob('*.pkl')
        new_filename = 'New_Data_' + str(len(files_all)) + '.pkl'
        new_file = "/mount/src/labinfrastructure/NewFiles/" + new_filename

        #--Save to the Data Path
        with open('/mount/src/labinfrastructure/New.pkl', 'wb') as handle:
            pickle.dump(Data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        st.write(Data)

