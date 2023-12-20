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

# Set Paths
home = os.getcwd()
#data_path = r'C:\Users\bhearley\Box\LabInfrastructureData'
data_path = "./"
data_template = "./Templates/DataTemplate.pkl"

#----------------------------------------------------------------
#   CREATE THE APP
#   Create the streamlit app for data collection

# Create the Title
st.title("NASA GRC Lab Infrastructure Data Collection")

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Labratory/Capability Information')

# Create Input for Asset Name
asset_name = st.text_input("Labratory/Capability Name:",value="")

# Create Input for Asset Description
asset_desc = st.text_area("Labratory/Capability Description:",value="")

# Create Input for Describing Challegen in Sustaining
challenge_desc = st.text_area("Challenge in sustaining this capablity:",value="")

# Create Input for Age
age = st.number_input("Age (years):",min_value=0,max_value=None,value=0)

# Create Input for Condition
condition = st.selectbox('Condition:',
    ('Excellent', 'Good', 'Fair','Poor')) #Options

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Current Mission/Projet Utilization')
# Create Input for Project Utilization and Risk
proj_rows = st.number_input('Number of Projects', min_value=0, max_value=10)
grid = st.columns(3)
proj_util = [None,None,None,None,None,None,None,None,None,None] #Store the projects
use_util = [None,None,None,None,None,None,None,None,None,None] #Store the use for each project
risk = [None,None,None,None,None,None,None,None,None,None] #Store the risk
def add_row(row):
    with grid[0]:
        if row == 0:
            proj_util[row]=st.text_input('Mission/Project Name', key=f'input_col1{row}')
        else:
            proj_util[row]=st.text_input('', key=f'input_col1{row}')
    with grid[1]:
        if row == 0:
            use_util[row]=st.number_input('Use (hours/week)', step=0.5, key=f'input_col2{row}')
        else:
            use_util[row]=st.number_input('', step=0.5, key=f'input_col2{row}')
    with grid[2]:
        if row == 0:
            risk[row]=st.selectbox('Risk to Projects', ('High', 'Moderate', 'Low'),key=f'input_col3{row}')
        else:
            risk[row]=st.selectbox('', ('High', 'Moderate', 'Low'),key=f'input_col3{row}')
for r in range(proj_rows):
    add_row(r)

#----------------------------------------------------------------------------------
#Create Divider for Name and Description
st.subheader('Utilization History an Impact')
# Create Input for History of Capability Utilization
hist = st.text_area("History of capability utilization:",value="")

# Create Input for Major Impact and Contributions
impact = st.text_area("Major impact and contributions this capability has made possible:",value="")

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('History of Down Time Due to Maintanence or Failure')
# Create Input for Downtime History
down_rows = st.number_input('Number of Rows', min_value=0, max_value=10)
grid2 = st.columns(4)
date_dt = [None,None,None,None,None,None,None,None,None,None] #Store date the asset went down
time_dt = [None,None,None,None,None,None,None,None,None,None] #Store the time down
unit_dt = [None,None,None,None,None,None,None,None,None,None] #Store the unit for time down
desc_dt = [None,None,None,None,None,None,None,None,None,None] #Store a description for the time down
def add_row2(row):
    with grid2[0]:
        if row == 0:
            date_dt[row]=st.date_input('Start Date', key=f'input_col4{row}')
        else:
            date_dt[row]=st.date_input('',key=f'input_col4{row}')
    with grid2[1]:
        if row == 0:
            time_dt[row]=st.number_input('Time Down', step=0.5, key=f'input_col5{row}')
        else:
            time_dt[row]=st.number_input('', step=0.5, key=f'input_col5{row}')
    with grid2[2]:
        if row == 0:
            unit_dt[row]=st.selectbox('Unit', ('Days', 'Weeks', 'Months','Years'),key=f'input_col6{row}')
        else:
            unit_dt[row]=st.selectbox('', ('Days', 'Weeks', 'Months','Years'),key=f'input_col6{row}')
    with grid2[3]:
        if row == 0:
            desc_dt[row]=st.text_input('Additional Notes', value='',key=f'input_col7{row}')
        else:
            desc_dt[row]=st.text_input('', value='',key=f'input_col7{row}')
for r in range(down_rows):
    add_row2(r)

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('Cost')
# Create Input for Cost of Replacement
cost_rep = st.number_input("Cost of Replacement ($):",min_value=0.00,max_value=None,step=0.01,value=0.00)

# Create Input for Cost of Service Contracts
cost_serv = st.number_input("Cost of Service Contracts ($):",min_value=0.00,max_value=None,step=0.01,value=0.00)

# Create Input for Annual Expenses to operate and sustain the lab
cost_ann = st.number_input("Annual Cost to Operate and Sustain the Lab ($/yr):",min_value=0.00,max_value=None,step=0.01,value=0.00)

#----------------------------------------------------------------------------------
#Create Divider for Down Time History
st.subheader('')
# Create SUBMIT Button
if st.button('Submit'):
    #Load the template
    #data_template = os.path.join(data_path,'Template','DataTemplate.pkl')
    with open(data_template, 'rb') as handle:
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
    req_txt_d = ['Labratory/Capability Name:',
                'Labratory/Capability Description:',
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
        os.chdir(data_path)
        files_all = glob.glob('*.pkl')
        new_filename = 'New_Data_' + str(len(files_all)) + '.pkl'
        new_file = os.path.join(data_path,new_filename)

        #--Save to the Data Path
        with open(new_file, 'wb') as handle:
            pickle.dump(Data, handle, protocol=pickle.HIGHEST_PROTOCOL)
