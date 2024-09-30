from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
import time

# Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")


# Function to click the cookie
def click_cookie():
    try:
        cookie = driver.find_element(By.ID, value="cookie")
        cookie.click()
    except NoSuchElementException:
        print("Cookie not found, retrying...")
        pass


# Function to get the current amount of money
def get_money():
    try:
        money = driver.find_element(By.ID, value="money").text.replace(",", "")
        int_money = int(money)
        return int_money
    except (ValueError, NoSuchElementException):
        return 0


# Function to get all store prices
def get_store_prices():
    prices_array = []
    try:
        store = driver.find_element(By.ID, value="store")
        prices = store.find_elements(By.CSS_SELECTOR, value="div b")
        for price_element in prices[:-1]:
            try:
                price = int(price_element.text.split()[-1].replace(",", ""))
                prices_array.append(price)
            except (ValueError, IndexError):
                continue
    except NoSuchElementException:
        print("Store not found.")
    return prices_array


# Function to purchase an item
def purchase_smth(index):
    try:
        store = driver.find_element(By.ID, value="store")
        store_items = store.find_elements(By.CSS_SELECTOR, value="div")
        if "grayed" not in store_items[index].get_attribute("class"):
            store_items[index].click()
    except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
        print("Unable to purchase item at index:", index)
        pass


# Logic for running the game
while True:
    start_time = time.time()

    while time.time() - start_time < 5:
        click_cookie()
    prices = get_store_prices()
    money = get_money()

    for index in range(len(prices)):
        if money >= prices[index]:
            purchase_smth(index)

    time.sleep(1)
