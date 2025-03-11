import csv
import subprocess


# Define the filenames
csv_filename = 'processed_data/user_data.csv'
config_filename = 'config.py'

# Initialize variables to hold the last row of data
camera_name = ""
camera_location = ""

field_of_view = 0
height=0
entry_exit_point = ""

# Open the CSV file
with open(csv_filename, mode='r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    # Read all rows into a list
    rows = list(csvreader)
    
    # Check if there are any rows
    if rows:
        # Get the last row
        last_row = rows[-1]
        
        # Store the values in variables
        camera_name = "samples/"+last_row['Camera Name']
        camera_location = last_row['Camera Location']
        field_of_view = int(last_row['Field of View'])
        height = int(last_row['Height'])
        entry_exit_point = last_row['Entry/Exit Point']


# Check the conditions
if (camera_location == "Const" and entry_exit_point == "No") or \
    (camera_location == "Out" and field_of_view < 120) :
    

        # Execute main.py
    subprocess.run(['python', 'config.py'])    
    subprocess.run(['C:/Users/ashek/OneDrive/Documents/projects/Crowd-Analysis-main/.venv/Scripts/python.exe', 'main.py'])
elif (camera_location == "Out" and field_of_view > 120 ) :
    subprocess.run(['python', 'config.py']) 
    subprocess.run(['C:/Users/ashek/OneDrive/Documents/projects/Crowd-Analysis-main/.venv/Scripts/python.exe', 'csrnet/run.py'])

elif (camera_location == "Const" and entry_exit_point == "Yes") :
    subprocess.run(['python', '2ndcamera.py'])

# Now you have the values stored in variables
# You can use camera_name, camera_location, crowd_dens ity, field_of_view, and entry_exit_point as needed