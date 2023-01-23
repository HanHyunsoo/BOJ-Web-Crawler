# BOJ Web Crawler

백준에 있는 문제집을 토대로 언어별로 프로젝트 템플릿을 생성합니다.

## Development Environment

* Python - 3.10.9
* MacOS - 13.0.1

## How To Use

*  Unix 계열

```bash
git clone https://github.com/HanHyunsoo/BOJ-Web-Crawler.git
cd BOJ_Web_Crawler
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

* Window(cmd)
```bash
git clone https://github.com/HanHyunsoo/BOJ-Web-Crawler.git
cd BOJ_Web_Crawler
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

[백준 사이트 문제집](https://www.acmicpc.net/workbook/top)에서 크롤링 하고싶은 문제집 번호를 찾습니다.

* 예시 - 10475


불러온 프로젝트에서 crawler.py를 실행합니다.

```bash
python3 crawler.py
백준 문제집 번호 입력: {크롤링 하고싶은 문제집 번호 입력}
언어 입력(java, python): {좌측에 나와있는 언어 타입 입력}
크롤링 성공
폴더 위치 = {크롤링 하여 만든 템플릿 위치}
3초뒤에 폴더를 엽니다.
```

해당 명령어를 수행하면 크롤링하여 만든 템플릿을 파일 탐색기를 통해 아래 경로를 자동으로 열어줍니다.

* 경로 - {crawler.py의 위치}/result/{Java일 경우 Java/src, Python일 경우 Python}/wb_{문제집 번호}

### Example

* Python - 3.10.9
* MacOS - 13.0.1

> [Case 1](example/Java/src/wb_10475)
```bash
백준 문제집 번호 입력: 10475
언어 입력(java, python): java
각 문제를 번호대로 정렬하고 티어 별로 문제를 나누겠습니까?(yY, nN): y
크롤링 성공
폴더 위치 = /Users/hanhyunsoo/dev/BOJ Web Crawlerresult/Java/src/wb_10475
3초뒤에 폴더를 엽니다.
```

> [Case 2](example/Python/wb_10475)
```bast
백준 문제집 번호 입력: 10475
언어 입력(java, python): python
각 문제를 번호대로 정렬하고 티어 별로 문제를 나누겠습니까?(yY, nN): n
크롤링 성공
폴더 위치 = /Users/hanhyunsoo/dev/BOJ Web Crawlerresult/Python/wb_10475
3초뒤에 폴더를 엽니다.
```

## ETC

* 너무 많은 요청을 하면 백준 서버측에서 거부할 수 있습니다.
* 티어별로 문제를 나누지 않는다면 wb_{문제집 번호}/README.md 에서 문제들의 순서는 실제 사이트 문제집의 순서를 따릅니다.

## License

* [백준](https://www.acmicpc.net/)
* [solvedac API](https://solvedac.github.io/unofficial-documentation/)