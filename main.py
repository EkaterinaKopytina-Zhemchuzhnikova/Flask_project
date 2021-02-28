from flask import Flask, render_template, redirect, request
from forms.login_form import LoginForm
from forms.proposal import Proposal
from data.search_and_show_hospitals import search, show
from data.graphic import plot_graph
import csv
from data.validation import validation_user_fio, validation_user_snils, validation_user_phone
from data.work_with_db import all_hospitals, get_specialitis, get_doctors, \
    give_my_future_record, verification, give_hospital_adress, give_num_file_of_analize, \
    send_refer_to_us, please_register_me, delete_future_record, get_date, get_time, record_me_to_doctor, \
    get_choose_doc_id, get_user_name
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        procced_user_fio = validation_user_fio(form.username.data)
        procced_user_snils = validation_user_snils(form.password.data)
        if procced_user_fio and procced_user_snils:
            if verification(procced_user_fio, procced_user_snils):
                return redirect('/home')
            return render_template("login.html", message="Wrong login or password", form=form)
        return render_template("login.html", message="Wrong login or password", form=form)
    return render_template("login.html", title='Электронная регистратура Воронежской области', form=form)


@app.route('/home', methods=['GET', 'POST'])
def show_record():
    my_record = give_my_future_record()
    hospitals = all_hospitals()
    user_name = get_user_name()
    if request.method == 'GET':
        return render_template("record.html", name=user_name, records=my_record, hospitals=hospitals, speciality=[],
                               doctors=[])
    elif request.method == 'POST':
        if request.form["choose_param"] == "have_del":
            del_my_record = request.form["my_record"]
            delete_future_record(del_my_record)
            return render_template("record.html", name=user_name, records=give_my_future_record(), hospitals=hospitals,
                                   speciality=[],
                                   doctors=[])

        elif request.form["choose_param"] == "have_hosp":
            choose_hosp = request.form["hosp"]
            specialitis = get_specialitis(choose_hosp)
            hosp_index = hospitals.index(choose_hosp)
            hospitals[0], hospitals[hosp_index] = hospitals[hosp_index], hospitals[0]
            return render_template("record.html", name=user_name, records=my_record, hospitals=hospitals,
                                   speciality=specialitis,
                                   doctors=[])
        elif request.form["choose_param"] == "have_spec":
            choose_hosp = request.form["hosp"]
            specialitis = get_specialitis(choose_hosp)
            choose_spec = request.form["spec"]
            spec_index = specialitis.index(choose_spec)
            doctors = get_doctors(choose_spec)
            specialitis[0], specialitis[spec_index] = specialitis[spec_index], specialitis[0]
            return render_template("record.html", name=user_name, records=my_record, hospitals=hospitals,
                                   speciality=specialitis,
                                   doctors=doctors)
        elif request.form["choose_param"] == "have_record":
            choose_doc = request.form["doc"]
            get_choose_doc_id(choose_doc)
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
        valid_fio = validation_user_fio(new_user)
        new_snils = request.form['password']
        valid_snils = validation_user_snils(new_snils)
        new_user_sex = request.form['sex']
        new_phone = request.form['telephone']
        valid_phone = validation_user_phone(new_phone)
        if valid_fio and valid_snils and valid_phone:
            please_register_me(valid_fio, int(valid_snils), new_user_sex, new_phone)
            return redirect("/register_me_thanks")
        return render_template("register_me.html", message="Wrong data", form=form)


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
    plot_graph()
    return render_template("statistic.html", graph="static/img/plot.png")


@app.route('/help')
def help_me():
    user = get_user_name()
    with open('static/files/help.txt', 'r', encoding="utf-8") as f:
        help_text = f.read().split(";")
    return render_template("help.html", help_text=help_text, hello=user, image_medcine="static/img/medcine.png")


@app.route('/choose_time', methods=['GET', 'POST'])
def choose_time():
    dates = get_date()
    if request.method == 'GET':
        return render_template("choose_time_for_record.html", dates=dates, time=[])
    elif request.method == 'POST':
        if request.form["choose_param"] == "have_date":
            choose_date = request.form['date']
            if len(dates) > 1:
                year, mon, date = map(int, choose_date.split('-'))
                date_index = dates.index(dt.date(year, mon, date))
                dates[0], dates[date_index] = dates[date_index], dates[0]
            time = get_time(choose_date)
            return render_template("choose_time_for_record.html", dates=dates, time=time)
        elif request.form["choose_param"] == "have_time":
            choose_time = request.form['time']
            message = record_me_to_doctor(choose_time)
            return render_template("choose_time_for_record_thanks.html", message=message)


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


def main():
    get_image_of_all_hospitals()
    get_image_of_department()
    app.run()


if __name__ == '__main__':
    main()
