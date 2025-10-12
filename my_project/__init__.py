"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""

import os
import re
from datetime import datetime, timedelta
from http import HTTPStatus
import secrets
import jwt
from typing import Dict, Any
from functools import wraps
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, request, g
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from my_project.auth.route import register_routes

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

# Database
db = SQLAlchemy()

todos = {}


def init_autodoc_swagger(app: Flask) -> None:
    app.config.setdefault("SWAGGER", {
        "uiversion": 3,
        "title": "Medical Management System API",
        "openapi": "3.0.3",
    })

    swagger_template = {
        "openapi": "3.0.3",
        "info": {
            "title": "Medical Management System API",
            "version": "1.0.0",
            "description": "Complete REST API for medical management system with authentication",
            "contact": {"name": "Andrii Pavelchak", "email": "apavelchak@gmail.com"},
            "license": {"name": "MIT"},
        },
        "servers": [
            {"url": "/"}
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"bearerAuth": []}],
    }

    Swagger(app, template=swagger_template)

def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    """
    Creates Flask application
    :param app_config: Flask configuration
    :param additional_config: additional configuration
    :return: Flask application object
    """
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config = {**app.config, **app_config}
    
    CORS(app)
    _init_db(app)
    register_routes(app)
    _init_swagger(app)
    _init_trigger(app)
    _init_procedures(app)
    #_init_doctor_symptome(app,2,3) #2b
    #_init_noname_insert(app)  #2c
    #create_dynamic_tables_procedure(app)  #2e iii
    #Billing_AVG(app)
    
    return app
#2b
def _init_doctor_symptome(app: Flask, current_doctor_id: int,current_symptome_id: int) -> None:
    with app.app_context():
        db.session.execute("CALL AddDoctorSymptome(:current_doctor_id, :current_symptome_id)", {
            'current_doctor_id': current_doctor_id,
            'current_symptome_id': current_symptome_id
        })
        db.session.commit()

#2c
def _init_noname_insert(app: Flask) -> None:
    with app.app_context():
        db.session.execute("""

DROP PROCEDURE IF EXISTS InsertNonameIllnesses;
        CREATE PROCEDURE InsertNonameIllnesses()
        BEGIN
            DECLARE i INT DEFAULT 0;
            DECLARE start_number INT DEFAULT 1000;

            WHILE i < 10 DO
                INSERT INTO illneses (illness_name, treatment_plan)
                VALUES (CONCAT('Noname', start_number + i), 'Treatment plan for Noname');

                SET i = i + 1;
            END WHILE;
        END;
        """)

        db.session.commit()

def Billing_AVG(app: Flask) -> None:
    with app.app_context():
        db.session.execute("""

    DROP FUNCTION IF EXISTS CalculateAverageTotalAmount;

    CREATE FUNCTION CalculateAverageTotalAmount()
    RETURNS DECIMAL(10, 2)
    DETERMINISTIC
    BEGIN
        DECLARE result DECIMAL(10, 2);
    
        SELECT AVG(total_amount) INTO result FROM Billing;
    
        RETURN result;
    END
        """)

        db.session.commit()

def create_dynamic_tables_procedure(app: Flask) -> None:

    with app.app_context():
        db.session.execute("""
        DROP PROCEDURE IF EXISTS CreateTablesWithRandomColumns;

        CREATE PROCEDURE CreateTablesWithRandomColumns()
        BEGIN
            DECLARE table_name VARCHAR(128);
            DECLARE done INT DEFAULT 0;

            DECLARE table_cursor CURSOR FOR SELECT DISTINCT id FROM award;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

            OPEN table_cursor;

            read_loop: LOOP
                FETCH table_cursor INTO table_name;

                IF done THEN
                    LEAVE read_loop;
                END IF;

                SET @dynamic_table_name = CONCAT(table_name, '_', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'));

                SET @num_columns = FLOOR(1 + RAND() * 9);

                SET @create_table_sql = CONCAT('CREATE TABLE ', @dynamic_table_name, ' (');

                SET @col_index = 1;
                WHILE @col_index <= @num_columns DO
                    SET @col_name = CONCAT('Column_', @col_index);
                    SET @col_type = CASE FLOOR(RAND() * 4)
                        WHEN 0 THEN 'INT'
                        WHEN 1 THEN 'VARCHAR(50)'
                        WHEN 2 THEN 'FLOAT'
                        WHEN 3 THEN 'DATETIME'
                    END;

                    SET @create_table_sql = CONCAT(@create_table_sql, @col_name, ' ', @col_type);

                    IF @col_index < @num_columns THEN
                        SET @create_table_sql = CONCAT(@create_table_sql, ', ');
                    END IF;

                    SET @col_index = @col_index + 1;
                END WHILE;

                SET @create_table_sql = CONCAT(@create_table_sql, ');');

                PREPARE stmt FROM @create_table_sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            END LOOP;

            CLOSE table_cursor;
        END;
        """)
        db.session.commit()




def _init_swagger(app: Flask) -> None:
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token. Format: Bearer <token>'
        }
    }
    
    api = Api(
        app, 
        title='Medical Management System API',
        description='Complete REST API for medical management system with authentication',
        version='1.0',
        doc='/api/docs/',
        prefix='/api/v1',
        authorizations=authorizations,
        security='Bearer'
    )
    
    # Doctor models
    doctor_model = api.model('Doctor', {
        'doctor_id': fields.Integer(description='Doctor ID'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'specialty_id': fields.Integer(description='Specialty ID'),
        'phone_number': fields.String(description='Phone number'),
        'email': fields.String(description='Email address')
    })
    
    doctor_large_model = api.model('DoctorLarge', {
        'doctor_id': fields.Integer(description='Doctor ID'),
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name'),
        'specialty': fields.Nested(api.model('Specialty', {
            'specialty_id': fields.Integer(description='Specialty ID'),
            'specialty_name': fields.String(description='Specialty name')
        })),
        'phone_number': fields.String(description='Phone number'),
        'email': fields.String(description='Email address')
    })
    
    # Patient models
    patient_model = api.model('Patient', {
        'patient_id': fields.Integer(description='Patient ID'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'date_of_birth': fields.Date(description='Date of birth'),
        'phone_number': fields.String(description='Phone number'),
        'email': fields.String(description='Email address'),
        'address': fields.String(description='Address')
    })
    
    # Specialty models
    specialty_model = api.model('Specialty', {
        'specialty_id': fields.Integer(description='Specialty ID'),
        'specialty_name': fields.String(required=True, description='Specialty name')
    })
    
    # Illness models
    illness_model = api.model('Illness', {
        'illness_id': fields.Integer(description='Illness ID'),
        'illness_name': fields.String(required=True, description='Illness name'),
        'treatment_plan': fields.String(description='Treatment plan')
    })
    
    # Symptom models
    symptom_model = api.model('Symptom', {
        'symptome_id': fields.Integer(description='Symptom ID'),
        'symptome_name': fields.String(required=True, description='Symptom name')
    })
    
    # Appointment models
    appointment_model = api.model('Appointment', {
        'appointment_id': fields.Integer(description='Appointment ID'),
        'doctor_id': fields.Integer(description='Doctor ID'),
        'patient_id': fields.Integer(description='Patient ID'),
        'appointment_date': fields.Date(required=True, description='Appointment date'),
        'appointment_time': fields.String(required=True, description='Appointment time'),
        'consultation_fee': fields.Float(description='Consultation fee')
    })
    
    # Billing models
    billing_model = api.model('Billing', {
        'bill_id': fields.Integer(description='Bill ID'),
        'appointment_id': fields.Integer(description='Appointment ID'),
        'total_amount': fields.Float(description='Total amount'),
        'payment_status': fields.String(description='Payment status'),
        'payment_method': fields.String(description='Payment method'),
        'billing_date': fields.Date(description='Billing date')
    })
    
    # Diagnosis models
    diagnosis_model = api.model('Diagnosis', {
        'diagnosis_id': fields.Integer(description='Diagnosis ID'),
        'illness_id': fields.Integer(description='Illness ID'),
        'doctor_id': fields.Integer(description='Doctor ID'),
        'patient_id': fields.Integer(description='Patient ID'),
        'diagnosis_date': fields.Date(required=True, description='Diagnosis date')
    })
    
    # Schedule models
    schedule_model = api.model('Schedule', {
        'schedule_id': fields.Integer(description='Schedule ID'),
        'doctor_id': fields.Integer(description='Doctor ID'),
        'day_of_week': fields.String(description='Day of week'),
        'start_time': fields.String(description='Start time'),
        'end_time': fields.String(description='End time')
    })
    
    # Appointment booking models
    appointment_booking_model = api.model('AppointmentBooking', {
        'booking_id': fields.Integer(description='Booking ID'),
        'appointment_id': fields.Integer(description='Appointment ID'),
        'booking_date': fields.Date(required=True, description='Booking date'),
        'booking_time': fields.String(required=True, description='Booking time')
    })
    
    # Recovery protocol models
    recovery_protocol_model = api.model('RecoveryProtocol', {
        'recovery_protocol_id': fields.Integer(description='Recovery Protocol ID'),
        'doctor_id': fields.Integer(description='Doctor ID'),
        'patient_id': fields.Integer(description='Patient ID'),
        'recovery_plan': fields.String(description='Recovery plan')
    })
    
    # Doctor-Symptom relation models
    doctor_symptom_model = api.model('DoctorSymptom', {
        'doctor_id': fields.Integer(description='Doctor ID'),
        'symptome_id': fields.Integer(description='Symptom ID')
    })
    
    # Authentication models
    login_model = api.model('Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })
    
    register_model = api.model('Register', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
        'email': fields.String(required=True, description='Email')
    })
    
    # Response models
    message_response_model = api.model('MessageResponse', {
        'message': fields.String(description='Response message')
    })
    
    token_response_model = api.model('TokenResponse', {
        'token': fields.String(description='JWT Access Token'),
        'user': fields.Nested(api.model('UserInfo', {
            'id': fields.Integer(description='User ID'),
            'username': fields.String(description='Username'),
            'email': fields.String(description='Email')
        })),
        'message': fields.String(description='Success message')
    })
    
    health_model = api.model('HealthStatus', {
        'status': fields.String(description='System status'),
        'message': fields.String(description='Status message'),
        'version': fields.String(description='API version'),
        'database': fields.String(description='Database status'),
        'timestamp': fields.String(description='Current timestamp')
    })
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                api.abort(401, 'Token is missing!')
            
            try:
                if token.startswith('Bearer '):
                    token = token[7:]
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                g.current_user = data['username']
            except:
                api.abort(401, 'Invalid token!')
            
            return f(*args, **kwargs)
        return decorated
    
    # Mock users for authentication
    users_db = {
        'admin': {
            'id': 1,
            'username': 'admin',
            'email': 'admin@medical.com',
            'password': generate_password_hash('admin123'),
        },
        'doctor': {
            'id': 2,
            'username': 'doctor',
            'email': 'doctor@medical.com', 
            'password': generate_password_hash('doctor123'),
        }
    }
    
    # Create namespaces
    ns_auth = api.namespace('auth', description='Authentication and authorization')
    ns_doctors = api.namespace('doctors', description='Doctor management')
    ns_patients = api.namespace('patients', description='Patient management')
    ns_specialties = api.namespace('specialties', description='Specialty management')
    ns_illnesses = api.namespace('illnesses', description='Illness management')
    ns_symptoms = api.namespace('symptoms', description='Symptom management')
    ns_appointments = api.namespace('appointments', description='Appointment management')
    ns_billing = api.namespace('billing', description='Billing management')
    ns_diagnoses = api.namespace('diagnoses', description='Diagnosis management')
    ns_schedules = api.namespace('schedules', description='Schedule management')
    ns_bookings = api.namespace('bookings', description='Appointment booking management')
    ns_recovery = api.namespace('recovery', description='Recovery protocol management')
    ns_relations = api.namespace('relations', description='Doctor-Symptom relations')
    ns_health = api.namespace('health', description='System monitoring')
    
    # Authentication endpoints
    @ns_auth.route('/register')
    class Register(Resource):
        @api.expect(register_model)
        @api.marshal_with(message_response_model)
        def post(self):
            """Register new user"""
            data = request.get_json()
            username = data.get('username')
            
            if not username or not data.get('password') or not data.get('email'):
                api.abort(400, 'Username, password and email are required')
            
            if username in users_db:
                api.abort(400, f'User {username} already exists')
            
            users_db[username] = {
                'id': len(users_db) + 1,
                'username': username,
                'email': data.get('email'),
                'password': generate_password_hash(data.get('password')),
            }
            
            return {'message': f'User {username} registered successfully!'}, 201
    
    @ns_auth.route('/login')
    class Login(Resource):
        @api.expect(login_model)
        @api.marshal_with(token_response_model)
        def post(self):
            """Login and get JWT token"""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            user = users_db.get(username)
            if not user or not check_password_hash(user['password'], password):
                api.abort(401, 'Invalid credentials')
            
            token = jwt.encode({
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return {
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                },
                'message': 'Login successful!'
            }
    
    # Doctor endpoints
    @ns_doctors.route('/')
    class DoctorsList(Resource):
        @api.marshal_list_with(doctor_model)
        def get(self):
            """Get all doctors"""
            from my_project.auth.controller import doctors_controller
            doctors = doctors_controller.find_all()
            return [doctor.put_into_dto() for doctor in doctors]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(doctor_model)
        @api.marshal_with(doctor_model)
        def post(self):
            """Create new doctor"""
            from my_project.auth.controller import doctors_controller
            from my_project.auth.domain.orders.doctors import Doctors
            data = request.get_json()
            doctor = Doctors.create_from_dto(data)
            doctors_controller.create_doctor(doctor)
            return doctor.put_into_dto(), 201
    
    @ns_doctors.route('/all')
    class DoctorsWithSpecialty(Resource):
        @api.marshal_list_with(doctor_large_model)
        def get(self):
            """Get all doctors with specialty information"""
            from my_project.auth.controller import doctors_controller
            doctors = doctors_controller.find_with_specialty()
            return [doctor.put_into_large_dto() for doctor in doctors]
    
    @ns_doctors.route('/<int:doctor_id>')
    class Doctor(Resource):
        @api.marshal_with(doctor_model)
        def get(self, doctor_id):
            """Get doctor by ID"""
            from my_project.auth.controller import doctors_controller
            doctor = doctors_controller.find_by_id(doctor_id)
            if not doctor:
                api.abort(404, 'Doctor not found')
            return doctor.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(doctor_model)
        @api.marshal_with(message_response_model)
        def put(self, doctor_id):
            """Update doctor by ID"""
            from my_project.auth.controller import doctors_controller
            from my_project.auth.domain.orders.doctors import Doctors
            data = request.get_json()
            doctor = Doctors.create_from_dto(data)
            doctors_controller.update_doctor(doctor_id, doctor)
            return {'message': 'Doctor updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, doctor_id):
            """Delete doctor by ID"""
            from my_project.auth.controller import doctors_controller
            doctors_controller.delete_doctor(doctor_id)
            return {'message': 'Doctor deleted successfully'}
    
    # Patient endpoints
    @ns_patients.route('/')
    class PatientsList(Resource):
        @api.marshal_list_with(patient_model)
        def get(self):
            """Get all patients"""
            from my_project.auth.controller import patients_controller
            patients = patients_controller.find_all()
            return [patient.put_into_dto() for patient in patients]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(patient_model)
        @api.marshal_with(patient_model)
        def post(self):
            """Create new patient"""
            from my_project.auth.controller import patients_controller
            from my_project.auth.domain.orders.patients import Patients
            data = request.get_json()
            patient = Patients.create_from_dto(data)
            patients_controller.create_patient(patient)
            return patient.put_into_dto(), 201
    
    @ns_patients.route('/<int:patient_id>')
    class Patient(Resource):
        @api.marshal_with(patient_model)
        def get(self, patient_id):
            """Get patient by ID"""
            from my_project.auth.controller import patients_controller
            patient = patients_controller.find_by_id(patient_id)
            if not patient:
                api.abort(404, 'Patient not found')
            return patient.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(patient_model)
        @api.marshal_with(message_response_model)
        def put(self, patient_id):
            """Update patient by ID"""
            from my_project.auth.controller import patients_controller
            from my_project.auth.domain.orders.patients import Patients
            data = request.get_json()
            patient = Patients.create_from_dto(data)
            patients_controller.update_patient(patient_id, patient)
            return {'message': 'Patient updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, patient_id):
            """Delete patient by ID"""
            from my_project.auth.controller import patients_controller
            patients_controller.delete_patient(patient_id)
            return {'message': 'Patient deleted successfully'}
    
    # Specialty endpoints
    @ns_specialties.route('/')
    class SpecialtiesList(Resource):
        @api.marshal_list_with(specialty_model)
        def get(self):
            """Get all specialties"""
            from my_project.auth.controller import specialties_controller
            specialties = specialties_controller.find_all()
            return [specialty.put_into_dto() for specialty in specialties]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(specialty_model)
        @api.marshal_with(specialty_model)
        def post(self):
            """Create new specialty"""
            from my_project.auth.controller import specialties_controller
            from my_project.auth.domain.orders.specialities import Specialties
            data = request.get_json()
            specialty = Specialties.create_from_dto(data)
            specialties_controller.create_specialty(specialty)
            return specialty.put_into_dto(), 201
    
    @ns_specialties.route('/<int:specialty_id>')
    class Specialty(Resource):
        @api.marshal_with(specialty_model)
        def get(self, specialty_id):
            """Get specialty by ID"""
            from my_project.auth.controller import specialties_controller
            specialty = specialties_controller.find_by_id(specialty_id)
            if not specialty:
                api.abort(404, 'Specialty not found')
            return specialty.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(specialty_model)
        @api.marshal_with(message_response_model)
        def put(self, specialty_id):
            """Update specialty by ID"""
            from my_project.auth.controller import specialties_controller
            from my_project.auth.domain.orders.specialities import Specialties
            data = request.get_json()
            specialty = Specialties.create_from_dto(data)
            specialties_controller.update_specialty(specialty_id, specialty)
            return {'message': 'Specialty updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, specialty_id):
            """Delete specialty by ID"""
            from my_project.auth.controller import specialties_controller
            specialties_controller.delete_specialty(specialty_id)
            return {'message': 'Specialty deleted successfully'}
    
    # Illness endpoints
    @ns_illnesses.route('/')
    class IllnessesList(Resource):
        @api.marshal_list_with(illness_model)
        def get(self):
            """Get all illnesses"""
            from my_project.auth.controller import illnesses_controller
            illnesses = illnesses_controller.find_all()
            return [illness.put_into_dto() for illness in illnesses]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(illness_model)
        @api.marshal_with(illness_model)
        def post(self):
            """Create new illness"""
            from my_project.auth.controller import illnesses_controller
            from my_project.auth.domain.orders.illnesses import Illnesses
            data = request.get_json()
            illness = Illnesses.create_from_dto(data)
            illnesses_controller.create_illness(illness)
            return illness.put_into_dto(), 201
    
    @ns_illnesses.route('/<int:illness_id>')
    class Illness(Resource):
        @api.marshal_with(illness_model)
        def get(self, illness_id):
            """Get illness by ID"""
            from my_project.auth.controller import illnesses_controller
            illness = illnesses_controller.find_by_id(illness_id)
            if not illness:
                api.abort(404, 'Illness not found')
            return illness.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(illness_model)
        @api.marshal_with(message_response_model)
        def put(self, illness_id):
            """Update illness by ID"""
            from my_project.auth.controller import illnesses_controller
            from my_project.auth.domain.orders.illnesses import Illnesses
            data = request.get_json()
            illness = Illnesses.create_from_dto(data)
            illnesses_controller.update_illness(illness_id, illness)
            return {'message': 'Illness updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, illness_id):
            """Delete illness by ID"""
            from my_project.auth.controller import illnesses_controller
            illnesses_controller.delete_illness(illness_id)
            return {'message': 'Illness deleted successfully'}
    
    # Symptom endpoints
    @ns_symptoms.route('/')
    class SymptomsList(Resource):
        @api.marshal_list_with(symptom_model)
        def get(self):
            """Get all symptoms"""
            from my_project.auth.controller import symptomes_controller
            symptoms = symptomes_controller.find_all()
            return [symptom.put_into_dto() for symptom in symptoms]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(symptom_model)
        @api.marshal_with(symptom_model)
        def post(self):
            """Create new symptom"""
            from my_project.auth.controller import symptomes_controller
            from my_project.auth.domain.orders.symptomes import Symptomes
            data = request.get_json()
            symptom = Symptomes.create_from_dto(data)
            symptomes_controller.create_symptome(symptom)
            return symptom.put_into_dto(), 201
    
    @ns_symptoms.route('/<int:symptom_id>')
    class Symptom(Resource):
        @api.marshal_with(symptom_model)
        def get(self, symptom_id):
            """Get symptom by ID"""
            from my_project.auth.controller import symptomes_controller
            symptom = symptomes_controller.find_by_id(symptom_id)
            if not symptom:
                api.abort(404, 'Symptom not found')
            return symptom.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(symptom_model)
        @api.marshal_with(message_response_model)
        def put(self, symptom_id):
            """Update symptom by ID"""
            from my_project.auth.controller import symptomes_controller
            from my_project.auth.domain.orders.symptomes import Symptomes
            data = request.get_json()
            symptom = Symptomes.create_from_dto(data)
            symptomes_controller.update_symptome(symptom_id, symptom)
            return {'message': 'Symptom updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, symptom_id):
            """Delete symptom by ID"""
            from my_project.auth.controller import symptomes_controller
            symptomes_controller.delete_symptome(symptom_id)
            return {'message': 'Symptom deleted successfully'}
    
    # Appointment endpoints
    @ns_appointments.route('/')
    class AppointmentsList(Resource):
        @api.marshal_list_with(appointment_model)
        def get(self):
            """Get all appointments"""
            from my_project.auth.controller import appointments_controller
            appointments = appointments_controller.find_all()
            return [appointment.put_into_dto() for appointment in appointments]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(appointment_model)
        @api.marshal_with(appointment_model)
        def post(self):
            """Create new appointment"""
            from my_project.auth.controller import appointments_controller
            from my_project.auth.domain.orders.appointments import Appointments
            data = request.get_json()
            appointment = Appointments.create_from_dto(data)
            appointments_controller.create_appointment(appointment)
            return appointment.put_into_dto(), 201
    
    @ns_appointments.route('/<int:appointment_id>')
    class Appointment(Resource):
        @api.marshal_with(appointment_model)
        def get(self, appointment_id):
            """Get appointment by ID"""
            from my_project.auth.controller import appointments_controller
            appointment = appointments_controller.find_by_id(appointment_id)
            if not appointment:
                api.abort(404, 'Appointment not found')
            return appointment.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(appointment_model)
        @api.marshal_with(message_response_model)
        def put(self, appointment_id):
            """Update appointment by ID"""
            from my_project.auth.controller import appointments_controller
            from my_project.auth.domain.orders.appointments import Appointments
            data = request.get_json()
            appointment = Appointments.create_from_dto(data)
            appointments_controller.update_appointment(appointment_id, appointment)
            return {'message': 'Appointment updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, appointment_id):
            """Delete appointment by ID"""
            from my_project.auth.controller import appointments_controller
            appointments_controller.delete_appointment(appointment_id)
            return {'message': 'Appointment deleted successfully'}
    
    # Billing endpoints
    @ns_billing.route('/')
    class BillingList(Resource):
        @api.marshal_list_with(billing_model)
        def get(self):
            """Get all billing records"""
            from my_project.auth.controller import billing_controller
            bills = billing_controller.find_all()
            return [bill.put_into_dto() for bill in bills]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(billing_model)
        @api.marshal_with(billing_model)
        def post(self):
            """Create new billing record"""
            from my_project.auth.controller import billing_controller
            from my_project.auth.domain.orders.billing import Billing
            data = request.get_json()
            bill = Billing.create_from_dto(data)
            billing_controller.create_bill(bill)
            return bill.put_into_dto(), 201
    
    @ns_billing.route('/<int:bill_id>')
    class Billing(Resource):
        @api.marshal_with(billing_model)
        def get(self, bill_id):
            """Get billing record by ID"""
            from my_project.auth.controller import billing_controller
            bill = billing_controller.find_by_id(bill_id)
            if not bill:
                api.abort(404, 'Billing record not found')
            return bill.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(billing_model)
        @api.marshal_with(message_response_model)
        def put(self, bill_id):
            """Update billing record by ID"""
            from my_project.auth.controller import billing_controller
            from my_project.auth.domain.orders.billing import Billing
            data = request.get_json()
            bill = Billing.create_from_dto(data)
            billing_controller.update_bill(bill_id, bill)
            return {'message': 'Billing record updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, bill_id):
            """Delete billing record by ID"""
            from my_project.auth.controller import billing_controller
            billing_controller.delete_bill(bill_id)
            return {'message': 'Billing record deleted successfully'}
    
    # Diagnosis endpoints
    @ns_diagnoses.route('/')
    class DiagnosesList(Resource):
        @api.marshal_list_with(diagnosis_model)
        def get(self):
            """Get all diagnoses"""
            from my_project.auth.controller import diagnoses_controller
            diagnoses = diagnoses_controller.find_all()
            return [diagnosis.put_into_dto() for diagnosis in diagnoses]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(diagnosis_model)
        @api.marshal_with(diagnosis_model)
        def post(self):
            """Create new diagnosis"""
            from my_project.auth.controller import diagnoses_controller
            from my_project.auth.domain.orders.diagnoses import Diagnoses
            data = request.get_json()
            diagnosis = Diagnoses.create_from_dto(data)
            diagnoses_controller.create_diagnosis(diagnosis)
            return diagnosis.put_into_dto(), 201
    
    @ns_diagnoses.route('/<int:diagnosis_id>')
    class Diagnosis(Resource):
        @api.marshal_with(diagnosis_model)
        def get(self, diagnosis_id):
            """Get diagnosis by ID"""
            from my_project.auth.controller import diagnoses_controller
            diagnosis = diagnoses_controller.find_by_id(diagnosis_id)
            if not diagnosis:
                api.abort(404, 'Diagnosis not found')
            return diagnosis.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(diagnosis_model)
        @api.marshal_with(message_response_model)
        def put(self, diagnosis_id):
            """Update diagnosis by ID"""
            from my_project.auth.controller import diagnoses_controller
            from my_project.auth.domain.orders.diagnoses import Diagnoses
            data = request.get_json()
            diagnosis = Diagnoses.create_from_dto(data)
            diagnoses_controller.update_diagnosis(diagnosis_id, diagnosis)
            return {'message': 'Diagnosis updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, diagnosis_id):
            """Delete diagnosis by ID"""
            from my_project.auth.controller import diagnoses_controller
            diagnoses_controller.delete_diagnosis(diagnosis_id)
            return {'message': 'Diagnosis deleted successfully'}
    
    # Schedule endpoints
    @ns_schedules.route('/')
    class SchedulesList(Resource):
        @api.marshal_list_with(schedule_model)
        def get(self):
            """Get all schedules"""
            from my_project.auth.controller import schedules_controller
            schedules = schedules_controller.find_all()
            return [schedule.put_into_dto() for schedule in schedules]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(schedule_model)
        @api.marshal_with(schedule_model)
        def post(self):
            """Create new schedule"""
            from my_project.auth.controller import schedules_controller
            from my_project.auth.domain.orders.scedules import Schedules
            data = request.get_json()
            schedule = Schedules.create_from_dto(data)
            schedules_controller.create_schedule(schedule)
            return schedule.put_into_dto(), 201
    
    @ns_schedules.route('/<int:schedule_id>')
    class Schedule(Resource):
        @api.marshal_with(schedule_model)
        def get(self, schedule_id):
            """Get schedule by ID"""
            from my_project.auth.controller import schedules_controller
            schedule = schedules_controller.find_by_id(schedule_id)
            if not schedule:
                api.abort(404, 'Schedule not found')
            return schedule.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(schedule_model)
        @api.marshal_with(message_response_model)
        def put(self, schedule_id):
            """Update schedule by ID"""
            from my_project.auth.controller import schedules_controller
            from my_project.auth.domain.orders.scedules import Schedules
            data = request.get_json()
            schedule = Schedules.create_from_dto(data)
            schedules_controller.update_schedule(schedule_id, schedule)
            return {'message': 'Schedule updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, schedule_id):
            """Delete schedule by ID"""
            from my_project.auth.controller import schedules_controller
            schedules_controller.delete_schedule(schedule_id)
            return {'message': 'Schedule deleted successfully'}
    
    # Appointment booking endpoints
    @ns_bookings.route('/')
    class AppointmentBookingsList(Resource):
        @api.marshal_list_with(appointment_booking_model)
        def get(self):
            """Get all appointment bookings"""
            from my_project.auth.controller import appointment_bookings_controller
            bookings = appointment_bookings_controller.find_all()
            return [booking.put_into_dto() for booking in bookings]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(appointment_booking_model)
        @api.marshal_with(appointment_booking_model)
        def post(self):
            """Create new appointment booking"""
            from my_project.auth.controller import appointment_bookings_controller
            from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings
            data = request.get_json()
            booking = AppointmentBookings.create_from_dto(data)
            appointment_bookings_controller.create_appointment_booking(booking)
            return booking.put_into_dto(), 201
    
    @ns_bookings.route('/<int:booking_id>')
    class AppointmentBooking(Resource):
        @api.marshal_with(appointment_booking_model)
        def get(self, booking_id):
            """Get appointment booking by ID"""
            from my_project.auth.controller import appointment_bookings_controller
            booking = appointment_bookings_controller.find_by_id(booking_id)
            if not booking:
                api.abort(404, 'Appointment booking not found')
            return booking.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(appointment_booking_model)
        @api.marshal_with(message_response_model)
        def put(self, booking_id):
            """Update appointment booking by ID"""
            from my_project.auth.controller import appointment_bookings_controller
            from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings
            data = request.get_json()
            booking = AppointmentBookings.create_from_dto(data)
            appointment_bookings_controller.update_appointment_booking(booking_id, booking)
            return {'message': 'Appointment booking updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, booking_id):
            """Delete appointment booking by ID"""
            from my_project.auth.controller import appointment_bookings_controller
            appointment_bookings_controller.delete_appointment_booking(booking_id)
            return {'message': 'Appointment booking deleted successfully'}
    
    # Recovery protocol endpoints
    @ns_recovery.route('/')
    class RecoveryProtocolsList(Resource):
        @api.marshal_list_with(recovery_protocol_model)
        def get(self):
            """Get all recovery protocols"""
            from my_project.auth.controller import recovery_protocol_controller
            protocols = recovery_protocol_controller.find_all()
            return [protocol.put_into_dto() for protocol in protocols]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(recovery_protocol_model)
        @api.marshal_with(recovery_protocol_model)
        def post(self):
            """Create new recovery protocol"""
            from my_project.auth.controller import recovery_protocol_controller
            from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol
            data = request.get_json()
            protocol = RecoveryProtocol.create_from_dto(data)
            recovery_protocol_controller.create_recovery_protocol(protocol)
            return protocol.put_into_dto(), 201
    
    @ns_recovery.route('/<int:protocol_id>')
    class RecoveryProtocol(Resource):
        @api.marshal_with(recovery_protocol_model)
        def get(self, protocol_id):
            """Get recovery protocol by ID"""
            from my_project.auth.controller import recovery_protocol_controller
            protocol = recovery_protocol_controller.find_by_id(protocol_id)
            if not protocol:
                api.abort(404, 'Recovery protocol not found')
            return protocol.put_into_dto()
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(recovery_protocol_model)
        @api.marshal_with(message_response_model)
        def put(self, protocol_id):
            """Update recovery protocol by ID"""
            from my_project.auth.controller import recovery_protocol_controller
            from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol
            data = request.get_json()
            protocol = RecoveryProtocol.create_from_dto(data)
            recovery_protocol_controller.update_recovery_protocol(protocol_id, protocol)
            return {'message': 'Recovery protocol updated successfully'}
        
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, protocol_id):
            """Delete recovery protocol by ID"""
            from my_project.auth.controller import recovery_protocol_controller
            recovery_protocol_controller.delete_recovery_protocol(protocol_id)
            return {'message': 'Recovery protocol deleted successfully'}
    
    # Doctor-Symptom relation endpoints
    @ns_relations.route('/')
    class DoctorSymptomRelations(Resource):
        @api.marshal_list_with(doctor_symptom_model)
        def get(self):
            """Get all doctor-symptom relations"""
            from my_project.auth.controller import doctorsymptomes_controller
            relations = doctorsymptomes_controller.find_all_relations()
            return [relation.put_into_dto() for relation in relations]
        
        @api.doc(security='Bearer')
        @token_required
        @api.expect(doctor_symptom_model)
        @api.marshal_with(doctor_symptom_model)
        def post(self):
            """Create new doctor-symptom relation"""
            from my_project.auth.controller import doctorsymptomes_controller
            from my_project.auth.domain.orders.doctorsymptomes import DoctorSymptomes
            data = request.get_json()
            relation = DoctorSymptomes.create_from_dto(data)
            doctorsymptomes_controller.create_relation(relation)
            return relation.put_into_dto(), 201
    
    @ns_relations.route('/by_doctor/<int:doctor_id>')
    class SymptomsByDoctor(Resource):
        @api.marshal_list_with(symptom_model)
        def get(self, doctor_id):
            """Get all symptoms for a specific doctor"""
            from my_project.auth.controller import doctorsymptomes_controller
            relations = doctorsymptomes_controller.find_symptomes_by_doctor(doctor_id)
            if not relations:
                api.abort(404, 'No symptoms found for this doctor')
            return [relation.symptome.put_into_dto() for relation in relations]
    
    @ns_relations.route('/by_symptom/<int:symptom_id>')
    class DoctorsBySymptom(Resource):
        @api.marshal_list_with(doctor_model)
        def get(self, symptom_id):
            """Get all doctors for a specific symptom"""
            from my_project.auth.controller import doctorsymptomes_controller
            relations = doctorsymptomes_controller.find_doctors_by_symptom(symptom_id)
            if not relations:
                api.abort(404, 'No doctors found for this symptom')
            return [relation.doctor.put_into_dto() for relation in relations]
    
    @ns_relations.route('/<int:doctor_id>/<int:symptom_id>')
    class DoctorSymptomRelation(Resource):
        @api.doc(security='Bearer')
        @token_required
        @api.marshal_with(message_response_model)
        def delete(self, doctor_id, symptom_id):
            """Delete doctor-symptom relation"""
            from my_project.auth.controller import doctorsymptomes_controller
            doctorsymptomes_controller.delete_relation(doctor_id, symptom_id)
            return {'message': 'Relation deleted successfully'}
    
    @ns_relations.route('/all')
    class AllRelationsDetails(Resource):
        def get(self):
            """Get all doctor-symptom relations with details"""
            from my_project.auth.controller import doctorsymptomes_controller
            details = doctorsymptomes_controller.find_with_details()
            return [row._asdict() for row in details]
    
    # Health check endpoint
    @ns_health.route('/status')
    class HealthCheck(Resource):
        @api.marshal_with(health_model)
        def get(self):
            """System health check"""
            return {
                'status': 'healthy',
                'message': 'Medical Management System API is running!',
                'version': '1.0',
                'database': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    # Root endpoint
    @app.route("/")
    def hello_world():
        return jsonify({
            'message': 'Welcome to Medical Management System API!',
            'docs_url': '/api/docs/',
            'api_version': '1.0',
            'features': [
                'JWT Authentication',
                'Doctor Management',
                'Patient Management',
                'Appointment Scheduling',
                'Billing System',
                'Diagnosis Tracking',
                'Recovery Protocols',
                'Real-time Statistics'
            ],
            'endpoints': {
                'authentication': {
                    'login': '/api/v1/auth/login',
                    'register': '/api/v1/auth/register'
                },
                'doctors': {
                    'list': '/api/v1/doctors/',
                    'with_specialty': '/api/v1/doctors/all',
                    'by_id': '/api/v1/doctors/{id}'
                },
                'patients': {
                    'list': '/api/v1/patients/',
                    'by_id': '/api/v1/patients/{id}'
                },
                'specialties': {
                    'list': '/api/v1/specialties/',
                    'by_id': '/api/v1/specialties/{id}'
                },
                'illnesses': {
                    'list': '/api/v1/illnesses/',
                    'by_id': '/api/v1/illnesses/{id}'
                },
                'symptoms': {
                    'list': '/api/v1/symptoms/',
                    'by_id': '/api/v1/symptoms/{id}'
                },
                'appointments': {
                    'list': '/api/v1/appointments/',
                    'by_id': '/api/v1/appointments/{id}'
                },
                'billing': {
                    'list': '/api/v1/billing/',
                    'by_id': '/api/v1/billing/{id}'
                },
                'diagnoses': {
                    'list': '/api/v1/diagnoses/',
                    'by_id': '/api/v1/diagnoses/{id}'
                },
                'schedules': {
                    'list': '/api/v1/schedules/',
                    'by_id': '/api/v1/schedules/{id}'
                },
                'bookings': {
                    'list': '/api/v1/bookings/',
                    'by_id': '/api/v1/bookings/{id}'
                },
                'recovery': {
                    'list': '/api/v1/recovery/',
                    'by_id': '/api/v1/recovery/{id}'
                },
                'relations': {
                    'list': '/api/v1/relations/',
                    'by_doctor': '/api/v1/relations/by_doctor/{id}',
                    'by_symptom': '/api/v1/relations/by_symptom/{id}',
                    'all_details': '/api/v1/relations/all'
                },
                'system': {
                    'health': '/api/v1/health/status'
                }
            },
            'test_credentials': {
                'admin': {'username': 'admin', 'password': 'admin123'},
                'doctor': {'username': 'doctor', 'password': 'doctor123'}
            },
            'instructions': [
                '1. Visit /api/docs/ for interactive API documentation',
                '2. Login with test credentials to get JWT token',
                '3. Use "Bearer <token>" in Authorization header for protected endpoints',
                '4. Admin users have access to all management features'
            ]
        })

#1
def _init_trigger(app: Flask) -> None:
    with app.app_context():
            # Drop the trigger if it exists
            db.session.execute('DROP TRIGGER IF EXISTS trigger_specialty_id;')

            # Create the trigger
            db.session.execute('''
            CREATE TRIGGER trigger_specialty_id
            BEFORE INSERT ON doctors
            FOR EACH ROW
            BEGIN
                IF NEW.doctor_id < 0 THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Primary key (doctor_id) cannot be negative';
                END IF;

                IF NOT EXISTS (SELECT 1 FROM specialties WHERE specialties.specialty_id = NEW.specialty_id) THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Specialty ID does not exist in the specialties table';
                END IF;
            END;
            ''')


            #3a,b,c




            db.session.execute('DROP TRIGGER IF EXISTS prevent_symptomes_deletion;')
            # db.session.execute('''
            #
            #            CREATE TRIGGER prevent_symptomes_deletion
            #            BEFORE DELETE ON symptomes
            #            FOR EACH ROW
            #            BEGIN
            #                SIGNAL SQLSTATE '45000'
            #                SET MESSAGE_TEXT = 'Deleting rows from Symptomes is not allowed';
            #            END;
            #            ''')
            db.session.execute('DROP TRIGGER IF EXISTS prevent_specialty_name_ending_with_00;')
            # db.session.execute('''
            #
            #                     CREATE TRIGGER prevent_specialty_name_ending_with_00
            #                     BEFORE INSERT ON specialties
            #                     FOR EACH ROW
            #                     BEGIN
            #                         IF RIGHT(NEW.specialty_name, 2) = '00' THEN
            #                             SIGNAL SQLSTATE '45000'
            #                             SET MESSAGE_TEXT = 'Specialty name cannot end with "00"';
            #                         END IF;
            #                     END;
            #                        ''')

            db.session.execute('DROP TRIGGER IF EXISTS validate_specialty_name;')
            db.session.execute('''

                                            CREATE TRIGGER validate_specialty_name
                                            BEFORE INSERT ON specialties
                                            FOR EACH ROW
                                            BEGIN
                                                IF NEW.specialty_name NOT IN ('Petro', 'Olha', 'Taras') THEN
                                                    SIGNAL SQLSTATE '45000'
                                                    SET MESSAGE_TEXT = 'Specialty name must be one of: Svitlana, Petro, Olha, Taras';
                                                END IF;
                                             END;
                                               ''')


            db.session.commit()

def _init_procedures(app: Flask) -> None:
    with app.app_context():
        db.session.execute('''
            DROP PROCEDURE IF EXISTS AddDoctorSymptome;

            CREATE PROCEDURE AddDoctorSymptome(
                IN p_doctor_id INT,
                IN p_symptome_id INT
            )
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM doctors WHERE doctor_id = p_doctor_id) THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'doctor_id does not exist in doctors table';
                END IF;
            
                IF NOT EXISTS (SELECT 1 FROM symptomes WHERE symptome_id = p_symptome_id) THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'symptome_id does not exist in symptomes table';
                END IF;
            
                INSERT IGNORE INTO doctor_symptomes (doctor_id, symptome_id)
                VALUES (p_doctor_id, p_symptome_id);
            END;
          ''')
        db.session.commit()

def _init_db(app: Flask) -> None:
    """
    Initializes DB with SQLAlchemy
    :param app: Flask application object
    """
    app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {})

    db.init_app(app)

    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])

    import my_project.auth.domain
    with app.app_context():
        db.create_all()

def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    load_dotenv()
    conn = os.getenv(SQLALCHEMY_DATABASE_URI)
    if conn:
        app_config["SQLALCHEMY_DATABASE_URI"] = conn
        return

    user = os.getenv(MYSQL_ROOT_USER, str(additional_config.get("MYSQL_ROOT_USER", "")))
    pwd  = os.getenv(MYSQL_ROOT_PASSWORD, str(additional_config.get("MYSQL_ROOT_PASSWORD", "")))

    template = app_config.get("SQLALCHEMY_DATABASE_URI", "")
    if not template:
        raise ValueError("SQLALCHEMY_DATABASE_URI is missing and no CONNECTION_STRING provided in env.")

    if "{user}" in template or "{password}" in template:
        app_config["SQLALCHEMY_DATABASE_URI"] = template.format(
            user=user,
            password=quote_plus(pwd),
        )
        return

    if "{}" in template:
        app_config["SQLALCHEMY_DATABASE_URI"] = template.format(
            user, quote_plus(pwd)
        )
        return

    app_config["SQLALCHEMY_DATABASE_URI"] = template