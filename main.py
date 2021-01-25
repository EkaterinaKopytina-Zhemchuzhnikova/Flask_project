from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask, render_template, redirect, request
from data import db_session
from data.patients_and_snils import LoginPatients
from data.login_form import LoginForm
# import data.search_and_show_hospitals

db_session.global_init("db/registry_base.sqlite")

# patient.patients_snils = 35061441102
# patient.patients_fio = "Модовин Петр Иванович"
# session.add(patient)
# session.commit()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        snils = session.query(LoginPatients).filter(LoginPatients.patients_snils == form.password.data).first()
        user_name = session.query(LoginPatients).filter(LoginPatients.patients_fio == form.username.data).first()
        if user_name and snils:
            return render_template('menu.html', user=user_name)
        return render_template("login.html", message="Wrong login or password", form=form)
    return render_template("login.html", title='Электронная регистратура Воронежской области', form=form)


@app.route('/success')
def success():
    return render_template('menu.html')

@app.route('/info')
def info():
    with open('static/files/info_file.txt', 'r', encoding="utf-8") as f:
        info_about = f.read()
    return render_template("info.html", info_text=info_about)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    app.run()