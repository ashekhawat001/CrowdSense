import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import csv
import cv2

global second_camera_button
second_camera_button = None  # Initialize it to None or just declare it here

global open_other_window_button  # Declare the Start Monitoring button
open_other_window_button = None

global exit_camera_label,exit_camera_id_entry



def toggle_entry_exit_checkbox():
    # Show or hide the entry/exit checkbox based on the selected camera location
    if camera_location_var.get() == "Const":
        entry_exit_checkbox.pack(anchor=tk.W, pady=5)
    else:
        entry_exit_checkbox.pack_forget()
    
    # Call to update the visibility of the second camera button
    toggle_second_camera_label()

def toggle_second_camera_label():
    global exit_camera_label  # Declare it as global to modify it
    global exit_camera_id_entry  
    # Show or hide the second camera button based on the Entry/Exit checkbox state
    if entry_exit_var.get():
               
        # Show the exit camera details
        exit_camera_label.pack(anchor=tk.W, pady=5, padx=20)
        exit_camera_id_entry.pack(anchor=tk.W, pady=5, padx=30)
    else:
        
        # Hide the exit camera details
        exit_camera_label.pack_forget()
        exit_camera_id_entry.pack_forget()

def save_data_and_monitor(camera_name, camera_location, field_of_view, height, entry_exit):
    exit_camera_id = exit_camera_id_entry.get() if entry_exit_var.get() else ""  # Get exit camera ID if entry/exit is checked
    save_data_to_file(camera_name, camera_location, field_of_view, entry_exit, height,  exit_camera_id)
    print("Data saved and monitoring started.")

def save_data_to_file(camera_name, camera_location, field_of_view, height, entry_exit, exit_camera_id):
    # Open the CSV file in append mode
    with open("processed_data/user_data.csv", "a", newline='') as file:
        writer = csv.writer(file)
        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writerow(["Camera Name", "Camera Location", "Field of View", "Height" , "Entry/Exit Point", "Exit Camera ID"])
        # Write the user data
        writer.writerow([camera_name, camera_location, field_of_view, height, 'Yes' if entry_exit else 'No', exit_camera_id])
def open_second_camera():
    # Close the current window
    root.destroy()
    # Open the second camera window
    subprocess.Popen(['python', '2ndcamera.py'])

def go_to_next(event):
    go_to_next_screen()

def on_canvas_enter(event):
    # Change the color when mouse enters
    canvas.itemconfig(button, fill='white', outline='#22C55E')
    canvas.itemconfig(text, fill="#22C55E")


def on_canvas_leave(event):
    # Change the color back when mouse leaves
    canvas.itemconfig(button, fill='#22C55E', outline='white')
    canvas.itemconfig(text,  fill="white")


def go_to_next_screen():



 # Declare it as global to modify it
    global open_other_window_button  
    global exit_camera_label, exit_camera_id_entry  # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()
    
    logo_image = Image.open("assets/horizlogo1.png")  # Replace with the path to your logo image
    #logo_image = logo_image.resize((50, 50), Image.LANCZOS)  # Resize the logo if needed  # Resize the logo if needed  # Resize the logo if needed
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    logo_label = tk.Label(root, image=logo_photo, bg='white')  # Create a label for the logo
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)  # Pack the logo to the top left


# Create a label for the camera name
    camera_name_label = tk.Label(root, text="Camera Id:", font=("Poppins", 14,"normal"), bg='white',fg='#252B41')
    camera_name_label.pack(anchor=tk.W, pady=5, padx=20)
    camera_name_entry = tk.Entry(root,bg='#e3e3e6')
    camera_name_entry.pack(anchor=tk.W, pady=5, padx=30)

# Frame for Camera Location
    location_frame = tk.Frame(root, bg='white')
    location_frame.pack(anchor=tk.W, pady=5, padx=20)

    location_label = tk.Label(location_frame, text="Camera Location:", font=("Poppins", 14), bg='white',fg='#252B41')
    location_label.pack(side=tk.TOP, anchor=tk.W)

    global camera_location_var
    camera_location_var = tk.StringVar(value=None)  # No default selection

    # Pack radio buttons horizontally for Camera Location
    outdoors_radio = tk.Radiobutton(location_frame,font=("Poppins", 12), bg='white', fg='#47474a', text="Outdoors/Unconstrained movement", variable=camera_location_var, value="Out", command=toggle_entry_exit_checkbox)
    outdoors_radio.pack(side=tk.LEFT, padx=10)
    constricted_radio = tk.Radiobutton(location_frame,font=("Poppins", 12), bg='white',fg='#47474a',  text="Restrictive movement/Choke Point", variable=camera_location_var, value="Const", command=toggle_entry_exit_checkbox)
    constricted_radio.pack(side=tk.LEFT, padx=10)

    # Frame for Field of View
    fov_frame = tk.Frame(root, bg='white')
    fov_frame.pack(anchor=tk.W, pady=5, padx=20)

    fov_label = tk.Label(fov_frame, text="Field of View:", font=("Poppins", 14), bg='white', fg='#252B41')
    fov_label.pack(side=tk.TOP, anchor=tk.W)

    global fov_scale
    fov_scale = tk.Scale(fov_frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300, bg='white', fg='#47474a', font=("Poppins", 12))
    fov_scale.pack(side=tk.LEFT, padx=10)

    # Create a label to display the selected FOV value
    fov_value_label = tk.Label(fov_frame, text="0", font=("Poppins", 12), bg='white', fg='#47474a')
    fov_value_label.pack(side=tk.LEFT, padx=10)
    # Function to update the FOV value label
    def update_fov_value(event):
        fov_value_label.config(text=str(fov_scale.get()))

    # Bind the slider movement to the update function
    fov_scale.bind("<Motion>", update_fov_value)
    # Frame for Mounting Height
    height_frame = tk.Frame(root, bg='white')
    height_frame.pack(anchor=tk.W, pady=5, padx=20)

    height_label = tk.Label(height_frame, text="Mounting Height (meters):", font=("Poppins", 14), bg='white', fg='#252B41')
    height_label.pack(side=tk.TOP, anchor=tk.W)

    # Create a Scale widget for Mounting Height input
    global height_scale
    height_scale = tk.Scale(height_frame, from_=0, to=10, orient=tk.HORIZONTAL, length=300, bg='white', fg='#47474a', font=("Poppins", 12))
    height_scale.pack(side=tk.LEFT, padx=10)

    # Create a label to display the selected Mounting Height value
    height_value_label = tk.Label(height_frame, text="0", font=("Poppins", 12), bg='white', fg='#47474a')
    height_value_label.pack(side=tk.LEFT, padx=10)

    # Function to update the Mounting Height value label
    def update_height_value(event):
        height_value_label.config(text=str(height_scale.get()))

    # Bind the slider movement to the update function for height
    height_scale.bind("<Motion>", update_height_value)

    # Checkbox for Entry/Exit point
    global entry_exit_var
    entry_exit_var = tk.BooleanVar()  # Variable to hold the state of the checkbox
    global entry_exit_checkbox
    entry_exit_checkbox = tk.Checkbutton(root, text="Entry/Exit point?", variable=entry_exit_var, font=("Poppins", 14), bg='white' ,padx=20, fg='#252B41')
    
    # Update the checkbox to call toggle_second_camera_button when clicked
    entry_exit_checkbox.config(command=toggle_second_camera_label)
    # Initialize exit_camera_label and exit_camera_id_entry
    global exit_camera_label, exit_camera_id_entry
    exit_camera_label = tk.Label(root, text="Exit Camera ID:", font=("Poppins", 14), bg='white', fg='#252B41')
    exit_camera_id_entry = tk.Entry(root,bg='#e3e3e6')

    # Call the function to toggle the second camera label based on the checkbox state
    toggle_second_camera_label()
    # Update the checkbox to call toggle_second_camera_button when clicked
    entry_exit_checkbox.config(command=toggle_second_camera_label)

    # Initialize the exit camera label and entry as hidden
    exit_camera_label.pack_forget()
    exit_camera_id_entry.pack_forget()
    # Create the Start Monitoring button (initially not packed)
    open_other_window_button = tk.Button(root, text="Start Monitoring", command=lambda: [save_data_and_monitor(camera_name_entry.get(), camera_location_var.get(), fov_scale.get(), height_scale.get(), entry_exit_var.get(), exit_camera_id_entry.get()), open_other_window()])
    open_other_window_button.pack(side=tk.BOTTOM, pady=30)  # Pack at the bottom with padding

    toggle_entry_exit_checkbox()
    # Call the function to show or hide the checkbox initially
    toggle_entry_exit_checkbox()
    

def save_data_and_monitor(camera_name, camera_location, field_of_view, height, entry_exit, exit_camera_id):
    save_data_to_file(camera_name, camera_location, field_of_view, height, entry_exit, exit_camera_id)
    # Here you can add the code to start monitoring or open another window
    print("Data saved and monitoring started.") 


def open_other_window():
    # Close the current window
    root.destroy()
    # Open the other Python file
    subprocess.Popen(["python", "norm_exec.py"])  # Adjust the command as necessary for your environment


class VideoPlayer:
    def __init__(self, label, video_path):
        self.label = label
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame = cv2.resize(frame, (200, 200))
            frame = Image.fromarray(frame)  # Convert to PIL Image
            frame = ImageTk.PhotoImage(frame)  # Convert to PhotoImage
            self.label.config(image=frame)
            self.label.image = frame  # Keep a reference to avoid garbage collection
            self.label.after(30, self.update_frame)  # Update every 30 ms
        else:
            self.cap.release()  # Release the video capture when done

# Create the main window
root = tk.Tk()
root.title("CrowdSense")
root.geometry("960x740")  # Increased height to accommodate the logo
root.configure(bg='white')  # Increased height to accommodate the logo

# Load the logo image
video_label = tk.Label(root,bd=0, highlightthickness=0)
video_label.pack(pady=10)

# Initialize the video player with the path to your MP4 file
video_player = VideoPlayer(video_label, "assets/videologo.mp4")  # Replace with your MP4 file path

# Create the welcome label
welcome_label = tk.Label(root, text="Welcome to CrowdSense !!", font=("Poppins", 20), bg='white', fg='#252B41')
welcome_label.pack(pady=40)


canvas = tk.Canvas(root, width=100, height=50, bg='white')
canvas.pack()


# Draw the main button
button = canvas.create_rectangle(3, 3, 101, 51, fill='#22C55E', outline='white', width=2)
text = canvas.create_text(52.5, 27, text="NEXT", font=("Poppins", 16), fill="white")
# Bind the click event to the button
canvas.bind('<Button-1>', go_to_next)

# Bind hover events to change color
canvas.bind('<Enter>', on_canvas_enter)
canvas.bind('<Leave>', on_canvas_leave)

# Create the next button
""" next_button = tk.Button(root, text="Next", font=("Poppins", 12), bg='#ececec', fg='#252B41', command=go_to_next_screen)
next_button.pack( pady=10) """

# Start the Tkinter event loop
root.mainloop()