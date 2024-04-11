import pandas as pd
import json
from constant import File_Path
import os
from datetime import datetime

class createExcel:

    def __init__(self,url : str = None) -> None:
        self.ExcelData = {
            "Title":[],
            "Filename": [],
            "WebsitePageLink":[],
            "WebsitePdfLink":[],
            "DriveLink":[]
        }

        self.url = url

    def create(self) -> None:

        try:
            with open(fr"{File_Path}\temp\tempFinal.json", "r") as read:
                tempFinal = json.load(read)

            with open(fr"{File_Path}\temp\filename.json", "r") as read:
                filename = json.load(read)

            with open(fr"{File_Path}\temp\driveurl.json", "r") as read:
                driveurl = json.load(read)

            for i in range(0,len(filename)):
                self.ExcelData["Title"].append(tempFinal["Titles"][i])
                self.ExcelData["Filename"].append(filename[i])
                self.ExcelData["WebsitePageLink"].append(tempFinal["PageLinks"][i])
                self.ExcelData["WebsitePdfLink"].append(tempFinal["DownloadLink"][i])
                self.ExcelData["DriveLink"].append(driveurl[i])

            # Creating Excel File Name
            excelfilename = "Excel"
            if self.url != None:
                excelfilename = self.url.split("&")
                excelfilename = excelfilename[1].split("=")
                excelfilename = excelfilename[-1]
            
            # Creating Folder to Save Excel Data if folder already exists saving into it
            pf = os.listdir(File_Path)

            if "ExcelSheets" not in pf:
                f = os.path.join(File_Path,"ExcelSheets")
                os.mkdir(f)

            # Getting Current date time to add at the end of the file to avoid same file names
            cd = datetime.now()
            fd = cd.strftime('%Y-%m-%d %H-%M')


            # Creating Datafram to save excel file
            df = pd.DataFrame(self.ExcelData)
            # Saving Excel Data
            print(f"{File_Path}/ExcelSheets/{excelfilename}_{fd}.xlsx")
            df.to_excel(f"{File_Path}/ExcelSheets/{excelfilename}_{fd}.xlsx")

        except Exception as e:
            print(e)


