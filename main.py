import requests
import os 
import re 
import time 
import shutil
from bs4 import BeautifulSoup as bs
from colorama import init,Fore 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

start_time = time.time()

init(convert=True if os.name == "nt" else False,autoreset=True)
try: 
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Made output folder.')
    os.mkdir('output')
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Made assets folder')
    os.mkdir('output/assets')
except:
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}*{Fore.LIGHTBLACK_EX}]{Fore.WHITE} output folder found, deleting it!')
    shutil.rmtree('output')
    os.mkdir('output')
    os.mkdir('output/assets')

print(f"""{Fore.LIGHTMAGENTA_EX}
╔╦╗┬┌─┐┌─┐┌─┐┬─┐┌┬┐  ╔═╗┬  ┬┌─┐┌┐┌┌┬┐  ╔╦╗┌─┐┬ ┬┌┐┌┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
 ║║│└─┐│  │ │├┬┘ ││  ║  │  │├┤ │││ │    ║║│ ││││││││  │ │├─┤ ││├┤ ├┬┘
═╩╝┴└─┘└─┘└─┘┴└──┴┘  ╚═╝┴─┘┴└─┘┘└┘ ┴   ═╩╝└─┘└┴┘┘└┘┴─┘└─┘┴ ┴─┴┘└─┘┴└─
                                                                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                             

{Fore.LIGHTGREEN_EX}Made by happy enderman. 
""")


assets_pattern = r'/assets/[a-z0-9.]+\.[a-zA-Z]+'


channel = input(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTCYAN_EX}>{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Enter the chanel: (stable, canary, ptb) [default: stable]')
if not channel in ['stable',"canary","ptb"]:
    channel = "stable"
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}*{Fore.LIGHTBLACK_EX}]{Fore.WHITE} channel not valid, using stable as default')


data = {
    "mainJS":"",
    "mainCSS":""
}

def getURL(path):
    return "https://discord.com" + path if channel == "stable" else f"https://{channel}.discord.com" + path
    

def save():
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Downloading assets of main page, and html of it')

    r = requests.get(getURL("/"))
    with open('output/index.html','a+',encoding="utf-8") as f:
        soup = bs(r.text,"html.parser")
        bueatifiedHTML = soup.prettify()
        pattern = r'integrity="([^"]*)"'
        integrity_values = re.findall(pattern, bueatifiedHTML)

        for value in integrity_values:
            bueatifiedHTML = bueatifiedHTML.replace("integrity="+'"'+value+'"',"")                
                    
        f.write(bueatifiedHTML)
    assets = re.findall(assets_pattern,r.text)
    for asset in assets:
        if not os.path.isfile("output"+asset):
            with open(f'output{asset}','a+',encoding="utf-8") as f:
                f.write(requests.get(getURL(asset)).text)
                print(f'{Fore.LIGHTGREEN_EX}+ {Fore.LIGHTBLACK_EX}{asset}')

    print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE}Downloading assets of app page, and html of it")
    
    r = requests.get(getURL("/app"))
    with open('output/app.html','a+',encoding="utf-8") as f:
        soup = bs(r.text,"html.parser")
        bueatifiedHTML = soup.prettify()
        pattern = r'integrity="([^"]*)"'
        integrity_values = re.findall(pattern, bueatifiedHTML)

        for value in integrity_values:
            bueatifiedHTML = bueatifiedHTML.replace("integrity="+'"'+value+'"',"")
        f.write(bueatifiedHTML)

    assets = re.findall(assets_pattern,r.text)
    for asset in assets:
        if not os.path.isfile("output"+asset):
            with open(f'output{asset}','a+',encoding="utf-8") as f:
                f.write(requests.get(getURL(asset)).text)
                print(f'{Fore.LIGHTGREEN_EX}+ {Fore.LIGHTBLACK_EX}{asset}')

    print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE}Downloading assets of login page, and html of it")
    
    options = FirefoxOptions()
    options.add_argument("-headless")
    options.set_preference('intl.accept_languages', 'en-GB')
    driver = webdriver.Firefox(options=options)

    driver.get(getURL("/login"))

    while True:
        if driver.execute_script('return document.readyState') == "complete" and 'src="/assets/092b071c3b3141a58787415450c27857.png"' in driver.execute_script('return document.querySelector("html").innerHTML'):
            h = driver.execute_script('return document.querySelector("html").innerHTML')
      
            with open('output/login.html','a+',encoding="utf-8") as f:
                soup = bs(h,"html.parser")
                bueatifiedHTML = soup.prettify()
                pattern = r'integrity="([^"]*)"'
                integrity_values = re.findall(pattern, bueatifiedHTML)

                for value in integrity_values:
                    bueatifiedHTML = bueatifiedHTML.replace("integrity="+'"'+value+'"',"")                
                f.write(bueatifiedHTML)
            
            assets = re.findall(assets_pattern,h)
            for asset in assets:
                if not os.path.isfile("output"+asset):
                    with open(f'output{asset}','a+',encoding="utf-8") as f:
                        f.write(requests.get(getURL(asset)).text)
                        print(f'{Fore.LIGHTGREEN_EX}+ {Fore.LIGHTBLACK_EX}{asset}')
            data['mainJS'] = driver.execute_script("return document.querySelectorAll('script[src]')[3].src")
            data['mainCSS'] = driver.execute_script("return document.querySelectorAll('link[rel=\"stylesheet\"]')[0].href")

            driver.close()
            break; 
            
    print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTBLACK_EX}]{Fore.WHITE}Downloading assets of register page, and html of it")
    
    options = FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(getURL("register"))
    
    while True:
        if driver.execute_script('return document.readyState') == "complete" and 'Already have an account?' in driver.execute_script('return document.querySelector("html").innerHTML'):
            h = driver.execute_script('return document.querySelector("html").innerHTML')
            with open('output/register.html','a+',encoding="utf-8") as f:
                soup = bs(h,"html.parser")
                bueatifiedHTML = soup.prettify()
                pattern = r'integrity="([^"]*)"'
                integrity_values = re.findall(pattern, bueatifiedHTML)

                for value in integrity_values:
                    bueatifiedHTML = bueatifiedHTML.replace("integrity="+'"'+value+'"',"")
                f.write(bueatifiedHTML)
            assets = re.findall(assets_pattern,h)
            for asset in assets:
                if not os.path.isfile("output"+asset):
                    with open(f'output{asset}','a+',encoding="utf-8") as f:
                        f.write(requests.get(getURL(asset)).text)
                        print(f'{Fore.LIGHTGREEN_EX}+ {Fore.LIGHTBLACK_EX}{asset}')

            driver.close()
            break; 
    return "done"



save()
end_time = time.time()
print(f"""         
{Fore.LIGHTGREEN_EX}Done, here is the informations:     

    ----> {Fore.LIGHTYELLOW_EX}Time taken:   {Fore.LIGHTBLUE_EX}{end_time - start_time} seconds                            
    ----> {Fore.LIGHTYELLOW_EX}Assets count: {Fore.LIGHTBLUE_EX}{len(os.listdir("output/assets"))}                                
    ----> {Fore.LIGHTYELLOW_EX}Main JS file: {Fore.LIGHTMAGENTA_EX}{data.get('mainJS')}                                 
    ----> {Fore.LIGHTYELLOW_EX}Main CSS file: {Fore.LIGHTMAGENTA_EX}{data.get('mainCSS')} 
         

""")