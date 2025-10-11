from .orders.appointmentbookings_dao import AppointmentBookingsDAO
from .orders.appointments_dao import AppointmentsDAO
from .orders.billing_dao import BillingDAO
from .orders.diagnoses_dao import DiagnosesDAO
from .orders.doctors_dao import DoctorsDAO
from .orders.illneses_dao import IllnessesDAO
from .orders.patients_dao import PatientsDAO
from .orders.recoveryprotocol_dao import RecoveryProtocolDAO
from .orders.scedules_dao import SchedulesDAO
from .orders.specialities_dao import SpecialtiesDAO
from .orders.sympromes_dao import SymptomesDAO
from .orders.doctorsymptomes_dao import DoctorSymptomesDAO
# Instantiate each DAO
appointment_bookings_dao = AppointmentBookingsDAO()
appointments_dao = AppointmentsDAO()
billing_dao = BillingDAO()
diagnoses_dao = DiagnosesDAO()
doctors_dao = DoctorsDAO()
illnesses_dao = IllnessesDAO()
patients_dao = PatientsDAO()
recovery_protocol_dao = RecoveryProtocolDAO()
schedules_dao = SchedulesDAO()
specialties_dao = SpecialtiesDAO()
symptomes_dao = SymptomesDAO()
doctorsymptomes_dao = DoctorSymptomesDAO()