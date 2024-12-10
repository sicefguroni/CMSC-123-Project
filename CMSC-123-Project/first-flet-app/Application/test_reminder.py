from datetime import datetime, date, time
import flet as ft
from typing import Callable


class Appointment_ReminderCard:
    def __init__(
        self,
        id: int,
        doctor_name: str,
        appt_date: str,
        appt_time: str,
        on_delete: Callable,
    ):
        self.id = id

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
            self.on_delete(self)  # Call the delete callback

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


def main(page: ft.Page):
    def mock_on_delete(card):
        print(f"Card {card.id} deleted.")
        page.controls.remove(card.card)
        page.update()

    # Create an appointment reminder card
    reminder = Appointment_ReminderCard(
        id=1,
        doctor_name="Smith",
        appt_date="2024-12-15",
        appt_time="15:30",
        on_delete=mock_on_delete,
    )

    # Add the card to the page
    page.controls.append(reminder.card)
    page.update()

    # Simulate a notification
    if reminder.notify_user():
        print("Notification triggered!")

# Run the Flet app
ft.app(target=main)
