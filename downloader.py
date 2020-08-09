import os,sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



save_Path = "D:/aSelenumTmp"
driverPath = "D:/YOUR_PATH/chromedriver.exe"

your_email = ""
your_password = ""
#example: user_to_scrap = "zuck"
user_to_scrap = ""




options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r"%s"%save_Path.replace("/","\\")}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(driverPath,options=options) # Chrome
wait = WebDriverWait(driver,5)
actions = ActionChains(driver)
driver.maximize_window()


###Load what already dowmloaded
dirs = os.listdir(save_Path+"/")



driver.get("https://www.facebook.com/")
time.sleep(2)
###Login
driver.find_element_by_name("email").send_keys(your_email)
driver.find_element_by_name("pass").send_keys(your_password)
try:
    driver.find_element_by_id("loginbutton").click()
except:
    driver.find_element_by_name("login").click()

time.sleep(3)


driver.get("https://www.facebook.com/"+user_to_scrap+"/photos_all")
time.sleep(2)


#get Current photo name
toDoAllPhotoList = driver.find_elements_by_xpath(".//i[@class='uiMediaThumbImg']")
toDoAllPhotoList[0].click()

curJpgName = wait.until(EC.presence_of_element_located((By.XPATH,".//div[@class='_2-sx']/img"))).get_attribute("src")
starJpgName = curJpgName
while True:

    for onedir in dirs:
        if onedir in curJpgName:
            #print("[Has Download]",onedir)
            break
        if onedir == dirs[-1]:
            #print("[Downloading...]",curJpgName)
            #download  >>location_once_scrolled_into_view
            try:
                wait.until(EC.presence_of_element_located((By.XPATH,".//div[@class='_6a _6b uiPopover bottomBarActions _5v-0']"))).click()
                wait.until(EC.presence_of_element_located((By.XPATH,".//div[@class='uiContextualLayerPositioner uiLayer']/div/div/div/ul/li[@data-action-type='download_photo']"))).click()
            except:
                print("[no download btn]",curJpgName)
                print(current_url)
                continue

    #next page
    wait.until(EC.presence_of_element_located((By.XPATH,".//a[@class='snowliftPager next hilightPager']"))).click()
    #next page's name
    curJpgName = wait.until(EC.presence_of_element_located((By.XPATH,".//div[@class='_2-sx']/img"))).get_attribute("src")
    if starJpgName == curJpgName:
        print("[ALL DONE ！]")
        break
