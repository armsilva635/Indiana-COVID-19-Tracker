import re
import urllib.request
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from datetime import datetime

def getData():
    # Pulls Indiana data from Indiana.gov website
    
    url = "https://hub.mph.in.gov/dataset/covid-19-county-statistics/resource/8b8e6cd7-ede2-4c41-a9bd-4266df783145?inner_span=True"
    web_page = urllib.request.urlopen(url)
    html = web_page.read().decode(errors='replace')
    web_page.close()

    body = re.findall('(?<=<div class="btn-group">).+?(?=</a>)',html, re.DOTALL)
    link = re.findall('(?<=href=").+?(?=">\n)',body[0],re.DOTALL)

    resp = requests.get(link[0])

    # Downloads excel sheet with given data
    
    output = open('data.xls', 'wb')
    output.write(resp.content)
    output.close()
    
def email(email, password, to, subject, message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
        {}
      </body>
    </html>
    """
    part1=MIMEText(html.format(message), 'html')

    msg.attach(part1)

    # SMTP Gmail port 587 or 465
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(email,password)
    s.sendmail(email, to, msg.as_string())
    s.quit()

def countyMessage(county, count, deaths, tests):
    countyM = """
    <h3>{} County</h3>
    Count: {}<br>
    Deaths: {}<br>
    Tests: {}<br>
    """
    message = countyM.format(county, "{:,}".format(count), "{:,}".format(deaths), "{:,}".format(tests))
    return message

def stateMessage(count, deaths, tests):
    totalM = """
    <h3>State Total</h3>
    Count: {}<br>
    Deaths: {}<br>
    Tests: {}<br>
    """
    return totalM.format("{:,}".format(count), "{:,}".format(deaths), "{:,}".format(tests))

def usaData():
    # Pulls US data from worldmeters.info
    
    url ="https://www.worldometers.info/coronavirus/country/us/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('utf-8')

    title = re.findall('(?<=<title>).+?(?=</title>)',webpage, re.DOTALL)
    US = title[0].replace("- Worldometer",'').split()

    cases = int(US[3].replace(",",""))
    
    m = """
    <h3>United States</h3>
    Count: {}<br>
    Deaths: {}<br>
    """
    
    return cases, m.format(US[3], US[6])

def news():
    # Displays top 5 articles pulled from Reuters
    
    url= "https://www.reuters.com/news/us"
    web_page = urllib.request.urlopen(url)
    html = web_page.read().decode(errors='replace')
    web_page.close()

    body = re.findall('(?<=<section  class="module  ">).+?(?=</section>)',html, re.DOTALL)

    link = re.findall('(?<=<div class="story-content">).+?(?=</time>)',html,re.DOTALL)
    
    message = "<h3>Top COVID-19 News</h3><ul>"
    for url in link[:5]:
        title = re.findall('(?<=<h3 class="story-title">).+?(?=</h3>)',url, re.DOTALL)
        url = re.findall('(?<=href=").+?(?=">)',url, re.DOTALL)
        hyperlink = "<li><a href="+"https://www.reuters.com/"+url[0]+">"+title[0]+"</a></li>"
        message += hyperlink

    # Time stamp of last updated    
    message += "</ul>"
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    time = "<br>Last updated: "+dt_string
    message += time
    
    return message
