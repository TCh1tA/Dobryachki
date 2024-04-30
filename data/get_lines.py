from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Миссия Колонизация Марса</h1>'


@app.route('/index')
def tibloki():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion')
def promotion():
    lst = ['Человечество вырастает из детства.',
           'Человечеству мала одна планета.',
           'Мы сделаем обитаемыми безжизненные пока планеты.',
           'И начнем с Марса!', 'Присоединяйся!']
    res = '<br>'.join(lst)
    return res


@app.route('/image_mars')
def mars_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src={url_for('static', filename='img/mars.png')} 
                    alt="здесь должна была быть картинка, но не нашлась">
                    <p>Вот она какая красная планета</p>
                  </body>
                </html>'''


@app.route('/promotion_image')
def bootstrap():
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" 
    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link href="static/css/style.css" rel="stylesheet">
  </head>
  <body>
    <h1>Жди нас, Марс!</h1>
    <img src={url_for('static', filename='img/mars.png')} 
                    alt="здесь должна была быть картинка, но не нашлась">
    <div class="alert alert-primary">Человечество вырастает из детства.</div>
    <div class="alert alert-secondary">Человечеству мала одна планета.</div>
    <div class="alert alert-success">Мы сделаем обитаемыми безжизненные пока планеты.</div>
    <div class="alert alert-danger">И начнем с Марса!</div>
    <div class="alert alert-warning">Присоединяйся!</div>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" 
    integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
  </body>
</html>'''


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
