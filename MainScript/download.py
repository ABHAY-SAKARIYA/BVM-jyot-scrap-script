import os
import re
import requests
from time import sleep
import json
from constant import File_Path


class DownloadPdfs:

    def __init__(self, downloadPath: str) -> None:
       self.downloadPath = downloadPath
       self.filenameList = []

    def download_file(self,url : str, destination: str) -> bool:
        '''
            Function to handle download of the file and save it to an pdfs file using with open() function in write binary mode..

            return True if download successfull
            return False if download failed
        '''
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            return True
        except:
            return False




    def download(self) -> bool:

        month_dict = {
                    "Jan": "01","Feb": "02","Mar": "03","Apr": "04","May": "05","Jun": "06","Jul": "07","Aug": "08","Sep": "09","Oct": "10","Nov": "11","Dec": "12"
                }

        downlaodCount = 1
        breakcount = 100

        
        try:
            with open(fr"{File_Path}\temp\tempFinal.json","r") as read:
                df = json.load(read)
            


            # Iterate over rows
            for index in range(0,len(df["PageLinks"])):
                url = df['DownloadLink'][index]  # Assuming URLs are in a column named 'DownloadLink'
                Date = df['Date'][index]  # Assuming values from Column Date

                # To Format Date in yyyymmdd format eg 19240121
                date = "".join(Date.split())
                date = date.split("-")
                if len(date) == 3:
                    newDate = f"{date[-1]}{month_dict[date[1]]}{date[0]}"
                elif len(date) == 2:
                    try:
                        newDate = f"{date[-1]}{month_dict[date[0]]}"
                    except:
                        if date[0] == " " & date[-1] == " ":    
                            newDate = f"0"
                elif len(date) == 1:
                    newDate = f"{date[0]}"
                else:
                    newDate = "0"

                # print(newDate)
                    
                # Removing special charaters which are not required..
                title = re.sub(r"[^a-zA-Z0-9\s\u0900-\u097F]","",df['Titles'][index])  # Assuming values from Column Title
                # pdfname = re.sub(r"[^a-zA-Z0-9\s\u0900-\u097F]","",df["Pdfname"][index]) # pdfname 
                pdfname = df["Pdfname"][index]

                # Checking if title is empty or UNSPECIFIED if yes then the filename should be date_pdfname
                # else date_title_pdfname
                if title == "UNSPECIFIED" or title == " ":
                    file_name = f"{downlaodCount}_{newDate}_{pdfname}"
                else:
                    file_name = f"{downlaodCount}_{newDate}_{title}_{pdfname}"


                # If the length of the file_name is more than 200 character then check if pdfname and title is same if yes then use only one among them now im using pdfname.. 
                if len(file_name) >= 200:
                    # this is only the pdfname but this is with removed special characters because title is without specail characters, so that i can compare both title and pdfname
                    testPdfName = re.sub(r"[^a-zA-Z0-9\s\u0900-\u097F]","",df["Pdfname"][index])[0:-3]
                    # print(testPdfName)
                    if testPdfName == title:
                        file_name = f"{downlaodCount}_{newDate}_{pdfname}"
                    else:
                        file_name = f"{downlaodCount}_{newDate}_{pdfname}"


                self.filenameList.append(file_name)

                destination = os.path.join(self.downloadPath, file_name)  # Destination directory
                # print(destination)
                # break

                # Download the file
                isDownloaded = self.download_file(url, destination)

                # If the isDownload is false means that the file is not download so that save details of that file into an logs.txt file
                if isDownloaded == False:
                    with open("Logs.txt","a") as writefile:
                        writefile.write(f"RowNo: {index} --- Title: {title if title == 'UNSPECIFIED' else pdfname} --- Date: {Date} --- FileName: {file_name} --- Url: {url}\n")

                print(downlaodCount)

                # this is to wait for some time after some amount of pdf is downloaded
                if downlaodCount == breakcount:
                    print(F"Total {downlaodCount} Downloaded waiting for 10 sec before moving further!")
                    sleep(10)
                    breakcount += 50



                # Wait until the file is downloaded completely if the isDownloaded is True only
                if isDownloaded:
                    while not os.path.exists(destination):
                        sleep(5)

                sleep(1)
                downlaodCount += 1

            print("Downloads complete!")
            with open(fr"{File_Path}\temp\filename.json","a") as writefile:
                writefile.write(json.dumps(self.filenameList,indent=4))
            return True
            
        except Exception as e:
            print(e)
            return False

            


