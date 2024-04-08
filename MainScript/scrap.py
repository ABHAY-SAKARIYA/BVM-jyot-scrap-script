from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
from constant import File_Path


class BVMScraper:

    def __init__(self,baseUrl) -> None:
        self.baseUrl = baseUrl
        d = "temp"
        p = os.path.join(File_Path,d)
        os.mkdir(p)


    def getData(self) -> bool:
        '''
            ### This Function is to get table records from the Different Webpage and save them in different html file so that later on it can be converted into excel files.
        '''

        try:
            option = webdriver.ChromeOptions()
            
            
            option.add_argument('--log-level=3')
            
            driver = webdriver.Chrome(options=option)
            

            driver.get(self.baseUrl)

            parser = BeautifulSoup(driver.page_source,"html.parser")
            
            for table in parser.select(".table"):
                with open(fr"{File_Path}\temp\temp.html", "a") as writefile:
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

            with open(fr"{File_Path}\temp\temp.html", "r") as read:
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


