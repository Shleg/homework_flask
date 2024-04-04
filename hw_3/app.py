from flask import Flask, render_template, request, redirect, url_for, make_response, flash
import logging

from homework_flask.hw_3.forms import RegistrationForm
from models import db, User
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'mysecretkey'
logger = logging.getLogger(__name__)

db.init_app(app)

with app.app_context():
    db.create_all()  # Создаем таблицы в базе данных


@app.route('/', methods=['GET', 'POST'])
def base():
    users = User.query.all()
    if users:
        context = {'users': users}
        return render_template('base.html', **context)
    return render_template('base.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, last_name=last_name, email=email)
        new_user.set_password(password)  # Хэшируем пароль перед сохранением

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешно завершена!', 'success')  # 'success' - это категория сообщения
        return redirect(url_for('base'))

    return render_template('register.html', form=form)


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
