from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
import datetime
import undetected_chromedriver as uc
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait as webdriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import locale

locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

username = "username"
password = "password"

solver = TwoCaptcha('your_api_key')

class Tenis_bot:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.get("https://online.spor.istanbul/uyegiris")
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        
    def login(self):
        username_input = self.driver.find_element(By.ID, "txtTCPasaport")
        for char in username:
            username_input.send_keys(char)
            time.sleep(0.3)
        
        password_input = self.driver.find_element(By.ID, "txtSifre")
        for char in password:
            password_input.send_keys(char)
            time.sleep(0.3)
        time.sleep(2)

        login_button = self.driver.find_element(By.ID, "btnGirisYap").click()
        time.sleep(4)
        dont_show_again = self.driver.find_element(By.ID, "checkBox").click()
        time.sleep(1)
        close_btn = self.driver.find_element(By.ID, 'closeModal').click()
        time.sleep(2)

    def goto_seanslarım(self):
        seanslarım = self.driver.find_element(By.XPATH, '//*[@id="liseanslarim"]/a').click()
        time.sleep(2)
        seans_btn = self.driver.find_element(By.ID, 'pageContent_rptListe_lbtnSeansSecim_0').click()
        time.sleep(5)


    def check_verification(self):
        try:
            webdriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
            return "Recaptcha"
        except Exception as e:
            print("Recaptcha not found")

        try:
            webdriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "pageContent_captchaImage")))
            return "Image"
        except Exception as e:
            print("Image not found")
        
        return None
    
    def solve_image_verification(self):
        image = self.driver.find_element(By.ID, "pageContent_captchaImage")
        image.screenshot("Image.png")
        time.sleep(2)
        try:
            result = solver.normal("Image.png")
            print(result)
            time.sleep(5)
        except Exception as e:
            print(e)

        os.remove("Image.png")

        self.driver.find_element(By.ID, "pageContent_txtCaptchaText").send_keys(result['code'])

    def solve_recaptcha(self):
        try:
            result = solver.recaptcha(sitekey='6Ld8vXIUAAAAAOQLow6s3rJvMJJO8g4D793T91Rl', url='https://online.spor.istanbul/uyeseanssecim')
            print(result)
            time.sleep(5)
        except Exception as e:
            print(e)

        webdriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "g-recaptcha-response")))

        self.driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = '{}'".format(result['code']))

    def three_days_after_index(self):
        today = datetime.datetime.today()
        day_name = today.strftime('%A')
        print(day_name)

        if day_name == "Pazartesi":
            return 3
        elif day_name == "Salı":
            return 4
        elif day_name == "Çarşamba":
            return 5
        elif day_name == "Perşembe":
            return 6
        elif day_name == "Cuma":
            return 0
        elif day_name == "Cumartesi":
            return 1
        elif day_name == "Pazar":
            return 2
        else:
            return None   
        
    def check_seans(self,id):
        seans = self.driver.find_element(By.ID, 'pageContent_rptListe_lbtnSeansSecim_{}'.format(id))
        
    def select_day(self):
        day_id = self.three_days_after_index()
        state = False
        counter = 0
        while state == False:
            try:
                seanslar = self.driver.find_element(By.XPATH, f'//div[{day_id}]/div/div[2]')
                found_input = seanslar.find_element(By.TAG_NAME, 'input')
                print(found_input)
                found_input.click()
                state = True
            except Exception as e:
                if counter == 25:
                    print("No input found BREAKING!!!")
                    break
                counter += 1
                print(e)
                print("No input found")
                self.driver.refresh()


    def select_seans(self):
        self.select_day()
        time.sleep(2)

        confirm_btn = self.driver.find_element(By.ID, 'pageContent_cboxOnay').click()
        time.sleep(2)

        verification = self.check_verification()
        if verification == "Recaptcha":
            self.solve_recaptcha()
        elif verification == "Image":
            self.solve_image_verification()
        else:
            print("No verification found")

        self.driver.find_element(By.ID, 'lbtnKaydet').click()
        print("Seans saved:" + str(datetime.datetime.today()))
        return True

now = datetime.datetime.now()
todays_hour = now.hour
todays_minute = now.minute
todays_time = "{}:{}".format(todays_hour, todays_minute)
str(todays_time)

wanted_hours = ["10:59", "11:59", "12:59", "8:59"]

state_try = True

while True:
    try:
        time.sleep(5)
        print("time = ", todays_time)
        if todays_time == wanted_hours[0] or todays_time == wanted_hours[1] or todays_time == wanted_hours[2]:
            while state_try == True:
                try:
                    print("True\nProgram başlıyor...")
                    bot = Tenis_bot()
                    bot.login()
                    bot.goto_seanslarım()
                    answer = bot.select_seans()
                    if answer == True:
                        print("Seans seçildi...")
                        state_try = False
                    else:
                        print("Seans seçilemedi... tekrar deniyorum...")
                except Exception as e:
                    print(e)
                    print("Error occured... Retrying...")
                    continue
            break
        else:
            print("False\nDaha erken...")
    except Exception as e:

        print(e)
        print("Error occured... Retrying...")

