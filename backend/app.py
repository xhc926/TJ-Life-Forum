import os
# from flask import Flask
from flaskr import create_app
from flask import Flask, jsonify, request, g, session

app = create_app()

# 清除 Jinja2 模板缓存
app.jinja_env.cache = {}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
