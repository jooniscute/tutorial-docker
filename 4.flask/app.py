import os
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

#APP_COLOR이라는 환경변수가 있으면 읽어와서 color 변수에 담음
color = os.environ.get('APP_COLOR')

@app.route('/')
def main():
    return render_template('hello.html', color=color)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
