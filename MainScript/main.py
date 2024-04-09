from scrap import BVMScraper
from asyncApp import AsyncRun
from download import DownloadPdfs
from createExcel import createExcel
from driveUpload import DriveUploader
import time
import os
from constant import File_Path

class Main:

    def __init__(self) -> None:
        pass

    def GetUserInput(self) -> None:
        self.webpage_url = input("Enter The Url: ")
        if self.webpage_url == "excel":
            return
        self.downloadPath = input("Enter The Download Path: ")
        self.driveFolder_name = input("Enter The Google Drive Folder Name To upload Data: ")


    def Runner(self) -> None:

        self.GetUserInput()

        if self.webpage_url == "excel":
            print("Saving Excel File.")
            # ----------------------------------BLOCK-----------------------------------

            excel = createExcel()
            excel.create()
            print("Saved succesfull")

            # --------------------------------------------------------------------------

        elif self.webpage_url == "":
            print("Last Step : uploading Files to Drive.")

            time.sleep(5)

            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

            print("Files Uploaded TO Drive")

            time.sleep(10)

            print("Saving Excel File.")
            # ----------------------------------BLOCK-----------------------------------

            excel = createExcel()
            excel.create()
            print("Saved succesfull")

            # --------------------------------------------------------------------------


        elif "temp.json" in self.webpage_url:
            print("Step 2: Getting Download link from the Website this will take some time.")

            time.sleep(5)
            
            # ----------------------------------BLOCK-----------------------------------
            asyncrun = AsyncRun()
            asyncrun.run()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Step 3: Downloading Files from the website..")
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("last Step : uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

            print("Files Uploaded TO Drive")

            time.sleep(10)

            print("Saving Excel File.")
            # ----------------------------------BLOCK-----------------------------------

            excel = createExcel()
            excel.create()
            print("Saved succesfull")

            # --------------------------------------------------------------------------



        elif "tempFinal.json" in self.webpage_url:
            print("Step 3: Downloading Files from the website..")
            
            time.sleep(5)
            
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Last Step : uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

            print("Files Uploaded TO Drive")

            time.sleep(10)

            print("Saving Excel File.")
            # ----------------------------------BLOCK-----------------------------------

            excel = createExcel()
            excel.create()
            print("Saved succesfull")

            # --------------------------------------------------------------------------


        else:

            print("Step 1: Running Program this will take some time Do Not Close this until all finished")
            
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

            print("Step 2: Getting Download link from the Website this will take some time.")
            # ----------------------------------BLOCK-----------------------------------
            asyncrun = AsyncRun()
            asyncrun.run()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Step 3: Downloading Files from the website..")
            # ----------------------------------BLOCK-----------------------------------
            downloading = DownloadPdfs(downloadPath=self.downloadPath)
            downloading.download()
            # --------------------------------------------------------------------------

            time.sleep(10)

            print("Last Step: uploading Files to Drive.")
            # ----------------------------------BLOCK-----------------------------------
            dupload = DriveUploader(Path=self.downloadPath,FolderName=self.driveFolder_name)
            dupload.upload()

            print("Files Uploaded TO Drive")
            # --------------------------------------------------------------------------
            time.sleep(10)

            print("Saving Excel File.")
            # ----------------------------------BLOCK-----------------------------------

            excel = createExcel(url=self.webpage_url)
            excel.create()
            print("Saved succesfull")

            # --------------------------------------------------------------------------

       



instance = Main()
instance.Runner()