from flask import Flask, render_template, request, redirect, make_response, session
from data import db_session, job_api
from data.jobs import Jobs
from data.user import User, RegisterForm
from data.login_form import LoginForm
from data.settings_form import SettingsForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_restful import Api, abort
from data import user_api
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        try:
            if user.hashed_password and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                print(current_user)
                return redirect('/')
            else:
                return render_template('login.html', message='Неверно', form=form)
        except(Exception):
            return render_template('login.html', message='Таких тут нет!', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/delete_account')
@login_required
def delete():
    db_sess = db_session.create_session()
    proff = db_sess.query(User).filter(current_user.id == User.id).first()
    if proff:
        db_sess.delete(proff)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/index')
@app.route('/')
def index():
    nazvanie = 'Главная'
    return render_template('base.html', title=nazvanie)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def setting():
    form = SettingsForm()
    if form.is_submitted():
        try:
            if (0 <= int(form.p_time.data.split()[1]) < 24) and (0 <= int(form.p_time.data.split()[3]) < 60):
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(current_user.id == User.id).first()
                user.p_time = form.p_time.data
                user.custom_podd = form.custom_podd.data
                user.prem_image = form.prem_image.data
                db_sess.commit()
                return redirect('/')
            else:
                return render_template('settings.html', title='Настройки',
                                   form=form,
                                   message="Неправильный формат времени")
        except(Exception):
            return render_template('settings.html', title='Настройки',
                                   form=form,
                                   message="Неправильный формат времени")
    return render_template('settings.html', title='Настройки', form=form)


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/training/<prof>')
def train(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list>')
def prof(list):
    lst = ['слесарь'] * 15
    return render_template('prof.html', list=lst, znak=list)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def add_user():
    sess = db_session.create_session()
    user = User()
    user.surname = 'Ridley'
    user.name = 'Scott'
    user.age = 21
    user.position = 'capitan'
    user.email = 'sr@mars.com'
    user.speciality = 'resercher'
    user.set_password('123')
    user.address = 'module 1'
    sess.add(user)
    sess.commit()
    sess.close()


def add_jobs():
    sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    sess.add(job)
    sess.commit()
    sess.close()


def zapros():
    sess = db_session.create_session()
    user = sess.query(User).filter(User.age == 21)
    for el in user:
        print(el.name)
    sess.close()


def main():
    db_session.global_init("db/dobry.db")
    # zapros()
    # add_user()
    # add_jobs()
    app.register_blueprint(job_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    app.run('127.0.0.1', port=80)


if __name__ == '__main__':
    main()