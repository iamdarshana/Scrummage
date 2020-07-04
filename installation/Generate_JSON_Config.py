import argparse, sys, os, secrets

Parser = argparse.ArgumentParser(description='To create users.')
Parser.add_argument('-d', '--database')
Parser.add_argument('-u', '--username')
Parser.add_argument('-p', '--password')
Arguments = Parser.parse_args()

if Arguments.database and Arguments.username and Arguments.password:

    if any(Char in Arguments.database or Char in Arguments.username or Char in Arguments.password for Char in ["\"", "'"]):
        sys.exit("[-] Bad character, please remove any quotes from the provided arguments.")

    try:
        API_Secret = secrets.token_hex(32)
        Config_Directory = '../lib/plugins/common/config'
        Configuration_File = os.path.join(Config_Directory, 'config.json')
        Open_File = open(Configuration_File,"w+")

        JSON_Payload = '''{
            "craigslist": {
                "city": "Sydney"
            },
            "csv": {
                "use-csv": false
            },
            "docx-report": {
                "use-docx": false
            },
            "defectdojo": {
                "api_key": "",
                "host": "https://host.com",
                "user": "admin",
                "engagement-id": 1,
                "product-id": 1,
                "test-id": 1,
                "user-id": 1
            },
            "ebay": {
                "access_key": ""
            },
            "email": {
                "smtp_server": "",
                "smtp_port": 25,
                "from_address": "",
                "from_password": "",
                "to_address": ""
            },
            "flickr": {
                "api_key": "",
                "api_secret": ""
            },
            "elasticsearch": {
                "service": "http://",
                "host": "",
                "port": 9200
            },
            "general": {
                "location": "au"
            },
            "google": {
                "cx": "",
                "application_name": "",
                "application_version": "v1",
                "developer_key": ""
            },
            "google-chrome": {
                "application-path": "/usr/bin/google-chrome",
                "chromedriver-path": "/usr/bin/chromedriver"
            },
            "haveibeenpwned": {
                "api_key": ""
            },
            "JIRA": {
                "project_key": "",
                "address": "",
                "username": "",
                "password": "",
                "ticket_type": ""
            },
            "pinterest": {
                "oauth_token": ""
            },
            "postgresql": {
                "host": "127.0.0.1",
                "port": 5432,
                "database": "''' + Arguments.database + '''",
                "user": "''' + Arguments.username + '''",
                "password": "''' + Arguments.password + '''"
            },
            "reddit": {
                "client_id": "",
                "client_secret": "",
                "user_agent": "",
                "username": "",
                "password": "",
                "subreddits": "all"
            },
            "rtir": {
                "service": "http",
                "host": "",
                "port": 80,
                "user": "",
                "password": "",
                "authenticator": ""
            },
            "scumblr": {
                "host": "",
                "port": 5432,
                "database": "",
                "user": "",
                "password": ""
            },
            "slack": {
                "token": "",
                "channel": ""
            },
            "sslmate": {
                "search_subdomain": false
            },
            "twitter": {
                "CONSUMER_KEY": "",
                "CONSUMER_SECRET": "",
                "ACCESS_KEY": "",
                "ACCESS_SECRET": ""
            },
            "ukbusiness": {
                "api_key": ""
            },
            "vulners": {
                "api_key": ""
            },
            "web-app": {
                "debug": false,
                "host": "127.0.0.1",
                "port": 5000,
                "certificate-file": "../certs/certificate.crt",
                "key-file": "../certs/privateKey.key",
                "api-secret": "''' + API_Secret + '''",
                "api-validity-minutes": 1440,
                "api-max-calls": 10,
                "api-period-in-seconds": 60
            },
            "youtube": {
                "developer_key": "",
                "application_name": "",
                "application_version": "v3",
                "location": "37.42307,-122.08427",
                "location_radius": "5km"
            }
        }'''

        Open_File.write(JSON_Payload)
        Open_File.close()
        print('[+] Generated main configuration file (config.json).')

    except:
        sys.exit('[-] Failed to write to file.')
