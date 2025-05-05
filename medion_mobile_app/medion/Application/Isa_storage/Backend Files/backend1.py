import flet as ft
from datetime import datetime, timedelta, date, time
from typing import Callable
from prescription_backend import PrescriptionManager
from abc import ABC, abstractmethod
import json



class Reminder:
    def __init__(self, title: str, content: str, timestamp: datetime.datetime = None):
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.datetime.now()


class ReminderManager:
    def __init__(self):
        # Store reminders in categories
        self.medicine_reminders = []
        self.appointment_reminders = []

    def add_reminder(self, category: str, title: str, content: str):
        reminder = Reminder(title, content)
        if category == "Medicine Intake":
            self.medicine_reminders.append(reminder)
        elif category == "Appointment":
            self.appointment_reminders.append(reminder)

    def get_reminders(self, category: str):
        if category == "Medicine Intake":
            return self.medicine_reminders
        elif category == "Appointment":
            return self.appointment_reminders
        return []

    def delete_reminder(self, category: str, reminder: Reminder):
        if category == "Medicine Intake" and reminder in self.medicine_reminders:
            self.medicine_reminders.remove(reminder)
        elif category == "Appointment" and reminder in self.appointment_reminders:
            self.appointment_reminders.remove(reminder)













































# Helper Functions
# ----------------------------------------------------------- #
from datetime import datetime, date, time

def str_to_date_mmddyyyy(date_str: str) -> date:
    return datetime.strptime(date_str, "%m/%d/%Y").date()

def date_to_str_mmddyyyy(date_obj: date) -> str:
    return date_obj.strftime("%m/%d/%Y")

def str_to_time_hhmm(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()

def time_to_str_hhmm(time_obj: time) -> str:
    return time_obj.strftime("%H:%M")



# Linked List Template: Data Structure
# ----------------------------------------------------------- #
class Node:
    def __init__(self, val):
        self.value = val
        self.nxt = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add(self, val):
        new_node = Node(val)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.nxt:
                current = current.nxt
            current.nxt = new_node
        self.size += 1

    def remove(self, val):
        if self.is_empty():
            return None

        if self.head.value == val:
            self.head = self.head.nxt
            self.size -= 1
            return val

        current = self.head
        while current.nxt and current.nxt.value != val:
            current = current.nxt

        if current.nxt is None:
            return None
        else:
            current.nxt = current.nxt.nxt
            self.size -= 1
            return val

    def get(self, index):
        if self.is_empty():
            return None

        if index < 0 or index >= self.size:
            return None

        current = self.head
        for i in range(index):
            current = current.nxt

        return current.value

    def find(self, value):
        current = self.head
        while current:
            if current.value == value:
                return current.value
            current = current.nxt
        return None

    def found(self, value):
        return self.find(value) is not None

    def __iter__(self):
        """Iterate over the linked list."""
        current = self.head
        while current:
            yield current.value
            current = current.nxt




# Reminder: Hold information to remind users
# ----------------------------------------------------------- #
class Reminder(ABC):
    @abstractmethod
    def create_reminder_content(self):
        pass

    @abstractmethod
    def notify_user(self):
        pass

    @abstractmethod
    def _on_checked(self, e):
        pass

class Appointment_RC(ReminderCard):
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

        # UI Components
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()
    
    def _create_reminder_card(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Upcoming Appointment Tomorrow!"),
                            trailing=self.chk_btn,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"You have an appointment with Dr. {self.doctor_name} "
                                f"on {self.appointment_date} at {self.appointment_time}. Get ready!"
                                f"Mark this checked if you have finished your appointment. :D"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def _on_checked(self, e):
        if self.chk_btn.value:
            time.sleep(2)
            id = self.id
            self.on_delete(self)  # Call the delete callback
            return id
        
    def notify_user(self):
        return self.card

    def is_tomorrow(self):
        date_today = date.today()
        day_before_appointment = str_to_date_mmddyyyy(self.appointment_date) - timedelta(days=1)
        return date_today == day_before_appointment

class MedicineIntake_RC(ReminderCard):
    def __init__(
            self,
            id:int,
            medication:str,
            frequency:str,
            time_interval:int,
            start_date:str,
            end_date:str,
            quantity_limit:int,
            on_delete:Callable
    ):
        self.id = id

        # Medication Info
        self.medication = medication
        self.quantity_limit = quantity_limit
        self.total_intake = 0

        # Med Intake Schedule Interval
        self.frequency_num = self._str_freq_to_int(frequency)
        self.frequency_sched = self._str_freq_to_timedelta(frequency)
        self.time_interval = timedelta(hours=time_interval)
        self.start_date = start_date
        self.end_date = end_date
        self.frequency_num_count = 0

        # Callback for deletion
        self.on_delete = on_delete

        # UI Components
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ReminderCard_SLL():
        reminder_cards_SLL = ReminderCard_SLL()
        for i in range(self.frequency_num):
            container = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListTile(
                                title=ft.Text(f"{self.medicine_name} ({self.dosage})"),
                                trailing=self.chk_btn,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"Take your medicine {self.medicine_name} ({self.dosage})! "
                                    f"Once you're done, check the checkbox! :D"
                                ),
                                padding=ft.padding.only(left=20, right=20),
                            ),
                        ],
                    ),
                    padding=ft.padding.symmetric(vertical=10),
                ),
            )



# Reminder System
class Medion_Reminder_System:
    def __init__(self):
        self.appointment_reminders = LinkedList()          #_Contains all reminders to be sent
        self.medicine_intake_reminders = LinkedList() #_Saves the id of the reminder that's done

    def























# File Names for Reminder Feature
# ----------------------------------------------------------- #
CURRENT_APPOINTMENTS_RCs_File = "current_appointments_RCList.json"
CURRENT_MEDICINE_INTAKE_RCs_File = "current_medicine_intake_RCList.json"
ONGOING_MED_INTAKE_RCs_File = "ongoing_med_intake_RCList.json"


# Reminder Manager
# ----------------------------------------------------------- #
class ReminderManager:
    def __init__(self):
        self.appointments_RCs_to_show = ReminderCard_SLL()
        self.med_intake_RCs_to_show = ReminderCard_SLL()

        self.on_going_medicine_intake = ReminderCard_SLL()
        self.appointments_today = ReminderCard_SLL()

    # Collects ongoing prescriptions and stores them as reminder cards
    def collect_ongoing_prescriptions(self):
        # Get all prescriptions
        prescription_module = PrescriptionManager()
        all_prescriptions = prescription_module.get_all_prescriptions()

        # Get all appointments today
        # If the id exists in the list of today's appointments, do not include them
        for p in all_prescriptions:
            if self.appointments_today.in_the_list(p['id']):
                continue

            appointment_date = datetime.strptime(p["appointment_date"], "%m/%d/%Y")
            if appointment_date != date.today():
                continue

            new_appt_reminder = Appointment_ReminderCard(p["id"], p["doctor"], p["appointment_date"],
                                                         p["appointment_time"],)
            self.appointments_today.add(new_appt_reminder)


        # Create on going medicine intake RCs
        # If id exists in the list of ongoing medicine intake, do not include
        # If id does not exist but not active, do not include
        for p in all_prescriptions:
            if self.on_going_medicine_intake.in_the_list(p["id"]):
                continue

            today = date.today()
            start_date = datetime.strptime(p["start_date"], "%m/%d/%Y")
            end_date = datetime.strptime(p["end_date"], "%m/%d/%Y")
            if today >= start_date and today <= end_date:
                new_MI_reminder = MedIntake_ReminderCard(p["id"], p["medication"], p["dosage"], p["frequency"], p["time_interval"], p["start_date"], p["end_date"], )
                self.on_going_medicine_intake.add(new_MI_reminder)

    def notify_user(self):
        # Check if there are any appointments today that are not done
        # If a reminder_today.is_done == False, notify by adding a
        # copy of itself to the appoinment_RCs_to_show
        for appt in self.appointments_today:
            if not appt.is_done:
                self.appointments_RCs_to_show.add(appt)
        
        # Check if there are any medicines to intake
        


    def load_from_file(self):
        pass

    def save_to_file(self):
        pass