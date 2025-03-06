from flask import Flask, request
from auto_sign import GongXueYun
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>工学云签到</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { padding: 20px; font-family: Arial; }
                input { width: 100%; padding: 10px; margin: 5px 0; }
                button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h2>工学云自动签到</h2>
            <form action="/sign" method="get">
                <input type="text" name="phone" placeholder="手机号" required><br>
                <input type="password" name="pwd" placeholder="密码" required><br>
                <button type="submit">一键签到</button>
            </form>
        </body>
    </html>
    '''

@app.route('/sign')
def sign():
    phone = request.args.get('phone', '')
    pwd = request.args.get('pwd', '')
    
    if not phone or not pwd:
        return "请输入手机号和密码"
    
    gxy = GongXueYun(phone, pwd)
    if gxy.login():
        if gxy.sign():
            return "签到成功！"
    return "签到失败，请检查账号密码"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
