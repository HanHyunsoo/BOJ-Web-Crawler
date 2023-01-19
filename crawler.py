from common import *;
import requests, os, sys, subprocess, time
from bs4 import BeautifulSoup as bs

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

# workbook_number = input("백준 문제집 번호 입력: ")
workbook_number = int(input("백준 문제집 번호 입력: "))
workbook_url = boj_url + "/workbook/view/" + str(workbook_number)


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0", 'Connection':'close'}
response = requests.get(workbook_url, headers=headers)
soup = bs(response.text, "html.parser")

if (response.status_code != 200):
    raise ConnectionError("해당 번호로 문제집을 찾을 수 없습니다.")

trs = soup.select("table.table.table-striped.table-bordered > tbody > tr")

problems = []

for tr in trs:
    tds = tr.select("td")
    problem = Problem(tds[0].text, tds[1].text)
    problems.append(problem)

workbook_name = soup.select_one(".page-header > h1:nth-child(1) > span:nth-child(1)").text

try:
    language = Language[input("언어 입력(java, python): ").upper()]
except KeyError:
    raise TypeError("타입을 확인 해주세요(JAVA, PYTHON)")

workbook = WorkBook(workbook_number, workbook_name, language, problems)

workbook_path = workbook.make_folders_and_files()

print("크롤링 성공 3초뒤에 폴더를 엽니다.")

time.sleep(3)

open_file(workbook_path)