import sys, re, time, csv, random, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd
from bs4 import BeautifulSoup
from selenium.common import exceptions
from csv import DictReader
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage, GoogleV3, OpenMapQuest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from fake_useragent import UserAgent
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

def delay ():
    time.sleep(random.randint(2,3))


arcgis = ArcGIS(timeout=100)
nominatim = Nominatim(timeout=100,user_agent="Visualizer")
googlev3 = GoogleV3(timeout=100)
geocoders = [arcgis, googlev3, nominatim]

def geocode(address):
    i = 0
    try:
        while i < len(geocoders):
            location = geocoders[i].geocode(address)
            if location != None:
                return [location.latitude, location.longitude]
            else:
                i += 1
    except:
        print(sys.exc_info()[0])
        return ['null','null']
    return ['null','null']


def evaluate(x):
    print(x)


myFile = open('infolinkedinscraped4.csv', 'w', newline='')
with myFile:
    writer = csv.writer(myFile)
    with open('linkedInfoclutch4.csv', 'r', errors='ignore') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        i = 0
        for row in csv_dict_reader:
            i +=1
            url = row['linkedin_URL']
            EMAIL = 'kevinopix@mail.com'
            PASSWORD = 'pa00037011'
            options = ChromeOptions()
            ua = UserAgent()
            userAgent = ua.random
            #print(userAgent)
            options.add_argument(f'user-agent={userAgent}')
            #options.add_argument("--incognito")
            #options.headless = True
            DRIVER_PATH = r'/usr/local/bin/chromedriver'
            driver=webdriver.Chrome(options=options,executable_path=DRIVER_PATH) 
            #driver = webdriver.Chrome()
            URL = url
            ib = URL + "/about/"
            if len(URL)>1 and 'https://www.linkedin.com' in URL:
                driver.get(URL)
                time.sleep(5)
                try:
                    #driver.find_element_by_id('captcha-internal')
                    driver.find_element_by_class_name("""join-form""")
                    driver.find_element_by_class_name("""login__form""")
                    driver.find_element_by_class_name("""section-container__title""")
                except:
                    pass
                # if driver.find_element_by_id('captcha-internal'):
                #     framez=driver.find_elements_by_tag_name("iframe")
                #     print(framez)
                #     driver.switch_to.frame(framez[-1]);
                #     delay()
                #     print(driver.find_element_by_class_name('audioBtn').get_attribute('aria-label'))
                #     pass
                if driver.find_element_by_class_name("""join-form"""):
                    driver.find_element_by_xpath('/html/body/main/div/div/form[2]/section/p/a').click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-email'))).send_keys(EMAIL)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-password'))).send_keys(PASSWORD)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-submit'))).click()
                    #driver.switch_to.default_content()
                    try:
                        if driver.find_element_by_xpath('//*[@id="captcha-internal"]'):
                            frames=driver.find_elements_by_tag_name("iframe")
                            print(frames)
                            print(len(frames))
                            driver.switch_to.frame(frames[-1]);
                            delay()
                            driver.find_elements_by_tag_name("iframe")[0].click()
                            delay()
                            framez=driver.find_elements_by_tag_name("iframe")
                            driver.switch_to.frame(framez[-1]);
                            delay()
                            #print(driver.find_element_by_id('recaptcha-audio-button').get_attribute('class'))
                            try:
                                driver.find_element_by_id('recaptcha-audio-button').click()
                                delay()
                                #driver.switch_to.default_content()
                                #frames2= driver.find_elements_by_tag_name("iframe")
                                #print(frames2)
                                #driver.switch_to.frame(frames2[0])
                                #delay()
                                if driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button"): 
                                    driver.find_element_by_xpath('/html/body/div/div/div[3]/div/button').click()
                                    src = driver.find_element_by_id("audio-source").get_attribute("src")
                                    print("[INFO] Audio src: %s"%src)
                                    urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
                                    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
                                    sound.export(os.getcwd()+"\\sample.wav", format="wav")
                                    sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
                                    r= sr.Recognizer()
                                    with sample_audio as source:
                                        audio = r.record(source)
                                    #translate audio to text with google voice recognition
                                    key=r.recognize_google(audio)
                                    print("[INFO] Recaptcha Passcode: %s"%key)
                                    time.sleep(5)
                                    driver.find_element_by_id("audio-response").send_keys(key.lower())
                                    time.sleep(5)
                                    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
                                    driver.switch_to.default_content()
                                    delay()
                                    driver.find_element_by_id("recaptcha-verify-button").click()
                                    delay()
                                else:
                                    driver.find_element_by_id("/html/body/div[1]/form/fieldset/ul/li[6]/input").click()
                                    delay()
                            except:
                                while driver.find_element_by_id('captcha-internal'):
                                    framez=driver.find_elements_by_tag_name("iframe")
                                    print(framez)
                                    driver.switch_to.frame(framez[-1]);
                                    delay()
                                    print(driver.find_element_by_id(':4').get_attribute('class'))
                                    driver.find_element_by_class_name('rc-button-default').click()  
                                    src = driver.find_element_by_id("audio-source").get_attribute("src")
                                    print("[INFO] Audio src: %s"%src)
                                    urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
                                    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
                                    sound.export(os.getcwd()+"\\sample.wav", format="wav")
                                    sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
                                    r= sr.Recognizer()
                                    with sample_audio as source:
                                        audio = r.record(source)
                                    #translate audio to text with google voice recognition
                                    key=r.recognize_google(audio)
                                    print("[INFO] Recaptcha Passcode: %s"%key)
                                    #key in results and submit
                                    driver.find_element_by_id("audio-response").send_keys(key.lower())
                                    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
                                    driver.switch_to.default_content()
                                    delay()
                                    driver.find_element_by_id("recaptcha-verify-button").click()
                                    delay()
                    except:
                        try:
                            if driver.find_element_by_class_name("""section-container__title"""):
                                title = driver.find_element_by_class_name("""top-card-layout__title""").text
                                driver.find_element_by_class_name("""about-us__basic-info-list""")
                                soup = BeautifulSoup(driver.page_source, "html.parser")
                                dl_data = soup.find_all("dd")
                                dt_data = soup.find_all("dt")
                                jaba = []
                                jaba2 = []
                                for each in dl_data:
                                    ite = each.text.strip().replace('\n','')
                                    jaba.append(ite)
                                for each in dt_data:
                                    ite2 = each.text.strip().replace('\n','')
                                    jaba2.append(ite2)
                                jaba = [ x for x in jaba if "on LinkedIn" not in x ]  
                                cdf = pd.DataFrame()
                                cdf['each'] = ["Website", "Phone","Industry", "Company size", "Headquarters","Type","Founded","Specialties"]
                                cdf['val2'] = ''
                                df = pd.DataFrame()
                                df['each'] = jaba2 
                                df['val'] = jaba 
                                fin = pd.merge(cdf,df,on=['each'], how='left').fillna('')
                                valus = fin['val'].tolist()
                                print(valus)
                                website = valus[0]
                                phone = valus[1].split(' ')[0]
                                industry = valus[2]
                                co_size = valus[3] 
                                hq = valus[4]
                                typ = valus[5]
                                founded = valus[6]
                                specialities = valus[7]
                                location = driver.find_element_by_class_name('locations__location').text.replace('Get directions','').replace('Primary','').split('to')[0]
                                location = location.replace('\n',' ').strip()
                                latlngz = geocode(str(location))
                                #print(latlngz)
                                latitude = latlngz[0]
                                longitude = latlngz[1]
                                if location is None or latitude is None or latitude is None:
                                    location = ''
                                    latitude = ''
                                    longitude = ''
                                out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, location,latitude,longitude]
                                print(out) 
                                writer.writerow(out)
                                driver.quit()
                                delay()
                            else:
                                pass
                        except:
                            try:
                                if driver.find_element_by_class_name('unsupported-page'):
                                    DRIVER_PATH2 = r'/usr/local/bin/geckodriver'
                                    driver=webdriver.Firefox(executable_path=DRIVER_PATH2) 
                                    driver.get(URL)
                                    time.sleep(5)
                                    if driver.find_element_by_class_name("""join-form"""):
                                        driver.find_element_by_xpath('/html/body/main/div/div/form[2]/section/p/a').click()
                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-email'))).send_keys(EMAIL)
                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-password'))).send_keys(PASSWORD)
                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-submit'))).click()
                                    else:
                                        pass
                                    driver.get(ib)
                                    if driver.find_element_by_class_name("""org-organization-page__container"""):
                                        title = driver.find_element_by_class_name("""org-top-card-summary__title""").text
                                        driver.find_element_by_class_name("""artdeco-card""")
                                        soup = BeautifulSoup(driver.page_source, "html.parser")
                                        dl_data = soup.find_all("dd")
                                        dt_data = soup.find_all("dt")
                                        jaba = []
                                        jaba2 = []
                                        for each in dl_data:
                                            ite = each.text.strip().replace('\n','')
                                            jaba.append(ite)
                                        for each in dt_data:
                                            ite2 = each.text.strip().replace('\n','')
                                            jaba2.append(ite2)
                                        jaba = [ x for x in jaba if "on LinkedIn" not in x ]  
                                        cdf = pd.DataFrame()
                                        cdf['each'] = ["Website", "Phone","Industry", "Company size", "Headquarters","Type","Founded","Specialties"]
                                        cdf['val2'] = ''
                                        df = pd.DataFrame()
                                        df['each'] = jaba2 
                                        df['val'] = jaba 
                                        fin = pd.merge(cdf,df,on=['each'], how='left').fillna('')
                                        valus = fin['val'].tolist()
                                        print(valus)
                                        website = valus[0]
                                        phone = valus[1].split(' ')[0]
                                        industry = valus[2]
                                        co_size = valus[3] 
                                        hq = valus[4]
                                        typ = valus[5]
                                        founded = valus[6]
                                        specialities = valus[7]
                                        if driver.find_elements_by_class_name("""highcharts-container"""):
                                            all_g_tags = driver.find_elements_by_class_name("""highcharts-root""")
                                            xc = []
                                            arias = []
                                            for node in all_g_tags:
                                                paths = node.find_elements_by_tag_name("path")
                                                for path in paths:
                                                    value = path.get_attribute("d")
                                                    ari = path.get_attribute("aria-label")         
                                                    xc.append(value)
                                                    arias.append(ari)
                                            val = len(xc)
                                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-mappoint-series")))
                                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "g")))
                                            test = driver.find_elements_by_tag_name('path')
                                            
                                            #driver.implicitly_wait(5)
                                            try:
                                                #driver.switch_to.default_content()
                                                delay()
                                                print(test)
                                                driver.implicitly_wait(5)
                                                test[-1].click()
                                                locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                                                if locationa == '':
                                                    zogo = list(range(2,10)) 
                                                    for each in zogo:
                                                        test[-each].click()
                                                        locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                                                else:
                                                    pass
                                                locationa = locationa.replace('\n',' ').strip()
                                                latlngza = geocode(str(locationa))
                                                latitudea = latlngza[0]
                                                longitudea = latlngza[1]
                                            except (exceptions.ElementClickInterceptedException):
                                                locationa = ''
                                                latitudea = ''
                                                longitudea = ''
                                                out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, location,latitude,longitude]
                                                print(out) 
                                                writer.writerow(out)
                                                driver.quit()
                                                delay()
                                                continue
                                        #location = driver.find_element_by_class_name('locations__location').text.replace('Get directions','').replace('Primary','').split('to')[0]
                                        #location = location.replace('\n',' ').strip()
                                        #latlngz = geocode(str(location))
                                        #print(latlngz)
                                        #latitude = latlngz[0]
                                        #longitude = latlngz[1]
                                        if location is None or latitude is None or latitude is None:
                                            location = ''
                                            latitude = ''
                                            longitude = ''
                                        out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, location,latitude,longitude]
                                        print(out) 
                                        writer.writerow(out)
                                        driver.quit()
                                        delay()
                                    else:
                                        pass
                                else:
                                    pass
                            except:
                                if driver.find_element_by_class_name("""login__form"""):
                                    driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(EMAIL)
                                    driver.implicitly_wait(2)
                                    driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(PASSWORD)
                                    driver.implicitly_wait(2)
                                    driver.find_element_by_xpath("""//*[@id="app__container"]/main/div[2]/form/div[3]/button""").click()
                                else:
                                    pass

                driver.get(ib)
                driver.implicitly_wait(5)
                driver.find_element_by_class_name("""artdeco-card""")
                title = driver.find_element_by_class_name("""org-top-card-summary__title""").text
                soup = BeautifulSoup(driver.page_source, "html.parser")
                dl_data = soup.find_all("dd")
                dt_data = soup.find_all("dt")
                jaba = []
                jaba2 = []
                for each in dl_data:
                    ite = each.text.strip().replace('\n','')
                    jaba.append(ite)
                for each in dt_data:
                    ite2 = each.text.strip().replace('\n','')
                    jaba2.append(ite2)
                jaba = [ x for x in jaba if "on LinkedIn" not in x ]   
                cdf = pd.DataFrame()
                cdf['each'] = ["Website", "Phone","Industry", "Company size", "Headquarters","Type","Founded","Specialties"]
                cdf['val2'] = ''
                df = pd.DataFrame()
                df['each'] = jaba2 
                df['val'] = jaba 
                fin = pd.merge(cdf,df,on=['each'], how='left').fillna('')
                valus = fin['val'].tolist()
                print(valus)
                website = valus[0]
                phone = valus[1].split(' ')[0:1]
                industry = valus[2]
                co_size = valus[3] 
                hq = valus[4]
                typ = valus[5]
                founded = valus[6]
                specialities = valus[7]
                try:
                    location = driver.find_element_by_class_name('org-location-card').text.replace('\n','').replace('Get directions','').replace('Primary','').split('to')[0]
                    latlngz = geocode(str(location))
                    latitude = latlngz[0]
                    longitude = latlngz[1]
                except:
                    location = ''
                    latitude = ''
                    longitude = ''

                out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, location,latitude,longitude]
                try:
                    if location=='' and driver.find_elements_by_class_name("""highcharts-mappoint-series"""):
                        all_g_tags = driver.find_elements_by_class_name("""highcharts-mappoint-series""")
                        xc = []
                        arias = []
                        for node in all_g_tags:
                            paths = node.find_elements_by_tag_name("path")
                            for path in paths:
                                value = path.get_attribute("d")
                                ari = path.get_attribute("aria-label")         
                                xc.append(value)
                                arias.append(ari)
                        val = len(xc)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-mappoint-series")))
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "g")))
                        test = driver.find_elements_by_tag_name('g')
                        
                        #driver.implicitly_wait(5)
                        try:
                            #driver.switch_to.default_content()
                            delay()
                            print(test)
                            driver.implicitly_wait(5)
                            test[-1].click()
                            locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                            if locationa == '':
                                zogo = list(range(2,10)) 
                                for each in zogo:
                                    test[-each].click()
                                    locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                            else:
                                pass
                            locationa = locationa.replace('\n',' ').strip()
                            latlngza = geocode(str(locationa))
                            latitudea = latlngza[0]
                            longitudea = latlngza[1]
                        except (exceptions.ElementClickInterceptedException):
                            locationa = ''
                            latitudea = ''
                            longitudea = ''
                            pass
                        out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, locationa,latitudea,longitudea]
                    else:
                        pass
                except:
                    if location=='' and driver.find_elements_by_class_name("""highcharts-mappoint-series"""):
                        all_g_tags = driver.find_elements_by_class_name("""highcharts-mappoint-series""")
                        xc = []
                        arias = []
                        for node in all_g_tags:
                            paths = node.find_elements_by_tag_name("path")
                            for path in paths:
                                value = path.get_attribute("d")
                                ari = path.get_attribute("aria-label")         
                                xc.append(value)
                                arias.append(ari)
                        val = len(xc)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-series-group")))
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "g")))
                        test = driver.find_elements_by_tag_name('g')
                        
                        #driver.implicitly_wait(5)
                        try:
                            #driver.switch_to.default_content()
                            delay()
                            print(test)
                            driver.implicitly_wait(5)
                            test[-2].click()
                            locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                            if locationa == '':
                                zogo = list(range(2,10)) 
                                for each in zogo:
                                    test[-each].click()
                                    locationa = driver.find_element_by_xpath("""/html/body/div[7]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/ul/li/div/p""").text
                            else:
                                pass
                            locationa = locationa.replace('\n',' ').strip()
                            latlngza = geocode(str(locationa))
                            latitudea = latlngza[0]
                            longitudea = latlngza[1]
                        except (exceptions.ElementClickInterceptedException):
                            locationa = ''
                            latitudea = ''
                            longitudea = ''
                            pass
                        out = [URL,title,website,phone,industry,co_size,typ,founded,specialities,hq, locationa,latitudea,longitudea]
                    else:
                        pass   
                print(i,out)
                writer.writerow(out)
                driver.quit()
            else:
                writer.writerow('')
                driver.quit()
                delay()
                continue

                

