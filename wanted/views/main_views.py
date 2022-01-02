from flask import Blueprint, make_response, request, Response
from sqlalchemy import or_, and_

from wanted import db
from wanted.models import Company, Company_name, Company_tags

import json

bp = Blueprint('main', __name__, url_prefix='/')


#샘플 데이터 저장
@bp.route('/setData')
def set_data():
    import csv

    exist = db.session.query(Company).first()

    #if not exist :

    f = open("./wanted/static/wanted_temp_data.csv", encoding='utf-8')
    fr = csv.reader(f)
    idx = 0
    for line in fr:
        if line[0] == 'company_ko':
            continue

        db.session.add(Company(id=idx))

        if line[0] != "" :
            db.session.add(Company_name(company_id=idx, name=line[0], language="ko"))
        if line[1] != "" :
            db.session.add(Company_name(company_id=idx, name=line[1], language="en"))
        if line[2] != "" :
            db.session.add(Company_name(company_id=idx, name=line[2], language="ja"))

        tags_ko = line[3].split("|")
        for tag in tags_ko:
            db.session.add(Company_tags(company_id=idx, tag=tag, language="ko"))
        tags_en = line[4].split("|")
        for tag in tags_en:
            db.session.add(Company_tags(company_id=idx, tag=tag, language="en"))
        tags_ja = line[5].split("|")
        for tag in tags_ja:
            db.session.add(Company_tags(company_id=idx, tag=tag, language="ja"))
        db.session.commit()

        idx += 1
    f.close()

    return make_response({"message": "success"}, 201)


#자동완성
@bp.route('/search')
def autoComplete():

    lang = request.headers.get("x-wanted-language")
    query = "%" + str(request.args.get('query')) + "%"

    #언어에 따라 쿼리를 다르게 처리
    result = []
    if lang == "ko":
        companies = db.session.query(Company_name.name).filter(and_(Company_name.name.like(query), Company_name.language=="ko"))
    elif lang == "en":
        companies = db.session.query(Company_name.name).filter(and_(Company_name.name.like(query), Company_name.language=="en"))
    elif lang == "ja":
        companies = db.session.query(Company_name.name).filter(and_(Company_name.name.like(query), Company_name.language=="ja"))
    else:
        return make_response({"error": "지원하지 않는 언어입니다."}, 400)

    #데이터 정제
    for company in companies:
        result.append({"company_name": company[0]})

    #json화
    response = json.dumps(result, ensure_ascii=False)

    return make_response(response, 200)


#검색
@bp.route('/companies/<string:query>')
def search(query):

    lang = request.headers.get("x-wanted-language")

    # 쿼리 처리
    company_id = db.session.query(Company_name.company_id).filter(Company_name.name==query).first_or_404()
    names =  db.session.query(Company_name.name, Company_name.language).filter(Company_name.company_id==company_id[0]).all()
    tags = db.session.query(Company_tags.tag, Company_tags.language).filter(Company_tags.company_id==company_id[0]).all()

    # 정제된 결과를 담을 딕셔너리
    result = {}

    # 언어별로 결과 정제
    for name in names :
        if name.language == lang :
            result['company_name'] = name.name
            break;

    #태그를 담을 리스트
    result_tags = []
    # 태그 처리
    for tag in tags :
        if tag.language == lang :
            result_tags.append(tag.tag)

    result['tags'] = result_tags
    #딕셔너리 json화
    result = json.dumps(result, ensure_ascii=False)

    return make_response(result, 200)


#새로운 회사 데이터 저장
@bp.route('/companies', methods=['POST'])
def create():

    #body 가져오기
    body = dict(json.loads(request.get_data(), encoding='utf-8'))

    names = body['company_name']

    company_id = 100

    #Company 생성
    last = db.session.query(Company.id).order_by(Company.id.desc()).first()
    company_id = last[0] + 1

    company = Company(id=company_id)
    db.session.add(company)

    #회사 이름 저장
    for lang in names :
        db.session.add(Company_name(company_id=company_id, name=names[lang], language=lang))

    #회사 태그 저장
    tags = body['tags']
    for item in tags :
        three = item['tag_name']
        for key in three:
            db.session.add(Company_tags(company_id=company_id, tag=three[key], language=key))

    #DB에 반영
    db.session.commit()

    #재검색
    lang = request.headers.get("x-wanted-language")
    name = db.session.query(Company_name.name).filter(and_(Company_name.company_id==company_id, Company_name.language==lang)).first()
    tag_items = db.session.query(Company_tags.tag).filter(and_(Company_tags.company_id==company_id, Company_tags.language==lang)).all()


    result = {}
    result["company_name"] = name[0]

    new_tags = []
    for tag in tag_items :
        new_tags.append(tag[0])

    result["tags"] = new_tags

    result = json.dumps(result, ensure_ascii=False)

    return make_response(result, 201)