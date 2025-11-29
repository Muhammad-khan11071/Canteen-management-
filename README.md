Canteen Web App

Welcome to the Canteen Web App repository! This project provides a simple system for managing a daily menu (admin dashboard) and displaying it publicly on a webpage (web server).

 Getting Started--->

To get the project running, follow the instructions below.

Prerequisites

This project is primarily written in Python. Ensure you have Python 3.x installed on your system.
install dependencies i.e: pandas, flask
Installation

Clone the Repository
run this command :
"cd canteen_web"


 System Components

The application is split into two main components: the Admin Dashboard for management and the Web Server for public viewing.

1. Admin Dashboard (Data Management)

This interface is used to manage the master list of food items and set the daily menu.

File to Run: wireframemain.py

Instructions:

Run the main dashboard script from your terminal:

python wireframemain.py


A graphical window (the dashboard) will open.

Access the Master Menu: From the dashboard, you can access the master menu to add, delete, or modify items available in the canteen. This data is typically stored in master_menu.csv.

Update Today's Menu: Use the dashboard to select items from the master menu to create the menu for the current day. This daily menu is likely saved to record.csv.

2. Public Web Server (Daily Menu Display)

This server runs the public-facing website where customers can view the current daily menu.

File to Run: app.py

Instructions:

Run the Python server script from your terminal:

python app.py


The terminal will display a URL (e.g., http://127.0.0.1:5000/).

Open this URL in any web browser to access the index.html page.

On this page, users will see the Today's Menu, which is dynamically loaded by the server using the data you set in the Admin Dashboard (record.csv).

ile Structure & Assets

The main application files (app.py, wireframemain.py, data_handling.py, etc.) are in the root directory.

The HTML file for the public-facing website is located in the templates/ folder: templates/index.html.

Images: All static image assets used by the website are located in the static/images directory.

If you encounter any issues or have suggestions, please open an issue on GitHub!