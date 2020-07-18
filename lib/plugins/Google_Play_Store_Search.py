#!/usr/bin/env python3

import requests, os, logging, re, json, plugins.common.General as General

Plugin_Name = "Play-Store"
Concat_Plugin_Name = "playstore"
The_File_Extensions = {"Main": ".json", "Query": ".html"}

def Search(Query_List, Task_ID, **kwargs):

    try:
        Data_to_Cache = []
        Directory = General.Make_Directory(Concat_Plugin_Name)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        Log_File = General.Logging(Directory, Concat_Plugin_Name)
        handler = logging.FileHandler(os.path.join(Directory, Log_File), "w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        Cached_Data = General.Get_Cache(Directory, Plugin_Name)
        Query_List = General.Convert_to_List(Query_List)
        Limit = General.Get_Limit(kwargs)

        for Query in Query_List:

            try:
                headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
                body = {"f.req": f'''[[["lGYRle","[[[],[[10,[10,50]],true,null,[96,27,4,8,57,30,110,11,16,49,1,3,9,12,104,55,56,51,10,34,31,77,145],[null,null,null,[[[[7,31],[[1,52,43,112,92,58,69,31,19,96,103]]]]]]],[\\"{Query}\\"],7,[null,1]]]",null,"2"]]]'''}
                Play_Store_Response = requests.post("https://play.google.com/_/PlayStoreUi/data/batchexecute", headers=headers, data=body).text
                Play_Store_Response = Play_Store_Response.replace(')]}\'\n\n', "").replace("\\\\u003d", "=")
                Play_Store_Response_JSON = json.dumps(json.loads(Play_Store_Response), indent=4, sort_keys=True)
                Main_File = General.Main_File_Create(Directory, Plugin_Name, Play_Store_Response_JSON, Query, The_File_Extensions["Main"])
                Output_Connections = General.Connections(Query, Plugin_Name, "play.google.com", "Application", Task_ID, Concat_Plugin_Name)
                Win_Store_Regex = re.findall(r"(\/store\/apps\/details\?id\\\\([\w\d\.]+))\\\"", Play_Store_Response)
                Current_Step = 0

                for Result, Item in Win_Store_Regex:
                    Result = Result.replace("\\\\u003d", "=")
                    Result_URL = f"https://play.google.com{Result}"
                    Item = Item.replace("u003d", "")
                    Title = f"Play Store | {Item}"
                    
                    if Result_URL not in Cached_Data and Result_URL not in Data_to_Cache and Current_Step < int(Limit):
                        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
                        Play_Store_Response = requests.get(Result_URL, headers=headers).text
                        Output_file = General.Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Play_Store_Response, Item, The_File_Extensions["Query"])

                        if Output_file:
                            Output_Connections.Output([Main_File, Output_file], Result_URL, Title, Concat_Plugin_Name)
                            Data_to_Cache.append(Result_URL)

                        else:
                            logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to create output file. File may already exist.")

                        Current_Step += 1

            except:
                logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - Failed to get results, this may be due to the query provided.")

        if Cached_Data:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "a")

        else:
            General.Write_Cache(Directory, Data_to_Cache, Plugin_Name, "w")

    except Exception as e:
        logging.warning(f"{General.Date()} - {__name__.strip('plugins.')} - {str(e)}")