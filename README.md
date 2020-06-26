## DriveAPI

This program was written to perform google drive cloud storage management operations.
Its functionality focuses more on excel and google sheets file format
Please consult the "help" option of the program for some assistance on how to invoke
the various operations and their commands that the program has to offer.

Take note of the following key words that can be invoked to create different file types
in the program
- folder    --> folder item (create command only)
- excel_gs  --> google sheet files (create command only)
- excel_ms  --> microsoft .xlsx excel file (upload command only)
- txt       --> text files (create command only)
- doc       --> google doc (create command only)

Google sheet files will be downloaded as ms excel files by default

# Set Up
- Use the email address for the google drive you wish to connect the api to to create a
  google cloud platform account if you dont have one yet
- Create a new project for this program
- Navigate to APIs & Services then click +ENABLE APIS AND SERVICES
- Search for Google Drive API and click then Enable API
- Navigate back to APIs & Services page and click on Credentials
- Then click +CREATE CREDENTIALS then OAuth Client ID
- Then fill the form like so:
  - Application type = Web application
  - Name             = <anything you want>
- Click Create
- You should get a pop up with client id, ignore
- You should be on the Credentials page now and will see yout newly created credential
  under OAuth 2.0 Client IDs
- Download your credentials file with the download icon on the far right

- Rename the json credentials file as client_secrets and place it in the program folder
- Create an virtual environment in this folder with python3.6
- Install the python libraries from requirements.txt

- Run the quickstart_googledriveapi.py first
- It should give you a url to go to if it doesnt directly open the webpage immediately
- choose your account and allow access
- Then run the DriveAPI_Functions.py with the list argument
- You might be requested to allow access again but after doing so, you should see the list 
  of your google drive files in the terminal

# Dont hesitate to holla at me if you encounter any problems

