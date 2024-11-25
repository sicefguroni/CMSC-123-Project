import flet as ft

def inventory_page(): 
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to Inventory Page!", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                text="Add New Item",
                on_click=lambda e: e.page.snack_bar(ft.SnackBar(content=ft.Text("New Item Added!"))),
                ),
            ],
        ),
        visible=False
    )