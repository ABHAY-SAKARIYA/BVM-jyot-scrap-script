
# Importing require modules
import aiohttp
import asyncio
import json
import time
from bs4 import BeautifulSoup
import pandas as pd


# Creating an async function that will capture data from the website url passed to it and the client is the aiohttp client that will handle the async requests to the website.
async def getData(client,url) -> str:
    async with client.get(url) as res:
        link = ""
        name = ""

        parser = BeautifulSoup(await res.text(),"html.parser")

    for d in parser.select("tr .break-all:nth-child(1) a"):
        ele = d.get("href")
        link = f"http://archives.biharvidhanmandal.in{ele}"
        name = d.text


    return [link,name]



async def main(count : int ,links : list, maxscrapecountatonce : int) -> list:
    
    downloadLink = []
    name = []

    async with aiohttp.ClientSession() as client:

        tasks = []
        try:
            for link in links[count:count+maxscrapecountatonce:1]:
                tasks.append(asyncio.create_task(getData(client=client,url=link)))
        except: 
            print(f"For Loop Stoped With an Error >>>> len of Final tasks list is >>> {len(tasks)} and counting is >>> {count}")

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




if __name__ == "__main__":

    fileNo = 19

    while fileNo <= 21:

        data = pd.read_excel(fr"D:\Abhay\bihar vidhan mandal scraping jyot\excel\Data{fileNo}.xlsx")

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
            downloadlink,pdfname = asyncio.run(main(startCount,data["link"],maxscrapecountatonce))
            newData["DownloadLink"].extend(downloadlink)
            newData["Pdfname"].extend(pdfname)
            print(startCount)
            startCount += maxscrapecountatonce



            # print(newData["DownloadLink"],newData["Pdfname"])
            # with open("test.json","a") as write:
            #     write.write(json.dumps(newData,indent=4))
        df = pd.DataFrame(newData)
        df.to_excel(fr"finalExcel\finalExcel{fileNo}.xlsx")
        print("Xlsx File Saved: ",fileNo)
        fileNo += 1