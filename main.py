from selenium import webdriver
import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROMISED_DOWN = 500
PROMISED_UP = 500
TWITTER_EMAIL = 'email'
TWITTER_PASSWORD = 'password'


class InternetSpeedTwitterBot:

    def __init__(self):
        self.twitter_pswd = None
        self.driver = webdriver.Firefox()  # Instance attribute
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(10)
        self.driver.find_element(By.CSS_SELECTOR, ".start-text").click()

        WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-result-id*='true']"))
        )

        self.down = float(self.driver.find_element(By.CSS_SELECTOR, ".download-speed").text)
        self.up = float(self.driver.find_element(By.CSS_SELECTOR, ".upload-speed").text)
        print(f"up {self.up} down {self.down}")
        #self.driver.close()

    def tweet_at_provider(self):
        print("Twitter")
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(5)

        username = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                      '2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div['
                                                      '2]/div/input')

        username.send_keys(TWITTER_EMAIL)

        next_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                         '2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        next_button.click()

        time.sleep(10)
        self.twitter_pswd = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                               '1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                               '2]/div[2]/div[1]/div/div/div[3]/div/label/div/div['
                                                               '2]/div[1]/input')

        self.twitter_pswd.send_keys(TWITTER_PASSWORD)
        login_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                          '1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                          '2]/div[2]/div[2]/div/div[1]/div/div/div/div')
        login_button.click()
        time.sleep(30)

        # Generate tweet
        input_t = self.driver.find_element(By.CSS_SELECTOR, '.notranslate.public-DraftEditor-content')
        input_t.send_keys(
            f'My upload speed is {self.up} Mbps and my download speed is {self.down} Mbps. Why are you playing with me though?')
        tweet_button_path = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[' \
                            '1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3] '
        tweet = self.driver.find_element(By.XPATH, tweet_button_path)
        tweet.click()
        time.sleep(4)


bot = InternetSpeedTwitterBot();
bot.get_internet_speed()
bot.tweet_at_provider()
bot.driver.quit()



