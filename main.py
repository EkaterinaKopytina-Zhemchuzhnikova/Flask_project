from flask import Flask, render_template, redirect, request
from data import db_session
from data.patients_and_snils import LoginPatients
from data.login_form import LoginForm
from data.proposal import Proposal
from data.search_and_show_hospitals import search, show
from data.graphic import plot_graph
import csv

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


@app.route('/info')
def info():
    with open('static/files/info_file.txt', 'r', encoding="utf-8") as f:
        info_about = f.read()
    return render_template("info.html", info_text=info_about, image_hospitals="static/img/map.png")


@app.route('/contact')
def contact_me():
    return render_template("contact.html", dep_adr=ADRESS_DEPARTMENT, dep_img="static/img/map1.png")


@app.route('/proposal', methods=['GET', 'POST'])
def proposal_me():
    form = Proposal()
    return render_template("register_me.html", form=form)


@app.route('/results')
def get_results():
    with open('static/files/1.csv', 'r', ) as f:
        param_dict = csv.DictReader(f, delimiter=';', quotechar='"')
        keys = param_dict.fieldnames
        values = [v for param in param_dict for v in param.values()]
    return render_template("results.html", keys=keys, values=values)


@app.route('/statistics')
def show_statistic():
    return render_template("statistic.html", graph="static/img/plot.png")


@app.route('/logout')
def logout():
    return redirect("/")


def get_image_of_all_hospitals():
    hospitals = ["Лиски, ул. Сеченова, 24", "Воронеж, ул. Красноармейская, 19", "Воронеж, ул. Героев Сибиряков, 37"]
    pt_list = search(hospitals)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(show(pt_list).content)


ADRESS_DEPARTMENT = 'Воронеж, ул. Красноармейская, 52'


def get_image_of_department():
    pt = search([ADRESS_DEPARTMENT])
    map_file = "static/img/map1.png"
    with open(map_file, "wb") as file:
        file.write(show(pt, scale="0.003,0.003").content)


if __name__ == '__main__':
    plot_graph()
    app.run()
    get_image_of_all_hospitals()
    get_image_of_department()

