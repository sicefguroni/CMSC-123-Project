import flet as ft
from datetime import datetime, timedelta, date, time
from typing import Callable
from prescription_backend import PrescriptionManager
from abc import ABC, abstractmethod
import json


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
        if self.is_empty():
            return None
        
        current = self.head
        if current.value == value:
            return current.value
        
        while current.nxt:
            current = current.next
            if current.value == value:
                return current.value
            
        return None
    
    def found(self, value):
        found_value = self.find(value)
        return found_value == value

# Reminder Cards: Hold information to remind users
# ----------------------------------------------------------- #
class ReminderCard(ABC):
    @abstractmethod
    def _create_reminder_card(self) -> ft.Card:
        pass

    @abstractmethod
    def notify_user(self):
        pass

    @abstractmethod
    def _on_checked(self, e):
        pass

class Appointment_ReminderCard(ReminderCard):
    def __init__(
        self,
        id: int,
        doctor_name: str,
        appt_date: str,
        appt_time: str,
        on_delete: Callable,
    ):
        self.id = id
        self.is_done = False

        # Appointment details
        self.doctor_name = doctor_name
        self.appointment_date = appt_date
        self.appointment_time = appt_time

        # Callback for deletion
        self.on_delete = on_delete

        # UI Components
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        """Create the Flet reminder card."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Upcoming Appointment!"),
                            trailing=self.chk_btn,
                        ),
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

    def notify_user(self, buffer_minutes: int = 30):
        """
        Notify the user if the appointment is today and the time is close.
        
        :param buffer_minutes: Minutes before the appointment to send a notification.
        :return: The Flet card if a notification is due, otherwise None.
        """
        if self.is_today() and self.is_within_time(buffer_minutes):
            return self.card

    def _on_checked(self, e):
        """Handle checkbox state changes."""
        if self.chk_btn.value:
            temp = self
            temp.is_done = True
            self.on_delete(self)  # Call the delete callback
            return temp

    def is_today(self) -> bool:
        """Check if the appointment is today."""
        appointment_date = self._str_to_date(self.appointment_date)
        return date.today() == appointment_date

    def is_within_time(self, buffer_minutes: int) -> bool:
        """Check if the current time is within the buffer period before the appointment."""
        current_time = datetime.now().time()
        appointment_time = self._str_to_time(self.appointment_time)

        # Calculate the buffer time range
        appointment_datetime = datetime.combine(date.today(), appointment_time)
        notification_window_start = appointment_datetime - timedelta(minutes=buffer_minutes)

        return datetime.now() >= notification_window_start

    # --- Helper Functions ---
    def _str_to_date(self, date_str: str) -> date:
        """Convert a date string (YYYY-MM-DD) to a date object."""
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def _str_to_time(self, time_str: str) -> time:
        """Convert a time string (HH:MM) to a time object."""
        return datetime.strptime(time_str, "%H:%M").time()

class MedIntake_ReminderCard(ReminderCard):
    def __init__(
        self,
        id: int,
        medicine_name: str,
        dosage: str,
        frequency_sched: str,
        time_interval: float,
        start_date: date,
        end_date: date,
        on_delete: Callable
    ):
        self.id = id
        self.intake_count_per_freq = 0
        self.frequency_sched_count = 0
        self.last_intake_datetime = None  # Track last intake datetime

        # Medicine details
        self.medicine_name = medicine_name
        self.dosage = dosage

        # Frequency and scheduling
        self.frequency_number = self._str_frequency_to_int(frequency_sched)
        self.frequency_schedule = self._str_frequency_sched_to_timedelta(frequency_sched)
        self.time_interval = timedelta(hours=time_interval)
        self.start_date = start_date
        self.end_date = end_date

        # Callback for deletion
        self.on_delete = on_delete

        # UI Components
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        """Creates a Flet card UI for the reminder."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(f"{self.medicine_name} ({self.dosage})"),
                            trailing=self.chk_btn,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"It's time to take your {self.medicine_name} ({self.dosage})! "
                                f"Once you're done, check the checkbox! :D"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def notify_user(self) -> ft.Card:
        """Check if it's time to notify the user and return the reminder card."""
        if self.is_active() and self.is_time():
            print(f"Reminder: It's time to take your {self.medicine_name} ({self.dosage})!")
            return self.card

    def _on_checked(self, e):
        """Handle checkbox state changes."""
        if self.chk_btn.value:  # Checkbox is checked
            self.on_delete(self)  # Call the delete callback
            self.intake_count_per_freq += 1
            self.last_intake_datetime = datetime.now()  # Update last intake timestamp

    # --- Core Logic ---
    def is_active(self) -> bool:
        """Check if the reminder is active based on start and end dates."""
        today = date.today()
        return self.start_date <= today <= self.end_date

    def is_time(self) -> bool:
        """Check if it's time for the next intake."""
        current_time = datetime.now().time()
        next_intake_time = self._get_next_interval_time()
        return current_time >= next_intake_time

    def _get_next_interval_time(self) -> time:
        """Calculate the next intake time."""
        base_time = time(7, 0)  # Example: First intake at 7:00 AM
        interval = self.intake_count_per_freq * self.time_interval
        next_time = (datetime.combine(date.today(), base_time) + interval).time()
        return next_time

    def has_frequency_interval_completed(self) -> bool:
        """Check if the frequency interval (e.g., daily, weekly) has been completed."""
        if self.last_intake_datetime is None:
            return True  # No intakes yet, interval is considered complete

        time_elapsed = datetime.now() - self.last_intake_datetime
        return time_elapsed >= self.frequency_schedule

    def _next_frequency_sched_count(self):
        """Update frequency schedule count when the interval is complete."""
        if self.has_frequency_interval_completed():
            self.frequency_sched_count += 1
            self.intake_count_per_freq = 0  # Reset intake count for the frequency
            self.last_intake_datetime = datetime.now()  # Reset last intake time

    # --- Helper Functions ---
    def _str_frequency_to_int(self, freq: str) -> int:
        """Convert a frequency string to an integer (e.g., daily = 1, weekly = 7)."""
        mapping = {"daily": 1, "weekly": 7}
        return mapping.get(freq.lower(), 0)

    def _str_frequency_sched_to_timedelta(self, freq: str) -> timedelta:
        """Convert a frequency string to a timedelta (e.g., daily = 1 day, weekly = 7 days)."""
        mapping = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        return mapping.get(freq.lower(), timedelta(days=0))


# SLL Template for Reminder Card
# ----------------------------------------------------------- #
class ReminderCard_SLL(LinkedList):
    def in_the_list(self, id:int):
        current = self.head

        if current.id == id:
            return True
        
        while current.nxt:
            current = current.nxt
            if current.id == id:
                return True
            
        return False


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

        self.finished_appointments = LinkedList()
        self.finished_medicine_intake = LinkedList()

    # Collects ongoing prescriptions and stores them as reminder cards
    def collect_ongoing_prescriptions(self):
        # Get all prescriptions
        prescription_module = PrescriptionManager()
        all_prescriptions = prescription_module.get_all_prescriptions()

        # Get all appointments today
        # If the id exists in the list of today's appointments, do not include them
        for p in all_prescriptions:
            if self.finished_appointments.found(p["id"]):
                continue

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
            if self.finished_medicine_intake.found(p["id"]):
                continue

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
        # if there are any, 
        for medIntake in self.on_going_medicine_intake:
            self.med_intake_RCs_to_show.add(medIntake.notify_user())

    def load_from_file(self):
        pass

    def save_to_file(self):
        pass