from flask import Blueprint, make_response

from wanted import db
from wanted.models import Company

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

#자동완성
@bp.route('/')

#검색

#새로운 회사 데이터 저장