#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/6 9:46
# @Author  : cyj
# @Site    : 
# @File    : server.py
# @Software: PyCharm

from flask import Flask, render_template, session, request

from AI import AI
import json

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'


@app.route('/', methods=['POST'])
def post_info():
    print('receive AI message:', request.form.get('game_id', 'wrong_game_id'))

    message = {'game_id': request.form.get('game_id', 'wrong_game_id'),
               'user_id': request.form.get('user_id', 'wrong_user_id'), 'msg': request.form.get('msg', 'wrong_msg')}

    ai = AI(message['game_id'])
    result = []
    result['msg'] = ai.play(message['msg'])
    result['user_id'] = 'MuGo'
    result['method'] = 'play'
    print('sending AI message:', result)
    return json.dumps(result)


if __name__ == '__main__':
    # listen all requests form port 6000
    app.run('0.0.0.0', port=6000)
