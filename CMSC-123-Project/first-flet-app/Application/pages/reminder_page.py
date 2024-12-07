import flet as ft
from typing import List


class Reminder_Card:
    def __init__(self, title: str, content: str, on_delete: callable):
        self.title = title
        self.content = content
        self.on_delete = on_delete  # Callback for deleting the card
        self.chk_btn = ft.Checkbox(value=False, on_change=self._on_checked)
        self.card = self._create_reminder_card()

    def _on_checked(self, e):
        if e.control.value:  # If checkbox is checked
            self.on_delete(self)

    def _create_reminder_card(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Title of Reminder Card + Checkbox
                        ft.ListTile(
                            title=ft.Text(self.title),
                            trailing=self.chk_btn,
                        ),
                        # Content of Reminder Card
                        ft.Container(
                            content=ft.Text(self.content),
                            padding=ft.padding.only(left=20, right=20),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=5),
            )
        )

    def get(self):
        return self.card




class Reminder_Page:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "Medicine Intake"  # Default view
        self.reminder_cards = []  # List of current reminders

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


    def _add_reminder(self, title: str, content: str):
        # Add a new reminder card
        reminder_card = Reminder_Card(
            title,
            content,
            on_delete=self._delete_reminder,
        )
        self.reminder_cards.append(reminder_card)
        self.reminder_list_view.controls.append(reminder_card.get())
        self.page.update()


    def _delete_reminder(self, reminder_card):
        # Delete a specific reminder card
        self.reminder_cards.remove(reminder_card)
        self.reminder_list_view.controls.remove(reminder_card.get())
        self.page.update()


    def _show_view(self, view_name: str):
        self.current_view = view_name
        # Clear existing list view and load new reminders
        self.reminder_list_view.controls.clear()
        if view_name == "Medicine Intake":
            self._load_medicine_reminders()
        elif view_name == "Appointment":
            self._load_appointment_reminders()
        self.page.update()

    def _load_medicine_reminders(self):
        # Load medicine reminders (example data)
        reminders = [
            ("Take morning pills", "8:00 AM"),
            ("Take vitamins", "12:00 PM"),
        ]
        for title, content in reminders:
            self._add_reminder(title, content)

    def _load_appointment_reminders(self):
        # Load appointment reminders (example data)
        reminders = [
            ("Visit Dr. Smith", "3:00 PM"),
            ("Dental check-up", "10:00 AM"),
        ]
        for title, content in reminders:
            self._add_reminder(title, content)

    def _create_reminder_page(self):
        # Create Reminder Page layout
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Enable Notifications Switch
                    self.notification_switch,
                    # Buttons for Medicine and Appointment
                    ft.Row(
                        controls=[
                            self.medicine_button,
                            self.appointment_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    # Reminder List
                    self.reminder_list_view,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            visible=False,
        )