import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import datetime
import xlsxwriter
from clinic_management.models import Doctor, Service, Appointment, Patient

dejavu_path = '/Users/PilotSoul/Desktop/clinic-automation/clinic_management/DejaVuSerif.ttf'
styles = getSampleStyleSheet()
styles['Normal'].fontName = 'DejaVuSerif'
styles['Heading1'].fontName = 'DejaVuSerif'

pdfmetrics.registerFont(TTFont('DejaVuSerif', dejavu_path, 'UTF-8'))


def find_service(appointment, date_appointment, patient_name, index, appointments_dict):
    services = appointment.services.all()
    for service in services:
        appointments_dict[index] = [date_appointment, patient_name, service.name, service.price]
        index += 1
    return appointments_dict, index


def find_patient(appointment):
    patient = Patient.objects.get(id=appointment.id_patient_id)
    patient_name = f'{patient.admin.last_name} {patient.admin.first_name} {patient.surname}'
    return patient_name


def find_appointments(doc_id, start, finish):
    index = 0
    appointments_dict = {}
    appointments = Appointment.objects.filter(id_doctor=doc_id, date_appointment__gte=start, date_appointment__lte=finish)
    for appoint in appointments:
        patient_name = find_patient(appoint)
        t = appoint.date_appointment
        date_appointment = t.strftime('%d/%m/%Y %H:%M')
        appointments_dict, index = find_service(appoint, date_appointment, patient_name, index, appointments_dict)
    return appointments_dict


def find_doctor(doc_id):
    doctor = Doctor.objects.get(admin=doc_id)
    doctor_name = f'Врач: {doctor.admin.last_name} {doctor.admin.first_name} {doctor.surname}'
    doctor_id = doctor.id
    return doctor_name, doctor_id


def document_by_doctor(doctor, start_date, finish_date):
    buf = io.BytesIO()

    doctor_name, doctor_id = find_doctor(doctor)
    appointments = find_appointments(doctor_id, start_date, finish_date)
    print(appointments)

    # render excel
    workbook = xlsxwriter.Workbook(buf)
    worksheet = workbook.add_worksheet()
    header = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'})
    doctor_header = workbook.add_format({'font_size': 18})
    money = workbook.add_format({'num_format': '#,#0.00', 'font_size': 14})
    normal = workbook.add_format({'font_size': 14})
    count = workbook.add_format({'font_size': 14, 'bold': True})
    header_name = f'Отчет за период: {start_date} - {finish_date}'
    header_table = workbook.add_format({'font_size': 14, 'align': 'center', 'border': 1})
    worksheet.merge_range('A1:E1', header_name, header)
    worksheet.merge_range('A2:E2', doctor_name, doctor_header)
    worksheet.write('A4', 'Дата', header_table)
    worksheet.write('B4', 'Время', header_table)
    worksheet.write('C4', 'Пациент', header_table)
    worksheet.write('D4', 'Услуга', header_table)
    worksheet.write('E4', 'Цена', header_table)
    index = 5
    for key in appointments:
        day, appoint_time = appointments[key][0].split(" ")
        worksheet.write(f'A{index}', f'{day}', normal)
        worksheet.write(f'B{index}', f'{appoint_time}', normal)
        worksheet.write(f'C{index}', f'{appointments[key][1]}', normal)
        worksheet.write(f'D{index}', f'{appointments[key][2]}', normal)
        worksheet.write(f'E{index}', appointments[key][3], money)
        index+=1
    formula = '{'+f'=SUM(E5:E{index-1})'+'}'
    worksheet.write(f'D{index}', 'Итого', count)
    worksheet.write_array_formula(f'E{index}', formula, money)
    worksheet.set_column(f'A1:E{index}', 20)
    workbook.close()

    buf.seek(0)
    return buf