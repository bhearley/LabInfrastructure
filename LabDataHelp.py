#==================================================================================================================================================================
#   NASA GRC Lab Data Help
#   Brandon Hearley - LMS
#   4/24/2024
#
#   PURPOSE: Create a Help Site for the Web App
#==================================================================================================================================================================
# SETUP
# Import the necessary modules to run the app

# Import Modules
# -- see requirements.txt for any specified versions need
import streamlit as st

#==================================================================================================================================================================
# GENERAL INFORMATION
# Set the web app general information not edited by the user

# Set the page configuration
st.set_page_config(layout="wide")

# Create the Title
st.title("NASA GRC Laboratory Infrastructure Data Collection Help Page")

# Create Instructions
st.markdown('The NASA GRC Laboratory Infrastructure Data Collection Tool is a web-based application built using Streamlit, an open-source Python framework. The purpose of the tool is to capture the current state of GRC capabilities. This information is necessary to assess the overall state of our infrastructure and assets and will be used to develop strategic plans for laboratory investment. The tool can be accessed via: https://nasagrclabwithlog.streamlit.app/')
st.markdown(' ')
st.markdown('Using the web-app, users should fill out each field for an individual lab and its assets. Assets should only be added to the record if it is associated with the infrastructure of the lab and not the facility. To limit the total number of entries, users should only enter assets that have a value over $50,000 or assets at lower values that are either extremely critical to the lab’s capability or are difficult to replace. Entries made by each user can be saved to the database as either a draft or a final submission, such that users can save their work and come back to it to further edit at a later date.')

# Defintions
with st.expander('Definitions'):
  col1_def, col2_def = st.columns([0.2,0.8])
  col1_def.markdown('Laboratory')
  col2_def.markdown('A dedicated facility, or dedicated infrastructure, for performing a specific type of testing, research, or development. A laboratory may encompass a unique capability and may include multiple high values assets such as test or analytical equipment (e.g., The Structural Dynamics Laboratory).')
  col1_def, col2_def = st.columns([0.2,0.8])
  col1_def.markdown('Asset')
  col2_def.markdown('A unique equipment that is segregable from the facility. An asset may be composed of multiple components. (e.g., a Scanning Electron Microscope).')
  
