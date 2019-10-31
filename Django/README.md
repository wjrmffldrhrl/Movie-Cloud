# 목적
크롤링한 데이터를 Django를 통해 웹 사이트화 하여 UI 제공

영화 별 상세정보 및 워드 클라우드 출력

# 개발환경
Pycharm

Mysql

# 동작 방법

1. Pycharm, Mysql 설치
2. 파이참 터미널에서 pip 명령어를 통해 mysqlclinet 설치
3. manage.py가 있는 폴더로 이동하여 python manage.py makemigrations 수행
3. python manage.py migrate로 마이그레이션 적용
4. python manage.py runserver 명령을 통해 서버 실행
5. http://127.0.0.1:8000/moviecloud/inputdata 를 한번 호출하여 수집된 데이터를 DB에 적용
6. http://127.0.0.1:8000/moviecloud/ <- 홈페이지로 이동하여 동작 
