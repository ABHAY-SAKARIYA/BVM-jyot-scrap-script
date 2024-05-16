
# Importing require modules
import aiohttp
import asyncio
import json
import time
from bs4 import BeautifulSoup
from constant import File_Path


class AsyncRun:

    def __init__(self) -> None:
        pass
    # Creating an async function that will capture data from the website url passed to it and the client is the aiohttp client that will handle the async requests to the website.
    async def getData(self,client,url) -> list:
        async with client.get(url) as res:
            link = ""
            name = ""

            parser = BeautifulSoup(await res.text(),"html.parser")

        for d in parser.select("tr .break-all:nth-child(1) a"):
            ele = d.get("href")
            link = f"http://archives.biharvidhanmandal.in{ele}"
            name = d.text


        return [link,name]



    async def main(self,count : int ,links : list, maxscrapecountatonce : int) -> list:
        
        downloadLink = []
        name = []

        async with aiohttp.ClientSession() as client:

            tasks = []
            try:
                for link in links[count:count+maxscrapecountatonce:1]:
                    tasks.append(asyncio.create_task(self.getData(client=client,url=link)))
            except: 
                print(f"len of Final tasks list is >>> {len(tasks)} and counting is >>> {count}")

            result = await asyncio.gather(*tasks)


            save_count = 0

            while save_count < maxscrapecountatonce:
                try:
                    downloadLink.append(result[save_count][0])
                    name.append(result[save_count][1])
                    save_count += 1
                except:
                    break

        time.sleep(5)
        return downloadLink,name




    def run(self) -> None:

        try:
            with open(fr"{File_Path}\temp\temp.json","r") as read:
                data = json.load(read)

            maxscrapecountatonce = 100

            newData = {
                "Date" : [],
                "Titles" : [],
                "PageLinks" : [],
                "DownloadLink" : [],
                "Pdfname" : []
            }


            endloop = len(data["link"])
            startCount = 0
            while startCount < endloop: 
                downloadlink,pdfname = asyncio.run(self.main(startCount,data["link"],maxscrapecountatonce))
                count = 0
                for i in range(0,len(pdfname)):

                    if (pdfname[i] in newData["Pdfname"] or downloadlink[i] in newData["DownloadLink"]):
                        print(f"\n\nFound Duplicate FileName : {pdfname[i]} \nPdfLink is : {downloadlink[i]}\n")
                        continue
                    else:
                        # print(data["title"][count])
                        newData["DownloadLink"].append(downloadlink[i])
                        newData["Pdfname"].append(pdfname[i])
                        newData["Date"].append(data["Date"][count])
                        newData["Titles"].append(data["title"][count])
                        newData["PageLinks"].append(data["link"][count])
                    count += 1
                print(startCount)
                startCount += maxscrapecountatonce



                # print(newData["DownloadLink"],newData["Pdfname"])
                with open(fr"{File_Path}\temp\tempFinal.json","a") as write:
                    write.write(json.dumps(newData,indent=4))
        except Exception as e:
            print(e)