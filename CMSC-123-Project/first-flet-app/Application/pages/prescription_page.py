import flet as ft
import datetime

class PrescriptionPage:
    def __init__(self, page: ft.Page):
        # Main page reference for global access if needed
        self.page = page

        # Create main prescription page container
        self.page_container = self._create_prescription_page()

        # Create add prescription page container
        self.add_prescription_container = self.create_add_prescription_page()

        # Current view tracking
        self.current_view = "prescription"

    def _create_prescription_page(self):

        page_container = ft.Container(
            expand=True,
            visible=True
        )

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

        def fab_click(e):
            self.toggle_view()

        # floating action button
        fab = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            tooltip="Add Prescription",
            bgcolor=ft.colors.LIGHT_BLUE,   
            on_click=fab_click
        )

        # search bar
        anchor = ft.SearchBar(
            width=400,
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text="Search prescriptions...",
            view_hint_text="Choose a prescription...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[
                ft.ListTile(title=ft.Text(f"Prescription {i}"), on_click=close_anchor, data=i)
                for i in range(10)
            ],
        )

        # Prescription List Creation
        def create_prescription_list():
            return ft.ListView(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.MEDICATION),
                                        title=ft.Text(f"Prescription {i+1}"),
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Intake Schedule: ", weight=ft.FontWeight.BOLD),
                                                ft.Text("Dispensing Quantity Limit: ", weight=ft.FontWeight.BOLD),
                                                ft.Text("Next Doctor's Appointment: ", weight=ft.FontWeight.BOLD),
                                                ft.Text("Doctor: ", weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=5,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                        ),
                                        padding=ft.padding.only(left=20),
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.icons.EDIT_OUTLINED,
                                                icon_color="blue50",
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE_OUTLINED,
                                                icon_color="blue50",
                                            ),
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
                expand=True
            )

        # Main content column
        main_content = ft.Column(
            controls=[
                ft.Container(
                    content=anchor,
                    margin=ft.margin.only(left=20, top=10, bottom=10)
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Recent Prescriptions", size=20, weight=ft.FontWeight.W_500),
                            create_prescription_list(),
                        ]
                    ),
                    margin=ft.margin.only(left=20, right=20, top=20),
                    expand=True,
                ),
                ft.Container(
                    content=fab,
                    alignment=ft.alignment.bottom_right,
                    padding=20,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        )

        page_container.content = main_content
        return page_container

    def create_add_prescription_page(self): 
        # medication name input
        medication_name = ft.TextField(
            label="Medication Name",
            width=400,
            border_radius=10,
        )

        # dosage input
        dosage = ft.TextField(
            label="Dosage",
            width=164,
            border_radius=10,
        )

        dosage_unit = ft.Dropdown(
            label="Dosage Unit",
            width=164,
            options=[
                ft.dropdown.Option("mg"),
                ft.dropdown.Option("ml"),
                ft.dropdown.Option("mcg"),
                ft.dropdown.Option("tablet"),
                ft.dropdown.Option("capsule"),
            ],
        )

        frequency = ft.TextField(
            label="Frequency",
            width=400,
            border_radius=10,
            hint_text="e.g., Once daily, Twice a day"
        )

        doctor_name = ft.TextField(
            label="Doctor's Name",
            width=400,
            border_radius=10,
        )   

        start_date = ft.TextField(
            label="Start Date",
            width=164,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        end_date = ft.TextField(
            label="End Date",
            width=164,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        quantity_limit = ft.TextField(
            label="Dispensing Quantity Limit",
            width=400, 
            border_radius=10,
            hint_text="HH:MM AM/PM"
        )

        def handle_save_prescription(e):
            # implement prescription saving logic
            print("Saving prescription...")
            print(f"Medication: {medication_name.value}")
            print(f"Dosage: {dosage.value} {dosage_unit.value}")
            print(f"Frequency: {frequency.value}")
            print(f"Start Date: {start_date.value}")
            print(f"End Date: {end_date.value}")

            # add your validation and saving logic here
            self.toggle_view()

        add_prescription_container = ft.Container(
            expand=True,
            visible=False,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.IconButton(icon=ft.icons.ARROW_BACK_OUTLINED, on_click=handle_save_prescription),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Text("Add New Prescription", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10), # spacer
                    medication_name,
                    ft.Row(
                        controls=[dosage, dosage_unit],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    frequency,
                    ft.Row(
                        controls=[start_date, end_date],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    quantity_limit,
                    doctor_name,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Save Prescription",
                        on_click=handle_save_prescription,
                        width=400,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )

        return add_prescription_container
    
    def toggle_view(self):
        # Toggle between prescription and add prescription views
        if self.current_view == "prescription":
            self.page_container.visible = False
            self.add_prescription_container.visible = True
            self.current_view = "add_prescription"
        else:
            self.page_container.visible = True
            self.add_prescription_container.visible = False
            self.current_view = "prescription"
        
        # Trigger page update
        if self.page:
            self.page.update()
    
    def get_pages(self):
        # Return both page containers for use in main app
        return [self.page_container, self.add_prescription_container]

