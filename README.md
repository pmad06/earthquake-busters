# Name 
Earthquake Risk Guide 
# Description 

Our web application is a tool that helps users learn more about earthquakes, either around their
location, or around the world. The relevant earthquake data is displayed on a map after the user either
inputs the magnitude or the location they are interested in searching. After inputting either a 
magnitude or location, the map zooms into the specific location and the earthquake location has a 
marker, which consists of a popup that includes information about the earthquake's location (city, state),
magnitude, and risk factor. The location and magnitude attributes were pulled directly from the USGS 
earthquakes dataset but the risk factor was manually calculated using the magnitude. Aside from the 
markers, other earthquake data is displayed on the side bar, which contains the earthquake's location, but
with the exact distance it was from a certain city, latitude/longitude, and a more info section which provides
an url to the USGS event page of the current earthquake displayed on the map. The url provides more in
depth information, such as regional information, the opportunity to report the users' experience, and nearby
seismiscity. 

# Installation 

To get the Earthquake Risk Guide running on your local machine, follow these instructions: 


# Usage

**To run our backend server, input these three commands into your terminal:**

**For Linux/Windows**
```bash
cd QuakeWatchWeb       # to switch into our QuakeWatchWeb folder
cd backend             # to switch into our backend folder
python server.py       # to run the backend server
```     
*For MacOS**
```bash
cd QuakeWatchWeb            # to switch into our QuakeWatchWeb folder
cd backend                  # to switch into our backend folder
source venv/bin/activate    # needed on Mac to create a virtual machine environment
python3 server.py           # to run the backend server
```
**To run our frontend server, input these two commands into a new terminal:** 

**For Linux/Windows/MacOS**
```bash 
cd QuakeWatchWeb    to switch into our QuakeWatchWeb folder
npm run dev         to run our react app
```
