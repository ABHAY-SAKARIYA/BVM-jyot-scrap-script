# This Is The Main Script.

### Work Flow

- First this script will take the url of the website as an input from the user.
- Then it will scrap the date, title and link of the page and save them to temp.html and then temp.json file.
- Then from temp.json file it will get all the links and further scrap the details from each links like filename and downloadLink and save them to tempFinal.json file.
- Then it will download the data using download.py code and save them to the folder named download.
- Then all the downloaded pdf are further uploaded to google drive in the specific folder.
- Ends Here.


### Requirements / Dependencies

- selenium
- beautifulsoup4
- aiohttp
- asyncio
- pydrive


### User inputs 

- Url : str : Required : Url of the webpage.
- downloadPath: str : Required : Destination where the files are being downloaded.
- FolderName: str : Required : FolderName in which all the file should be saved in google drive.


### Use Cases

- If Url Consist of link to the website means perfomr all the operations.
- If Url is empty means only upload to google drive
- if Url consist of temp.json file means scrap details from website from the link in json file and then download them and upload to drive.
- If Url Consist of tempFinal.json means download the files and upload them to drive.


### File Wise Input Functions and Output

* scrap.py
    - BVMScraper: Class
    - Input:
        - Url : str : Required : Url of the webpage.

    - Functions:
        - getData() -> bool
            -This Function is to get table records from the Different Webpage and save them in different html file so that later on it can be converted into excel files

        - formatHtmltoexcel() -> bool
            - This function is to format and get the required data from different html files and save them to different excel files

* asyncApp.py
    - AsyncRun - class
    - Input:
        - None

    - Functions : 
        - getData() -> list
            - client, url
        
        - main() -> list
            - count : int ,links : list, maxscrapecountatonce : int

        - run() -> bool


* download.py
    - DownloadPdfs - class
    - Input :
        - downloadPath: str : Required : Destination where the files are being downloaded

    - Functions :
        - download_file() -> bool
            - url : str, destination: str

        - download() -> bool
            

* driveUpload.py
    - DriveUploader - class
    - Input:
        - Path: str : Required : Path where all the pdfs are downloaded.
        - FolderName: str : Required : FolderName in which all the file should be saved in google drive.

    - Functions: 
        - upload() -> bool