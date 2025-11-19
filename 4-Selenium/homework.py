import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# 建立 Service 物件，指定 chromedriver.exe 的路徑


# 設定 Chrome 瀏覽器的選項
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
options.add_argument("--incognito") # 無痕模式
options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

# 建立 Chrome 瀏覽器物件
driver = webdriver.Chrome(options=options)
driver.get("https://www.momoshop.com.tw/main/Main.jsp")
time.sleep(4)

search_but=driver.find_element(By.CSS_SELECTOR,".mx-auto.flex.w-content.flex-wrap input")
search_but.send_keys("stanley保溫杯")
driver.find_element(By.CSS_SELECTOR,".mx-auto.flex.w-content.flex-wrap button").click()

search_all = driver.find_elements(By.CSS_SELECTOR,".listAreaUl .listAreaLi")

search_page = driver.find_element(By.CSS_SELECTOR,".page-control")
allpage =int(search_page.find_element(By.CSS_SELECTOR,".page-number").text.split('/')[-1])


cnt = 0
while 0 < allpage:
    for p in search_all:
        p_name = p.find_element(By.CSS_SELECTOR,".prdNameTitle h3").text
        p_price = p.find_element(By.CSS_SELECTOR,".price").text
        p_url = p.find_element(By.CSS_SELECTOR, ".goods-img-url").get_attribute("href")
        p_img = p.find_element(By.CSS_SELECTOR,'.goods-img img').get_attribute("src")
        

        print(p_name,p_price,p_url,p_img)
        time.sleep(5)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});")
        driver.find_element(By.CSS_SELECTOR,".pageArea.topPage .page-btn.page-next a").click()
        cnt+=1

