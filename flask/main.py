from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def q():
    return 'http://127.0.0.1:8080/training/Врач  http://127.0.0.1:8080/training/инженер'
@app.route('/table/<sex>/<int:years>')
def index(sex,years):
    if 'famele' in sex and years <= 21:
        return render_template('1.html')

#<img src="..\static\123.png"  alt="картинка">
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
