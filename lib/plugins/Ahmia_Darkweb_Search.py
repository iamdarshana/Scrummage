#!/usr/bin/env python3

import plugins.common.General as General, os, logging

Plugin_Name = "Ahmia"
Tor_Plugin_Name = "Ahmia-Tor"
I2P_Plugin_Name = "Ahmia-I2P"
The_File_Extension = ".txt"

Request_Tor = ""
Request_I2P = ""
Tor_Pull_URL = ""
I2P_Pull_URL = ""
Tor_General_URL = "https://ahmia.fi/search/?q="
I2P_General_URL = "https://ahmia.fi/search/i2p/?q="
Tor_Scrape_Regex_URL = "(http\:\/\/[\d\w]+\.onion(?:\/[\/\.\-\?\=\%\d\w]+)?)"
I2P_Scrape_Regex_URL = "(http\:\/\/[\d\w]+\.i2p(?:\/[\/\.\-\?\=\%\d\w]+)?)"

def Search(Query_List, Task_ID, **kwargs):
    Data_to_Cache = []
    Cached_Data = []

    if kwargs.get('Limit'):

        if int(kwargs["Limit"]) > 0:
            Limit = int(kwargs["Limit"])

        else:
            Limit = 10

    else:
        Limit = 10

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

    if not Cached_Data:
        Cached_Data = []

    Query_List = General.Convert_to_List(Query_List)

    for Query in Query_List:
        Tor_Pull_URL = Tor_General_URL + Query
        Tor_Scrape_URLs = General.Get_Latest_URLs(Tor_Pull_URL, Tor_Scrape_Regex_URL)

        if Tor_Scrape_URLs:
            Output_file = General.Main_File_Create(Directory, Tor_Plugin_Name.lower(), "\n".join(Tor_Scrape_URLs), Query, The_File_Extension)

            if Output_file:
                Current_Step = 0
                Output_Connections = General.Connections(Query, Tor_Plugin_Name, "ahmia.fl", "Domain Spoof", Task_ID, Plugin_Name.lower())

                for URL in Tor_Scrape_URLs:

                    if URL not in Cached_Data and URL not in Data_to_Cache and Current_Step < int(Limit):
                        Output_Connections.Output(Output_file, URL, General.Get_Title(URL))
                        Data_to_Cache.append(URL)
                        Current_Step += 1

        else:
            logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - No Tor links scraped.")

        I2P_Pull_URL = I2P_General_URL + Query
        I2P_Scrape_URLs = General.Get_Latest_URLs(I2P_Pull_URL, I2P_Scrape_Regex_URL)

        if I2P_Scrape_URLs:
            Output_file = General.Main_File_Create(Directory, I2P_Plugin_Name.lower(), "\n".join(I2P_Scrape_URLs), Query, The_File_Extension)

            if Output_file:
                Current_Step = 0
                Output_Connections = General.Connections(Query, I2P_Plugin_Name, "ahmia.fl", "Domain Spoof", Task_ID, Plugin_Name.lower())

                for URL in I2P_Scrape_URLs:

                    if URL not in Cached_Data and URL not in Data_to_Cache and Current_Step < int(Limit):
                        Output_Connections.Output(Output_file, URL, General.Get_Title(URL))
                        Data_to_Cache.append(URL)
                        Current_Step += 1

        else:
            logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - No I2P links scraped.")

    if Cached_Data:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

    else:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")