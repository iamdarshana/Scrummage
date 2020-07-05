#!/usr/bin/env python3
import requests, logging, os, re, plugins.common.General as General, json, flickr_api
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0', 'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5'}

Plugin_Name = "Flickr"
The_File_Extensions = {"Main": ".json", "Query": ".html"}

def Load_Configuration():
    File_Dir = os.path.dirname(os.path.realpath('__file__'))
    Configuration_File = os.path.join(File_Dir, 'plugins/common/config/config.json')
    logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Loading configuration data.")

    try:

        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)
            Flickr_Details = Configuration_Data[Plugin_Name.lower()]

            if Flickr_Details['api_key'] and Flickr_Details['api_secret']:
                return [Flickr_Details['api_key'], Flickr_Details['api_secret']]

            else:
                return None

    except:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to load location details.")

def Convert_to_JSON(Data):
    Data = str(Data)
    Flickr_Regex = re.search(r"\[(.+)\]", Data)

    if Flickr_Regex:
        New_Data = Flickr_Regex.group(1).replace("id=b", "'id': ").replace("title=b", "'title': ").replace("(", "{").replace(")", "}")
        New_Data = New_Data.replace("Photo", "")
        New_Data = f"[{New_Data}]"
        New_Data = eval(New_Data)
        New_Data = json.dumps(New_Data, indent=4, sort_keys=True)
        return New_Data

def Search(Query_List, Task_ID, **kwargs):

    try:
        Data_to_Cache = []
        Directory = General.Make_Directory(Plugin_Name.lower())
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        Log_File = General.Logging(Directory, Plugin_Name.lower())
        handler = logging.FileHandler(os.path.join(Directory, Log_File), "w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        Cached_Data = General.Get_Cache(Directory, Plugin_Name)
        Query_List = General.Convert_to_List(Query_List)
        Limit = General.Get_Limit(kwargs)

        try:
            Flickr_Details = Load_Configuration()
            flickr_api.set_keys(api_key=Flickr_Details[0], api_secret=Flickr_Details[1])

        except:
            logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to establish API identity.")

        for Query in Query_List:
            Email_Regex = re.search(r"[^@]+@[^\.]+\..+", Query)

            if Email_Regex:

                try:
                    User = flickr_api.Person.findByEmail(Query)
                    Photos = User.getPhotos()

                    if Photos:
                        Main_File = General.Main_File_Create(Directory, Plugin_Name, Convert_to_JSON(Photos), Query, The_File_Extensions["Main"])
                        Output_Connections = General.Connections(Query, Plugin_Name, "flickr.com", "Data Leakage", Task_ID, Plugin_Name.lower())
                        Current_Step = 0

                        for Photo in Photos:
                            Photo_URL = f"https://www.flickr.com/photos/{Query}/{Photo['id']}"

                            if Photo_URL not in Cached_Data and Photo_URL not in Data_to_Cache and Current_Step < int(Limit):
                                Photo_Response = requests.get(Photo_URL, headers=headers).text
                                Output_file = General.Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Photo_Response, Photo, The_File_Extensions["Query"])

                                if Output_file:
                                    Output_Connections.Output([Main_File, Output_file], Photo_URL, General.Get_Title(Photo_URL), Plugin_Name.lower())
                                    Data_to_Cache.append(Photo_URL)

                                else:
                                    logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to create output file. File may already exist.")

                                Current_Step += 1

                    else:
                        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - No photos found.")

                except:
                    logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to make API call.")

            else:

                try:
                    User = flickr_api.Person.findByUserName(Query)
                    Photos = User.getPhotos()

                    if Photos:
                        Main_File = General.Main_File_Create(Directory, Plugin_Name, Convert_to_JSON(Photos), Query, The_File_Extensions["Main"])
                        Output_Connections = General.Connections(Query, Plugin_Name, "flickr.com", "Data Leakage", Task_ID, Plugin_Name.lower())
                        Current_Step = 0

                        for Photo in Photos:
                            Photo_URL = f"https://www.flickr.com/photos/{Query}/{Photo['id']}"

                            if Photo_URL not in Cached_Data and Photo_URL not in Data_to_Cache and Current_Step < int(Limit):
                                Photo_Response = requests.get(Photo_URL, headers=headers).text
                                Output_file = General.Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Photo_Response, str(Photo['id']), The_File_Extensions["Query"])

                                if Output_file:
                                    Output_Connections.Output([Main_File, Output_file], Photo_URL, General.Get_Title(Photo_URL), Plugin_Name.lower())
                                    Data_to_Cache.append(Photo_URL)

                                else:
                                    logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to create output file. File may already exist.")

                                Current_Step += 1

                    else:
                        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - No photos found.")

                except:
                    logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to make API call.")

        if Cached_Data:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

        else:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")

    except Exception as e:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - {str(e)}")