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
        Div = val[0:2]
        Branch = val[0:3]

# Filter Criteria - By Branch or Division
filt_opts = ['Division', 'Branch']
filt_opt1 = st.selectbox('Filter by:',filt_opts,key='filt_opt1')
