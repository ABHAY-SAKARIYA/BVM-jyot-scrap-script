from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
from constant import File_Path


class BVMScraper:

    def __init__(self,baseUrl) -> None:
        # Create an Temp Folder If not Exists
        try:
            self.baseUrl = baseUrl
            d = "temp"
            p = os.path.join(File_Path,d)
            os.mkdir(p)
        except:
            # If Temp Folder Exists Delete All the other Files.
            list_of_temp_files = ["temp.html","temp.json","tempFinal.json","filename.json","driveurl.json"]

            for i in list_of_temp_files:
                if os.path.exists(fr"{File_Path}\temp\{i}"):
                    os.remove(fr"{File_Path}\temp\{i}")



    def getData(self) -> bool:
        '''
            ### This Function is to get table records from the Different Webpage and save them in different html file so that later on it can be converted into excel files.
        '''

        try:
            option = webdriver.ChromeOptions()
            
            
            option.add_argument('--log-level=3')
            
            driver = webdriver.Chrome(options=option)
            

            driver.get(self.baseUrl)

            # Waiting till the table appears
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME,"table")))

            parser = BeautifulSoup(driver.page_source,"html.parser")
            
            for table in parser.select(".table"):
                with open(fr"{File_Path}\temp\temp.html", "a",encoding="utf-8") as writefile:
                    writefile.write(table.prettify())
                # print("table for loop")

            return True
    
        except Exception as e:
            return False



    def formatHtmltoexcel(self) -> bool:
        '''
            ## This function is to format and get the required data from different html files and save them to different excel files.

            #### Data required are
            - Date
            - Title
            - Link
        '''
        try:

            with open(fr"{File_Path}\temp\temp.html", "r", encoding="utf-8") as read:
                data = read.read()

            parser = BeautifulSoup(data,"html.parser")

            Data = {"Date":[],"title":[],"link":[]}

            for aTag in parser.select(".table tbody tr td:nth-child(3) a"):
                Data["link"].append(f"http://archives.biharvidhanmandal.in/{aTag.get('href')}")
                
                Data["title"].append(" ".join(aTag.text.split()))

            for d in parser.select(".table tbody tr td:nth-child(2)"):
                Data["Date"].append("".join(d.text.split()))

            with open(fr"{File_Path}\temp\temp.json", "a") as write:
                write.write(json.dumps(Data, indent=4))

            return True
        
        except Exception as e:
            return False


