**If you're enjoying this tool, feel free to buy me a cup of coffee :)**  
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/matamorphosis?locale.x=en_AU)

# Scrummage  
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  
**VERSION 2.5**
- Major UI Improvements.
- Lots of New Plugins. Read more [here](https://github.com/matamorphosis/Scrummage/wiki/The-Long-List-of-Tasks).
- Code enhancements.
- More verbose result types.
- New API endpoints to manage tasks, results, accounts, etc. Refer to the [Wiki Page](https://github.com/matamorphosis/Scrummage/wiki/The-Scrummage-API).
   
**There is currently a known bug with the Google Play Store plugin.**

Scrummage is an OSINT tool that centralises search functionality from powerful, yet simple OSINT sites. This project draws inspiration mainly from two other projects, including:  
- The https://github.com/Netflix-Skunkworks/Scumblr project, which while is now deprecated, inspired this concept.
- The OSINT framework, a high-level overview of a range of sites that can be used to search for a variety of things, which can be found at https://osintframework.com/ or https://github.com/lockfale/OSINT-Framework.

While at first glance the web application may not look that original when compared to Scumblr, the plugins this tool uses is mainly what makes this project unique, where the provided Python/Flask web application is just a simple, lightweight, and scalable way of providing users with the ability to manage large pools of results. The other main benefit this projects brags is a simpler, up-to-date installation process. 

Any feedback is welcome.

**FOR INSTRUCTIONS REFER TO THE [WIKI](https://github.com/matamorphosis/Scrummage/wiki)**

# An Overview of the Web Application

**Some of the Available Plugins**  
* Blockchain Search
* Domain Fuzzer
* Twitter Scraper
* Instagram Search
* Have I Been Pwned Search
* Ahmia Darkweb Search
* Many more... Refer to the "Long List of Tasks" Wiki file for the full list.

---

**Dashboard**  
The dashboard is the home screen which the application directs a user to when they log in. It provides a high-level chart which shows the amount of each results based on their result type. It does this for each kind of finding. However, if a graph doesn’t load, this is most likely due to none of the results being in that category, I.e if there are no closed results, no graph will appear under “Overview of Closed Results”.  




**Events**  
The events page shows anything that changes within the web application, from logins, to failed login attempts, to any actions performed against a task. This assists with understanding what has recently been happening in the web app, and can assist in matters such as detecting brute-force login attempts or tracking down who altered a task.  
  
*Note: This page only loads the latest 1000 events, for optimisation of the web application.*  

![Events](/installation/images_dark_theme/Events.png)


**Results**  
The results page, simply shows results that have been created by a task. The results table shows the basic metadata of the result, but also provides a “Details” button which can be used to investigate the result further. As mentioned all results have some kind of output file, if a result is a link the file will be a copy of the HTML of the page. Furthermore screenshot functionality is provided to assist in keeping a photographic record of a result. Both the output and screenshot file will be deleted if the result is deleted.  
  
*Note: This page only loads the latest 1000 results, for optimisation of the web application.*  

![Results](/installation/images_dark_theme/Results.png)

For optimisation purposes, the results table only displays some of the general information regarding a result, to investigate a result further, the user should use the Details button. The details page allows the user to view the soft copy of the result's link and provides the ability for a user to generate a screenshot.  
  
![Results](/installation/images_dark_theme/Result_Details1.png)

*Results are categorised into the following:*  
* Data Leakage
* Domain Spoof
* Phishing
* Exploit
* Blockchain Address
* Blockchain Transaction

**Tasks**  
The tasks page shows all created task, and provides the ability for the user to run each task.
This page doesn’t have a limit on tasks; however, don’t go crazy creating tasks, you can always add a list to a task, rather than having the same task created multiple times for one search. So really you shouldn’t have any more than 50 tasks.
Tasks have caching and logging for each which can be found in the “protected/output” directory under the tasks name, ex. Google Search is called “google”. If you need to remove the cache, you can edit/delete the appropriate cache file.
  
![Tasks](/installation/images_dark_theme/Tasks.png)

All the plugins are open-source, free to individuals, just like the rest of the code. Furthermore, feel free to use the pre-existing libraries used in other plugins. If you are creating or editting a plugin, make sure to understand that when you run it for the first time, the web app may reload to reload the python cache. This is normal.

**Account**
This page changes according to the user's privileges, if a user is an admin, they have the ability to change their password as well as other user's passwords, they can block/unblock users, demote/promote users' privileges. They can also create new users and delete existing users. The account page looks as per below for administrative users:

![Account](/installation/images_dark_theme/Account.png)

The account page looks as per below for non-administrative users:

![AccountLP](/installation/images_dark_theme/Account_Low_Priv.png)

**Developer Information**  
***Contributions Welcome!!***  
Knock yourself out, create any plugins you like, and feel free to leverage existing libraries to help you. Refer to the plugin development guide [here](https://github.com/matamorphosis/Scrummage/wiki/Plugin-Development-Guide).
