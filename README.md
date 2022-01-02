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

[Company_name]

id : integer primary key

company_id : integer foreign key(Company)

name : varchar(100)

language : varchar(10)

[Company_tags]

id : integer primary key

company_id : integer foreign key(Company)

tag : varchar(200)

language : varchar(10)



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
- GET /search?query=<:query> : 자동완성
    
    └ response : [ { "company" : 회사명 } ], 200
  
- GET /companies/<:query> : 검색
  
    └ response : { "company_name": 회사명, "tags" : [ 태그 리스트 ] }, 200
    └ response for fail : 404
- POST /create : 새로운 회사 데이터 저장
    
    └ request : { 'company_name' : {언어 : 회사명}, 'tags': [ { "tag_name": { 언어 : 태그명 } ] }
    
    └ response : { "company_name" : 회사명, "tags" : [ 태그 리스트 ] }, 201
