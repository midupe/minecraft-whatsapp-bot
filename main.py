from mcstatus import JavaServer
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def sendWhatsapp(text):
    text = str(text).replace('\n', '')
    if not text: #not empty
        return
    if not text.startswith('<') and not text.startswith('O servidor ') and not "left the game" in text and not "joined the game":
        text = '💀👋💩 *' + text + '*'
    elif text.startswith('O servidor '):
        text = '⚠️ *' + text + '*'
    else:
        text = '_' + text + '_'

    print(text)
    driver.find_element(By.XPATH, """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]""").click() #Sitio de escrever a msg
    time.sleep(1)
    driver.find_element(By.XPATH, """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]""").send_keys(text)
    driver.find_element(By.XPATH, """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]""").send_keys(Keys.RETURN)

def online_players():
    try:
        server = JavaServer.lookup("mc.midupe.pt")
        query = server.query()
        sendWhatsapp(f"O servidor tem {len(query.players.names)} players online: {', '.join(query.players.names)}")
    except:
        sendWhatsapp("O servidor está offline!")


def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line



#Iniciar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Miguel\\AppData\\Local\\Google\\Chrome\\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument('--profile-directory=Profile 7') #e.g. Profile 3
driver = webdriver.Chrome(executable_path=r'C:\\Users\\Miguel\\Coding\\minecraft-whatsapp-bot\\driver\\chromedriver.exe', chrome_options=options)
driver.get("https://web.whatsapp.com/")
print('ESCOLHER CONVERSA')
time.sleep(20)
#----------------

timecounter = time.time()
online_players()
logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
loglines = follow(logfile)
for line in loglines:
    if "[Render thread/INFO]: [CHAT]" in line:
        sendWhatsapp(line[40:])
    if time.time()-timecounter > 60*15:
        online_players()
        timecounter = time.time() #reset

