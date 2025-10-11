from .orders.appointments_service import AppointmentsService
from .orders.appointmentsbookings_service import AppointmentBookingsService
from .orders.billing_service import BillingService
from .orders.diagnoses_service import DiagnosesService
from .orders.doctors_service import DoctorsService
from .orders.illnesses_service import IllnessesService
from .orders.patients_service import PatientsService
from .orders.recovery_protocol_service import RecoveryProtocolService
from .orders.schedules_service import SchedulesService
from .orders.specialities_service import SpecialtiesService
from .orders.sympromes_service import SymptomesService
from .orders.doctorsymptomes_service import DoctorSymptomesService

# Instantiate each service
appointments_service = AppointmentsService()
appointment_bookings_service = AppointmentBookingsService()
billing_service = BillingService()
diagnoses_service = DiagnosesService()
doctors_service = DoctorsService()
illnesses_service = IllnessesService()
patients_service = PatientsService()
recovery_protocol_service = RecoveryProtocolService()
schedules_service = SchedulesService()
specialties_service = SpecialtiesService()
symptomes_service = SymptomesService()
doctorsymptomes_service = DoctorSymptomesService()