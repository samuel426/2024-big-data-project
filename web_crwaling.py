from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv  # CSV 모듈 추가

# 웹 드라이버 설정
chrome_driver_path = "/usr/local/bin/chromedriver-linux64/chromedriver"  # 크롬 드라이버의 경로를 지정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드 (브라우저 UI 없이 실행)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 방문할 웹 페이지 URL
url = "https://www.vms.or.kr/partspace/recruit.do?area=0101&areagugun=&acttype=&status=1&volacttype=&sttdte=2024-02-07&enddte=2024-03-08&termgbn=&searchType=title&searchValue=&page=1#none"  # 시작할 URL을 지정하세요
driver.get(url)

# 데이터 배열 초기화
data_list = []

# 게시판의 항목을 찾기
board_items = driver.find_elements(By.CSS_SELECTOR, "#rightArea > div.con > div.boardList.boardListService > ul > li > a")

# 게시판 항목을 순차적으로 클릭
for i in range(len(board_items)):
    # 리스트에서 i번째 링크 클릭
    board_items[i].click()
    time.sleep(2)  # 페이지 로드 시간 대기

    # 클릭 후 페이지에서 원하는 데이터 추출
    con_element = driver.find_element(By.CSS_SELECTOR, "#rightArea > div.con")
    data = con_element.text  # 원하는 데이터 추출
    data_list.append(data)  # 배열에 데이터 추가

    # 뒤로 가기
    driver.back()
    time.sleep(2)  # 페이지 로드 시간 대기

    # 뒤로 간 후 리스트를 다시 찾기
    board_items = driver.find_elements(By.CSS_SELECTOR, "#rightArea > div.con > div.boardList.boardListService > ul > li > a")

# CSV 파일에 데이터 저장
csv_file_path = "/home/user/Desktop/workspace/bigdata/project/web_crwaling.csv"  # CSV 파일의 절대 경로 또는 상대 경로 지정
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)

    # 데이터 배열의 각 항목을 CSV 파일에 추가
    for item in data_list:
        csv_writer.writerow([item])  # 각 행에 데이터 작성

# 웹 드라이버 종료
driver.quit()
