#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime, os, logging, re, requests, urllib, json, plugins.common.Connectors as Connectors
from bs4 import BeautifulSoup

Bad_Characters = ["|", "/", "&", "?", "\\", "\"", "\'", "[", "]", ">", "<", "~", "`", ";", "{", "}", "%", "^"]
Configuration_File = os.path.join('plugins/common/config', 'config.json')

def Date():
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def Get_Limit(kwargs):

    try:

        if kwargs.get('Limit'):

            if int(kwargs["Limit"]) > 0:
                Limit = int(kwargs["Limit"])

            else:
                Limit = 10

        else:
            Limit = 10

        return Limit

    except:
        logging.warning(f"{Date()} General Library - Failed to set limit.")

def Logging(Directory, Plugin_Name):

    try:
        Main_File = f"{Plugin_Name}-log-file.log"
        General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

        if General_Directory_Search:
            Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)
            return Complete_File

    except:
        logging.warning(f"{Date()} General Library - Failed to initialise logging.")


def Get_Cache(Directory, Plugin_Name):
    Main_File = f"{Plugin_Name}-cache.txt"
    General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

    if General_Directory_Search:
        Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)

        try:

            if os.path.exists(Complete_File):
                File_Input = open(Complete_File, "r")
                Cached_Data = File_Input.read()
                File_Input.close()
                return Cached_Data

            else:
                logging.info(f"{Date()} General Library - No cache file found, caching will not be used for this session.")
                return []

        except:
            logging.warning(f"{Date()} General Library - Failed to read file.")

    else:
        logging.warning(f"{Date()} General Library - Failed to regex directory. Cache not read.")

def Write_Cache(Directory, Data_to_Cache, Plugin_Name, Open_File_Type):
    Main_File = f"{Plugin_Name}-cache.txt"
    General_Directory_Search = re.search(r"(.*)\/\d{4}\/\d{2}\/\d{2}", Directory)

    if General_Directory_Search:
        Complete_File = os.path.join(General_Directory_Search.group(1), Main_File)

        try:
            File_Output = open(Complete_File, Open_File_Type)
            Current_Output_Data = "\n".join(Data_to_Cache) + "\n"
            File_Output.write(Current_Output_Data)
            File_Output.close()

        except:
            logging.warning(f"{Date()} General Library - Failed to create file.")

    else:
        logging.warning(f"{Date()} General Library - Failed to regex directory. Cache not written.")

def Convert_to_List(String):

    try:

        if ', ' in String:
            List = String.split(', ')
            return List

        elif ',' in String:
            List = String.split(',')
            return List

        else:
            List = [String]
            return List

    except:
        logging.warning(f"{Date()} General Library - Failed to convert the provided query to a list.")

class Connections():

    def __init__(self, Input, Plugin_Name, Domain, Result_Type, Task_ID, Concat_Plugin_Name):

        try:
            self.Plugin_Name = str(Plugin_Name)
            self.Domain = str(Domain)
            self.Result_Type = str(Result_Type)
            self.Task_ID = str(Task_ID)
            self.Input = str(Input)
            self.Concat_Plugin_Name = str(Concat_Plugin_Name)

        except:
            logging.warning(f"{Date()} General Library - Error setting initial variables.")

    def Output(self, Complete_File_List, Link, DB_Title, Directory_Plugin_Name, **kwargs):

        try:
            Text_Complete_Files = "\n- ".join(Complete_File_List)

            if kwargs.get("Dump_Types"):
                self.Dump_Types = kwargs["Dump_Types"]
                Joined_Dump_Types = ", ".join(Dump_Types)
                self.Title = f"Data for input: {self.Input}, found by Scrummage plugin {self.Plugin_Name}.\nData types include: {Joined_Dump_Types}.\nAll data is stored in\n- {Text_Complete_Files}."
                self.Ticket_Subject = f"Scrummage {self.Plugin_Name} results for query {self.Input}."
                NL_Joined_Dump_Types = "\n- ".join(Dump_Types)
                self.Ticket_Text = f"Results were identified for the search {self.Input} performed by the Scrummage plugin {self.Plugin_Name}.\nThe following types of sensitive data were found:\n- {NL_Joined_Dump_Types}. Please ensure these results do not pose a threat to your organisation, and take the appropriate action necessary if they pose a security risk.\n\nResult data can be found in the following output files:\n- {Text_Complete_Files}."

            else:
                self.Title = f"Data for input: {self.Input}, found by Scrummage plugin {self.Plugin_Name}.\nAll data is stored in the files:\n- {Text_Complete_Files}."
                self.Ticket_Subject = f"Scrummage {self.Plugin_Name} results for query {self.Input}."
                self.Ticket_Text = f"Results were identified for the search {self.Input} performed by the Scrummage plugin {self.Plugin_Name}. Please ensure these results do not pose a threat to your organisation, and take the appropriate action necessary if they pose a security risk.\n\nResult data can be found in the following output files:\n- {Text_Complete_Files}."

        except:
            logging.warning(f"{Date()} General Library - Error setting unique variables.")

        logging.info(f"{Date()} General Library - Adding item to Scrummage database and other configured outputs.")
        CSV_File = Connectors.CSV_Output(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, ", ".join(Complete_File_List), self.Task_ID, Directory_Plugin_Name)
        DOCX_File = Connectors.DOCX_Output(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, "\n".join(Complete_File_List), self.Task_ID, Directory_Plugin_Name)

        if CSV_File:
            Complete_File_List.append(CSV_File)

        if DOCX_File:
            Complete_File_List.append(DOCX_File)

        Relative_File_List = []

        for File in Complete_File_List:
            Relative_File = File.replace(os.path.dirname(os.path.realpath('__file__')), "")
            Relative_File_List.append(Relative_File)

        Connectors.Main_Database_Insert(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, ", ".join(Relative_File_List), self.Task_ID)
        Connectors.Elasticsearch_Main(DB_Title, self.Plugin_Name, self.Domain, Link, self.Result_Type, ", ".join(Complete_File_List), self.Task_ID, self.Concat_Plugin_Name)
        Connectors.Defect_Dojo_Output(DB_Title, self.Ticket_Text)
        Connectors.Scumblr_Main(self.Input, DB_Title, self.Title)
        Connectors.RTIR_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.JIRA_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.Email_Main(self.Ticket_Subject, self.Ticket_Text)
        Connectors.Slack_Main(self.Ticket_Text)

def Main_File_Create(Directory, Plugin_Name, Output, Query, Main_File_Extension):
    Main_File = f"Main-file-for-{Plugin_Name}-query-{Query}{Main_File_Extension}"
    Complete_File = os.path.join(Directory, Main_File)
    Appendable_Output_Data = []

    try:

        if not os.path.exists(Complete_File):
            File_Output = open(Complete_File, "w")
            File_Output.write(Output)
            File_Output.close()
            logging.info(f"{Date()} General Library - Main file created.")

        else:

            if not Main_File_Extension == ".json":
                File_Input = open(Complete_File, "r")
                Cache_File_Input = File_Input.read()
                File_Input.close()

                if Appendable_Output_Data:
                    logging.info(f"{Date()} General Library - New data has been discovered and will be appended to the existing file.")
                    Appendable_Output_Data_String = "\n".join(Cache_File_Input)
                    File_Output = open(Complete_File, "a")
                    File_Output.write(f"\n{Appendable_Output_Data_String}\n{Output}")
                    File_Output.close()
                    logging.info(f"{Date()} General Library - Main file appended.")

                else:
                    logging.info(f"{Date()} General Library - No existing data found in file, will overwrite.")
                    os.remove(Complete_File)
                    File_Output = open(Complete_File, "w")
                    File_Output.write(Output)
                    File_Output.close()

            else:
                prv_i = 0
                i = 0

                while os.path.exists(Complete_File):
                    Complete_File = Complete_File.strip(f"-{str(prv_i)}.json")
                    Complete_File = f"{Complete_File}-{str(i)}.json"
                    prv_i = i
                    i += 1

                File_Output = open(Complete_File, "w")
                File_Output.write(Output)
                File_Output.close()
                logging.info(f"{Date()} General Library - Main file created.")

        return Complete_File

    except:
        logging.warning(f"{Date()} General Library - Failed to create main file.")

def Data_Type_Discovery(Data_to_Search):
    # Function responsible for determining the type of data found. Examples: Hash_Type, Credentials, Email, or URL.

    try:
        Dump_Types = []
        Hash_Types = [["MD5","([a-fA-F0-9]{32})\W"],["SHA1","([a-fA-F0-9]{40})\W"],["SHA256","([a-fA-F0-9]{64})\W"]]

        for Hash_Type in Hash_Types: # Hash_Type identification
            Hash_Regex = re.search(Hash_Type[1], Data_to_Search)

            if Hash_Regex:
                Hash_Type_Line = f"{Hash_Type[0]} hash"

                if not Hash_Type_Line in Dump_Types:
                    Dump_Types.append(Hash_Type_Line)

            else:
                pass

        Credential_Regex = re.search(r"[\w\d\.\-\_]+\@[\w\.]+\:.*", Data_to_Search)

        if Credential_Regex: # Credentials identification

            if not "Credentials" in Dump_Types:
                Dump_Types.append("Credentials")

        else:
            EmailRegex = re.search("[\w\d\.\-\_]+\@[\w\.]+", Data_to_Search)
            URLRegex = re.search("(https?:\/\/(www\.)?)?([-a-zA-Z0-9:%._\+#=]{2,256})(\.[a-z]{2,6}\b([-a-zA-Z0-9:%_\+.#?&//=]*))", Data_to_Search)

            if EmailRegex: # Email Identification

                if not "Email" in Dump_Types:
                    Dump_Types.append("Email")

            if URLRegex: # URL Indentification

                if not "URL" in Dump_Types:
                    Dump_Types.append("URL")

        return Dump_Types

    except:
        logging.warning(f"{Date()} General Library - Failed to determine data type.")

def Create_Query_Results_Output_File(Directory, Query, Plugin_Name, Output_Data, Query_Result_Name, The_File_Extension):

    try:
        Query_Bad_Characters = Bad_Characters
        Query_Bad_Characters.extend(["https://", "http://", "www.", "=", ",", " ", "@", ":", "---", "--"])

        for Character in Query_Bad_Characters:

            if Character in Query:
                Query = Query.replace(Character, "-")

            if Character in Query_Result_Name and Character not in ["https://", "http://", "www."]:
                Query_Result_Name = Query_Result_Name.replace(Character, "-")

            elif Character in Query_Result_Name and Character in ["https://", "http://", "www."]:
                Query_Result_Name = Query_Result_Name.replace(Character, "")

        try:
            The_File = f"{Plugin_Name}-Query-{Query}-{Query_Result_Name}{The_File_Extension}"
            Complete_File = os.path.join(Directory, The_File)

            if not os.path.exists(Complete_File):

                with open(Complete_File, 'w') as Current_Output_file:
                    Current_Output_file.write(Output_Data)

                logging.info(f"{Date()} General Library - File: {Complete_File} created.")

            else:
                logging.info(f"{Date()} General Library - File already exists, skipping creation.")

            return Complete_File

        except:
            logging.warning(f"{Date()} General Library - Failed to create query file.")

    except:
        logging.warning(f"{Date()} General Library - Failed to initialise query file.")

def Load_Location_Configuration():
    Valid_Locations = ['ac', 'ac', 'ad', 'ae', 'af', 'af', 'ag', 'ag', 'ai', 'ai', 'al', 'am', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'az', 'ba', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bi', 'bj', 'bn', 'bo', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'cn', 'co', 'co', 'co', 'cr', 'cu', 'cv', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ec', 'ee', 'eg', 'es', 'et', 'eu', 'fi', 'fj', 'fm', 'fr', 'ga', 'ge', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gp', 'gp', 'gr', 'gr', 'gt', 'gy', 'gy', 'gy', 'hk', 'hk', 'hn', 'hr', 'ht', 'ht', 'hu', 'hu', 'id', 'id', 'ie', 'il', 'im', 'im', 'in', 'in', 'io', 'iq', 'iq', 'is', 'it', 'je', 'je', 'jm', 'jo', 'jo', 'jp', 'jp', 'ke', 'kg', 'kh', 'ki', 'kr', 'kw', 'kz', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'ma', 'md', 'me', 'mg', 'mk', 'ml', 'mm', 'mn', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'mx', 'my', 'mz', 'na', 'ne', 'nf', 'ng', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pe', 'pf', 'pg', 'ph', 'pk', 'pk', 'pl', 'pl', 'pn', 'pr', 'ps', 'ps', 'pt', 'py', 'qa', 'qa', 're', 'ro', 'rs', 'rs', 'ru', 'ru', 'rw', 'sa', 'sb', 'sc', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'td', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tt', 'tz', 'ua', 'ua', 'ug', 'uk', 'us', 'us', 'uy', 'uz', 'uz', 'vc', 've', 've', 'vg', 'vi', 'vn', 'vu', 'ws', 'za', 'zm', 'zw']

    try:

        with open(Configuration_File) as JSON_File:  
            Configuration_Data = json.load(JSON_File)
            General_Details = Configuration_Data['general']
            Location = General_Details['location']

            if (len(Location) > 2) or (Location not in Valid_Locations):
                logging.warning(f"{Date()} General Library - An invalid location has been specified, please provide a valid location in the config.json file.")

            else:
                logging.info(f"{Date()} General Library - Country code {Location} selected.")
                return Location

    except:
        logging.warning(f"{Date()} General Library - Failed to load location details.")

def Make_Directory(Plugin_Name):
    Today = datetime.datetime.now()
    Year = str(Today.year)
    Month = str(Today.month)
    Day = str(Today.day)

    if len(Month) == 1:
        Month = f"0{Month}"

    if len(Day) == 1:
        Day = f"0{Day}"

    File_Path = os.path.dirname(os.path.realpath('__file__'))
    Directory = f"{File_Path}/static/protected/output/{Plugin_Name}/{Year}/{Month}/{Day}"

    try:
        os.makedirs(Directory)
        logging.info(f"{Date()} General Library - Using directory: {Directory}.")
        return Directory

    except:
        logging.warning(f"{Date()} General Library - Using directory: {Directory}.")
        return Directory

def Get_Latest_URLs(Pull_URL, Scrape_Regex_URL):
    Scrape_URLs = []
    Content = ""
    Content_String = ""

    try:
        Content = requests.get(Pull_URL).text
        Content_String = str(Content)

    except:
        logging.warning(f"{Date()} General Library - Failed to connect.")

    try:
        Scrape_URLs_Raw = re.findall(Scrape_Regex_URL, Content_String)

        for Temp_URL_Extensions in Scrape_URLs_Raw:

            if not Temp_URL_Extensions in Scrape_URLs:
                Scrape_URLs.append(Temp_URL_Extensions)

    except:
        logging.warning(f"{Date()} General Library - Failed to regex URLs.")

    return Scrape_URLs

def Get_Title(URL):

    try:

        if 'file:/' not in URL:
            Soup = BeautifulSoup(urllib.request.urlopen(URL), features="lxml")
            return Soup.title.text

        else:
            logging.warning(f"{Date()} General Library - This function does not work on files.")

    except:
        logging.warning(f"{Date()} General Library - Failed to get title.")