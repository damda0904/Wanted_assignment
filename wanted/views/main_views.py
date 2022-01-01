from flask import Blueprint, make_response, request
from sqlalchemy import or_

from wanted import db
from wanted.models import Company

import json

bp = Blueprint('main', __name__, url_prefix='/')


#샘플 데이터 저장
@bp.route('/setData')
def set_data():
    import csv

    exist = db.session.query(Company).first()

    if not exist :
        f = open("./wanted/static/wanted_temp_data.csv", encoding='utf-8')
        fr = csv.reader(f)
        for line in fr:
            if line[0] == 'company_ko':
              continue
            company = Company(company_name_ko=line[0], company_name_en=line[1], company_name_ja=line[2], tag_ko=line[3], tag_en=line[4], tag_ja=line[5])
            db.session.add(company)
            db.session.commit()
        f.close()

    return make_response("", 200)


#자동완성 및 검색
@bp.route('/autoComplete/<string:keyword>/')
def auto_complete(keyword):

    #검색쿼리
    keyword_query = "%" + keyword + "%"
    companies = db.session.query(Company).filter(or_(Company.company_name_ko.like(keyword_query),
                                                     Company.company_name_ja.like(keyword_query),
                                                     Company.company_name_en.like(keyword_query))).all()

    result = {} #정제된 결과를 담을 딕셔너리
    idx = 0
    #언어별로 결과 정제
    for company in companies :

        item = {}
        item['ko'] = company.company_name_ko
        item['en'] = company.company_name_en
        item['ja'] = company.company_name_ja

        result[idx] = item

        idx += 1

    #딕셔너리 json화
    result = json.dumps(result, ensure_ascii=False).encode('utf-8')

    return make_response(result, 200)


#새로운 회사 데이터 저장
@bp.route('/create', methods=['POST'])
def create():

    #body 가져오기
    body = dict(json.loads(request.get_data(), encoding='utf-8'))

    name_ko = body['company_ko'] if "company_ko" in body.keys() else ""
    name_en = body['company_en'] if "company_en" in body.keys() else ""
    name_ja = body['company_ja'] if "company_ja" in body.keys() else ""

    #회사 중복 확인
    if name_ko != "" :
        if db.session.query(Company).filter(Company.company_name_ko == name_ko) :
            return make_response({"message": "이미 존재하는 회사입니다."}, 400)
    elif name_en != "" :
        if db.session.query(Company).filter(Company.company_name_en == name_en) :
            return make_response({"message": "이미 존재하는 회사입니다."}, 400)
    elif name_ja != "" :
        if db.session.query(Company).filter(Company.company_name_ja == name_ja) :
            return make_response({"message": "이미 존재하는 회사입니다."}, 400)

    #중복이 없을 경우, 회사 추가
    company = Company(company_name_ko=name_ko, company_name_en=name_en, company_name_ja=name_ja)
    db.session.add(company)
    db.session.commit()

    return make_response("Success", 201)