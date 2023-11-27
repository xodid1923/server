from flask import Flask, request, render_template # flask.py 안에 Flask class 로드, 요청 관련 클래스, html로드하는 클래스
from werkzeug.utils import secure_filename # 파일이름, 경로에 대한 기본적인 보안

# flask server 보안 규칙
# 1. html 문서들은 render_template으로 로드 시
# 반드시 templates 폴더 내에 존재해야 한다
# 2. 모든 경로에 대해 접근 불가
# 단, static 경로만 접근 가능

import os
# 'static/imgs'폴더가 없으면 만들어라
if not os.path.exists('static/imgs'):
    os.makedirs('static/imgs')

#내장 변수 __name__을 매개변수로 Flask클래스를 생성
#생성된 인스턴스를 app에 저장!!
app = Flask(__name__)

@app.route('/') # IPv4:port + '/' 경로에 접속 시 호출되는 함수 정의!!
def index():
    # return 쓸 수 있는 결과는 html
    # 1. 태그를 직접
    # 2. 라이브러리 render_template 이용
    
    return '''
    <style>
      form{
         transform: scale(4);
         transform-origin: top left;
      }
      </style>
   <form action="/detect" method="post" enctype="multipart/form-data">
      <input type="file" name="file"></br>
      <input type="submit" value="전송">
   </form>
    
    '''

@app.route('/detect', methods=['POST']) # root경로에서 넘어온 이미지를 받아오는 페이지
def detect():
    # request 관련 페이지들은 
    # route 설정 시 반드시 전송방식을 정의해야 한다
    # GET -> request.arg['Key값']
    # POST -> request.form['Key값']
    # file -> request.files['Key값']

    f = request.files['file']
    filename = secure_filename(f.filename)

    img_path = 'static/imgs/' + filename
    
    # f.save('저장경로/' + filename)
    f.save(img_path)

    i = ImageDetect()
    result = i.detect_img(img_path)

    if result.size == 0:
        return '<h1>탐색 결과 없음</h1>'
    
    cnf = result[0][4]
    nc = int(result[0][5])
    label = i.data[nc]
    output = '<h1>{}일 확률이 {:.2f}%입니다</h1>'.format(label,cnf*100)
    
    # file관련 경로, 이름들은 보안을 지켜주자
    return output
    
# 내가 직접 실행(run)시 내장 변수 __name__이 __main__으로 변한다
if __name__ == '__main__':
    app.run(port=5028)