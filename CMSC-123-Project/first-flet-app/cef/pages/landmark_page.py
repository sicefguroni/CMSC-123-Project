import flet as ft

def landmark_page():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Landmark Page!", size=20, weight=ft.FontWeight.BOLD),
                ft.Image(src="Pharmacy-Image-Sample.jpg", height=150, width=150),
                ft.ElevatedButton(
                    text="Explore Nearby Landmarks",
                    on_click=lambda e: e.page.snack_bar(ft.SnackBar(content=ft.Text("Exploration Started!"))),
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False
    )