# README

Wanted Lab internship 지원자 이지수(suen0904@gmail.com)

-github : https://github.com/damda0904/Wanted_assignment

- 데이터베이스는 SQLite3을 사용하였습니다.


# Version

<img src="https://img.shields.io/badge/Python 3.8.5-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Flask 2.0.2-000000?style=for-the-badge&logo=Flask&logoColor=white">
<img src="https://img.shields.io/badge/sqlite 3.12.1-003B57?style=for-the-badge&logo=SQLite3&logoColor=black">


# 데이터 베이스 스키마

[Company]

id : integer primary key

company_name_ko : varchar(50) unique

company_name_en : varchar(50) unique

company_name_ja : varchar(50) unique

tag_ko : varchar(50)

tag_en : varchar(50)

tag_ja : varchar(50)



# 파일 구조
wanted/

┗ migrations/

┗ wanted/
  
    ┗ __init__.py : 플라스크 어플리케이션 생성
    
    ┗ models.py : 데이터베이스 스키마
    
    ┗ views/
  
        ┗ main_views.py : router, controller(비즈니스 로직)
    
    ┗ static/
        
        ┗ wanted_temp_data.csv : 테스트 데이터

┗ config.py : 데이터베이스 설정

┗ wanted.db : 데이터베이스 data value

# 실행 url
- default : http://localhost:5000/
- GET /setData : 샘플 데이터 저장
   
    └ response : { "message" : "success" }, 201
- GET /search/<:keyword> : 자동완성 혹은 검색
    
    └ response : { index : { 'ko' : 한국어 회사명, 'en': 영어 회사명, 'ja': 일본어 회사명 } }, 200
- POST /create : 새로운 회사 데이터 저장
    
    └ request : { 'company_ko' : 한국어 회사명, 'company_en' : 영어 회사명, 'company_ja' : 일본어 회사명 } (모든 속성은 선택이다)
    
    └ response : { "message" : "success" }, 201
    └ response for fail : { "message" : "이미 존재하는 회사입니다." }, 400
