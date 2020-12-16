# Indiana COVID-19 Tracker

<h2>About</h2>
This program was created due to the COVID-19 pandemic in which allows users to track current cases in Indiana. With information coming from trusted sources (Indiana.gov, Worldometer.info, and Reuters.com) users can stay informed of the current situation in their county, region, and state. 

<h2>Goal and requirements</h2>

The goal was to stay informed of the numbers in the area. In order for this program to work properly, the program must be constantly running. For best use, I recommend running program on a Raspberry Pi or any computer that can remain in a on-state.  
This program will email an HTML message containing current COVID-19 cases, deaths, and tests. As the numbers change, the next email sent reflects the number of cases that has changed. Additionally in the email, the top five news article are included with their respective links to their sites. 

<h2>Installation</h2>

1. Download this project as zip and extract it.
2. Open credentials.txt and insert your Gmail email and password. 
3. Open emails.txt and enter email of recipients.
4. Using IDLE or preferred Python IDE, open covid_tracker1.py.
4. In the file, update the counties you are interested in with their respective county number found in the data.xls file. 
5. Save and run the program.
5. Leave the program running.

<h2>Project status</h2>
As the code in the websites change, web scraping must be adjusted. 