from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from ascraper.ascraper import File
import pandas as pd
import requests as re


class BVMScraper:

    def __init__(self) -> None:
        self.pageStart = 0
        self.pageEnd = 200000
        self.recordsPerPage = 10000
        self.maxHtmlFiles = 21
        self.baseUrl = f"http://archives.biharvidhanmandal.in/jspui/simple-search?query=&sort_by=dc.date.issued_dt&order=asc&rpp=10000&etal=0&start=0"


    def getData(self) -> None:
        '''
            ### This Function is to get table records from the Different Webpage and save them in different html file so that later on it can be converted into excel files.
        '''


        option = webdriver.ChromeOptions()
        
        pref = {
        'download.default_directory':r"D:\Abhay\bihar vidhan mandal scraping jyot",
        'safebrowsing.enabled':'false',
        'plugins.always_open_pdf_externally':True
        }
        
        option.add_experimental_option('prefs',pref)
        
        option.add_argument('--log-level=3')
        
        driver = webdriver.Chrome(options=option)
        
        checkOne = 0
        fileCount = 1

        while self.pageStart <= self.pageEnd:

            driver.get(f"http://archives.biharvidhanmandal.in/jspui/simple-search?query=&sort_by=dc.date.issued_dt&order=asc&rpp=10000&etal=0&start={self.pageStart}")

            parser = BeautifulSoup(driver.page_source,"html.parser")
            
            for table in parser.select(".table"):
                File.Html.write(f"data{fileCount}.html",table.prettify())
                # print("table for loop")

            if checkOne < 1:
                if self.pageStart == 0:
                    self.pageStart = 0
                    checkOne += 1
                    # print("Checkone if if")
                    continue
            
            
            fileCount += 1
            self.pageStart += self.recordsPerPage


    def formatHtmltoexcel(self):
        '''
            ## This function is to format and get the required data from different html files and save them to different excel files.

            #### Data required are
            - Date
            - Title
            - Link
        '''

        count = 11

        month_dict = {
                "Jan": "01",
                "Feb": "02",
                "Mar": "03",
                "Apr": "04",
                "May": "05",
                "Jun": "06",
                "Jul": "07",
                "Aug": "08",
                "Sep": "09",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12"
            }
        

        while count <= self.maxHtmlFiles:

            data = File.Html.read(filename=fr"htmldata\data{count}.html")

            parser = BeautifulSoup(data,"html.parser")

            Data = {"Date":[],"title":[],"link":[]}

            for aTag in parser.select(".table tbody tr td:nth-child(3) a"):
                Data["link"].append(f"http://archives.biharvidhanmandal.in/{aTag.get('href')}")
                
                Data["title"].append(" ".join(aTag.text.split()))

            for d in parser.select(".table tbody tr td:nth-child(2)"):
                Data["Date"].append("".join(d.text.split()))
                # To Format Date in yyyymmdd format eg 19240121
                # date = "".join(d.text.split())
                # date = date.split("-")
                # if len(date) == 3:
                #     newDate = f"{date[-1]}{month_dict[date[1]]}{date[0]}"
                # elif len(date) == 2:
                #     try:
                #         newDate = f"{date[-1]}{month_dict[date[0]]}"
                #     except:
                #         if date[0] == " " & date[-1] == " ":    
                #             newDate = f"No Date"
                # elif len(date) == 1:
                #     newDate = f"{date}"
                # else:
                #     newDate = "No date"
                # # print(newDate)
                # Data["Date"].append(newDate)

        

            print(f"link: {len(Data['link'])},title: {len(Data['title'])}, Date: {len(Data['Date'])}, Count: {count}")


            df = pd.DataFrame(Data)
            df.to_excel(fr"excel\Data{count}.xlsx")

            count += 1

            




scraper = BVMScraper()
# scraper.getData()
# scraper.formatHtmltoexcel()
