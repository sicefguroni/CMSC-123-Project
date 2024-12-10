import flet as ft
from datetime import datetime, timedelta, date, time
from typing import Callable
from abc import ABC, abstractmethod
import json
from prescription_backend import PrescriptionManager


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
    def __init__(self, id: int, doctor_name: str, appt_date: str, appt_time: str, on_delete: Callable):
        self.id = id
        self.is_done = False
        self.doctor_name = doctor_name
        self.appointment_date = appt_date
        self.appointment_time = appt_time
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
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

    def notify_user(self) -> ft.Card:
        if self.is_day_before():
            return self.card

    def _on_checked(self, e):
        if self.chk_btn.value:  # Checkbox is marked
            self.is_done = True
            self.delay_before_delete()

    def delay_before_delete(self):
        import threading
        threading.Timer(3, lambda: self.on_delete(self)).start()

    def is_day_before(self) -> bool:
        appointment_date = self._str_to_date(self.appointment_date)
        return date.today() == (appointment_date - timedelta(days=1))

    def _str_to_date(self, date_str: str) -> date:
        return datetime.strptime(date_str, "%Y-%m-%d").date()


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
        on_delete: Callable,
    ):
        self.id = id
        self.intake_count_per_freq = 0
        self.frequency_sched_count = 0
        self.last_intake_datetime = None
        self.medicine_name = medicine_name
        self.dosage = dosage
        self.frequency_number = self._str_frequency_to_int(frequency_sched)
        self.frequency_schedule = self._str_frequency_sched_to_timedelta(frequency_sched)
        self.time_interval = timedelta(hours=int(time_interval))
        self.start_date = start_date
        self.end_date = end_date
        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _create_reminder_card(self) -> ft.Card:
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
        if self.is_active() and self.is_time():
            return self.card

    def _on_checked(self, e):
        if self.chk_btn.value:  # Checkbox is marked
            self.intake_count_per_freq += 1
            self.last_intake_datetime = datetime.now()
            self.delay_before_delete()

    def delay_before_delete(self):
        import threading
        threading.Timer(3, lambda: self.on_delete(self)).start()

    def is_active(self) -> bool:
        today = date.today()
        return self.start_date <= today <= self.end_date

    def is_time(self) -> bool:
        current_time = datetime.now().time()
        next_intake_time = self._get_next_interval_time()
        notification_time = (datetime.combine(date.today(), next_intake_time) - timedelta(minutes=5)).time()
        return current_time >= notification_time

    def _get_next_interval_time(self) -> time:
        base_time = time(7, 0)
        interval = timedelta(seconds=self.intake_count_per_freq * self.time_interval.total_seconds())
        next_time = (datetime.combine(date.today(), base_time) + interval).time()
        return next_time

    def _str_frequency_to_int(self, freq: str) -> int:
        mapping = {"daily": 1, "weekly": 7}
        return mapping.get(freq.lower(), 0)

    def _str_frequency_sched_to_timedelta(self, freq: str) -> timedelta:
        mapping = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        return mapping.get(freq.lower(), timedelta(days=0))


class ReminderCard_SLL(LinkedList):
    def in_the_list(self, id: int):
        for card in self:
            if card.id == id:
                return True
        return False

# File paths remain unchanged
APPOINTMENT_RCs_TO_SHOW_File = "appointment_RCs_to_show.json"
MED_INTAKE_RCs_TO_SHOW_File = "med_intake_RCs_to_show.json"
CURRENT_APPOINTMENTS_RCs_File = "current_appointments_RCList.json"
CURRENT_MEDICINE_INTAKE_RCs_File = "current_medicine_intake_RCList.json"
FINISHED_APPOINTMENTS_File = "finished_appointments.json"
FINISHED_MED_INTAKE_File = "finished_med_intake.json"


class ReminderManager:
    def __init__(self):
        self.appointments_RCs_to_show = ReminderCard_SLL()
        self.med_intake_RCs_to_show = ReminderCard_SLL()
        self.on_going_medicine_intake = ReminderCard_SLL()
        self.appointments_today = ReminderCard_SLL()
        self.finished_appointments = LinkedList()
        self.finished_medicine_intake = LinkedList()

    def collect_ongoing_prescriptions(self):
        prescription_module = PrescriptionManager()
        all_prescriptions = prescription_module.get_all_prescriptions()

        for p in all_prescriptions:
            # Skip if already marked as finished or added
            if self.finished_appointments.found(p["id"]) or self.appointments_today.in_the_list(p["id"]):
                continue

            appointment_date = datetime.strptime(p["appointment_date"], "%m/%d/%Y").date()
            if appointment_date == date.today():
                new_appt_reminder = Appointment_ReminderCard(
                    id=p["id"],
                    doctor_name=p["doctor"],
                    appt_date=p["appointment_date"],
                    appt_time=p["appointment_time"],
                    on_delete=self.remove_appointment,
                )
                self.appointments_today.add(new_appt_reminder)

        for p in all_prescriptions:
            if self.finished_medicine_intake.found(p["id"]) or self.on_going_medicine_intake.in_the_list(p["id"]):
                continue

            start_date = datetime.strptime(p["start_date"], "%m/%d/%Y").date()
            end_date = datetime.strptime(p["end_date"], "%m/%d/%Y").date()
            today = date.today()
            if start_date <= today <= end_date:
                new_MI_reminder = MedIntake_ReminderCard(
                    id=p["id"],
                    medicine_name=p["medication"],
                    dosage=p["dosage"],
                    frequency_sched=p["frequency"],
                    time_interval=p["time_interval"],
                    start_date=start_date,
                    end_date=end_date,
                    on_delete=self.remove_medicine_intake,
                )
                self.on_going_medicine_intake.add(new_MI_reminder)

    def notify_user(self):
        for appt in self.appointments_today:
            if not appt.is_done:
                self.appointments_RCs_to_show.add(appt)

        for medIntake in self.on_going_medicine_intake:
            if medIntake.is_active():
                reminder = medIntake.notify_user()
                if reminder:
                    self.med_intake_RCs_to_show.add(reminder)

    def remove_appointment(self, card: Appointment_ReminderCard):
        self.appointments_RCs_to_show.remove(card)
        self.appointments_today.remove(card)
        self.finished_appointments.add(card.id)
        self.save_to_file()

    def remove_medicine_intake(self, card: MedIntake_ReminderCard):
        self.med_intake_RCs_to_show.remove(card)
        self.on_going_medicine_intake.remove(card)
        self.finished_medicine_intake.add(card.id)
        self.save_to_file()

    def save_to_file(self):
        try:
            # Serialize appointment reminders
            with open(CURRENT_APPOINTMENTS_RCs_File, "w") as f:
                json.dump([
                    {
                        "id": card.id,
                        "doctor_name": card.doctor_name,
                        "appointment_date": card.appointment_date.strftime("%Y-%m-%d"),  # Convert to string
                        "appointment_time": card.appointment_time.strftime("%H:%M:%S"),  # Convert to string
                    }
                    for card in self.appointments_today
                ], f)

            # Serialize medicine intake reminders
            with open(CURRENT_MEDICINE_INTAKE_RCs_File, "w") as f:
                json.dump([
                    {
                        "id": card.id,
                        "medicine_name": card.medicine_name,
                        "dosage": card.dosage,
                        "frequency_schedule": card.frequency_schedule,
                        "time_interval": card.time_interval.total_seconds(),  # Convert timedelta to seconds
                        "start_date": card.start_date.strftime("%Y-%m-%d"),  # Convert date to string
                        "end_date": card.end_date.strftime("%Y-%m-%d"),  # Convert date to string
                    }
                    for card in self.on_going_medicine_intake
                ], f)

            # Serialize finished reminders
            with open(FINISHED_APPOINTMENTS_File, "w") as f:
                json.dump(list(self.finished_appointments), f)

            with open(FINISHED_MED_INTAKE_File, "w") as f:
                json.dump(list(self.finished_medicine_intake), f)

        except Exception as e:
            print(f"Error saving to file: {e}")


    def load_from_file(self):
        try:
            self.appointments_today = ReminderCard_SLL()
            self.on_going_medicine_intake = ReminderCard_SLL()
            self.finished_appointments = LinkedList()
            self.finished_medicine_intake = LinkedList()

            # Load appointment reminders
            try:
                with open(CURRENT_APPOINTMENTS_RCs_File, "r") as f:
                    appointments = json.load(f)
                    for appt_data in appointments:
                        new_appt = Appointment_ReminderCard(
                            id=appt_data["id"],
                            doctor_name=appt_data["doctor_name"],
                            appt_date=datetime.strptime(appt_data["appointment_date"], "%Y-%m-%d").date(),  # Convert string back to date
                            appt_time=datetime.strptime(appt_data["appointment_time"], "%H:%M:%S").time(),  # Convert string back to time
                            on_delete=self.remove_appointment,
                        )
                        self.appointments_today.add(new_appt)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {CURRENT_APPOINTMENTS_RCs_File} due to missing or invalid data.")

            # Load medicine intake reminders
            try:
                with open(CURRENT_MEDICINE_INTAKE_RCs_File, "r") as f:
                    med_intakes = json.load(f)
                    for med_data in med_intakes:
                        new_med = MedIntake_ReminderCard(
                            id=med_data["id"],
                            medicine_name=med_data["medicine_name"],
                            dosage=med_data["dosage"],
                            frequency_sched=med_data["frequency_schedule"],
                            time_interval=timedelta(seconds=med_data["time_interval"]),  # Convert seconds back to timedelta
                            start_date=datetime.strptime(med_data["start_date"], "%Y-%m-%d").date(),  # Convert string back to date
                            end_date=datetime.strptime(med_data["end_date"], "%Y-%m-%d").date(),  # Convert string back to date
                            on_delete=self.remove_medicine_intake,
                        )
                        self.on_going_medicine_intake.add(new_med)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {CURRENT_MEDICINE_INTAKE_RCs_File} due to missing or invalid data.")

            # Load finished reminders
            try:
                with open(FINISHED_APPOINTMENTS_File, "r") as f:
                    self.finished_appointments = LinkedList(json.load(f))
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {FINISHED_APPOINTMENTS_File} due to missing or invalid data.")

            try:
                with open(FINISHED_MED_INTAKE_File, "r") as f:
                    self.finished_medicine_intake = LinkedList(json.load(f))
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Skipping loading {FINISHED_MED_INTAKE_File} due to missing or invalid data.")

        except Exception as e:
            print(f"Error loading from file: {e}")




