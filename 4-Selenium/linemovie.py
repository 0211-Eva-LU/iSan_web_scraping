import time
import json
import os


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
driver.get("https://today.line.me/tw/v2/movie/incinemas/playing")

movie_list=driver.find_elements(By.CSS_SELECTOR,".detailListItem.movieListing-movie")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(5)

# last_movie= movie_list[-1]
# print(f'目前數量:{len(movie_list)}')
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#     time.sleep(2)
#     movie_list = driver.find_elements(By.CSS_SELECTOR,".detailListItem.movieListing-movie")
#     if last_movie == movie_list[-1]:
#         break

# last_movie = movie_list[-1]
# print(f'目前數量:{len(movie_list)}')

all_movie_info = []
for movie in movie_list :
    movie_name=movie.find_element(By.CSS_SELECTOR,".detailListItem-titles").text
    movie_grad=movie.find_element(By.CSS_SELECTOR,".iconInfo.detailListItem-iconInfo").text
    movie_time=movie.find_element(By.CSS_SELECTOR,".detailListItem-status>span").text
    movie_link=movie.find_element(By.CSS_SELECTOR,".detailListItem-bookingButton").get_attribute("href")

    all_movie_info.append({
        "name":movie_name,
        "average_grade":movie_grad,
        "time": movie_time,
        "link":movie_link}
    )





start_mapping={"M12 18.344l-5.81 3.609c-.147.091-.34.046-.43-.1-.043-.07-.057-.152-.04-.23l1.469-6.96-5.09-4.736c-.126-.118-.133-.316-.016-.442.052-.056.122-.091.198-.099l6.746-.68 2.684-6.513c.066-.16.249-.235.408-.17.077.032.138.094.17.17l2.684 6.514 6.746.68c.172.017.297.17.28.342-.008.075-.043.146-.099.198l-5.09 4.736 1.47 6.96c.036.169-.072.334-.24.37-.08.017-.161.002-.23-.04L12 18.343z":2,

"M12.12 2.024c.076.031.137.093.169.17l2.684 6.513 6.746.68c.172.017.297.17.28.342-.008.075-.043.146-.099.198l-5.09 4.736 1.47 6.96c.036.169-.072.334-.24.37-.08.017-.161.002-.23-.04L12 18.343l-5.81 3.61c-.147.091-.34.046-.43-.1-.043-.07-.057-.152-.04-.23l1.469-6.96-5.09-4.736c-.126-.118-.133-.316-.016-.442.052-.056.122-.091.198-.099l6.746-.68 2.684-6.513c.066-.16.249-.235.408-.17zM12 6.463v9.651l3.662 2.275-.925-4.383 3.316-3.086-4.398-.443L12 6.463z":1,

"M12.12 2.024c.076.031.137.093.169.17l2.684 6.513 6.746.68c.172.017.297.17.28.342-.008.075-.043.146-.099.198l-5.09 4.736 1.47 6.96c.036.169-.072.334-.24.37-.08.017-.161.002-.23-.04L12 18.343l-5.81 3.61c-.147.091-.34.046-.43-.1-.043-.07-.057-.152-.04-.23l1.469-6.96-5.09-4.736c-.126-.118-.133-.316-.016-.442.052-.056.122-.091.198-.099l6.746-.68 2.684-6.513c.066-.16.249-.235.408-.17zm1.6 8.365L12 6.216l-1.72 4.173-4.549.458 3.43 3.191-.961 4.546 3.8-2.36 3.799 2.36-.96-4.546 3.429-3.191-4.548-.458z":0}


def get_all_comment(url):
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR,"ul.tabs-list.movie li:nth-child(3)").click()
    time.sleep(2)
    comment_info = []
    comment_cards=driver.find_elements(By.CSS_SELECTOR,".css-hnvcda")
    movie_name=driver.find_element(By.CSS_SELECTOR,".title.header.css-ybyea6").text
    for comment_card in comment_cards:
        comment_user = comment_card.find_element(By.CSS_SELECTOR,".ratingCommentItemUser").text
        comment_date=comment_card.find_element(By.CSS_SELECTOR,".ratingCommentItemUser-createdTime.css-squ0i5").text
        comment=comment_card.find_element(By.CSS_SELECTOR,".ratingCommentItemContent").text
        stars=comment_card.find_elements(By.CSS_SELECTOR,".ratingStar path")
        
        grade = 0
        for star in stars:
            path_d = star.get_attribute('d')
            grade += start_mapping[path_d]


        comment_info.append({
            "comment_user":comment_user,
            "grade":grade,
            "comment_date":comment_date,
            "comment":comment
        })

        
    return (movie_name,comment_info)


if not os.path.exists("movie_comment"):
    os.mkdir("movie_comment")

for info in all_movie_info:
    try:
        comment_info: list = get_all_comment(info['link'])
    except Exception as e:
        with open("error_log.txt",'a') as f:
            f.write(f'{info['name']}-{info['link']}:{e}')

    all_info = {
        "avarage_grade":info["average_grade"],
        "movie_time":info["time"],
        "comments":comment_info
    }

    info['name'] = info['name'].replace('\n','')

    with open(f'movie_comment/{info['name']}.json','w',encoding='utf-8')as f:
            json.dump(all_info,f,indent=4,ensure_ascii=False)

