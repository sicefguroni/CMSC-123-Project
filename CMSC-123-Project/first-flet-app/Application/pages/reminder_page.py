import flet as ft

def reminder_page(): 
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Reminders Page!", size=20, weight=ft.FontWeight.BOLD),
                ft.Switch(label="Enable Notifications", value=True),
                ft.ListView(
                    [ft.Text(f"Notification {i}") for i in range(1, 4)],
                    height=150,
                    spacing=5,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        visible=False
    )