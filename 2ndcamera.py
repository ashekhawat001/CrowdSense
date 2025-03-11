import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

# This is your second counter variable (initialize it as needed)
import csv
import matplotlib.pyplot as plt
import time
from datetime import datetime 
# Define the CSV filenames
csv1_filename = 'output.csv'
csv2_filename = 'output1.csv'

def read_csv_values(filename):
    """Read all values from the given CSV file and return them as a list."""
    values = []
    try:
        with open(filename, mode='r') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip the header
            next(csvreader)
            for row in csvreader:
                # Assuming the value is in the second column
                values.append(float(row[1]))  # Append each value as a float
    except (FileNotFoundError, IndexError, ValueError) as e:
        print(f"Error reading {filename}: {e}")
    return values  # Return the list of values

def display_difference(stop_event):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_title("Difference between Values")
    ax.set_xlabel("Time")
    ax.set_ylabel("Difference")
    differences = []
    times = []

    while not stop_event.is_set():
        try:
            # Read values from both CSV files
            values1 = read_csv_values('output.csv')
            values2 = read_csv_values('output1.csv')



            if values1 and values2:  # Ensure there are values to compare
                # Get the most recent values
                value1 = values1[-1]  # Last value from output.csv
                value2 = values2[-1]  # Last value from output1.csv

                # Calculate the difference
                difference = value1 - value2
                
                # Store the difference and time
                differences.append(difference)
                current_time = datetime.now().strftime("%H:%M:%S")  # Get current time as a formatted string
                times.append(current_time)  # Append formatted time as x-axis value
                
                # Clear the plot and redraw
                ax.clear()
                line_color = 'blue'  # Default color
                if difference > 10:
                    line_color = 'red'                 
                ax.plot(times, differences, label='number', color=line_color)
                ax.axhline(10, color='red', linestyle='--', label='Threshold (+10)')
                
                ax.legend()
                ax.set_title("Number of people present Inside")
                ax.set_xlabel("Time")
                ax.set_ylabel("Number")
                if len(times) > 10:  # Display up to 10 time labels
                    ax.set_xticks(times[::len(times)//10])  # Show every nth label
                plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

                plt.draw()
                plt.pause(0.5)  # Pause to allow the plot to update
            
        except Exception as e:
            print(f"An error occurred in display_difference: {e}")
            break

    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final plot



if __name__ == "__main__":
    stop_event = threading.Event() 


    script1_thread = threading.Thread(target=run_script, args=("trackingin.py",))
    script2_thread = threading.Thread(target=run_script, args=("trackingout.py",))

    script1_thread.start()
    script2_thread.start()

    display_difference(stop_event)  # Start displaying the difference

    script1_thread.join()  # Wait for script1 to finish
    script2_thread.join()  # Wait for script2 to finish

    stop_event.set() 

    print("Both scripts have finished executing.")