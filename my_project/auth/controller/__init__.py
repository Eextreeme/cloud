from .orders.appointmentbookings_controller import AppointmentBookingsController
from .orders.appointments_controller import AppointmentsController
from .orders.billing_controller import BillingController
from .orders.diagnoses_controller import DiagnosesController
from .orders.doctors_controller import DoctorsController
from .orders.illnesses_controller import IllnessesController
from .orders.patients_controller import PatientsController
from .orders.recoveryprotocol_controller import RecoveryProtocolController
from .orders.scedules_controller import SchedulesController
from .orders.specialities_controller import SpecialtiesController
from .orders.sypmtomes_controller import SymptomesController
from .orders.doctorsymptomes_controller import DoctorSymptomesController

# Initialize each controller instance
appointment_bookings_controller = AppointmentBookingsController()
appointments_controller = AppointmentsController()
billing_controller = BillingController()
diagnoses_controller = DiagnosesController()
doctors_controller = DoctorsController()
illnesses_controller = IllnessesController()
patients_controller = PatientsController()
recovery_protocol_controller = RecoveryProtocolController()
schedules_controller = SchedulesController()
specialties_controller = SpecialtiesController()
symptomes_controller = SymptomesController()
doctorsymptomes_controller = DoctorSymptomesController()
