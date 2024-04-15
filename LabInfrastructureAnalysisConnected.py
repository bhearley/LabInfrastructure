# Import Modules
import streamlit as st
import os
import glob
import numpy as np
import streamlit as st
from pymongo.mongo_client import MongoClient
import dns
import certifi
from datetime import date

# Set Path
data_path = "/mount/src/labinfrastructure/"

# Set the page configuration
st.set_page_config(layout="wide")

# Connect to the Database
@st.cache_resource
def init_connection():
    uri = "mongodb+srv://nasagrc:brookpark21000@nasagrclabdatatest.hnx1ick.mongodb.net/?retryWrites=true&w=majority&appName=NASAGRCLabDataTest"
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
    items = db['LabData'].find()
    items = list(items)  # make hashable for st.cache_data
    return items

# Get All Data in Database
all_data = get_data()


# Create the Title
st.title("NASA GRC Laboratory Infrastructure Data Collection Analysis")
st.markdown('Set the filter criteria and generate a Word Document report summarizing the information collected on the GRC Lab Infrastructure. \n\n For all questions, please email brandon.l.hearley@nasa.gov')

#Create Divider for Name and Description
st.subheader('Select Divisions or Branches')
st.markdown('Only select labs from specific divisions or branches. Use the drop down menu to filter by either division or branch, then check all options you would like in the report.')

Div = []
Branch = []

for q in range(len(all_data)):
    branch_q = all_data[q]['Branch']
    div_q = branch_q[0:2]
    
    if div_q not in Div:
        Div.append(div_q)
    if branch_q not in Branch:
        Branch.append(branch_q)
    
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

st.markdown(' ')
st.subheader('Select Labs by Asset or Replacement Costs')
st.markdown('Only select labs whose total asset replacement cost for the specified conditions are within a certain range. Use the two inputs to set the minimum and maximum total value of assets that meet the condition criteria for a lab. Use the checkboxes to select which asset conditions you would like to consider.')

# Convert String Number to Have Comma Separators
def convert_num(key):
    if key in st.session_state:
        raw_val = st.session_state[key]
        test_val = raw_val.replace(',','')
        flag = 0
        try:
            float(test_val)
        except ValueError:
            flag = 1
            st.error('Not a valid number')
        if flag == 0:
            if len(test_val)>3:
                num = ''
                for k in range(len(test_val)):
                    num = test_val[len(test_val)-1-k] + num
                    chk = k+1
                    if chk%3 == 0 and k!= len(test_val)-1:
                        num = ',' + num
                st.session_state[key] = num

grid_vals1 = st.columns(2)
with grid_vals1[0]:
    min_asset_cost = st.text_input('Min. Value of Total Assets', value=None, key='min_asset_cost_key', on_change=convert_num('min_asset_cost_key'))
with grid_vals1[1]:
    max_asset_cost = st.text_input('Max. Value of Total Assets', value=None, key='max_asset_cost_key', on_change=convert_num('max_asset_cost_key'))


grid = st.columns(4)
with grid[0]:
    asset_chk1 = st.checkbox('Poor', value=True)
with grid[1]:
    asset_chk2 = st.checkbox('Fair', value=True)
with grid[2]:
    asset_chk3 = st.checkbox('Good', value=True)
with grid[3]:
    asset_chk4 = st.checkbox('Excellent', value=True)
            
st.markdown(' ')
st.markdown('Only select labs whose total replacement cost is within a certain range.  Use the two inputs to set the minimum and maximum total value of assets that meet the condition criteria for a lab.')
grid_vals2 = st.columns(2)
with grid_vals2[0]:
    min_tot_cost = st.text_input('Min. Value of Total Replacement Cost', value=None, key='min_tot_cost_key', on_change=convert_num('min_tot_cost_key'))
with grid_vals2[1]:
    max_tot_cost = st.text_input('Max. Value of Total Replacement Cost', value=None, key='max_tot_cost_key', on_change=convert_num('max_tot_cost_key'))

status_opts = ['All Entries (Draft and Final)','Final Only']
status_opt1 = st.selectbox('Select Status of Data Entries:',status_opts,key='status_opt1')

st.markdown(' ')
st.markdown('Filter all data in the database for the above criteria and write to a report. Once filtered, select the "Download Report" button to download the Word Document.')
if st.button('Filter Data'):
    # Get List of Divisions
    Div_List = []
    for j in range(len(Div_Disp)):
        if Div_Disp[j] == True:
            Div_List.append(Div[j])

    # Get List of Divisions
    Branch_List = []
    for j in range(len(Branch_Disp)):
        if Branch_Disp[j] == True:
            Branch_List.append(Branch[j])
    
    # Get List of Asset Criteria
    Asset_Cond_List = []
    if asset_chk1 == True:
        Asset_Cond_List.append('Poor')
    if asset_chk2 == True:
        Asset_Cond_List.append('Fair')
    if asset_chk3 == True:
        Asset_Cond_List.append('Good')
    if asset_chk4 == True:
        Asset_Cond_List.append('Excellent')

    # Get Status Criteria
    if st.session_state['status_opt1'] == 'All Entries (Draft and Final)':
        status_choice = ['Draft','Final']
    else:
        statis_choice = ['Final']

    # Create Criteria Dictionary
    criteria= {
             'Div':Div_List,
             'Branches':Branch_List,
             'AssetValCond':Asset_Cond_List,
             'AssetVal':[float(min_asset_cost.replace(',','')), float(max_asset_cost.replace(',',''))],
             'RepCost':[float(min_tot_cost.replace(',','')), float(max_tot_cost.replace(',',''))],
            'Status':status_choice}

    FilesOut = {}
    
    # Get Organized List of Records
    for q in range(len(all_data)):
        # Get the individual record
        record = all_data[q]

        # Get the Directorate, Division, and Branch
        Branch = record['Branch']
        Div = Branch[0:2]
        Direc = Branch[0]

        # Set Flag
        crit_flag = 1

        # Evaluate Division Criteria
        if criteria['Div'] != None:
            if Div not in criteria['Div']:
                crit_flag = 0

        # Evaluate Division Criteria
        if criteria['Branches'] != None:
            if Branch not in criteria['Branches']:
                crit_flag = 0

        # Get Total Asset Cost and Filter
        num_assets  = int(record['Number of Assets'])
        tot_asset_cost = 0
        
        for k in range(num_assets):
            if record['T1-Asset Condition'][k] in criteria['AssetValCond'] and record['T1-Replacement Cost ($)'][k] != None:
                tot_asset_cost = tot_asset_cost + float(record['T1-Replacement Cost ($)'][k])

        if criteria['AssetVal'][0] != None or criteria['AssetVal'][1] != None:
            if criteria['AssetVal'][0] != None and tot_asset_cost < criteria['AssetVal'][0]:
                crit_flag = 0
            if criteria['AssetVal'][1] != None and tot_asset_cost > criteria['AssetVal'][1]:
                crit_flag = 0
        
        # -- Estimated Cost to Replace Entire Laboratory/Capability ($):
        if criteria['RepCost'][0] != None or criteria['RepCost'][1] != None:
            if record['Estimated Cost to Replace Entire Laboratory/Capability ($)'] == None:
                crit_flag = 0
            elif criteria['RepCost'][0] != None and record['Estimated Cost to Replace Entire Laboratory/Capability ($)'] < criteria['RepCost'][0]:
                crit_flag = 0
            elif criteria['RepCost'][1] != None and record['Estimated Cost to Replace Entire Laboratory/Capability ($)'] > criteria['RepCost'][1]:
                crit_flag = 0

        # -- Check Status
        if record['Status'] not in criteria['Status']:
            crit_flag= 0


        if crit_flag == 1:
            div_keys = list(FilesOut.keys())
            if Div not in div_keys:
                FilesOut[Div] = {}

            branch_keys = list(FilesOut[Div].keys())
            if Branch not in branch_keys:
                FilesOut[Div][Branch] = []

            FilesOut[Div][Branch].append(q)

    # Write the Report
    import docx
    from docx.shared import Pt 
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.text import WD_BREAK
    from docx.enum.section import WD_ORIENT, WD_SECTION
    import matplotlib.pyplot as plt
    from docx.shared import Inches

    # Utility Functions
    def change_orientation():
        current_section = doc.sections[-1]
        new_width, new_height = current_section.page_height, current_section.page_width
        new_section = doc.add_section(WD_SECTION.NEW_PAGE)
        new_section.orientation = WD_ORIENT.LANDSCAPE
        new_section.page_width = new_width
        new_section.page_height = new_height

        return new_section

    # Format Entires
    def format_values(test_val, key):
        if test_val == None:
            val = ''
        else:
            if key == "string":
                val = str(test_val)
            if key == "money":
                if isinstance(test_val,str) == False:
                    test_val = str(int(test_val))
                val = ''
                for k in range(len(test_val)):
                    val = test_val[len(test_val)-1-k] + val
                    chk = k+1
                    if chk%3 == 0 and k!= len(test_val)-1:
                        val = ',' + val
            if key == "WBS":
                if len(test_val) > 6:
                    val = test_val[0:6]
                else:
                    val = test_val
        return val

    # Create the Document
    doc = docx.Document() 

    # Create the Title Page
    para = doc.add_paragraph()
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = para.add_run('NASA GRC Lab Infrastructure Data')
    run1.font.name = 'Times New Roman'
    run1.font.size = Pt(18)
    run1.bold = True

    # Create Date Time Stamp
    today = date.today()
    para = doc.add_paragraph()
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = para.add_run('Created on: ' + str(today))
    run1.font.name = 'Times New Roman'
    run1.font.size = Pt(12)

    # Loop Through Divisions
    divisions = list(FilesOut.keys())
    divisions.sort()

    for d in range(len(divisions)):
        # Start on New Page
        doc.add_page_break()

        run_lab1 = doc.add_paragraph().add_run(divisions[d])
        run_lab1.font.name = 'Times New Roman'
        run_lab1.font.size = Pt(18)
        run_lab1.bold = True

        # Get list of branches
        branches = list(FilesOut[divisions[d]].keys())
        branches.sort()

        for b in range(len(branches)):
            run_lab1 = doc.add_paragraph().add_run(branches[b])
            run_lab1.font.name = 'Times New Roman'
            run_lab1.font.size = Pt(14)
            run_lab1.bold = True

            # Get List of files
            files = FilesOut[divisions[d]][branches[b]]

            for q in range(len(files)):
                # Get the data
                record = all_data[files[q]]

                run_lab1 = doc.add_paragraph().add_run(record['Laboratory/Capability Name'])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # HEADER: Laboratory/Capability Information
                run_lab1 = doc.add_paragraph().add_run('Laboratory/Capability Information')
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # -- Point of Contact
                key = 'Point of Contact'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Branch
                key = 'Branch'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Laboratory/Capability Description
                key = 'Laboratory/Capability Description'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Laboratory/Capability Website
                key = 'Laboratory/Capability Website'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Challenges in sustaining this laboratory/capability
                key = 'Challenges in sustaining this laboratory/capability'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Age (yrs):
                key = 'Age (yrs)'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + str(record[key]))
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Condition:
                key = 'Condition'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

    
                # -- Asset Table
                num_assets = record['Number of Assets']
                if num_assets > 0:
                    change_orientation()

                    run_lab1 = doc.add_paragraph().add_run('Assets:')
                    run_lab1.font.name = 'Times New Roman'
                    run_lab1.font.size = Pt(11)

                    table = doc.add_table(rows=1, cols=11) 
                    row = table.rows[0].cells 
                    row[0].text = 'Asset Name'
                    row[1].text = 'Location (Bldg/Rm)'
                    row[2].text = 'Age (yrs)'
                    row[3].text = 'Asset Date of Entry'
                    row[4].text = 'Expected Date of Obsolescence'
                    row[5].text = 'Asset Condition'
                    row[6].text = 'Replacement Cost ($)'
                    row[7].text = 'Impact to Capability if Lost'
                    row[8].text = 'Associated Software/Required OS'
                    row[9].text = 'IT Hardware Repalcement?'
                    row[10].text = 'Part or Full Replacement?'

                    col_dict = {'T1-Asset Name':"string",
                  'T1-Location (Bldg/Rm)':"string",
                  'T1-Age (yrs)':"string",
                  'T1-Acquisition Year':"string",
                  'T1-Expected Year of Obsolescence':"string",
                  'T1-Asset Condition':"string",
                  'T1-Replacement Cost ($)':"money",
                  'T1-Impact to Capability if Lost':"string",
                  'T1-Associated Software':"string",
                  'T1-Inlcudes IT Hardware?':"string",
                  'T1-Replacement':"string"}

                    col_keys = list(col_dict.keys())
                    
                    for j in range(num_assets):
                        row = table.add_row().cells
                        for k in range(len(col_keys)):
                            val = record[col_keys[k]][j]
                            val_frmt = format_values(val, col_dict[col_keys[k]])
                            row[k].text = val_frmt
                    table.style = 'Light Grid Accent 4'

                    # Set Font Fize
                    for row in table.rows:
                        for cell in row.cells:
                            paragraphs = cell.paragraphs
                            for paragraph in paragraphs:
                                for run in paragraph.runs:
                                    font = run.font
                                    font.size= Pt(10)
                                    font.name = 'Times New Roman'

                    # Set Column Widths
                    table.autofit = False
                    table.allow_autofit =False
                    col_widths =  [0.85,0.79,0.44,0.63,0.94,0.75,0.94,1.19,0.81,1,0.94]
                    for row in table.rows:
                        for k in range(len(col_keys)):
                            row.cells[k].width = Inches(col_widths[k])
                    for k in range(len(col_keys)):
                        table.columns[k].width = Inches(col_widths[k])
                    
                    run_lab1 = doc.add_paragraph().add_run('')

                    change_orientation()

                # -- Sustainment Funding Source:
                key = 'Sustainment Funding Source'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Funding Table
                num_fund = record['Number of Funding Sources']
                if num_fund > 0:
                    run_lab1 = doc.add_paragraph().add_run('Funding Sources:')
                    run_lab1.font.name = 'Times New Roman'
                    run_lab1.font.size = Pt(11)
                    table2 = doc.add_table(rows=1, cols=4) 
                    row = table2.rows[0].cells 
                    row[0].text = 'Funding Source'
                    row[1].text = 'Funding Start Date'
                    row[2].text = 'Funding End Date'
                    row[3].text = 'Funding Amount per Year ($)'

                    col_dict = {'T3-Funding Source':"string",
                  'T3-Funding Start Date':"string",
                  'T3-Funding End Date':"string",
                  'T3-Funding Amount per Year ($)':"money"
                               }

                    col_keys = list(col_dict.keys())

                    for j in range(num_fund):
                        row = table2.add_row().cells
                        for k in range(len(col_keys)):
                            val = record[col_keys[k]][j]
                            val_frmt = format_values(val, col_dict[col_keys[k]])
                            row[k].text = val_frmt
                    table2.style = 'Light Grid Accent 4'

                    # Set Font Fize
                    for row in table2.rows:
                        for cell in row.cells:
                            paragraphs = cell.paragraphs
                            for paragraph in paragraphs:
                                for run in paragraph.runs:
                                    font = run.font
                                    font.size= Pt(10)
                                    font.name = 'Times New Roman'
                                    
                    run_lab1 = doc.add_paragraph().add_run('')

                # HEADER: Current Mission/Project Utilization
                run_lab1 = doc.add_paragraph().add_run('Current Mission/Project Utilization')
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # Project Table
                num_proj = record['Number of Projects']

                if num_proj > 0:
                    run_lab1 = doc.add_paragraph().add_run('Projects:')
                    run_lab1.font.name = 'Times New Roman'
                    run_lab1.font.size = Pt(11)
                    table3 = doc.add_table(rows=1, cols=5) 
                    row = table3.rows[0].cells 
                    row[0].text = 'Mission/Project Name'
                    row[1].text = 'WBS Number'
                    row[2].text = 'Project Use (%)'
                    row[3].text = 'Risk to Project'
                    row[4].text = 'Impact if Laboratory/Capability is Lost'

                    col_dict = {
                        'T4-Mission/Project Name':"string",
                  'T4-WBS Number':"WBS",
                  'T4-Project Use (%)':"string",
                  'T4-Risk to Project':"string",
                  'T4-Impact if Laboratory/Capability is Lost':"string"
                    }

                    col_keys = list(col_dict.keys())


                    for j in range(num_proj):
                        row = table3.add_row().cells
                        for k in range(len(col_keys)):
                            val = record[col_keys[k]][j]
                            val_frmt = format_values(val, col_dict[col_keys[k]])
                            row[k].text = val_frmt
                    table3.style = 'Light Grid Accent 4'

                    # Set Font Fize
                    for row in table3.rows:
                        for cell in row.cells:
                            paragraphs = cell.paragraphs
                            for paragraph in paragraphs:
                                for run in paragraph.runs:
                                    font = run.font
                                    font.size= Pt(10)
                                    font.name = 'Times New Roman'

                    # Create Pie Chart
                    labels = []
                    vals = []
                    for j in range(num_proj):
                        try: 
                            float(record[col_keys[2]][j])
                            labels.append(record[col_keys[0]][j])
                            vals.append(float(record[col_keys[2]][j]))
                        except:
                            temp=1

                    if len(vals) > 0 and max(vals) > 0:
                        run_lab1 = doc.add_paragraph().add_run('')
                        fig, ax = plt.subplots()
                        ax.pie(vals, labels=labels, autopct='%1.0f%%')
                        plt.savefig(os.path.join(data_path,'Project_chart_' + str(q)+'.png'))
                        doc.add_picture(os.path.join(data_path,'Project_chart_' + str(q)+'.png'), width=Inches(4), height=Inches(3))

                # HEADER: Utilization History/Impact
                run_lab1 = doc.add_paragraph().add_run('Utilization History/Impact')
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # -- History of capability utilization
                key = 'History of capability utilization'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Major impact and contributions this capability has made possible:
                key = 'Major impact and contributions this capability has made possible'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Overall impact of laboratory/capability is lost:
                key = 'Overall impact of laboratory/capability is lost'
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + record[key])
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # HEADER: History of Down Time Due to Maintenance or Failure
                run_lab1 = doc.add_paragraph().add_run('History of Down Time Due to Maintenance or Failure')
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # -- Read Down Time Table
                num_dt = record['Number of Failures']
                if num_dt > 0:
                    run_lab1 = doc.add_paragraph().add_run('Previous Laboratory/Asset Failures:')
                    run_lab1.font.name = 'Times New Roman'
                    run_lab1.font.size = Pt(11)
                    table4 = doc.add_table(rows=1, cols=6) 
                    row = table4.rows[0].cells 
                    row[0].text = 'Asset'
                    row[1].text = 'Start Date'
                    row[2].text = 'Time Down'
                    row[3].text = 'Time Down Unit'
                    row[4].text = 'Additional Notes'
                    row[5].text = 'Impact on Mission/Project'

                    col_dict = { 
                  'T5-Asset':"string",
                  'T5-Start Date':"string",
                  'T5-Time Down':"string",
                  'T5-Unit':"string",
                  'T5-Additional Notes':"string",
                  'T5-Impact':"string"
                               }

                    col_keys = list(col_dict.keys())

                    for j in range(num_dt):
                        row = table4.add_row().cells
                        for k in range(len(col_keys)):
                            val = record[col_keys[k]][j]
                            val_frmt = format_values(val, col_dict[col_keys[k]])
                            row[k].text = val_frmt
                    table4.style = 'Light Grid Accent 4'
                    
                    # Set Font Fize
                    for row in table4.rows:
                        for cell in row.cells:
                            paragraphs = cell.paragraphs
                            for paragraph in paragraphs:
                                for run in paragraph.runs:
                                    font = run.font
                                    font.size= Pt(10)
                                    font.name = 'Times New Roman'
                    run_lab1 = doc.add_paragraph().add_run('')

                # HEADER: Cost
                run_lab1 = doc.add_paragraph().add_run('Cost')
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(12)
                run_lab1.bold = True

                # -- Estimated Cost to Replace Entire Laboratory/Capability ($):
                key = 'Estimated Cost to Replace Entire Laboratory/Capability ($)'
                val = record[key]
                val_frmt = format_values(val, "money")
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + val_frmt)
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)
    
        
                # -- Cost of Service Contracts ($):
                key = 'Cost of Service Contracts ($)'
                val = record[key]
                val_frmt = format_values(val, "money")
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + val_frmt)
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)
        
                # -- Annual Cost to Operate and Sustain the Lab ($/yr):
                key = 'Annual Cost to Operate and Sustain the Lab ($/yr)'
                val = record[key]
                val_frmt = format_values(val, "money")
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + val_frmt)
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)
        
                # -- Cost of Service Contracts ($):
                key = 'Incurred Cost For Downtime ($/yr)'
                val = record[key]
                val_frmt = format_values(val, "money")
                run_lab1 = doc.add_paragraph().add_run(key + ': ' + val_frmt)
                run_lab1.font.name = 'Times New Roman'
                run_lab1.font.size = Pt(11)

                # -- Read Divisons Table
                num_div  = record['Number of Divisions (Labor Costs)']
                if num_div > 0:
                    run_lab1 = doc.add_paragraph().add_run('Directorate Labor Division:')
                    run_lab1.font.name = 'Times New Roman'
                    run_lab1.font.size = Pt(11)
                    table = doc.add_table(rows=1, cols=2) 
                    row = table.rows[0].cells 
                    row[0].text = 'Directorate'
                    row[1].text = 'Labor Division (%)'
                    
                    col_dict = {'T6-Directorate':"string",
                  'T6-Labor Cost (%)':"string"
                               }

                    col_keys = list(col_dict.keys())
                    
                    for j in range(num_div):
                        row = table.add_row().cells
                        for k in range(len(col_keys)):
                            val = record[col_keys[k]][j]
                            val_frmt = format_values(val, col_dict[col_keys[k]])
                            row[k].text = val_frmt
                    table.style = 'Light Grid Accent 4'

                    # Set Font Fize
                    for row in table.rows:
                        for cell in row.cells:
                            paragraphs = cell.paragraphs
                            for paragraph in paragraphs:
                                for run in paragraph.runs:
                                    font = run.font
                                    font.size= Pt(10)
                                    font.name = 'Times New Roman'
                                    
                    run_lab1 = doc.add_paragraph().add_run('')

                    # Create Pie Chart
                    labels = []
                    vals = []
                    for j in range(num_div):
                        labels.append(record[col_keys[0]][j])
                        vals.append(float(record[col_keys[1]][j]))

                    run_lab1 = doc.add_paragraph().add_run('')
                    fig, ax = plt.subplots()
                    ax.pie(vals, labels=labels, autopct='%1.0f%%')
                    plt.savefig(os.path.join(data_path,'Labor_chart_' + str(q)+'.png'))
                    doc.add_picture(os.path.join(data_path,'Labor_chart_' + str(q)+'.png'), width=Inches(4), height=Inches(3))

                # Start on New Page
                doc.add_page_break()




    # Save the Document
    doc.save('Lab Data Output.docx')

    import io
    doc_download = doc

    bio = io.BytesIO()
    doc_download.save(bio)
    if doc_download:
        st.download_button(
            label="Download Report",
            data=bio.getvalue(),
            file_name='Lab Data Output.docx',
            mime="docx"
        )
