from __future__ import print_function
import httplib2
import os
import io
import glob
import auth
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    import argparse
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds',
SCOPES = [
	'https://www.googleapis.com/auth/drive',
	'https://www.googleapis.com/auth/drive.file',
	'https://www.googleapis.com/auth/drive.metadata',
	'https://www.googleapis.com/auth/drive.appdata',
	]
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

auth_Inst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = auth_Inst.get_credentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

mimeType = {
	'folder': 'application/vnd.google-apps.folder',
	'excel_gs': 'application/vnd.google-apps.spreadsheet',
	'excel_ms': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
	'txt': 'text/plain',
	'text': 'text/plain',
	'doc': 'application/vnd.google-apps.document',
}

downloads_dir = 'downloads_dir/'
SPREADSHEET_DRIVE_URL = "https://docs.google.com/spreadsheets/d/"


class DriveAPI_Functions:

	def __init__(self,command,args_list=[]):

		if (command=="help"):
			if not args_list:
				print("Here are the possible commands for this program")
				print(" [1.] help	- recieves 1 argument to print a list of the possile commands")
				print(" 		like so: python DriveAPI_Functions.py help\n")

				print(" [2.] list	- recieves 1 argument to print all the files and folders in google drive")
				print(" 		like so: python DriveAPI_Functions.py list\n")

				print(" [3.] search	- recieves 2 arguments to search for a file or folder in google drive")
				print(" 		like so: python DriveAPI_Functions.py search README\n")

				print(" [4.] create	- recieves 3 arguments to create a file or folder in google drive")
				print(" 		like so: python DriveAPI_Functions.py create excel_ms HelloWorld")
				print(" 		like so: python DriveAPI_Functions.py create excel_gs HelloWorld\n")

				print(" [5.] delete	- recieves 2 arguments to permanently delete a file or folder from google drive (non-recorverable)")
				print(" 		like so: python DriveAPI_Functions.py delete HelloWorld\n")

				print(" [6.] rename	- recieves 3 arguments to rename a file or folder in google drive")
				print(" 		like so: python DriveAPI_Functions.py rename HelloWorld Hello_NewWorld\n")

				print(" [7.] move	- recieves 3 arguments to move a file or folder to another existing folder in google drive")
				print(" 		like so: python DriveAPI_Functions.py move Hello_NewWorld New_Folder\n")

				print(" [8.] upload	- recieves 3 arguments to upload a given file in google drive")
				print(" 		like so: python DriveAPI_Functions.py upload excel_ms newExcel_sheet\n")

				print(" [9.] duplicate	- recieves 3 arguments to duplicate a given file in google drive")
				print(" 		like so: python DriveAPI_Functions.py duplicate newExcel_sheet newExcel_sheet_name\n")

				print(" [10.] download	- recieves 2 arguments to download a googlesheet file in google drive")
				print(" 		like so: python DriveAPI_Functions.py download googlesheet_file\n")

				print(" [11.] get_url	- recieves 2 arguments to echo the url of a googlesheet file in google drive into the url .txt file")
				print(" 		like so: python DriveAPI_Functions.py get_url googlesheet_file\n")

				print(" [12.] change_permission	- recieves 2 arguments to change the document permission to 'anyone with link can edit'")
				print(" 		like so: python DriveAPI_Functions.py change_permission googlesheet_file\n")
			else:
				print("help command requires no other arguments, it recieved ", len(args_list))

		elif (command=="list"): # TESTED
			if not args_list:
				self.list_files()
			else:
				print("list command requires no other arguments, it recieved ", len(args_list))

		elif (command=="search"): # TESTED
			if len(args_list)==1:
				self.searchFile(10,("name='%s'" % args_list[0]))
			else:
				print("search command requires 1 other argument, it recieved ", len(args_list))

		elif (command=="create"): # TESTED
			if len(args_list)==2:
				mime = mimeType[(args_list[0]).lower()]
				self.createItem(args_list[1],mime)
			else:
				print("create command requires 2 other arguments, it recieved ", len(args_list))

		elif (command=="delete"): # TESTED
			if len(args_list)==1:
				self.del_filefolder(args_list[0])
			else:
				print("delete command requires 1 other argument. it recieved ", len(args_list))

		elif (command=="rename"): # TESTED
			if len(args_list)==2:
				self.renameFile(args_list[0],args_list[1])
			else:
				print("rename command requires 2 arguments. it recieved ", len(args_list))

		elif (command=="move"): # TESTED
			if len(args_list)==2:
				self.insert_file_into_folder(args_list[0], args_list[1])
			else:
				print("move command requires 2 arguments. it recieved ", len(args_list))

		elif (command=='download'):
			if len(args_list)==1:
				mime = mimeType['excel_ms']
				# mime = mimeType[(args_list[0]).lower()]
				# print(mime)
				self.downloadFile(args_list[0],mime)
			else:
				print("download command requires 1 arguments. it recieved ", len(args_list))

		elif (command=='upload'): # TESTED
			if len(args_list)==3:
				mime = mimeType['excel_ms']

				if args_list[1] not in args_list[2]:
					# full_path = args_list[2] + '\\' + args_list[1]
					full_path = args_list[2] + '/' + args_list[1] # for ubuntu
				else:
					full_path = args_list[2]

				# print(full_path)
				self.uploadFile(args_list[1],full_path,mime)
			else:
				print("upload command requires 2 arguments. it recieved ", len(args_list))

		elif (command=='duplicate'): # TESTED
			if len(args_list)==2:
				self.duplicateFile(args_list[0],args_list[1])
			else:
				print("duplicate command requires 2 arguments. it recieved ", len(args_list))

		elif (command=='get_url'): # TESTED
			if len(args_list)==1:
				self.get_url(args_list[0])
			else:
				print("get_url command requires 1 arguments. it recieved ", len(args_list))

		elif (command=='change_permission'): 
			if len(args_list)==1:
				self.permission_swt(args_list[0])
			else:
				print("change_permission command requires 1 arguments. it recieved ", len(args_list))
		else:
			print(command, " is not a valid command. seek help with: python DriveAPI_Functions.py help")


	def list_files(self):
	    # Call the google drive api files().list() method to list all the files and folder
	    # within google drive
	    results = drive_service.files().list(
	        pageSize=10,fields="nextPageToken, files(id, name)").execute()
	    # Extract the file properties with the get() method
	    items = results.get('files', [])
	    # Print the results
	    if not items:
	        print('No files found.')
	    else:
	        print('Files:')
	        # Print the file name and id for each file found
	        for item in items:
	            print('{0} ({1})'.format(item['name'], item['id']))

	def searchFile(self,size,query):
		# Call the google drive api files().list() method with query parameter to specify
		# the exact file property to look for
	    results = drive_service.files().list(
	    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
	    items = results.get('files', [])
	    if not items:
	        print('No files found.')
	        exit()
	        return 0
	    else:
	        print('Files:')
	        for item in items:
	            # print(item)
	            print('{0} ({1})'.format(item['name'], item['id']))
	        return items


	def createItem(self,name,mime):
		# Define the folder metadata: name and folder mimeType
	    file_metadata = {
	    'name': name,
	    # 'mimeType': 'application/vnd.google-apps.folder'
	    'mimeType': mime
	    }
	    # Call the google drive api files().create() method to create the folder
	    file = drive_service.files().create(body=file_metadata,
	                                        fields='id').execute()
	    print ('Created Item: %s, with item id: %s' % (name, file.get('id')))

	def insert_file_into_folder(self,file_name,folder_name):

		search_names = [file_name,folder_name]
		search_ids = []
		for i in range(len(search_names)):
			# Use search to get file and folder ids
			item = self.searchFile(10,("name='%s'" % search_names[i]))
			if (item==0 | len(item)>1):
				if (len(item)>1):
					if i==0:
						print("More than one iten found with the name: %s" % file_name)
					else:
						print("More than one file found with the name: %s" % folder_name)

				exit()
			else:
				search_ids.append(item[0]['id'])

		file_id = search_ids[0]
		folder_id = search_ids[1]

		# Retrieve the file to be moved using its unique file id
		file = drive_service.files().get(fileId=file_id, fields='parents').execute()
		# Retrieve the existing parents to remove
		previous_parents = ",".join(file.get('parents'))
		# Move the file to the new folder with the update() method
		file = drive_service.files().update(fileId=file_id,
			addParents=folder_id,
			removeParents=previous_parents,
			fields='id, parents').execute()

	def duplicateFile(self,file_name, newFile_name):
		# Use search to get file id
		item = self.searchFile(10,("name='%s'" % file_name))
		if (item==0 | len(item)>1):
			if (len(item)>1):
				print("More than one file found with the name: %s" % file_name)
			exit()

		file_id = item[0]['id']

		# Call the google drive api files().copy() method to duplicate the file specified
		# by the unique file id
		copy = (
			drive_service.files().copy(
				fileId=file_id, body={"title": "copiedFile"}).execute()
			)
		# Define the file metadata: name
		metadata = {'name': newFile_name}
		# Get the copied file's file id using the .get('id') method
		copied_file_id = copy.get("id")
		# Call the google drive api files().update() method to rename the duplicated file, 
		# new name defined in the metadata
		drive_service.files().update(
			fileId=copied_file_id,
			body=metadata).execute()
		print(file_name, " duplicated and saved as ", newFile_name)
		# Call the insert_file_into_folder function to move the renamed copied file to a new folder
		return copied_file_id

	def existinList(self,List,target):
		# Loop through the elements in the provided list to find the specified element in target
		for elem in List:
			# if found, return True to indicate that the target exists in the list
			if elem==target:
				return True
		# else, return False to specify the target does not exist in the list
		return False


	def downloadFile(self,file_name,mimetype):
		# Use search to get file id
		item = self.searchFile(10,("name='%s'" % file_name))
		if (item==0 | len(item)>1):
			if (len(item)>1):
				print("More than one file found with the name: %s" % file_name)
			exit()

		file_id = item[0]['id']
		# Call the google drive api files().export_media() to retrieve a file specified by its
		# file id and mimeType
		request = drive_service.files().export_media(fileId=file_id,mimeType=mimetype)
		# Allocate some ram space for the binary file to be downloaded
		fh = io.BytesIO()
		# Setup a MediaIoBaseDownload method downloader with the file to download (request) and
		# the download location (fh)
		downloader = MediaIoBaseDownload(fh, request)
		done = False
		# Call the next_chunk() downloader method to download the binary file one chunk at a time
		# until the done == True
		while done is False:
			status, done = downloader.next_chunk()
			print("Download %d%%." % int(status.progress() * 100))

		# save the file into the specified file path

		if '.xlsx' not in file_name:
			file_name_n_ext = file_name+'.xlsx'
		else:
			file_name_n_ext = file_name

		with io.open(downloads_dir+file_name_n_ext,'wb') as f:
			# Call the seek(0) method to find the absolute position of the allocated ram space
			# where the file was downloaded
			fh.seek(0)
			# Read the binary file from the ram space, then write the file into the specified
			# file path
			f.write(fh.read())

	def del_filefolder(self,file_name):
	  # Use search to get file id
	  item = self.searchFile(10,("name='%s'" % file_name))
	  if (item==0 | len(item)>1):
	  	if (len(item)>1):
	  		print("More than one file found with the name: %s" % file_name)
	  	exit()

	  # print(item[0])
	  # print('{0} ({1})'.format(item['name'], item['id']))

	  file_id = item[0]['id']
	  # print(file_id)

	  try:
	    drive_service.files().delete(fileId=file_id).execute()
	    print("%s with id %s deleted!" % (file_name, file_id))
	  except(errors.HttpError, errors):
	    print('An error occurred: %s' % errors)
	    os.remove(f)

	def renameFile(self,file_name,newFile_name):
		# Use search to get file id
		item = self.searchFile(10,("name='%s'" % file_name))
		if (item==0 | len(item)>1):
			if (len(item)>1):
				print("More than one file found with the name: %s" % file_name)
			exit()

		file_id = item[0]['id']

		# Call the google drive api files().update() method to rename the duplicated file, 
		# new name defined in the metadata
		metadata = {'name': newFile_name}
		drive_service.files().update(
			fileId=file_id,
			body=metadata).execute()
		print(file_name, " --> ", newFile_name, ". Renaming successful!")

	def uploadFile(self,file_name,file_path,mime):
	    file_metadata = {'name': file_name}
	    media = MediaFileUpload(file_path,
	                            mimetype=mime)
	    file = drive_service.files().create(body=file_metadata,
	                                        media_body=media,
	                                        fields='id').execute()

	    file['mimeType'] = mimeType['excel_gs'] #'mimeType': new_mime_type} 
	    print(mimeType['excel_gs'])

	    file_c = self.excel_ms_2_gs(file.get('id'))

	    print('File name: %s and ID: %s' % (file_c.get('name'), file_c.get('id')))

	def excel_ms_2_gs(self,file_id):

		metadata = {'mimeType': mimeType['excel_gs']}
		file = drive_service.files().copy(body=metadata, fileId=file_id).execute()
		try:
			drive_service.files().delete(fileId=file_id).execute()

		except(errors.HttpError, errors):
			print('An error occurred: %s' % errors)
			os.remove(f)

		return file

	def get_url(self,file_name):

		file = self.searchFile(10,("name='%s'" % file_name))
		if len(file)==1:
			url_file = open('url.txt','w')
			url_file.write(SPREADSHEET_DRIVE_URL+file[0]['id'])

		else:
			print("More than one item with the name: %s was found" % file_name)

	def permission_swt(self,file_name):
		file = self.searchFile(10,("name='%s'" % file_name))
		if len(file)==1:
			new_permission = {
			  # 'value': value,
			  'type': 'anyone',
			  'role': 'writer'
			}
			drive_service.permissions().create(fileId=file[0]['id'], body=new_permission).execute()
			print("Privacy for file %s toggled to 'anyone with link can edit'" % file_name)
		else:
			print("More than one item with the name: %s was found" % file_name)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    # DriveAPI_Functions(*sys.argv[1:])
    DriveAPI_Functions(sys.argv[1:][0], sys.argv[1:][1:])

# DriveAPI_Functions("list")
# DriveAPI_Functions("search",['Udacity CV.docx'])
# DriveAPI_Functions('upload',['excel', 'tmnt.xlsx', 'tmnt.xlsx'])
# DriveAPI_Functions.uploadFile('tmnt.xlsx','C:\\Users\\User\\Documents\\GitHub\\API_Dev\\DriveAPI\\tmnt.xlsx',mimeType['excel_ms'])
# DriveAPI_Functions.excel_ms_2_gs('1ssCZuyEXRPyCM1de8vUwRphkYPX2aLuR')
# file = DriveAPI_Functions.searchFile(10,"name='tmnt'")
# print(file)
