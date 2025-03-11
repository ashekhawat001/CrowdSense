import datetime
import csv

csv_filename = 'processed_data/user_data.csv'
camera_name=""
with open(csv_filename, mode='r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    # Read all rows into a list
    rows = list(csvreader)
    
    # Check if there are any rows
    if rows:
        # Get the last row
        last_row = rows[-1]
        
        # Store the values in variables
        camera_name = "samples/"+last_row['Camera Name']+".mp4"
        

video=camera_name
# Video Path
VIDEO_CONFIG = {
	"VIDEO_CAP" : video,
	"IS_CAM" : False,
	"CAM_APPROX_FPS": 3,
	"HIGH_CAM": True,
	"START_TIME": datetime.datetime(2020, 11, 5, 0, 0, 0, 0)
}

# Load YOLOv3-tiny weights and config
YOLO_CONFIG = {
	"WEIGHTS_PATH" : "YOLOv4-tiny/yolov4-tiny.weights",
	"CONFIG_PATH" : "YOLOv4-tiny/yolov4-tiny.cfg"
}
# Show individuals detected
SHOW_PROCESSING_OUTPUT = True
# Show individuals detected
SHOW_DETECT = True
# Data record
DATA_RECORD = True
# Data record rate (data record per frame)
DATA_RECORD_RATE = 5
# Check for restricted entry
RE_CHECK = False
# Restricted entry time (H:M:S)
RE_START_TIME = datetime.time(0,0,0) 
RE_END_TIME = datetime.time(23,0,0)
# Check for social distance violation
SD_CHECK = False
# Show violation count
SHOW_VIOLATION_COUNT = False
# Show tracking id
SHOW_TRACKING_ID = False
# Threshold for distance violation
SOCIAL_DISTANCE = 50
# Check for abnormal crowd activity
ABNORMAL_CHECK = True
# Min number of people to check for abnormal
ABNORMAL_MIN_PEOPLE = 8
# Abnormal energy level threshold
ABNORMAL_ENERGY = 2000
# Abnormal activity ratio threhold
ABNORMAL_THRESH = 0.65
# Threshold for human detection minumun confindence
MIN_CONF = 0.01
# Threshold for Non-maxima surpression
NMS_THRESH = 0.4
# Resize frame for processing
FRAME_SIZE = 1080
# Tracker max missing age before removing (seconds)
TRACK_MAX_AGE = 5