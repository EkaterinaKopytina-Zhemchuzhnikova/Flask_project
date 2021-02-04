from data.hospitals import Hospitals
from data import db_session
from data.patients import LoginPatients
from data.doctors import Doctors
from data.reception import Reception
from data.tests import Tests
from data.registered import RegistredPatients
from data.refere import Refer
from data.register_me import Register_me
import datetime as dt
from flask import session as se

db_session.global_init("db/registry_base.sqlite")
session = db_session.create_session()


def verification(name, snils):
    user = session.query(LoginPatients).filter(LoginPatients.snils == snils, LoginPatients.patient_fio == name).first()
    if user:
        patient_snils, patient_name = se.get('patient_snils', None), se.get('patient_name', None)
        se['patient_snils'], se['patient_name'] = user.snils, user.patient_fio
    return user


def get_user_name():
    return se['patient_name']


def give_my_future_record():
    record_list = []
    for data in session.query(RegistredPatients).filter(RegistredPatients.snils == se['patient_snils'],
                                                        RegistredPatients.date >= dt.date.today()).all():
        for doc in session.query(Doctors).filter(Doctors.doc_id == data.doc_id).all():

            if data.doc_id == doc.doc_id:
                record_list.append(f'{data.date} {data.time} {doc.doctor_fio}')
    return record_list


def delete_future_record(record):
    rec_date, rec_time, *rec_doc_fio = record.split()
    for data in session.query(RegistredPatients).filter(RegistredPatients.snils == se['patient_snils'],
                                                        RegistredPatients.date == rec_date,
                                                        RegistredPatients.time == rec_time).all():
        for doc in session.query(Doctors).all():
            if doc.doc_id == data.doc_id:
                session.delete(data)
                session.commit()


def count_data_for_graph():
    count_record_dict = {}
    all_date = [data.date for data in
                session.query(RegistredPatients).filter(RegistredPatients.snils == se['patient_snils']).all()]
    month = list(set([mon.month for mon in all_date]))
    for mon in month:
        count_record_dict[mon] = len([data for data in all_date if data.month == mon])
    return count_record_dict


def give_hospital_adress():
    return [data.location for data in session.query(Hospitals).all()]


def all_hospitals():
    return [hospital.name for hospital in session.query(Hospitals).all()]


def get_specialitis(hosp):
    hospitals = session.query(Hospitals).filter(Hospitals.name == hosp).first()
    choose_hosp = se.get('choose_hosp_id', None)
    se['choose_hosp_id'] = hospitals.id
    return [speciality.direction for speciality in
            session.query(Doctors).filter(Doctors.hosp_id == se['choose_hosp_id']).all()]


def get_doctors(spec):
    choose_spec = se.get('choose_spec', None)
    se['choose_spec'] = spec
    return [doctor.doctor_fio for doctor in
            session.query(Doctors).filter(Doctors.hosp_id == se['choose_hosp_id'],
                                          Doctors.direction == se['choose_spec']).all()]


def get_choose_doc_id(doc_fio):
    doctor = session.query(Doctors).filter(Doctors.hosp_id == se['choose_hosp_id'],
                                           Doctors.direction == se['choose_spec'],
                                           Doctors.doctor_fio == doc_fio).first()
    choose_doc_id = se.get('choose_doc_id', None)
    se['choose_doc_id'] = doctor.doc_id


def get_date():
    return list(set([data.date_work for data in
                     session.query(Reception).filter(Reception.doc_id == se['choose_doc_id'],
                                                     Reception.date_work >= dt.date.today(),
                                                     Reception.free == 1).all()]))


def get_time(data):
    choose_date = se.get('choose_date', None)
    se['choose_date'] = data
    return [data.time for data in
            session.query(Reception).filter(Reception.doc_id == se['choose_doc_id'],
                                            Reception.date_work == se['choose_date']).all()]


def record_me_to_doctor(time):
    new_record = RegistredPatients(snils=se['patient_snils'], patient_fio=se['patient_name'],
                                   date=se['choose_date'], time=time, doc_id=se['choose_doc_id'])
    session.add(new_record)
    session.commit()


def give_num_file_of_analize():
    data = session.query(Tests).filter(Tests.patient_snils == se['patient_snils']).first()
    return data.num_file


def send_refer_to_us(mes_text):
    refer = Refer(snils=se['patient_snils'], refer_text=mes_text)
    session.add(refer)
    session.commit()


def please_register_me(new_user, new_snils, new_user_sex, new_phone):
    new_user = Register_me(fio=new_user, snils=new_snils, phone=new_phone, sex=new_user_sex)
    session.add(new_user)
    session.commit()
