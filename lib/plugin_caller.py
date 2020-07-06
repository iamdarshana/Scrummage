import threading, plugins.common.Connectors as Connectors, plugins.common.General as General

def Starter(Task_ID):
    Connection = Connectors.Load_Main_Database()
    Cursor = Connection.cursor()
    PSQL_Update_Query = 'UPDATE tasks SET status = %s WHERE task_id = %s'
    Cursor.execute(PSQL_Update_Query, ("Running", int(Task_ID),))
    Connection.commit()

def Stopper(Task_ID):
    Connection = Connectors.Load_Main_Database()
    Cursor = Connection.cursor()
    PSQL_Update_Query = 'UPDATE tasks SET status = %s WHERE task_id = %s'
    Cursor.execute(PSQL_Update_Query, ("Stopped", int(Task_ID),))
    Connection.commit()

class Plugin_Caller:

    def __init__(self, **kwargs):
        self.plugin_name = kwargs["Plugin_Name"]
        self.query = kwargs["Query"]
        self.limit = kwargs["Limit"]
        self.task_id = kwargs["Task_ID"]

    def Call_Plugin(self):
        Thread_0 = threading.Thread(target=Starter, args=[self.task_id])
        Thread_0.start()
        Thread_0.join()

        try:

            if self.plugin_name == "YouTube Search":
                import plugins.YouTube_Search as YT_Search
                Thread_1 = threading.Thread(target=YT_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Windows Store Search":
                import plugins.Windows_Store_Search as WS_Search
                Thread_1 = threading.Thread(target=WS_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Vulners Search":
                import plugins.Vulners_Search as Vulners_Search
                Thread_1 = threading.Thread(target=Vulners_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Vehicle Registration Search":
                import plugins.Vehicle_Registration_Search as Vehicle_Registration_Search
                Thread_1 = threading.Thread(target=Vehicle_Registration_Search.Search, args=(self.query, self.task_id))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Twitter Scraper":
                import plugins.Twitter_Scraper as Twitter_Scraper
                Thread_1 = threading.Thread(target=Twitter_Scraper.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Torrent Search":
                import plugins.Torrent_Search as Torrent_Search
                Thread_1 = threading.Thread(target=Torrent_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "RSS Feed Search":
                import plugins.RSS_Feed_Search as RSS_Feed_Search
                Thread_1 = threading.Thread(target=RSS_Feed_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Reddit Search":
                import plugins.Reddit_Search as Reddit_Search
                Thread_1 = threading.Thread(target=Reddit_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Phishstats Search":
                import plugins.Phishstats_Search as Phishstats_Search
                Thread_1 = threading.Thread(target=Phishstats_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Pinterest Pin Search":
                import plugins.Pinterest_Search as Pinterest_Search
                Thread_1 = threading.Thread(target=Pinterest_Search.Search, args=(self.query, self.task_id, "pin"), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Pinterest Board Search":
                import plugins.Pinterest_Search as Pinterest_Search
                Thread_1 = threading.Thread(target=Pinterest_Search.Search, args=(self.query, self.task_id, "board"), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Library Genesis Search":
                import plugins.Library_Genesis_Search as Library_Genesis_Search
                Thread_1 = threading.Thread(target=Library_Genesis_Search.Search, args=(self.query, self.task_id), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "iTunes Store Search":
                import plugins.ITunes_Store_Search as ITunes_Store_Search
                Thread_1 = threading.Thread(target=ITunes_Store_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Instagram User Search":
                import plugins.Instagram_Search as Instagram_Search
                Thread_1 = threading.Thread(target=Instagram_Search.Search, args=(self.query, self.task_id, "User"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Instagram Tag Search":
                import plugins.Instagram_Search as Instagram_Search
                Thread_1 = threading.Thread(target=Instagram_Search.Search, args=(self.query, self.task_id, "Tag"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Instagram Media Search":
                import plugins.Instagram_Search as Instagram_Search
                Thread_1 = threading.Thread(target=Instagram_Search.Search, args=(self.query, self.task_id, "Media"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Instagram Location Search":
                import plugins.Instagram_Search as Instagram_Search
                Thread_1 = threading.Thread(target=Instagram_Search.Search, args=(self.query, self.task_id, "Location"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Have I Been Pwned - Password Search":
                import plugins.Have_I_Been_Pwned as Have_I_Been_Pwned
                Thread_1 = threading.Thread(target=Have_I_Been_Pwned.Search, args=(self.query, self.task_id, "password"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Have I Been Pwned - Email Search":
                import plugins.Have_I_Been_Pwned as Have_I_Been_Pwned
                Thread_1 = threading.Thread(target=Have_I_Been_Pwned.Search, args=(self.query, self.task_id, "email"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Have I Been Pwned - Breach Search":
                import plugins.Have_I_Been_Pwned as Have_I_Been_Pwned
                Thread_1 = threading.Thread(target=Have_I_Been_Pwned.Search, args=(self.query, self.task_id, "breach"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Have I Been Pwned - Account Search":
                import plugins.Have_I_Been_Pwned as Have_I_Been_Pwned
                Thread_1 = threading.Thread(target=Have_I_Been_Pwned.Search, args=(self.query, self.task_id, "account"))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Google Search":
                import plugins.Google_Search as Google_Search
                Thread_1 = threading.Thread(target=Google_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Google Play Store Search":
                import plugins.Google_Play_Store_Search as Google_Play_Store_Search
                Thread_1 = threading.Thread(target=Google_Play_Store_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Flickr Search":
                import plugins.Flickr_Search as Flickr_Search
                Thread_1 = threading.Thread(target=Flickr_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Ebay Search":
                import plugins.Ebay_Search as Ebay_Search
                Thread_1 = threading.Thread(target=Ebay_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Domain Fuzzer - Regular Domain Suffixes":
                import plugins.Domain_Fuzzer as Domain_Fuzzer
                Domain_Fuzz_Obj = Domain_Fuzzer.Fuzzer(self.query, self.task_id)
                Thread_1 = threading.Thread(target=Domain_Fuzz_Obj.Regular_Extensions)
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Domain Fuzzer - Global Domain Suffixes":
                import plugins.Domain_Fuzzer as Domain_Fuzzer
                Domain_Fuzz_Obj = Domain_Fuzzer.Fuzzer(self.query, self.task_id)
                Thread_1 = threading.Thread(target=Domain_Fuzz_Obj.Global_Extensions)
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Domain Fuzzer - Punycode (Comprehensive)":
                import plugins.Domain_Fuzzer as Domain_Fuzzer
                Domain_Fuzz_Obj = Domain_Fuzzer.Fuzzer(self.query, self.task_id)
                Thread_1 = threading.Thread(target=Domain_Fuzz_Obj.Character_Switch, args=(True,))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Domain Fuzzer - Punycode (Condensed)":
                import plugins.Domain_Fuzzer as Domain_Fuzzer
                Domain_Fuzz_Obj = Domain_Fuzzer.Fuzzer(self.query, self.task_id)
                Thread_1 = threading.Thread(target=Domain_Fuzz_Obj.Character_Switch, args=(False,))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Domain Fuzzer - All Extensions":
                import plugins.Domain_Fuzzer as Domain_Fuzzer
                Domain_Fuzz_Obj = Domain_Fuzzer.Fuzzer(self.query, self.task_id)
                Thread_1 = threading.Thread(target=Domain_Fuzz_Obj.All_Extensions)
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "DNS Reconnaissance Search":
                import plugins.DNS_Recon_Search as DNS_Recon_Search
                Thread_1 = threading.Thread(target=DNS_Recon_Search.Search, args=(self.query, self.task_id,))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Default Password Search":
                import plugins.Default_Password_Search as Default_Password_Search
                Thread_1 = threading.Thread(target=Default_Password_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Ahmia Darkweb Search":
                import plugins.Ahmia_Darkweb_Search as Ahmia_Darkweb_Search
                Thread_1 = threading.Thread(target=Ahmia_Darkweb_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Craigslist Search":
                import plugins.Craigslist_Search as Craigslist_Search
                Thread_1 = threading.Thread(target=Craigslist_Search.Search, args=(self.query, self.task_id,), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Certificate Transparency":
                import plugins.Certificate_Transparency as Certificate_Transparency
                Thread_1 = threading.Thread(target=Certificate_Transparency.Search, args=(self.query, self.task_id,))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - United Kingdom Business Number":
                import plugins.UK_Business_Search as UK_Business_Search
                Thread_1 = threading.Thread(target=UK_Business_Search.Search, args=(self.query, self.task_id, "UKBN",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - United Kingdom Company Name":
                import plugins.UK_Business_Search as UK_Business_Search
                Thread_1 = threading.Thread(target=UK_Business_Search.Search, args=(self.query, self.task_id, "UKCN",), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - New Zealand Business Number":
                import plugins.NZ_Business_Search as NZ_Business_Search
                Thread_1 = threading.Thread(target=NZ_Business_Search.Search, args=(self.query, self.task_id, "NZBN",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - New Zealand Company Name":
                import plugins.NZ_Business_Search as NZ_Business_Search
                Thread_1 = threading.Thread(target=NZ_Business_Search.Search, args=(self.query, self.task_id, "NZCN",), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - Canadian Business Number":
                import plugins.Canadian_Business_Search as Canadian_Business_Search
                Thread_1 = threading.Thread(target=Canadian_Business_Search.Search, args=(self.query, self.task_id, "CBN",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - Canadian Company Name":
                import plugins.Canadian_Business_Search as Canadian_Business_Search
                Thread_1 = threading.Thread(target=Canadian_Business_Search.Search, args=(self.query, self.task_id, "CCN",), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - Australian Business Number":
                import plugins.Australian_Business_Search as Australian_Business_Search
                Thread_1 = threading.Thread(target=Australian_Business_Search.Search, args=(self.query, self.task_id, "ABN",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - Australian Company Name":
                import plugins.Australian_Business_Search as Australian_Business_Search
                Thread_1 = threading.Thread(target=Australian_Business_Search.Search, args=(self.query, self.task_id, "ACN",), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - American Central Index Key":
                import plugins.American_Business_Search as American_Business_Search
                Thread_1 = threading.Thread(target=American_Business_Search.Search, args=(self.query, self.task_id, "CIK",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Business Search - American Company Name":
                import plugins.American_Business_Search as American_Business_Search
                Thread_1 = threading.Thread(target=American_Business_Search.Search, args=(self.query, self.task_id, "ACN",), kwargs={"Limit": self.limit, })
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "BSB Search":
                import plugins.BSB_Search as BSB_Search
                Thread_1 = threading.Thread(target=BSB_Search.Search, args=(self.query, self.task_id))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Monero Transaction Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Transaction_Search, args=(self.query, self.task_id, "monero",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Ethereum Transaction Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Transaction_Search, args=(self.query, self.task_id, "eth",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Bitcoin Cash Transaction Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Transaction_Search, args=(self.query, self.task_id, "bch",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Bitcoin Transaction Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Transaction_Search, args=(self.query, self.task_id, "btc",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Ethereum Address Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Address_Search, args=(self.query, self.task_id, "eth",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Bitcoin Cash Address Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Address_Search, args=(self.query, self.task_id, "bch",))
                Thread_1.start()
                Thread_1.join()

            elif self.plugin_name == "Blockchain Bitcoin Address Search":
                import plugins.Blockchain_Search as Blockchain_Search
                Thread_1 = threading.Thread(target=Blockchain_Search.Address_Search, args=(self.query, self.task_id, "btc",))
                Thread_1.start()
                Thread_1.join()

        except Exception as e:
            logging.warning(f"{General.Date()} - Plugin Caller Error - {e}")
            
        Thread_2 = threading.Thread(target=Stopper, args=[self.task_id])
        Thread_2.start()
        
if __name__ == "__main__":
    import argparse, sys
    Parser = argparse.ArgumentParser(description='Plugin Caller calls Scrummage plugins.')
    Parser.add_argument('-t', '--task', help='This option is used to specify a task ID to run. ./plugin_caller.py -t 1')
    Arguments = Parser.parse_args()/pro

    Task_ID = 0

    if Arguments.task:

        try:
            Task_ID = int(Arguments.task)
            Connection = Connectors.Load_Main_Database()
            cursor = Connection.cursor()
            PSQL_Select_Query = 'SELECT * FROM tasks WHERE task_id = %s;'
            cursor.execute(PSQL_Select_Query, (Task_ID,))
            result = cursor.fetchone()

            if result:
                print(result[2])
                print(result[5])
                Plugin_to_Call = Plugin_Caller(Plugin_Name=result[2], Limit=result[5], Task_ID=Task_ID, Query=result[1])
                Plugin_to_Call.Call_Plugin()

        except:
            sys.exit("[-] Invalid Task ID, please provide a valid Task ID")
