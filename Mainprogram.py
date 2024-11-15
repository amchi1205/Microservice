import zmq
import subprocess
import json
import os

# Set up ZeroMQ context and socket to receive requests
context = zmq.Context()
socket = context.socket(zmq.REP)  # Reply socket type
socket.bind("tcp://*:5555")  # Bind to the address to receive requests

while True:
    # Wait for a message from the client (Microservice.py)
    wine_name = socket.recv_string()
    print(f"Received wine name: {wine_name}")

    # Trigger the Vivino API Node.js script with the wine name
    vivino_output_file = "vivino-out.json"
    node_command = f"node vivino.js --name={wine_name} --minPrice=10 --maxPrice=50"  # Modify price ranges as needed

    # Run the command and capture the output
    subprocess.run(node_command, shell=True)

    # Check if the output file exists
    if os.path.exists(vivino_output_file):
        with open(vivino_output_file, "r") as file:
            vivino_data = json.load(file)

            # Check if wines were found in the results
            if "vinos" in vivino_data and len(vivino_data["vinos"]) > 0:
                # If more than 4 wines are returned, send an error asking for more details
                if len(vivino_data["vinos"]) > 4:
                    response = "Error: Too many results found. Please provide more specific wine details in the name."

                else:
                    # Extract information for the first wine
                    wine = vivino_data["vinos"][0]
                    wine_name = wine.get("name", "N/A")
                    wine_thumb = wine.get("thumb", "No image available")
                    wine_link = wine.get("link", "No link available")

                    # Prepare response with wine info
                    response = f"Wine: {wine_name}, Thumbnail: {wine_thumb}, Link: {wine_link}"

            else:
                response = "Error: No results found. Please check the wine name or provide more details."
    else:
        response = "Error: Unable to fetch wine data from Vivino. Please try again."

    # Send the response back to the client (Microservice.py)
    socket.send_string(response)

