#!/usr/bin/env python3

import os, re, praw, json, logging, requests, plugins.common.General as General

Plugin_Name = "Reddit"
The_File_Extension = ".html"
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0', 'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5'}

def Load_Configuration():
    File_Dir = os.path.dirname(os.path.realpath('__file__'))
    Configuration_File = os.path.join(File_Dir, 'plugins/common/config/config.json')
    logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Loading configuration data.")

    try:
        with open(Configuration_File) as JSON_File:  
            Configuration_Data = json.load(JSON_File)
            Reddit_Details = Configuration_Data[Plugin_Name.lower()]
            Reddit_Client_ID = Reddit_Details['client_id']
            Reddit_Client_Secret = Reddit_Details['client_secret']
            Reddit_User_Agent = Reddit_Details['user_agent']
            Reddit_Username = Reddit_Details['username']
            Reddit_Password = Reddit_Details['password']
            Subreddit_to_Search = Reddit_Details["subreddits"]

            if Reddit_Client_ID and Reddit_Client_Secret and Reddit_User_Agent and Reddit_Username and Reddit_Password and Subreddit_to_Search:
                return [Reddit_Client_ID, Reddit_Client_Secret, Reddit_User_Agent, Reddit_Username, Reddit_Password, Subreddit_to_Search]

            else:
                return None
    except:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to load Reddit details.")

def Search(Query_List, Task_ID, **kwargs):

    try:
        Data_to_Cache = []
        Results = []
        Directory = General.Make_Directory(Plugin_Name.lower())
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        Log_File = General.Logging(Directory, Plugin_Name.lower())
        handler = logging.FileHandler(os.path.join(Directory, Log_File), "w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        Reddit_Details = Load_Configuration()
        Cached_Data = General.Get_Cache(Directory, Plugin_Name)
        Limit = General.Get_Limit(kwargs)
        Query_List = General.Convert_to_List(Query_List)

        for Query in Query_List:

            try:
                Reddit_Connection = praw.Reddit(client_id=Reddit_Details[0], client_secret=Reddit_Details[1], user_agent=Reddit_Details[2], username=Reddit_Details[3], password=Reddit_Details[4])
                All_Subreddits = Reddit_Connection.subreddit(Reddit_Details[5])

                for Subreddit in All_Subreddits.search(Query, limit=Limit): # Limit, subreddit and search to be controlled by the web app.
                    Results.append(Subreddit.url)

            except:
                logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to get results. Are you connected to the internet?")

            Output_Connections = General.Connections(Query, Plugin_Name, "reddit.com", "Data Leakage", Task_ID, Plugin_Name.lower())

            for Result in Results:

                if Result not in Cached_Data and Result not in Data_to_Cache:

                    try:
                        Reddit_Regex = re.search("https\:\/\/www\.reddit\.com\/r\/(\w+)\/comments\/(\w+)\/([\w\d]+)\/", Result[0])

                        if Reddit_Regex:
                            Reddit_Response = requests.get(Result, headers=headers).text
                            Output_file = General.Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Reddit_Response, Reddit_Regex.group(3), The_File_Extension)

                            if Output_file:
                                Output_Connections.Output([Output_file], Result, General.Get_Title(Result[0]), Plugin_Name.lower())
                                Data_to_Cache.append(Result[0])

                            else:
                                logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to create output file. File may already exist.")

                    except:
                        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to create file.")

        if Cached_Data:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

        else:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")

    except Exception as e:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - {str(e)}")