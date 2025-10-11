

from flask import Flask
from .error_handler import err_handler_bp

def register_routes(app: Flask) -> None:

    app.register_blueprint(err_handler_bp)

    # Importing each route Blueprint
    from .orders.appointmentbookings_route import appointment_bookings_bp
    from .orders.appointments_route import appointments_bp
    from .orders.billing_route import billing_bp
    from .orders.diagnoses_route import diagnoses_bp
    from .orders.doctors_route import doctors_bp
    from .orders.illnesses_route import illnesses_bp
    from .orders.patients_route import patients_bp
    from .orders.recoveryprotocol_route import recovery_protocol_bp
    from .orders.schedules_route import schedules_bp
    from .orders.specialities_route import specialties_bp
    from .orders.symptomes_route import symptomes_bp
    from .orders.doctorsymptomes_route import doctor_symptomes_bp

    # Registering each Blueprint with the app
    app.register_blueprint(appointment_bookings_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(diagnoses_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(illnesses_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(recovery_protocol_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(specialties_bp)
    app.register_blueprint(symptomes_bp)
    app.register_blueprint(doctor_symptomes_bp)