
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
            with open(fr"{File_Path}\temp.json","r") as read:
                data = json.load(read)

            maxscrapecountatonce = 1000

            newData = {
                "Date" : [x for x in data["Date"]],
                "Titles" : [x for x in data["title"]],
                "PageLinks" : [x for x in data["link"]],
                "DownloadLink" : [],
                "Pdfname" : []
            }


            endloop = len(data["link"])
            startCount = 0
            while startCount < endloop: 
                downloadlink,pdfname = asyncio.run(self.main(startCount,data["link"],maxscrapecountatonce))
                newData["DownloadLink"].extend(downloadlink)
                newData["Pdfname"].extend(pdfname)
                print(startCount)
                startCount += maxscrapecountatonce



                # print(newData["DownloadLink"],newData["Pdfname"])
                with open(fr"{File_Path}\tempFinal.json","a") as write:
                    write.write(json.dumps(newData,indent=4))
        except Exception as e:
            print(e)