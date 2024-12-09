import flet as ft
from typing import List
from datetime import date, datetime, timedelta
from abc import ABC, abstractmethod
import json

# Convert MM/DD/YYYY to date
def dateStr_to_dateFormat(date_str:str) -> date:
    date_obj = datetime.strptime(date_str, "%m/%d%Y").date()
    return date_obj


#-----------------------------------------------------------#
# Access contents from prescriptions.json
file_path = "prescriptions.json"
with open(file_path, 'r') as file:
    prescriptions_data = json.load(file)



#-----------------------------------------------------------#
# Reminder Cards class to show for the Reminders Page
class Reminder_Card(ABC):
    @abstractmethod
    def _on_checked(self, e):
        pass

    @abstractmethod
    def _create_reminder_card(self):
        pass

    @abstractmethod
    def get_card(self):
        pass

        


class Appointment_Reminder_Card(Reminder_Card):
    def __init__(self, doctorName:str, appointmentDate:str, appointmentTime:str, id:int, on_delete:callable):
        self.doctor_Name = doctorName
        self.appointment_Date = appointmentDate
        self.appointment_Time = appointmentTime
        self.id = id

        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)

        self.card = self._create_reminder_card()

    # If checkbox is checked, self delete
    def _on_checked(self, e):
        if e.control.value:
            self.on_delete(self)

    def _create_reminder_card(self):
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
                                f"You have an appointment with Dr. {self.doctor_Name} "
                                f"on {self.appointment_Date} at {self.appointment_Time}. Get ready!"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
        )

    def get_card(self):
        return self.card

    def isTomorrow(self):
        current_day = datetime.now().strftime("%m/%d/%Y")
        day_before_appointment = self.appointment_Date - timedelta(days=1)
        
        if current_day == day_before_appointment:
            return True
        
        return False
    
    def isToday(self):
        current_day = datetime.now()
        
        if current_day == self.appointment_Date:
            return True
        
        return False
    


class Med_Intake_Reminder_Card(Reminder_Card):
    def __init__(self, medicineName:str, dosage:str, frequency:int, time_interval:float, id:int, on_delete: callable):
        self.medicine_name = medicineName
        self.dosage = dosage
        self.frequency = frequency
        self.time_interval = time_interval
        self.id = id

        self.on_delete = on_delete
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)

        self.card = self._create_reminder_card()

    # If checkbox is checked, self delete
    def _on_checked(self, e):
        if e.control.value:
            self.on_delete(self)

    def _create_reminder_card(self):
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
                                f"It's time to take your {self.medicine_name} ({self.dosage})!"
                            ),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=5),
            ),
        )

    def get_card(self):
        return self.card



#-----------------------------------------------------------#
# Class to manage reminders
class Reminder_Manager:
    def __init__(self):
        pass

    def remind_medicine_intake(self):
        pass

    def remind_appointment(self):
        pass


    # Helper functions:
    def convert_frequency_to_str(self, frequency:str):
        pass





#--------------- DATA STRUCTURE: LINKED LIST ---------------#
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



# -----------------------------------------------------------#
# Reminder Page Class
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
