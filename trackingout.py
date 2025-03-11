import numpy as np
import cv2
import csv

from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet

# Initialize counter for people crossing the line
counter = 0
csv2_filename = 'output1.csv'
def get_counter():
    return counter
# Define the reference line's y-coordinate
  # You can adjust this value as needed
# Store previous centroid positions to determine direction
previous_centroids = {}

MIN_CONF=0.85
NMS_THRESH =0.2
def detect_human(net, ln, frame, encoder, tracker, time):
    global counter
    # Get the dimension of the frame
    (frame_height, frame_width) = frame.shape[:2]
    reference_line_y = int(frame_height * 0.7)  
    # Initialize lists needed for detection
    boxes = []
    centroids = []
    confidences = []

    # Construct a blob from the input frame 
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                  swapRB=True, crop=False)

    # Perform forward pass of YOLOv3, output are the boxes and probabilities
    net.setInput(blob)
    layer_outputs = net.forward(ln)

    # For each output
    for output in layer_outputs:
        # For each detection in output 
        for detection in output:
            # Extract the class ID and confidence 
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Class ID for person is 0, check if the confidence meets threshold
            if class_id == 0 and confidence > MIN_CONF:
                # Scale the bounding box coordinates back to the size of the image
                box = detection[0:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (center_x, center_y, width, height) = box.astype("int")
                # Derive the coordinates for the top left corner of the bounding box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                # Add processed results to respective list
                boxes.append([x, y, int(width), int(height)])
                centroids.append((center_x, center_y))
                confidences.append(float(confidence))
    
    # Perform Non-maxima suppression to suppress weak and overlapping boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONF, NMS_THRESH)

    tracked_bboxes = []
    expired = []
    if len(idxs) > 0:
        del_idxs = []
        for i in range(len(boxes)):
            if i not in idxs:
                del_idxs.append(i)
        for i in sorted(del_idxs, reverse=True):
            del boxes[i]
            del centroids[i]
            del confidences[i]

        boxes = np.array(boxes)
        centroids = np.array(centroids)
        confidences = np.array(confidences)
        features = np.array(encoder(frame, boxes))
        detections = [Detection(bbox, score, centroid, feature) for bbox, score, centroid, feature in zip(boxes, scores, centroids, features)]

        tracker.predict()
        expired = tracker.update(detections, time)

        # Obtain info from the tracks
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 5:
                continue 
            
            tracked_bboxes.append(track)
            centroid = track.to_tlbr()  # Get the bounding box for the tracked object
            centroid_position = (int((centroid[0] + centroid[2]) / 2), int((centroid[1] + centroid[3]) / 2))

            # Draw the centroid
            cv2.circle(frame, centroid_position, 5, (0, 255, 0), -1)

            # Determine movement direction
            if track.track_id in previous_centroids:
                previous_centroid = previous_centroids[track.track_id]
                if previous_centroid[1] < reference_line_y and centroid_position[1] >= reference_line_y:
                    counter += +1  # Person crossed upwards
                elif previous_centroid[1] >= reference_line_y and centroid_position[1] < reference_line_y:
                    counter -= 0 # Person crossed downwards

            # Update the previous centroid position
            previous_centroids[track.track_id] = centroid_position
            
            x1, y1, x2, y2 = [int(i) for i in centroid]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Draw the reference line
    cv2.line(frame, (int(0), reference_line_y), (frame_width, reference_line_y), (0, 255, 0), 2)  # Change color to green
    # Display the counter on the frame
    cv2.putText(frame, f'Counter: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    frame = cv2.resize(frame, (640, 360))

    with open(csv2_filename, mode='a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["c2", counter])  # Append the counter value

    return frame, tracked_bboxes, expired

def main(video_path):
    # Load YOLO model
    from config import YOLO_CONFIG
    WEIGHTS_PATH = YOLO_CONFIG["WEIGHTS_PATH"]
    CONFIG_PATH = YOLO_CONFIG["CONFIG_PATH"]
    net = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    max_cosine_distance = 0.5
    nn_budget = None
    cap = cv2.VideoCapture(video_path)
    tracker = Tracker(nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget), max_age=100)

    # Clear the CSV file and write the header
    with open(csv2_filename, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Variable Name', 'Variable Value'])  # Write the header


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        time = cv2.getTickCount() / cv2.getTickFrequency()  # Get current time for tracking
        frame, tracked_bboxes, expired = detect_human(net, ln, frame, encoder, tracker, time)

        # Show the output frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

csv1_filename = 'processed_data/user_data.csv'
camera_name=""
with open(csv1_filename, mode='r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    rows = list(csvreader)
    if rows:
        last_row = rows[-1]
        camera_name = "samples/"+last_row['Exit Camera ID']+".mp4"

video = camera_name

if __name__ == "__main__":
    main(video) # Replace with your video file path