# coding=utf-8

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    response = '<h1>Hellow World</h1>\n<p>Your browser is {}</p>'.format(user_agent)
    return response
    
@app.route('/user/<name>')
def user(name):
    return '<h1>Hellow, {}!</h1>'.format(name)

@app.route('/cookie')
def cookie():
    response = make_response('<p>This document carries a cookie!</p>')
    response.set_cookie('answer', '42')
    return response

if __name__ == '__main__':
    app.run()