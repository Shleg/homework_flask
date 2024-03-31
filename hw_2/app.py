from flask import Flask, render_template, request, redirect, url_for, make_response
import logging

from werkzeug.exceptions import HTTPException

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Создание cookie с данными пользователя
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('user_data', f'name={name}&email={email}')

        return response
    return render_template('base.html')


@app.route('/welcome/')
def welcome():
    # Получение данных из cookie
    user_data_cookie = request.cookies.get('user_data')
    if user_data_cookie:
        user_data = dict(item.split('=') for item in user_data_cookie.split('&'))
        name = user_data.get('name')
    else:
        name = None
    return render_template('welcome.html', name=name)


@app.route('/logout/')
def logout():
    # Удаление cookie с данными пользователя
    response = make_response(redirect(url_for('base')))
    response.set_cookie('user_data', expires=0)
    return response


@app.get('/about/')
def about():
    context = {
        'title': 'О нас'
    }
    return render_template('about.html', **context)


@app.route('/getcookie/')
def get_cookies():
    # получаем значение cookie
    user_data_cookie = request.cookies.get('user_data')
    if user_data_cookie:
        user_data = dict(item.split('=') for item in user_data_cookie.split('&'))
        context = {
            'name': user_data.get('name'),
            'email': user_data.get('email')
        }

        return render_template('getcookie.html', **context)
    return redirect(url_for('base'))

@app.errorhandler(HTTPException)
def handle_exception(e):
    if 400 <= e.code < 500:
        error_type = 'Ошибка клиента'
    elif 500 <= e.code < 600:
        error_type = 'Ошибка сервера'
    else:
        error_type = 'Ошибка'
    logger.warning(e)
    context = {
        'title': error_type,
        'url': request.base_url,
        'error': e.code
    }
    return render_template('error.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
