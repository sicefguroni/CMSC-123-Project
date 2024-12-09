import flet as ft
from typing import List
from datetime import date, datetime, timedelta
from abc import ABC, abstractmethod

# Helper Functions
#-----------------------------------------------------------#
# Convert MM/DD/YYYY to date and vice versa
def str_to_date(date_str:str):
    date_obj = datetime.strptime(date_str, "%m/%d%Y").date()
    return date_obj

def date_to_str(date_obj):
    date_str = date_obj.strftime("%m/%d/%Y")
    return date_str

# Convert HH:MM to time and vice versa
def str_to_time(time_str:str):
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    return time_obj

def time_to_str(time_obj):
    time_str = time_obj.strftime("%H:%M")
    return time_str

# Convert str of frequency
def strFrequencySched_to_day(frequency:str):
    frequency_sched = frequency.split("/")[1]
    if frequency_sched.lower() == "day":
        return timedelta(days=1)

    elif frequency_sched.lower == "week": 
        return timedelta(days=7)
    
    return None

#-----------------------------------------------------------#
class Appointment_ReminderCard:
    def __init__(self, id:int, doctorName:str, appt_Date:str, appt_Time:str, reminder_count:int, on_delete:callable):
        self.id = id
        self.reminder_count = reminder_count

        self.doctor_name = doctorName
        self.appointment_date = appt_Date
        self.appointment_time = appt_Time

        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Appointment reminder title
                        ft.ListTile(
                            title=ft.Text("Upcoming Appointment!"),
                            trailing=self.chk_btn,
                        ),
                        
                        # Show details of the appointment
                        ft.Container(
                            content=ft.Text(
                                f"You have an appointment with Dr. {self.doctor_name} "
                                f"on {self.appointment_date} at {self.appointment_time}. Get ready!"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )
    
    def is_tomorrow(self):
        current_day = date.today()
        day_before_appointment = str_to_date(self.appointment_date)-timedelta(days=1)

        if current_day == day_before_appointment and self.reminder_count == 0:
            self.reminder_count += 1
            return True
        
        return False
    
    def is_today(self):
        current_day = date.today()
        day_of_appointment = str_to_date(self.appointment_date)

        if current_day == day_of_appointment and self.reminder_count == 1:
            self.reminder_count += 1
            return True
        
        return False

    def _on_checked(self, e):
        if e.control.value:
            self.on_delete(self)

    
class Medicine_Intake_ReminderCard:
    def __init__(self, id:int, medicine_name:str, dosage:str, frequency_number:int,
                frequency_sched:str, time_interval:float, reminder_count_present:int,
                reminder_count_total:int, on_delete:callable):
        self.id = id
        self.reminder_count_today = reminder_count_present
        self.reminder_count_total = reminder_count_total

        self.medicine_name = medicine_name
        self.dosage = dosage
        self.frequency_number = frequency_number
        self.frequency_schedule = frequency_sched
        self.time_interval = timedelta(hours=time_interval)



