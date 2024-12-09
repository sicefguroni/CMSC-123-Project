import flet as ft
from typing import Callable
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


def str_frequency_sched_to_timedelta(frequency: str) -> timedelta:
    """Convert frequency schedule to timedelta."""
    try:
        frequency_unit = frequency.split("/")[1].lower()
        if frequency_unit == "day":
            return timedelta(days=1)
        elif frequency_unit == "week":
            return timedelta(days=7)
        else:
            raise ValueError("Invalid frequency schedule unit.")
    except (IndexError, ValueError):
        raise ValueError("Invalid frequency schedule format. Expected <number>/<unit>.")

def str_frequency_to_int(frequency: str) -> int:
    """Extract the number of occurrences from the frequency string."""
    try:
        return int(frequency.split("/")[0])
    except (IndexError, ValueError):
        raise ValueError("Invalid frequency format. Expected <number>/<unit>.")


# Reminder Cards
# ----------------------------------------------------------- #
class AppointmentReminderCard:
    """Represents a reminder card for an appointment."""

    def __init__(
        self, 
        id: int, 
        doctor_name: str, 
        appt_date: str, 
        appt_time: str, 
        reminder_count: int, 
        on_delete: Callable
    ):
        self.id = id
        self.reminder_count = reminder_count
        self.doctor_name = doctor_name
        self.appointment_date = appt_date
        self.appointment_time = appt_time
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        if self.is_today() or self.is_tomorrow():
            """Create a reminder card UI component."""
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

    def is_tomorrow(self) -> bool:
        """Check if the appointment is tomorrow."""
        return date.today() == str_to_date(self.appointment_date) - timedelta(days=1)

    def is_today(self) -> bool:
        """Check if the appointment is today."""
        return date.today() == str_to_date(self.appointment_date)

    def _on_checked(self, e):
        """Handle checkbox state changes."""
        if e.control.value:
            self.on_delete(self)
        return self.id

class MedicineIntakeReminderCard:
    """Represents a reminder card for medicine intake."""

    def __init__(
        self,
        id: int,
        medicine_name: str,
        dosage: str,
        frequency_sched: str,
        time_interval: float,
        reminder_count_today: int,
        reminder_count_total: int,
        frequency_sched_count: int,
        on_delete: Callable
    ):
        self.id = id
        self.reminder_count_today = reminder_count_today
        self.reminder_count_total = reminder_count_total
        self.frequency_schedule_count = frequency_sched_count
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.frequency_number = str_frequency_to_int(frequency_sched)
        self.frequency_schedule = str_frequency_sched_to_timedelta(frequency_sched)
        self.time_interval = timedelta(hours=time_interval)
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _reset_reminder_count(self):
        """Reset the daily reminder count at the start of a new day."""
        if datetime.now().time() >= str_to_time("07:00"):
            self.reminder_count_today = 0

    def _create_reminder_card(self) -> ft.Card:
        """Create a reminder card UI component."""
        self._reset_reminder_count()  # Ensure daily reset
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

    def is_time(self) -> bool:
        """Check if it's time for the next intake."""
        current_time = datetime.now().time()
        next_intake_time = self._get_next_interval_time()
        return current_time >= next_intake_time

    def _get_next_interval_time(self) -> datetime.time:
        """Calculate the next interval time."""
        base_time = str_to_time("07:00")
        interval = self.reminder_count_today * self.time_interval
        next_time = (datetime.combine(date.today(), base_time) + interval).time()
        return next_time

    def _on_checked(self, e):
        """Handle checkbox state changes."""
        if e.control.value:
            if self.reminder_count_today < self.frequency_number:
                self.reminder_count_today += 1
                self.reminder_count_total += 1
                self.on_delete(self)
            else:
                print("Maximum daily intake reached!")
        return self.id



# Linked List: Data Structure
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



# Reminder Files
# ----------------------------------------------------------- #
# File to save id of prescriptions that have accomplished appointments and med intake
APPOINTMENTS_ACCOMPLISHED_File = "appointments_accomplished.json"
MEDICINE_INTAKE_ACCOMPLISHED_File = "medicine_intake_accomplished.json"

# File to save reminders for persistence
APPOINTMENTS_REMINDERS_File = "appointments_reminders.json"
MEDICINE_INTAKE_REMINDERS_File = "medicine_intake_reminders.json"

# File to save shown reminders for persistence
SHOWN_APPTS_File = "shown_appointments_reminder.json"
SHOWN_MED_INTAKE_File = "shown_med_intake_reminder.json"



# Load all prescriptions from prescription_backend.py
# ----------------------------------------------------------- #
prescription_module = PrescriptionManager()
all_prescriptions = prescription_module.get_all_prescriptions()

def ensure_file_exists(file_path: str, default_content=None):
    """Ensure the file exists. If not, create it with default content."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(default_content if default_content is not None else [], file)
        print(f"File '{file_path}' created with default content.")

def load_from(file_path: str) -> LinkedList:
    """Load data from a JSON file into a LinkedList. Supports any data type."""
    loaded_list = LinkedList()

    ensure_file_exists(file_path)

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Add all data directly to the linked list
        if isinstance(data, list):
            for item in data:
                loaded_list.add(item)
        else:
            loaded_list.add(data)  # Add as a single node if not a list
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{file_path}'. File may be corrupted.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while loading '{file_path}': {e}")

    return loaded_list



# Reminder manager class
# ----------------------------------------------------------- #
class Reminder_Manager:
    def __init__(self):
        self.showing_appointment_cards = LinkedList()  # A container containing a list of cards
        self.showing_med_intake_cards = LinkedList()

        self.appointments = LinkedList()
        self.medicine_intake_reminders = LinkedList()
        self.APPT_accomplished = LinkedList()
        self.MIR_accomplished = LinkedList()

    def load_data(self):
        """Load reminders and accomplished records from files."""
        self.appointments = load_from(APPOINTMENTS_REMINDERS_File)
        self.medicine_intake_reminders = load_from(MEDICINE_INTAKE_REMINDERS_File)
        self.APPT_accomplished = load_from(APPOINTMENTS_ACCOMPLISHED_File)
        self.MIR_accomplished = load_from(MEDICINE_INTAKE_ACCOMPLISHED_File)

    def save_data(self):
        """Save reminders and accomplished records to files."""
        self._save_to_file(self.appointments, APPOINTMENTS_REMINDERS_File)
        self._save_to_file(self.medicine_intake_reminders, MEDICINE_INTAKE_REMINDERS_File)
        self._save_to_file(self.APPT_accomplished, APPOINTMENTS_ACCOMPLISHED_File)
        self._save_to_file(self.MIR_accomplished, MEDICINE_INTAKE_ACCOMPLISHED_File)

    @staticmethod
    def _save_to_file(linked_list, file_path):
        """Save a LinkedList to a JSON file."""
        data = []
        current = linked_list.head
        while current:
            data.append(current.value)
            current = current.nxt

        with open(file_path, 'w') as file:
            json.dump(data, file)

    def _create_reminders(self):
        """Create reminders for new prescriptions."""
        for prescription in all_prescriptions:
            # Check if an appointment reminder already exists
            if not self._is_prescription_in_list(prescription['id'], self.appointments):
                self.appointments.add(
                    AppointmentReminderCard(
                        id=prescription['id'],
                        doctor_name=prescription['doctor_name'],
                        appt_date=prescription['appt_date'],
                        appt_time=prescription['appt_time'],
                        reminder_count=0,
                        on_delete=self._on_reminder_checked
                    )
                )
            # Check if a medicine intake reminder already exists
            if not self._is_prescription_in_list(prescription['id'], self.medicine_intake_reminders):
                self.medicine_intake_reminders.add(
                    MedicineIntakeReminderCard(
                        id=prescription['id'],
                        medicine_name=prescription['medicine_name'],
                        dosage=prescription['dosage'],
                        frequency_sched=prescription['frequency_sched'],
                        time_interval=prescription['time_interval'],
                        reminder_count_today=0,
                        reminder_count_total=0,
                        frequency_sched_count=0,
                        on_delete=self._on_reminder_checked
                    )
                )

    @staticmethod
    def _is_prescription_in_list(prescription_id, linked_list):
        """Check if a prescription ID exists in a LinkedList."""
        current = linked_list.head
        while current:
            if current.value.id == prescription_id:
                return True
            current = current.nxt
        return False

    def _notify_user(self):
        """Notify user of appointments and medicine intake."""
        # Notify appointments
        current = self.appointments.head
        while current:
            reminder = current.value
            if reminder.is_today() or reminder.is_tomorrow():
                if not self._is_prescription_in_list(reminder.id, self.showing_appointment_cards):
                    self.showing_appointment_cards.add(reminder)
            current = current.nxt

        # Notify medicine intake
        current = self.medicine_intake_reminders.head
        while current:
            reminder = current.value
            if reminder.is_time():
                if not self._is_prescription_in_list(reminder.id, self.showing_med_intake_cards):
                    self.showing_med_intake_cards.add(reminder)
            current = current.nxt

    def _on_reminder_checked(self, reminder):
        """Handle when a reminder is checked (marked as completed)."""
        if isinstance(reminder, AppointmentReminderCard):
            # Remove from appointments and move to accomplished
            self.appointments.remove(reminder)
            self.APPT_accomplished.add(reminder.id)
        elif isinstance(reminder, MedicineIntakeReminderCard):
            # Remove from medicine intake reminders and move to accomplished
            self.medicine_intake_reminders.remove(reminder)
            self.MIR_accomplished.add(reminder.id)
        self.save_data()


class Reminder_Page:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "Medicine Intake"  # Default view
        self.Medicine_Intake_Reminders_List = LinkedList()
        self.Appointment_Reminders_List = LinkedList()
        self.Finished_Appointments = []

        self.notification_switch = ft.Switch(label="Enable Notifications", value=True)
        self.medicine_button = ft.TextButton(
            text="Medicine Intake",
            width=150,
            on_click=lambda e: self._show_view("Medicine Intake"),
        )
        self.appointment_button = ft.TextButton(
            text="Appointment",
            width=150,
            on_click=lambda e: self._show_view("Appointment"),
        )

        self.reminder_list_view = ft.ListView(
            spacing=10, height=500, expand=True
        )
        self.page_container = self._create_reminder_page()

        # Initialize reminders from the JSON file
        self._initialize_reminders()

    def _initialize_reminders(self):
        for prescription in prescriptions_data:
            # Load medicine intake reminders
            medicine_card = Med_Intake_Reminder_Card(
                medicineName=prescription["medication"],
                dosage=prescription["dosage"],
                id=prescription["id"],
                on_delete=self._delete_reminder,
            )
            self.Medicine_Intake_Reminders_List.add(medicine_card)

            # Load appointment reminders
            appointment_card = Appointment_Reminder_Card(
                doctorName=prescription["doctor"],
                appointmentDate=prescription["appointment_date"],
                appointmentTime=prescription["appointment_time"],
                id=prescription["id"],
                on_delete=self._delete_reminder,
            )
            self.Appointment_Reminders_List.add(appointment_card)

    def _delete_reminder(self, reminder_card):
        """
        Handle the deletion of a reminder card.
        """
        self.reminder_list_view.controls.remove(reminder_card.get())

        # Remove the reminder from the linked list
        if isinstance(reminder_card, Med_Intake_Reminder_Card):
            self.Medicine_Intake_Reminders_List.remove(reminder_card)
        elif isinstance(reminder_card, Appointment_Reminder_Card):
            self.Appointment_Reminders_List.remove(reminder_card)

        self.page.update()

    def _show_view(self, view_name: str):
        """
        Display the selected view and populate the ListView with the appropriate reminders.
        """
        self.current_view = view_name
        self.reminder_list_view.controls.clear()

        if view_name == "Medicine Intake":
            self._load_medicine_reminders()
        elif view_name == "Appointment":
            self._load_appointment_reminders()

        self.page.update()

    def _load_medicine_reminders(self):
        """
        Populate the ListView with medicine intake reminders from the linked list.
        """
        current = self.Medicine_Intake_Reminders_List.head
        while current:
            self.reminder_list_view.controls.append(current.value.get())
            current = current.nxt

    def _load_appointment_reminders(self):
        """
        Populate the ListView with appointment reminders from the linked list.
        """
        current = self.Appointment_Reminders_List.head
        while current:
            self.reminder_list_view.controls.append(current.value.get())
            current = current.nxt

    def _create_reminder_page(self):
        """
        Create the reminder page layout.
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.notification_switch,
                    ft.Row(
                        controls=[
                            self.medicine_button,
                            self.appointment_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    self.reminder_list_view,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            visible=False,
        )



