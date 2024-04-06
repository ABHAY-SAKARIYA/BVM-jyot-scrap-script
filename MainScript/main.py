from scrap import BVMScraper
from asyncApp import AsyncRun
from download import DownloadPdfs
from driveUpload import DriveUploader
import time
import os
from constant import File_Path

class Main:

    def __init__(self) -> None:
        pass

    def GetUserInput(self) -> None:
        self.webpage_url = input("Enter The Url: ")
        self.downloadPath = input("Enter The Download Path: ")
        self.driveFolder_name = input("Enter The Google Drive Folder Name To upload Data: ")


    def Runner(self) -> None:

        self.GetUserInput()

        if self.webpage_url == "":
            print("uploading Files to Drive.")

            time.sleep(5)

            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()


        elif "temp.json" in self.webpage_url:
            print("Getting Download link from the Website this will take some time.")

            time.sleep(5)
            
            # ----------------------------------BLOCK-----------------------------------
            asyncrun = AsyncRun()
            asyncrun.run()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Downloading Files from the website..")
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()


        elif "tempFinal.json" in self.webpage_url:
            print("Downloading Files from the website..")
            
            time.sleep(5)
            
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

        else:

            print("Running Program this will take some time Do Not Close this until all finished")
            
            time.sleep(5)
            
            # ----------------------------------BLOCK-----------------------------------
            scrap = BVMScraper(baseUrl=self.webpage_url)
            getData = scrap.getData()
            if getData == False:
                print("Something went wrong in scrap getData function")
                return
            print("successfull get data")
            
            formatHtmltoexcel = scrap.formatHtmltoexcel()
            if formatHtmltoexcel == False:
                print("Something went wrong in scrap formatHtmltoexcel function")
                return
            print("successfull Formated data")
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Getting Download link from the Website this will take some time.")
            # ----------------------------------BLOCK-----------------------------------
            asyncrun = AsyncRun()
            asyncrun.run()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Downloading Files from the website..")
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

       



instance = Main()
instance.Runner()