# 15.01.2023
# Author: @mertcantoglu
# https://www.maxbet.rs/ibet-web-client/#/home/game/spribe/aviator tracker for @Highlinkseo


from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from telegram_sender import Sender

TOKEN = "7675002602:AAEyW_J6wQQMoCpzEKQY96KuGTg8D_o_wOc" #Your token that you got the BotFather
USERNAME = "yannbot570@gmail.com" #YOUR-EMAIL
PASSWORD = "yannbot@237" #YOUR-PASSWORD
numberOfConsec = 3 #Number of consecutive
ratio = 2.0 #Trigger ratio. Ex: (Bets below 2.00x.)
url = "https://www.maxbet.rs/ibet-web-client/#/home/game/spribe/aviator"

def login():
    while(not checkLogin()):
        try:
            driver.switch_to.default_content()
            log_but = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/input').click()
            time.sleep(1)
            mail = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[1]')
            password = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[2]')
            mail.send_keys(USERNAME)
            time.sleep(1)
            password.send_keys(PASSWORD)
            log_but = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[4]').click()
            time.sleep(10)
            login_flag=checkLogin()
        except:
            print("Login attempt failed. I'm trying again.")
    print("Logging successfuly.")    
    
def checkLogin():
    driver.switch_to.default_content()
    username = driver.find_elements_by_class_name("profile-and-gifts-wrapper")
    if len(username) > 0 and username[0].text:
        return True
    else: return False
    
    
def iframe():
    iframe_flag = False
    while(not iframe_flag):
        try:
            iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "seven-plugin")))
            driver.switch_to.frame(iframe)
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='button-block'])//div/div")))
            button.click()
            iframe_flag = True
        except:
            pass
    


def get_blocks():
    rates = []
    while(len(rates) == 0):
        try:
            blocks = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "(//div[@class='payouts-block'])[1]//app-payout-item/div")))
            for block in blocks:
                if block.text != '':
                    rates.append(float(block.text.replace('x','')))
            if(len(rates) != 0):
                return rates
        except:
            pass
    
    
def checkTrigger(rates, ratio):
    string = "".join(["Y" if rate < ratio else "N" for rate in rates ])
    counter = 0
    for i in string:
        if i == "Y":
            counter+=1
        else: break
    return counter
    
    
def send_msg(rates, numberOfConsec):
    try:
        sender.send_msg(f"!Alert Aviator has {numberOfConsec} blue in a row.")
        sender.send_msg(f"Last {len(rates)} round: " +  ", ".join([f"{rate}x" for rate in rates ]))
    except: 
        print("Message service has a problem. Check your tokens")
    
    
    # <span ng-if="profileInfo.config != 'ug'" class="ng-binding ng-scope">mert</span>
    # //*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[2]/div[1]/div/div[1]/div[2]/span

print("Welcome to Aviator Tracker Bot..")
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
sender = Sender(TOKEN)
driver.get(url)
time.sleep(10)
login()
time.sleep(1)
iframe()
time.sleep(1)
old_rates = []
while True:
    try:
        if checkLogin():
            iframe()
            rates = get_blocks()
            if old_rates != rates:
                print(f"Last {len(rates)} round: " +  ", ".join([f"{rate}x" for rate in rates ]))
                count= checkTrigger(rates,ratio)
                if count >= numberOfConsec:
                    print(f"!Alert Aviator has {count} blue in a row. Message sending via Telegram.")
                    send_msg(rates,count)
            time.sleep(3)
            old_rates = rates
        else:
            driver.refresh()
            time.sleep(3)
            login()
    except:
        pass
    



