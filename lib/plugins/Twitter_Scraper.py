#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json, os, requests, logging, tweepy, plugins.common.General as General

Plugin_Name = "Twitter"
The_File_Extensions = {"Main": ".json", "Query": ".html"}

def Load_Configuration():
    File_Dir = os.path.dirname(os.path.realpath('__file__'))
    Configuration_File = os.path.join(File_Dir, 'plugins/common/config/config.json')
    logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Loading configuration data.")

    try:

        with open(Configuration_File) as JSON_File:  
            Configuration_Data = json.load(JSON_File)
            Twitter_Details = Configuration_Data[Plugin_Name.lower()]
            Consumer_Key = Twitter_Details['CONSUMER_KEY']
            Consumer_Secret = Twitter_Details['CONSUMER_SECRET']
            Access_Key = Twitter_Details['ACCESS_KEY']
            Access_Secret = Twitter_Details['ACCESS_SECRET']

            if Consumer_Key and Consumer_Secret and Access_Key and Access_Secret:
                return [Consumer_Key, Consumer_Secret, Access_Key, Access_Secret]

            else:
                return None

    except:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to load Twitter details.")

def General_Pull(Handle, Limit, Directory, API, Task_ID):

    try:
        Data_to_Cache = []
        JSON_Response = []
        Cached_Data = General.Get_Cache(Directory, Plugin_Name)
        Latest_Tweets = API.user_timeline(screen_name=Handle, count=Limit)

        for Tweet in Latest_Tweets:
            Link = ""

            try:
                JSON_Response.append({
                    'id': Tweet.id,
                    'text': Tweet.text,
                    'author_name': Tweet.user.screen_name,
                    'url': Tweet.entities['urls'][0]["expanded_url"]
                })
                Link = Tweet.entities['urls'][0]["expanded_url"]

            except:
                JSON_Response.append({
                    'id': Tweet.id,
                    'text': Tweet.text,
                    'author_name': Tweet.user.screen_name
                })

        JSON_Output = json.dumps(JSON_Response, indent=4, sort_keys=True)
        Output_Connections = General.Connections(Handle, Plugin_Name, "twitter.com", "Social Media - Media", Task_ID, Plugin_Name.lower())
        Main_File = General.Main_File_Create(Directory, Plugin_Name, JSON_Output, Handle, The_File_Extensions["Main"])

        for JSON_Item in JSON_Response:

            if 'text' in JSON_Item and 'url' in JSON_Item:
                Link = JSON_Item['url']

                if Link not in Cached_Data and Link not in Data_to_Cache:
                    logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - {Link}")
                    Item_Response = requests.get(Link).text
                    Output_file = General.Create_Query_Results_Output_File(Directory, Handle, Plugin_Name, Item_Response, str(JSON_Item['id']), The_File_Extensions["Query"])

                    if Output_file:
                        Output_Connections.Output([Main_File, Output_file], Link, General.Get_Title(Link), Plugin_Name.lower())
                        Data_to_Cache.append(Link)

                    else:
                        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Output file not returned.")

            else:
                logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Insufficient parameters provided.")

        if Cached_Data:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

        else:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")

    except Exception as e:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - {str(e)}")

def Search(Query_List, Task_ID, **kwargs):

    try:
        Directory = General.Make_Directory(Plugin_Name.lower())
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        Log_File = General.Logging(Directory, Plugin_Name.lower())
        handler = logging.FileHandler(os.path.join(Directory, Log_File), "w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        Twitter_Credentials = Load_Configuration()
        Query_List = General.Convert_to_List(Query_List)
        Limit = General.Get_Limit(kwargs)

        for Query in Query_List:

            try:
                Authentication = tweepy.OAuthHandler(Twitter_Credentials[0], Twitter_Credentials[1])
                Authentication.set_access_token(Twitter_Credentials[2], Twitter_Credentials[3])
                API = tweepy.API(Authentication)
                General_Pull(Query, Limit, Directory, API, Task_ID)

            except:
                logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to get results. Are you connected to the internet?")

    except Exception as e:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - {str(e)}")