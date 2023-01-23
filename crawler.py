from api import *
from typing import Union
from bs4 import BeautifulSoup as bs
import requests, os, sys, subprocess, time

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

workbook_name = soup.select_one(".page-header > h1:nth-child(1) > span:nth-child(1)").text # type: ignore
if (response.status_code != 200 or workbook_name is None):
    raise ConnectionError("해당 번호로 문제집을 찾을 수 없습니다.")

trs = soup.select("table.table.table-striped.table-bordered > tbody > tr")

problems = []

for tr in trs:
    tds = tr.select("td")

    if tds[1].text == "":
        continue

    problem = Problem(int(tds[0].text), tds[1].text)
    problems.append(problem)

try:
    language = Language[input("언어 입력(java, python): ").upper()]
except KeyError:
    raise TypeError("타입을 확인 해주세요(JAVA, PYTHON)")

workbook = WorkBook(workbook_number, workbook_name, language, problems)

given_rank = input("각 문제를 번호대로 정렬하고 티어 별로 문제를 나누겠습니까?(yY, nN): ").upper() == "Y"

workbook_path = workbook.make_folders_and_files(given_rank)

print(
f"""크롤링 성공
폴더 위치 = {os.getcwd() + workbook_path}
3초뒤에 폴더를 엽니다."""
)

time.sleep(3)

open_file(workbook_path)