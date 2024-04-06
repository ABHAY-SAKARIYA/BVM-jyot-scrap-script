from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 

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

            # Creates local webserver and auto 
            # handles authentication. 
            gauth.LocalWebserverAuth()	 
            self.drive = GoogleDrive(gauth) 


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
  

            # Saving Data to that folder.
            for x in os.listdir(self.path): 

                try:
                    f = self.drive.CreateFile({'title': x}) 
                    f.SetContentFile(os.path.join(self.path, x)) 
                    f["parents"] = [{"id" : folder["id"]}]
                    f.Upload() 

                    f = None
                except Exception as e:
                    print(e)
                    continue
            
        except Exception as e:
            print(e)
