import flet as ft

def prescription_page():
    def close_anchor(e):
        text = f"Color {e.control.data}"
        print(f"closing view from {text}")
        anchor.close_view(text)
    
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")
        anchor.open_view()

    anchor = ft.SearchBar(
        width=400,
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    content = ft.Column(
        controls=[
            ft.Container(
                margin=ft.margin.only(left=20, top=10, bottom=20)
            ),
            ft.Container(
                content=anchor,
                margin=ft.margin.only(left=20, right=20)
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Recent Prescriptions", size=20, weight=ft.FontWeight.W_500),
                        ft.ListView(
                            controls=[
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.ListTile(
                                                    leading=ft.Icon(ft.icons.MEDICATION),
                                                    title=ft.Text(f"Prescription {i+1}"),
                                                    subtitle=ft.Text("Details about the prescription"),
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.TextButton("View Details"),
                                                        ft.TextButton("Refill"),
                                                    ],
                                                    alignment=ft.MainAxisAlignment.END,
                                                ),
                                            ],
                                        ),
                                        padding=10,
                                    )
                                )
                                for i in range(3)
                            ],
                            spacing=10,
                            height=300,
                            expand=True,
                        ),
                    ]
                ),
                margin=ft.margin.only(left=20, right=20, top=20),
                expand=True,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )
    
    return ft.Container(
        content=content,
        expand=True,
        visible=True
    )