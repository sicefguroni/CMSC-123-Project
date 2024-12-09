import flet as ft
from typing import Callable, Any
from datetime import date, datetime, timedelta
from prescription_backend import PrescriptionManager
import json
import os

# Helper Functions
# ----------------------------------------------------------- #
def str_to_date(date_str: str) -> date:
    """Convert MM/DD/YYYY string to a date object."""
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").date()
    except ValueError:
        raise ValueError("Invalid date format. Expected MM/DD/YYYY.")

def date_to_str(date_obj: date) -> str:
    """Convert a date object to MM/DD/YYYY string."""
    return date_obj.strftime("%m/%d/%Y")

def str_to_time(time_str: str) -> datetime.time:
    """Convert HH:MM string to a time object."""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Invalid time format. Expected HH:MM.")

def time_to_str(time_obj: datetime.time) -> str:
    """Convert a time object to HH:MM string."""
    return time_obj.strftime("%H:%M")

# LinkedList Definition
# ----------------------------------------------------------- #
class Node:
    """Node class for LinkedList."""
    def __init__(self, data: Any):
        self.data = data
        self.next = None

class LinkedList:
    """Simple LinkedList class for managing reminders."""
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, data: Any):
        """Add a new node to the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def remove(self, data: Any):
        """Remove a node by data."""
        current = self.head
        prev = None
        while current:
            if current.data == data:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return
            prev = current
            current = current.next

    def __iter__(self):
        """Iterate through the LinkedList."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        """Return the size of the list."""
        return self.size

# Reminder Card Base Class
# ----------------------------------------------------------- #
class ReminderCard:
    """Base class for reminder cards."""
    def __init__(self, id: int, on_delete: Callable):
        self.id = id
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)

    def _on_checked(self, e):
        """Handle checkbox state changes."""
        if e.control.value:
            self.on_delete(self)

# Appointment Reminder Card
# ----------------------------------------------------------- #
class AppointmentReminderCard(ReminderCard):
    def __init__(self, id: int, doctor_name: str, appt_date: str, appt_time: str, on_delete: Callable):
        super().__init__(id, on_delete)
        self.doctor_name = doctor_name
        self.appointment_date = appt_date
        self.appointment_time = appt_time
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        """Create the UI for the reminder card."""
        appointment_date = "TODAY" if self.is_today() else self.appointment_date
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
                                f"on {appointment_date} at {self.appointment_time}. Get ready!"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def is_today(self) -> bool:
        """Check if the appointment is today."""
        return date.today() == str_to_date(self.appointment_date)

# Medicine Intake Reminder Card
# ----------------------------------------------------------- #
class MedicineIntakeReminderCard(ReminderCard):
    def __init__(
        self,
        id: int,
        medicine_name: str,
        dosage: str,
        frequency_sched: str,
        time_interval: float,
        reminder_count_today: int,
        reminder_count_total: int,
        on_delete: Callable
    ):
        super().__init__(id, on_delete)
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.frequency_sched = frequency_sched
        self.time_interval = timedelta(hours=time_interval)
        self.reminder_count_today = reminder_count_today
        self.reminder_count_total = reminder_count_total
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        """Create the UI for the reminder card."""
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
                                f"Check the checkbox once done!"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

# Reminder Manager
# ----------------------------------------------------------- #
class ReminderManager:
    def __init__(self):
        self.appointments = LinkedList()
        self.medicine_reminders = LinkedList()

    def add_appointment(self, reminder: AppointmentReminderCard):
        self.appointments.add(reminder)

    def add_medicine_reminder(self, reminder: MedicineIntakeReminderCard):
        self.medicine_reminders.add(reminder)

    def remove_appointment(self, reminder: AppointmentReminderCard):
        self.appointments.remove(reminder)

    def remove_medicine_reminder(self, reminder: MedicineIntakeReminderCard):
        self.medicine_reminders.remove(reminder)

    def get_all_appointments(self):
        return list(self.appointments)

    def get_all_medicine_reminders(self):
        return list(self.medicine_reminders)

# Main Application
# ----------------------------------------------------------- #
def main(page: ft.Page):
    reminder_manager = ReminderManager()
    # Example: Adding a reminder
    reminder_manager.add_appointment(
        AppointmentReminderCard(
            id=1,
            doctor_name="Smith",
            appt_date="12/15/2024",
            appt_time="10:30",
            on_delete=lambda r: reminder_manager.remove_appointment(r),
        )
    )
    for reminder in reminder_manager.get_all_appointments():
        page.add(reminder.card)

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
