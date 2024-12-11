import flet as ft
from typing import List
from pages.reminder_page_backend import ReminderManager, Appointment_ReminderCard, MedIntake_ReminderCard


class Reminder_Page:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "Medicine Intake"  # Default view
        self.reminder_manager = ReminderManager()  # Instantiate the backend ReminderManager
        self.reminder_cards = []

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
        """Remove a specific reminder card."""
        if reminder_card in self.reminder_cards:
            self.reminder_cards.remove(reminder_card)
            self.reminder_list_view.controls.remove(reminder_card.card)

            if isinstance(reminder_card, Appointment_ReminderCard):
                self.reminder_manager.remove_appointment(reminder_card)
            elif isinstance(reminder_card, MedIntake_ReminderCard):
                self.reminder_manager.remove_medicine_intake(reminder_card)

            # Save state only after removing
            self.reminder_manager.save_state()

            # Show no reminders text if list becomes empty
            if not self.reminder_cards:
                self.no_reminders_text.visible = True

            self.page.update()

    def _show_view(self, view_name: str):
        self.current_view = view_name
        self.reminder_list_view.controls.clear()  # Clear the list view

        if view_name == "Medicine Intake":
            self._load_medicine_reminders()
        elif view_name == "Appointment":
            self._load_appointment_reminders()

        # Update the placeholder visibility
        self.no_reminders_text.visible = len(self.reminder_list_view.controls) == 0

        self.page.update()

    def _load_medicine_reminders(self):
        # Get list of medicine intake reminders
        self.med_intake_cards = self.reminder_manager.get_med_intake_cards()

        if not self.med_intake_cards:  # Check if list is empty
            self.no_reminders_text.visible = True
            return

        for med_reminder in self.med_intake_cards:
            self._add_reminder(med_reminder)

    def _load_appointment_reminders(self):
        # Get list of appointment reminders
        self.appointment_cards = self.reminder_manager.get_appointment_cards()

        if not self.appointment_cards:  # Check if list is empty
            self.no_reminders_text.visible = True
            return

        for appt_reminder in self.appointment_cards:
            self._add_reminder(appt_reminder)

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
