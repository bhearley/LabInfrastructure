# Import Modules
import streamlit as st
import os
import glob

# Set Paths
home = os.getcwd()
data_path = "/mount/src/labinfrastructure/Final/"


# Set the page configuration
st.set_page_config(layout="wide")

# Create the Title
st.title("NASA GRC Laboratory Infrastructure Data Collection Analysis")

#Create Divider for Name and Description
st.subheader('Set Filter Criteria')

# Get List of Divisions and Branches
os.chdir(data_path)
files_all = glob.glob('*.txt')

Div = []
Branch = []

for q in range(len(files_all)):
    # Read the Text File
    with open(os.path.join(data_path,files_all[q])) as f:
        lines = f.readlines()

    # Get the Branch Name
    key = 'Branch:'
    for i in range(len(lines)):
        if key in lines[i]:
            val  = lines[i][len(key)+1:len(lines[i])-1]

    if len(val) == 3:
        Direc = val[0]
        if val[0:2] not in Div:
            Div.append(val[0:2])
        if val[0:3] not in Branch:
            Branch.append(val[0:3])
    
Div.sort()
Branch.sort()


# Filter Criteria - By Branch or Division
filt_opts = ['','Division', 'Branch']
filt_opt1 = st.selectbox('Filter by:',filt_opts,key='filt_opt1')

Div_Disp = []
for k in range(len(Div)):
    Div_Disp.append(True)
Branch_Disp = []
for k in range(len(Branch)):
    Branch_Disp.append(True)

if filt_opt1 == 'Division':
    for j in range(len(Div)):
        Div_Disp[j] = st.checkbox(Div[j], value=True, key='div_' + str(j), label_visibility="visible")
if filt_opt1 == 'Branch':
    for j in range(len(Branch)):
        Branch_Disp[j] = st.checkbox(Branch[j], value=True, key='div_' + str(j), label_visibility="visible")

asset_slider = st.slider('Total Asset Value Range', 0, 1000000, (250000, 750000), step = 1000)
grid = st.columns(4)
with grid[0]:
    asset_chk1 = st.checkbox('Poor', value=True)
with grid[1]:
    asset_chk2 = st.checkbox('Fair', value=True)
with grid[2]:
    asset_chk13 = st.checkbox('Good', value=True)
with grid[3]:
    asset_chk4 = st.checkbox('Excellent', value=True)
