# This Is The Main Script.

### Work Flow

- First this script will take the url of the website as an input from the user.
- Then it will scrap the date, title and link of the page and save them to temp.html and then temp.json file.
- Then from temp.json file it will get all the links and further scrap the details from each links like filename and downloadLink and save them to tempFinal.json file.
- Then it will download the data using download.py code and save them to the folder which user defines and also create an filename.json file consists of all the pdfs filename require to create excel.
- Then all the downloaded pdf are further uploaded to google drive in the specific folder which user defines and also create an driveUrl.json file consist of all the url of file which are uploaded to drive.
- lastly create an excel file which includes columns like Title,Filename,WebsitePageLink,WebsitePdfLink,DriveLink.
- Ends Here.


### Requirements / Dependencies

- aiohttp==3.9.1
- beautifulsoup4==4.12.2
- PyDrive==1.3.1
- selenium==4.16.0


### User inputs 

- Url : str : Required : Url of the webpage.
- downloadPath: str : Required : Destination where the files are being downloaded.
- FolderName: str : Required : FolderName in which all the file should be saved in google drive.


### Use Cases

- If Url Consist of link to the website means perfome all the operations.
- If Url is empty means only upload to google drive
- if Url consist of temp.json file means scrap details from website from the link in json file and then download them and upload to drive.
- If Url Consist of tempFinal.json means download the files and upload them to drive.
- If url is equal to "excel" then only create an excel file takes data from the temp folder.


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


* createExcel.py
    - createExcel - class
    - Input:
        - url : str : None : Url of the website.

    - Functions:
        - create() -> None