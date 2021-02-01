from flask import Flask, render_template, redirect, request, url_for
from data.login_form import LoginForm
from data.proposal import Proposal
from data.search_and_show_hospitals import search, show
from data.graphic import plot_graph
import csv
from data.work_with_db import all_hospitals, get_specialitis, get_doctors, \
    give_my_future_record, verification, give_hospital_adress, give_num_file_of_analize, \
    send_refer_to_us, please_register_me

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = verification(form.username.data, form.password.data)
        if user:
            return redirect('/home')
        return render_template("login.html", message="Wrong login or password", form=form)
    return render_template("login.html", title='Электронная регистратура Воронежской области', form=form)


@app.route('/home', methods=['GET', 'POST'])
def show_record():
    my_record = []
    hospitals = all_hospitals()
    if request.method == 'GET':
        return render_template("record.html", records=my_record, hospitals=hospitals, speciality=[],
                               doctors=[])
    elif request.method == 'POST':
        if request.form["choose_param"] == "have_hosp":
            choose_hosp = request.form["hosp"]
            specialitis = get_specialitis(choose_hosp)
            hosp_index = hospitals.index(choose_hosp)
            hospitals[0], hospitals[hosp_index] = hospitals[hosp_index], hospitals[0]
            return render_template("record.html", records=my_record, hospitals=hospitals, speciality=specialitis,
                                   doctors=[])
        elif request.form["choose_param"] == "have_spec":
            choose_hosp = request.form["hosp"]
            specialitis = get_specialitis(choose_hosp)
            choose_spec = request.form["spec"]
            spec_index = specialitis.index(choose_spec)
            doctors = get_doctors(hospitals[0], choose_spec)
            specialitis[0], specialitis[spec_index] = specialitis[spec_index], specialitis[0]
            return render_template("record.html", records=my_record, hospitals=hospitals, speciality=specialitis,
                                   doctors=doctors)
        elif request.form["choose_param"] == "have_record":
            return redirect("/choose_time")


@app.route('/info')
def info():
    with open('static/files/info_file.txt', 'r', encoding="utf-8") as f:
        info_about = f.read()
    return render_template("info.html", info_text=info_about, image_hospitals="static/img/map.png")


@app.route('/info_for_login')
def info_for_login():
    with open('static/files/info_file.txt', 'r', encoding="utf-8") as f:
        info_about = f.read()
    return render_template("info_for_login.html", info_text=info_about, image_hospitals="static/img/map.png")


@app.route('/contact')
def contact_me():
    return render_template("contact.html", dep_adr=ADRESS_DEPARTMENT, dep_img="static/img/map1.png")


@app.route('/contact_for_login')
def contact_me_for_login():
    return render_template("contact_for_login.html", dep_adr=ADRESS_DEPARTMENT, dep_img="static/img/map1.png")


@app.route('/proposal', methods=['GET', 'POST'])
def proposal_me():
    form = Proposal()
    if request.method == 'GET':
        return render_template("register_me.html", form=form)
    elif request.method == 'POST':
        new_user = request.form['username']
        new_snils = request.form['password']
        new_user_sex = request.form['sex']
        new_phone = request.form['telephone']
        please_register_me(new_user, new_snils, new_user_sex, new_phone)
        return redirect("/register_me_thanks")


@app.route('/refere_to_us', methods=['GET', 'POST'])
def refere_to_us():
    if request.method == 'GET':
        return render_template("refer_to_us.html")
    elif request.method == 'POST':
        user_text_for_us = request.form['about']
        send_refer_to_us(user_text_for_us)
        return redirect("/refer_to_us_thanks")


@app.route('/register_me_thanks')
def register_me_thanks():
    return render_template("register_me_thanks.html")


@app.route('/refer_to_us_thanks')
def refer_to_us_thanks():
    return render_template("refer_to_us_thanks.html")


@app.route('/results')
def get_results():
    num_file = give_num_file_of_analize()
    with open(f'static/files/{num_file}.csv', 'r', ) as f:
        param_dict = csv.DictReader(f, delimiter=';', quotechar='"')
        keys = param_dict.fieldnames
        values = [v for param in param_dict for v in param.values()]
    return render_template("results.html", keys=keys, values=values)


@app.route('/statistics')
def show_statistic():
    return render_template("statistic.html", graph="static/img/plot.png")


@app.route('/choose_time', methods=['GET', 'POST'])
def choose_time():
    if request.method == 'GET':
        dates = ['16.05', '18.06']
        time = ['15.30']
        return render_template("choose_time_for_record.html", dates=dates, time=time)
    elif request.method == 'POST':
        choose_date = request.form['date']
        choose_time = request.form['time']
        return render_template("choose_time_for_record_thanks.html")


@app.route('/logout')
def logout():
    return redirect("/")


def get_image_of_all_hospitals():
    hospitals = give_hospital_adress()
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


get_image_of_all_hospitals()
get_image_of_department()
plot_graph()
app.run()
