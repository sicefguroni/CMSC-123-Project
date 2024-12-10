from prescription_backend import PrescriptionManager
from datetime import datetime, timedelta, date, time
from typing import Callable
import flet as ft


# Load All Prescriptions
# ----------------------------------------------------------- #
presciption_module = PrescriptionManager()
all_prescriptions = presciption_module.get_all_prescriptions()


# Helper Functions
# ----------------------------------------------------------- #
def str_to_date_mmddyyyy(date_str: str) -> date:
    return datetime.strptime(date_str, "%m/%d/%Y").date()

def date_to_str_mmddyyyy(date_obj: date) -> str:
    return date_obj.strftime("%m/%d/%Y")

def str_to_time_hhmm(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()

def time_to_str_hhmm(time_obj: time) -> str:
    return time_obj.strftime("%H:%M")


# Reminder
# ----------------------------------------------------------- #
class Appointment:
    def __init__(
            self,
            id:int,
            doctor:str,
            appointment_date:str,
            appointment_time:str,
    ):
        # Appointment creation ID
        self.id = id

        # Appointment Information
        self.doctor = doctor
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
    
    def tell_user(self):
        return [f"You have an appointment with Dr. {self.doctor}",
                f"on {self.appointment_date} at {self.appointment_time}.",
                f"Better get ready!"]


class MedicineIntake:
    def __init__(
            self,
            id:int,
            medication:str,
            dosage:int,
            dosage_unit:str,
            frequency:str,
            time_interval:int,
            start_date:str,
            end_date:str,
            quantity_limit:int,
    ):
        self.id = id

        # Medication Info
        self.medication = medication
        self.dosage = dosage
        self.dosage_unit = dosage_unit
        self.quantity_limit = quantity_limit
        self.total_intake = 0

        # Med Intake Schedule Interval
        self.frequency_num = self._str_freq_to_int(frequency)
        self.frequency_sched = self._str_freq_to_timedelta(frequency)
        self.time_interval = timedelta(hours=time_interval)
        self.start_date = start_date
        self.end_date = end_date

    def tell_user(self):
        return [f"It's time to take your {self.medication} ({self.dosage} {self.dosage_unit})!",
                f"Make sure to mark this done after taking it!"]

    # --- Helper Functions ---
    def _str_freq_to_int(self, freq: str) -> int:
        mapping = {"daily": 1, "weekly": 7}
        return mapping.get(freq.lower(), 0)

    def _str_freq_to_timedelta(self, freq: str) -> timedelta:
        mapping = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        return mapping.get(freq.lower(), timedelta(days=0))
    

class AppointmentReminder:
    def 

class Medicine_Intake:
    

class AppointmentReminder:
    def __init__(
            self,
            id:int,
            doctor:str,
            appointment_date:str,
            appointment_time:str,
            on_delete:Callable
    ):
        self.id = id

        # Appointment Information
        self.doctor = doctor
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

        # Callback for deletion
        self.on_delete:Callable = on_delete


    def notify_user(self):
        return ft

    def is_tomorrow(self):
        date_today = date.today()
        day_before_appointment = str_to_date_mmddyyyy(self.appointment_date) - timedelta(days=1)
        return date_today == day_before_appointment


