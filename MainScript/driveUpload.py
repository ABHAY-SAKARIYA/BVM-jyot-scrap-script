from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
from constant import File_Path
import json

# For using listdir() 
import os 

class DriveUploader:
    def __init__(self,Path: str, FolderName: str):

        self.path = Path
        self.folder_name = FolderName
        
        


    def upload(self) -> bool:

        try:
            # Below code does the authentication 
            # part of the code 
            gauth = GoogleAuth() 
            
            # Loading credentials if already exists
            gauth.LoadCredentialsFile("credentials.json")
            
            # Checking credentials 

            if gauth.credentials is None:
                gauth.LocalWebserverAuth()      	 
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()


            # Saving Auth Credentials in json file
            gauth.SaveCredentialsFile("credentials.json")
            # Creates local webserver and auto 
            # handles authentication. 
            self.drive = GoogleDrive(gauth) 


            # Creating an list to store the urls of the uploaded files
            Uploaded_url = []


            # Finding the folder in the drive..
            try:
                file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
                for file in file_list:
                    if file["title"] == self.folder_name:
                        print('Saving files to this folder in Drive : FolderName: %s, id: %s' % (file['title'], file['id']))

                        folder = file
                        break
            except Exception as e:
                print(e)
  
            upload_count = 1
            # Saving Data to that folder.
            for x in os.listdir(self.path): 

                try:
                    # First Check if file already exists in drive if yes then do not upload them.
                    file_exists = self.drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false and title='{x}'"}).GetList()

                    if file_exists:
                        print(f"File Already Exists In Google Drive : filename is : {x}")
                        Uploaded_url.append(file_exists[0]["alternateLink"])
                        continue
                    else:
                        # Create and upload drive file to drive
                        f = self.drive.CreateFile({'title': x}) 
                        f.SetContentFile(os.path.join(self.path, x)) 
                        f["parents"] = [{"id" : folder["id"]}]
                        f.Upload()
                        Uploaded_url.append(f["alternateLink"])
                        print(f"{upload_count} file uploaded")

                        f = None
                        upload_count+=1
                except Exception as e:
                    print(e)
                    continue

            with open(rf"{File_Path}\temp\driveurl.json", "a") as writeFile:
                writeFile.write(json.dumps(Uploaded_url,indent=4))
            
        except Exception as e:
            print(e)
