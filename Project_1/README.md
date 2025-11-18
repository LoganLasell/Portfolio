# Running TheBus Webiste! 🚌
Quinn McHenry, Logan Lasell, Ashley Holen

For our CS 401 Software Engineering and Design Spring 2025 final project, our group decided to create a web based software application which assists the general public in navigating public transportation systems, specifically TheBus on O’ahu. Our website provides a user-friendly and accessible resource for users to quickly and easily find the bus which is that of their best interest. We have three features of the website - locating the buses nearest to you, finding the buses based on address, and finding the nearest bus stops.

Below are the instructions needed to run our website created as our website!

In this assignment, we used Docker to containerize 2 python files, routes.py and test_routes.py. 
When app.py runs, a Flask app starts, allowing for the user to use the API from their local device by URL. 
The test_app.py is used to ensure the accuracy of app.py using pytest. Below are instuctions how to run this webiste on your local device.  

Link to public API from the offical TheBus website: https://hea.thebus.org/api_info.asp

## Before You Begin! 📩
To begin, you are provided with these files in this GitHub Repostitory. Download them all onto your local device - this includes the Dockerfile, two python files, 2 txt files, 7 html files, and the static folder containing the images on our webiste.


![Unknown](https://github.com/user-attachments/assets/fdb25b2b-b803-44d8-bb16-e47aefb3ed5d)


Once Docker is up and running, locate your Terminal and enter the commands below based on your username.


## Building Image from the Dockerfile

Example
```bash
docker build -t llasell/the-bus_website:1.0 -f Dockerfile .
```
Template
```bash
docker build -t <dockerhubusername>/<code>:<version> <dockerfile> . 
```
#

## Running the website on port 5000

Example
```bash
docker run --rm -p 5000:5000 llasell/the-bus_website:1.0
```
Template
```bash
docker run --rm  -p <port> <dockerhubusername>/<code>:<version> 
```

Resulting Output Example (PUT NEW HERE!!)
```bash
* Serving Flask app 'routes'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 828-644-499

#

You are all set, enjoy your ride! 
