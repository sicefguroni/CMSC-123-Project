import flet as ft
from datetime import date, datetime, time, timedelta
from typing import Callable
from abc import ABC, abstractmethod
import json
from prescription_backend import PrescriptionManager


# Helper Functions
# ----------------------------------------------------------- #
def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%m/%d/%Y").date()

def date_to_str(date_obj: datetime.date) -> str:
    return date_obj.strftime("%m/%d/%Y")

def str_to_time(time_str: str) -> datetime.time:
    return datetime.strptime(time_str, "%H:%M").time()

def time_to_str(time_obj: datetime.time) -> str:
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

class Reminder_SLL(LinkedList):
    def in_the_list(self, id: int):
        for reminder in self:
            if reminder.id == id:
                return True
        return False



# Reminder: Hold information to remind users
# ----------------------------------------------------------- #
class Appointment:
    def __init__(self, id: int, doctor_name: str, appointment_date: str, appointment_time: str):
        self.id = id
        self.doctor_name = doctor_name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

    def is_day_before(self) -> bool:
        appointment_date = str_to_date(self.appointment_date)
        return date.today() == (appointment_date - timedelta(days=1))


class MedIntake:
    def __init__(
        self,
        id: int,
        medicine_name: str,
        dosage: str,
        frequency_sched: str,
        time_interval: float,
        start_date: str,
        end_date: str,
    ):
        self.id = id
        self.intake_count_per_freq = 0
        self.last_intake_datetime = None
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.frequency_number = self._get_number_from_frequency(frequency_sched)
        self.frequency_days = self._get_days_from_frequency(frequency_sched)
        self.time_interval = time_interval
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self) -> bool:
        today = date.today()
        start_date = str_to_date(self.start_date)
        end_date = str_to_date(self.end_date)
        return start_date <= today <= end_date

    def is_5_minutes_before_time(self) -> bool:
        current_time = datetime.now().time()
        next_intake_time = self._get_next_interval_time()
        notification_time = (datetime.combine(date.today(), next_intake_time) - timedelta(minutes=5)).time()
        return current_time >= notification_time

    def _get_next_interval_time(self) -> time:
        base_time = time(7, 0)
        interval = timedelta(hours=int(self.time_interval)) * self.intake_count_per_freq
        next_time = (datetime.combine(date.today(), base_time) + interval).time()
        return next_time

    @staticmethod
    def _get_number_from_frequency(input_str: str) -> int:
        try:
            number, _ = input_str.split('/')
            return int(number)
        except ValueError:
            raise ValueError("Frequency must be in the format 'number/frequency', e.g., '2/daily'.")

    @staticmethod
    def _get_days_from_frequency(input_str: str) -> int:
        try:
            _, frequency = input_str.split('/')
            if frequency.lower() == "daily":
                return 1
            elif frequency.lower() == "weekly":
                return 7
            else:
                raise ValueError("Invalid frequency. Must be 'daily' or 'weekly'.")
        except ValueError:
            raise ValueError("Frequency must be in the format 'number/frequency', e.g., '2/daily'.")



# Reminder Cards: Creates cards for each type of reminder
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

    @abstractmethod
    def delay_before_delete(self):
        pass


class Appointment_ReminderCard(ReminderCard):
    def __init__(self, reminder_info:Appointment, on_delete: Callable):
        self.reminder_info = reminder_info
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
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
                                f"You have an appointment with Dr. {self.reminder_info.doctor_name} ",
                                f"on {self.reminder_info.appointment_date} at {self.reminder_info.appointment_time}. Get ready!"
                                f"Mark this done when you have finished your appointment. :D"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def notify_user(self) -> ft.Card:
        if self.reminder_info.is_day_before():
            return self.card

    def _on_checked(self, e):
        if self.chk_btn.value:
            self.delay_before_delete()

    def delay_before_delete(self):
        import threading
        threading.Timer(3, lambda: self.on_delete(self)).start()


class MedIntake_ReminderCard(ReminderCard):
    def __init__(self, reminder_info:MedIntake, on_delete: Callable):
        self.reminder_info = reminder_info
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(f"{self.reminder_info.medicine_name} ({self.reminder_info.dosage})"),
                            trailing=self.chk_btn,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"It's almost time to take your {self.reminder_info.medicine_name} ({self.reminder_info.dosage})! "
                                f"Once you're done, mark the reminder done! :D"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def notify_user(self) -> ft.Card:
        if self.reminder_info.is_active() and self.reminder_info.is_5_minutes_before_time():
            return self.card

    def _on_checked(self, e):
        if self.chk_btn.value:  # Checkbox is marked
            self.reminder_info.intake_count_per_freq += 1
            self.reminder_info.last_intake_datetime = date_to_str(datetime.now())
            self.delay_before_delete()

    def delay_before_delete(self):
        import threading
        threading.Timer(3, lambda: self.on_delete(self)).start()

    

# File names to save reminders
# ----------------------------------------------------------- #
APPOINTMENT_TO_SHOW_File = "appointment_to_show.json"
MED_INTAKE_TO_SHOW_File = "med_intake_to_show.json"
FINISHED_APPOINTMENTS_File = "finished_appointments.json"
FINISHED_MED_INTAKE_File = "finished_med_intake.json"



class ReminderManager:
    def __init__(self):
        # Using dictionaries instead of linked lists
        self.appointments_RCs_to_show = {}  # Dictionary to hold Appointment_ReminderCard objects
        self.med_intake_RCs_to_show = {}  # Dictionary to hold MedIntake_ReminderCard objects

        self.med_intake_to_show = {}  # Dictionary to hold MedIntake objects
        self.appointments_to_show = {}  # Dictionary to hold Appointment objects

        self.finished_appointments = set()  # Using a set to store finished appointment IDs
        self.finished_medicine_intake = set()  # Using a set to store finished medicine intake IDs

    def collect_ongoing_prescriptions(self):
        prescription_module = PrescriptionManager()
        all_prescriptions = prescription_module.get_all_prescriptions()

        # Collect appointments
        for p in all_prescriptions:
            if p["id"] in self.finished_appointments or p["id"] in self.appointments_to_show:
                continue

            new_appt_reminder = Appointment(
                id=p["id"],
                doctor_name=p["doctor"],
                appointment_date=p["appointment_date"],
                appointment_time=p["appointment_time"],
            )

            self.appointments_to_show[p["id"]] = new_appt_reminder
            print("New Prescription! Reminder created")

        # Collect medicine intake reminders
        for p in all_prescriptions:
            if p["id"] in self.finished_medicine_intake or p["id"] in self.med_intake_to_show:
                continue

            new_MI_reminder = MedIntake(
                id=p["id"],
                medicine_name=p["medication"],
                dosage=p["dosage"],
                frequency_sched=p["frequency"],
                time_interval=p["time_interval"],
                start_date=p["start_date"],
                end_date=p["end_date"],
            )
            self.med_intake_to_show[p["id"]] = new_MI_reminder

    def notify_user(self):
        self.appointments_RCs_to_show = {}
        self.med_intake_RCs_to_show = {}

        # Check appointments for reminders
        for appt_id, appt in self.appointments_to_show.items():
            if appt.is_day_before():
                self.appointments_RCs_to_show[appt_id] = Appointment_ReminderCard(appt, self.remove_appointment)

        # Check medicine intake for reminders
        for med_id, medIntake in self.med_intake_to_show.items():
            if medIntake.is_active():
                card = MedIntake_ReminderCard(medIntake, self.remove_medicine_intake)
                if card.notify_user():
                    self.med_intake_RCs_to_show[med_id] = card

    def remove_appointment(self, card: Appointment_ReminderCard):
        del self.appointments_RCs_to_show[card.reminder_info.id]
        del self.appointments_to_show[card.reminder_info.id]
        self.finished_appointments.add(card.reminder_info.id)  # Store ID in the set
        self.save_state()

    def remove_medicine_intake(self, card: MedIntake_ReminderCard):
        del self.med_intake_RCs_to_show[card.reminder_info.id]
        del self.med_intake_to_show[card.reminder_info.id]
        self.finished_medicine_intake.add(card.reminder_info.id)  # Store ID in the set
        self.save_state()

    def save_state(self):
        try:
            # Save appointments to file
            with open(APPOINTMENT_TO_SHOW_File, "w") as f:
                json.dump([
                    {
                        "id": appt.id,
                        "doctor_name": appt.doctor_name,
                        "appointment_date": appt.appointment_date,
                        "appointment_time": appt.appointment_time,
                    }
                    for appt in self.appointments_to_show.values()
                ], f)

            # Save medicine intake to file
            with open(MED_INTAKE_TO_SHOW_File, "w") as f:
                json.dump([
                    {
                        "id": med.id,
                        "medicine_name": med.medicine_name,
                        "dosage": med.dosage,
                        "frequency_sched": med.frequency_sched,
                        "time_interval": med.time_interval,
                        "start_date": med.start_date,
                        "end_date": med.end_date,
                    }
                    for med in self.med_intake_to_show.values()
                ], f)

            # Save finished reminders
            with open(FINISHED_APPOINTMENTS_File, "w") as f:
                json.dump(list(self.finished_appointments), f)  # Save IDs in the set

            with open(FINISHED_MED_INTAKE_File, "w") as f:
                json.dump(list(self.finished_medicine_intake), f)  # Save IDs in the set

        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self):
        try:
            self.appointments_to_show = {}
            self.med_intake_to_show = {}
            self.finished_appointments = set()
            self.finished_medicine_intake = set()

            # Load appointments
            try:
                with open(APPOINTMENT_TO_SHOW_File, "r") as f:
                    appointments = json.load(f)
                    for appt_data in appointments:
                        self.appointments_to_show[appt_data["id"]] = Appointment(
                            id=appt_data["id"],
                            doctor_name=appt_data["doctor_name"],
                            appointment_date=appt_data["appointment_date"],
                            appointment_time=appt_data["appointment_time"],
                        )
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {APPOINTMENT_TO_SHOW_File} due to missing or invalid data.")

            # Load medicine intake
            try:
                with open(MED_INTAKE_TO_SHOW_File, "r") as f:
                    med_intakes = json.load(f)
                    for med_data in med_intakes:
                        self.med_intake_to_show[med_data["id"]] = MedIntake(
                            id=med_data["id"],
                            medicine_name=med_data["medicine_name"],
                            dosage=med_data["dosage"],
                            frequency_sched=med_data["frequency_sched"],
                            time_interval=med_data["time_interval"],
                            start_date=med_data["start_date"],
                            end_date=med_data["end_date"],
                        )
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {MED_INTAKE_TO_SHOW_File} due to missing or invalid data.")

            # Load finished reminders
            try:
                with open(FINISHED_APPOINTMENTS_File, "r") as f:
                    self.finished_appointments = set(json.load(f))  # Load IDs into the set
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {FINISHED_APPOINTMENTS_File} due to missing or invalid data.")

            try:
                with open(FINISHED_MED_INTAKE_File, "r") as f:
                    self.finished_medicine_intake = set(json.load(f))  # Load IDs into the set
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {FINISHED_MED_INTAKE_File} due to missing or invalid data.")

        except Exception as e:
            print(f"Error loading from file: {e}")

    def get_appointment_cards(self):
        return list(self.appointments_RCs_to_show.values())

    def get_med_intake_cards(self):
        return list(self.med_intake_RCs_to_show.values())



