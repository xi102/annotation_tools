from flask import jsonify, request
from flask_mail import Message

from app import db, mail
from app.apis import api
from app.models.user import User


@api.route('/login', methods=['POST'])
def login():
    username = request.json.get("_username")
    password = request.json.get('_password')
    result = User.query.filter_by(username=username).first()
    # if result is None or result.password != password:
    if result is None or result.password != password:
        return jsonify({
            'flag': 0,
            'errorText': '用户名或密码错误'
        })
    if result.password == password:
        return jsonify({
            'flag': 1
        })


@api.route('/register', methods=['POST'])
def register():
    username = request.json.get('_username')
    password = request.json.get('_password')
    email = request.json.get('_email')
    if username is None or password is None or email is None:
        # return jsonify({"flag":0})
        return jsonify({
            'flag': 0,
            'errorText': '注册信息不合要求'
        })
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            'flag': 2,
            'errorText': '用户名已存在'
        })
    user = User(username=username)
    user.password = password
    user.email = email
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'flag': 1
    })


@api.route('/forget', methods=['POST'])
def createCode():
    findUser = request.json.get("_username")
    findEmail = request.json.get("_email")
    codeReceived = request.json.get("_code")
    result = User.query.filter_by(email=findEmail, username=findUser).first()
    if result is None:
        return jsonify({
            'flag': 0,
            'errorText': '该邮箱未注册'
        })
    if result is not None:
        codeSent = result.code
        if codeReceived is None:
            msg = Message("Hi!This is a test ", sender='924981812@qq.com',
                          recipients=['me_xingwei@163.com'])
            msg.body = "你的验证码为：      " + codeSent
            mail.send(msg)
            return jsonify({
                "flag": 1
            })
        if codeReceived is not None:
            if codeReceived == codeSent:
                # 修改密码
                return jsonify({
                    "flag": 1
                })
            else:
                return jsonify({
                    "flag": 0,
                    "errorText": "验证码错误"
                })
