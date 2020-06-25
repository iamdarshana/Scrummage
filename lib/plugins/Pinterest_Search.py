#!/usr/bin/env python3
import plugins.common.General as General, json, logging, os, requests

The_File_Extension = ".html"
Plugin_Name = "Pinterest"

def Load_Configuration():
    File_Dir = os.path.dirname(os.path.realpath('__file__'))
    Configuration_File = os.path.join(File_Dir, 'plugins/common/config/config.json')
    logging.info(f"{General.Date()} - {__name__.strip('plugins.')} - Loading configuration data.")

    try:

        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)
            Pinterest_Details = Configuration_Data[Plugin_Name.lower()]

            if Pinterest_Details['oauth_token']:
                return Pinterest_Details['oauth_token']

            else:
                return None

    except:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to load location details.")

def Search(Query_List, Task_ID, Type, **kwargs):
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

        if Type == "pin":
            Local_Plugin_Name = Plugin_Name + "-" + Type
            Request_URL = "https://api.pinterest.com/v1/pins/" + Query + "/?access_token=" + Load_Configuration() + "&fields=id%2Clink%2Cnote%2Curl%2Ccreated_at%2Ccreator%2Cmedia%2Coriginal_link%2Cmetadata%2Ccounts%2Ccolor%2Cboard%2Cattribution"
            Search_Response = requests.get(Request_URL).text
            Search_Response = json.loads(Search_Response)
            JSON_Response = json.dumps(Search_Response, indent=4, sort_keys=True)
            General.Main_File_Create(Directory, Plugin_Name, JSON_Response, Query, ".json")

            Result_Title = Search_Response["data"]["metadata"]["link"]["title"]
            Result_URL = Search_Response["data"]["url"]
            Search_Result_Response = requests.get(Result_URL).text

            if Result_URL not in Cached_Data and Result_URL not in Data_to_Cache:
                Output_file = General.Create_Query_Results_Output_File(Directory, Query, Local_Plugin_Name, Search_Result_Response, Result_Title, The_File_Extension)

                if Output_file:
                    Output_Connections = General.Connections(Query, Local_Plugin_Name, "pinterest.com", "Data Leakage", Task_ID, Local_Plugin_Name.lower())
                    Output_Connections.Output(Output_file, Result_URL, Result_Title)

                Data_to_Cache.append(Result_URL)

        elif Type == "board":
            Local_Plugin_Name = Plugin_Name + "-" + Type
            Request_URL = "https://api.pinterest.com/v1/boards/" + Query + "/pins/?access_token=" + Load_Configuration() + "&fields=id%2Clink%2Cnote%2Curl%2Coriginal_link%2Cmetadata%2Cmedia%2Cimage%2Ccreator%2Ccreated_at%2Ccounts%2Ccolor%2Cboard%2Cattribution"
            Search_Response = requests.get(Request_URL).text
            Search_Response = json.loads(Search_Response)
            JSON_Response = json.dumps(Search_Response, indent=4, sort_keys=True)
            General.Main_File_Create(Directory, Plugin_Name, JSON_Response, Query, ".json")
            Output_Connections = General.Connections(Query, Local_Plugin_Name, "pinterest.com", "Data Leakage", Task_ID, Local_Plugin_Name.lower())
            Current_Step = 0

            for Response in Search_Response["data"]:
                Result_Title = Response["note"]
                Result_URL = Response["url"]
                Search_Result_Response = requests.get(Result_URL).text

                if Result_URL not in Cached_Data and Result_URL not in Data_to_Cache and Current_Step < int(Limit):
                    Output_file = General.Create_Query_Results_Output_File(Directory, Query, Local_Plugin_Name, Search_Result_Response, Result_Title, The_File_Extension)

                    if Output_file:
                        Output_Connections.Output(Output_file, Result_URL, Result_Title)

                    Data_to_Cache.append(Result_URL)
                    Current_Step += 1

    if Cached_Data:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

    else:
        General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")