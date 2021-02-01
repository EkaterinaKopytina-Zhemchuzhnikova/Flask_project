from data.hospitals import Hospitals
from data import db_session
from data.patients_and_snils import LoginPatients
from data.doctors import Doctors
from data.reception import Reception
from data.tests import Tests
from data.registered import RegistredPatients
from data.refere import Refer
from data.register_me import Register_me
import datetime as dt

db_session.global_init("db/registry_base1.sqlite")
session = db_session.create_session()


def verification(name, snils):
    user = session.query(LoginPatients).filter(LoginPatients.snils == snils, LoginPatients.fio == name).first()
    return user


def give_my_future_record(snils):  # TODO:
    date = session.query(RegistredPatients).filter(RegistredPatients.snils == snils,
                                                   RegistredPatients.date >= dt.date.today()).first()
    print(date)


def give_hospital_adress():
    return [data.location for data in session.query(Hospitals).all()]


def all_hospitals():
    return [hospital.name for hospital in session.query(Hospitals).all()]


def get_specialitis(hosp):
    hospitals = session.query(Hospitals).filter(Hospitals.name == hosp).first()
    return [speciality.direction for speciality in session.query(Doctors).filter(Doctors.hospid == hospitals.id).all()]


def get_doctors(hosp, spec):
    hospitals = session.query(Hospitals).filter(Hospitals.name == hosp).first()
    return [doctor.doctorsname for doctor in
            session.query(Doctors).filter(Doctors.hospid == hospitals.id, Doctors.direction == spec).all()]


def get_date(docname):  # TODO:
    doctor = session.query(Doctors).filter(Doctors.doctorsname == docname).first()
    return [data.datework for data in session.query(Reception).filter(Reception.docid == doctor.id).all()]


def get_time(docname, data):  # TODO:
    doctor = session.query(Doctors).filter(Doctors.doctorsname == docname).first()
    return [data.time for data in
            session.query(Reception).filter(Reception.docid == doctor.id, Reception.datework == data).all()]


def give_num_file_of_analize(snils=25819001861):  # TODO:сделать нормальный аргумент
    data = session.query(Tests).filter(Tests.patient_snils == snils).first()
    return data.num_file


def send_refer_to_us(mes_text, snils=25819001861):  # TODO:сделать нормальный аргумент
    refer = Refer(id=2, snils=snils, refer_text=mes_text) # TODO:сделать автоинкремент
    session.add(refer)
    session.commit()


def please_register_me(new_user, new_snils, new_user_sex, new_phone): # TODO:сделать автоинкремент
    new_user = Register_me(id=1, fio=new_user, snils=new_snils, phone=new_phone, sex=new_user_sex)
    session.add(new_user)
    session.commit()
