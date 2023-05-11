import time
import sqlite3
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   Name TEXT,
   ShortName TEXT,
   Price  TEXT,
   Сapitalization TEXT);
""")
conn.commit()

def PathX(a):
    return '/html/body/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div/' \
                'table/tbody/tr[' + str(a) + ']/td[2]/div/div/div/div/div'

def PathK(a):
    return '/html/body/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div/' \
                'table/tbody/tr[' + str(a) + ']/td[5]/div/div/div/div/div'
options = Options()
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
  '''
})
driver.get("https://www.coinbase.com/ru/explore")
driver.set_window_size(500, 500)
time.sleep(10)
ActionChains(driver).move_by_offset(350, 350).click().perform()
driver.set_window_size(1000, 500)
ls = []
lsS = []
lsP = []
lsL = []
i = 0
while i != 4:
    flag = 0
    flag1 = 0
    flag2 = 1
    flag3 = 0
    text = driver.find_elements(By.TAG_NAME, "h2")
    text1 = driver.find_elements(By.CLASS_NAME, "cds-label2-l5adacs")
    for flag2 in range(1, 30):
        XPath = PathX(flag2)
        price = driver.find_element(By.XPATH, XPath)
        lsP.append(price.text)
        print(1)
    for flag2 in range(1, 30):
        XPath = PathK(flag2)
        price = driver.find_element(By.XPATH, XPath)
        lsL.append(price.text)
        print(1)
    for e in text1:
        if flag1 < 31:
            print(e.text)
            lsS.append(e.text)
        flag1 += 1
    for e in text:
        if flag != 0 and flag < 31:
            print(e.text)
            ls.append(e.text)
            print(flag)
        flag += 1
    time.sleep(2)
    flag = 0

    elem = driver.find_elements(By.CLASS_NAME, "dAnHxd")
    if i == 0:
        elem[0].click()
    else:
        elem[1].click()
    time.sleep(1)
    i += 1
time.sleep(2)
for i in range(0, 100):
    user = (ls[i], lsS[i], lsP[i], lsL[i])
    cur.execute("INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?);", user)
    conn.commit()

time.sleep(10)
