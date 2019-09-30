from pathlib import Path
from os import sys
from time import ctime
from pprint import pprint
import json
import shutil


class FileSorter:
    files = {}
    folders = {}
    extensions = {}
    file_name_with_sizes = {}
    path_obects = []
    all_extensions = {
        "Documents" : ['.doc' , '.docx' , '.odt' , '.pdf' , '.rtf' , '.tex' ,'.txt' ,'.wks' , '.wps' , '.wpd','.json'],
        "Videos" : ['.3g2' , '.3gp','.avi' , '.flv' , '.h264' , '.m4v' , '.mkv' , '.mov','mp4','.mkv','.mov','.mp4','.mpg','.mpeg','.rm','.swf','.vob','.wmv'],
        "Images" : ['.ai','.bmp','.gif','.ico','.jpeg','.jpg','.png','.ps','.psd','.svg','.tif','.tiff'],
        "Compressed" : ['.7z','.arj','.deb','.pkg','.rar','.rpm','.tar.gz','.z','.zip'],
        "Executable" : ['.apk' , '.bat' , '.bin' , '.cgi' , '.pl' , '.com','.exe','.gadget','.wsf'],
        "Font" : ['.fnt','.fon','.otf','.ttf'],
        "Audio" : ['.aif','.cda','.mid','.midi','.mp3','.mpa','.ogg','.wav','.wma','.wpl'],
        "Disc" : ['.dmg' , 'iso' , '.toast' , '.vcd'],
        "Database" : ['.db' , '.sql' , '.mdb' , '.log' , '.dbf' , '.dat'],
        "Presentaion" : ['.ppt' , '.pptx' , '.key' , '.odp' , '.pps'],
        "Programming" : ['.html' , '.htm' , '.py' , '.java' , '.css' , '.js' , '.ts' , '.kt' , '.c' , '.cpp' , '.cs' , '.sh' , '.swift' , '.vb'],
        "Spreadsheets" : ['.ods' , '.xlr' , '.xls' , '.xlsx'],
    }

    def __init__(self, path):
        self.path = Path(path) if len(path) > 0 else Path()

    def __str__(self):
        return f" The Path is -> {self.path.absolute()}"

    def scan(self):
        """

        scan() :

        This method scans the given path recursively and stores them in a dictionary for further use.
        File information such as -> name, full_path, size, creation_time, etc.

        Parameters : None

        Returns : Dictionary with all details of files

        """

        for x in self.path.rglob("*.*"):
            self.files[x.name] = dict(name=x.name,
                                      absolute_path=x.as_posix(),
                                      size=x.stat().st_size,
                                      creation_time=ctime(x.stat().st_ctime),
                                      extension=x.suffix,
                                      file_name_without_ext=x.stem,
                                      is_folder=x.is_dir(),
                                      is_file=x.is_file(),
                                      info=self.getFileInfo(x.stat()))

        self.files['total_files'] = len(self.files)
        return self.files

    def getPaths(self):
        """

        getPaths() :

        This method scans the given path and writtens a list of subpaths.
        Example : 
            Given -> C:/../../Desktop
            Returns -> [Path() , Path("new_folde")]

        Parameters : None

        Returns : List of Path Objects
        """


        for x in self.path.rglob("*.*"):
            self.path_obects += [x]
        return self.path_obects

    def getFileInfo(self, stat):
        return dict(mode=stat.st_mode, dev=stat.st_dev, uid=stat.st_uid, atime=stat.st_atime, mtime=stat.st_mtime, ctime=stat.st_ctime)

    def storeInJson(self, file_name):
        """

        storeInJson(file_name):
            This method simply takes the dictionary of files and then stores them into json file

        Parameteres : file_name (Please type just filename without extension)

        Returns : None

        """

        if self.files['total_files']:
            with open(file_name + ".json", "w") as f:
                json.dump(self.files, f)
        else:
            print("Error : " , "There are no files to store.")
            print("INFO : " , "Please class the scan() to generate some files.")

    def moveFiles(self , destination):
        print("Moving files : ")
        for x in self.getPaths():
            if x.is_file():
                folder_name = [ k for k,v  in self.all_extensions.items() if x.suffix in v]
                if len(folder_name) > 0:
                    source = x.as_posix()
                    new_dest = destination / folder_name[0]
                    new_dest.mkdir(parents=True, exist_ok=True)
                    new_dest = new_dest / x.name
                    shutil.move(source, new_dest.as_posix())
                    print("File moved : ")
                    print("\tS :", source)
                    print("\tD :", new_dest.as_posix())
                else:
                    source = x.as_posix()
                    new_dest = destination / "Others"
                    new_dest.mkdir(parents=True, exist_ok=True)
                    new_dest = new_dest / x.name
                    shutil.move(source, new_dest.as_posix())
                    print("File moved : ")
                    print("\tS :", source)
                    print("\tD :", new_dest.as_posix())


    def sort(self, destination=""):
        """
        sort(destination):
            
            This method is the main method as it does all the works of sorting files into folders.
            Example : invoive.pdf -> pdf/invoice.pdf
                (The above pdf file will go into pdf folder)

            like that every file has its own directory


        """
        if len(self.files) > 1:
            if not destination == "":
                destination = Path(destination)
                self.moveFiles(destination)
            else:
                destination = Path()
                self.moveFiles(destination)


file_sorter = FileSorter("D:/Projects/Testing")
files = file_sorter.scan()
file_sorter.storeInJson("files_info.json")
file_sorter.sort()


