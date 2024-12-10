import flet as ft
from typing import List
from pages.reminder_page_backend import ReminderManager


class Reminder_Page:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "Medicine Intake"  # Default view
        self.reminder_manager = ReminderManager()  # Instantiate the backend ReminderManager
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

        # Add a placeholder text for when no reminders are available
        self.no_reminders_text = ft.Text(
            "No reminders available", 
            visible=False, 
            text_align=ft.TextAlign.CENTER
        )

        self.reminder_list_view = ft.ListView(
            spacing=10, height=500, expand=True
        )
        self.page_container = self._create_reminder_page()

        # Load reminders from backend at initialization
        self._initialize_reminders()

    def _initialize_reminders(self):
        try:
            # Load ongoing prescriptions and notify users at app startup
            self.reminder_manager.load_from_file()  # Added this to restore previous state
            self.reminder_manager.collect_ongoing_prescriptions()
            self.reminder_manager.notify_user()

            # Load the default view
            self._show_view(self.current_view)
        except Exception as e:
            print(f"Error initializing reminders: {e}")
            # Show an error message to the user if needed

    def _add_reminder(self, reminder_card):
        # Add a new reminder card to the list view
        self.reminder_cards.append(reminder_card)
        self.reminder_list_view.controls.append(reminder_card.card)
        
        # Hide no reminders text if reminders exist
        self.no_reminders_text.visible = False
        self.page.update()

    def _delete_reminder(self, reminder_card):
        """Remove a specific reminder card after a delay."""
        if reminder_card in self.reminder_cards:
            self.reminder_cards.remove(reminder_card)
            self.reminder_list_view.controls.remove(reminder_card.card)
            
            # Show no reminders text if list is now empty
            if not self.reminder_cards:
                self.no_reminders_text.visible = True
            
            self.page.update()

    def _show_view(self, view_name: str):
        self.current_view = view_name
        # Clear existing list view and load new reminders
        self.reminder_list_view.controls.clear()
        
        if view_name == "Medicine Intake":
            self._load_medicine_reminders()
        elif view_name == "Appointment":
            self._load_appointment_reminders()
        
        # Show/hide no reminders text based on list contents
        self.no_reminders_text.visible = len(self.reminder_list_view.controls) == 0
        
        self.page.update()

    def _load_medicine_reminders(self):
        # Load medicine reminders from the ReminderManager
        for med_card in self.reminder_manager.med_intake_RCs_to_show:
            self._add_reminder(med_card)

    def _load_appointment_reminders(self):
        # Load appointment reminders from the ReminderManager
        for appt_card in self.reminder_manager.appointments_RCs_to_show:
            self._add_reminder(appt_card)

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
                    # No reminders placeholder
                    self.no_reminders_text,
                    # Reminder List
                    self.reminder_list_view,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            visible=False,
        )


