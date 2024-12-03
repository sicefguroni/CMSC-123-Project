import flet as ft
from prescription_backend import PrescriptionManager

class PrescriptionPage:
    def __init__(self, page: ft.Page):
        # Main page reference for global access if needed
        self.page = page

        # Initialize Prescription
        self.prescription_manager = PrescriptionManager()

        # Create main prescription page container
        self.page_container = self._create_prescription_page()

        # Create add prescription page container
        self.add_prescription_container = self.create_add_prescription_page()

        # Current view tracking
        self.current_view = "prescription"

        self.prescription_list_view = None

    def _create_prescription_page(self):

        page_container = ft.Container(
            expand=True,
            visible=True
        )

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
            bar_hint_text="Search prescriptions...",
            divider_color=ft.colors.AMBER,
        )

        # Prescription List Creation
        def create_prescription_list():
            self.prescription_list_view = ft.ListView(
                controls=self._create_prescription_cards(), # Use new method to populate list
                spacing=10,
                height=300,
                expand=True
            )
            return self.prescription_list_view

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
        self.medication_name = ft.TextField(
            label="Medication Name",
            width=400,
            border_radius=10,
        )

        # dosage input
        self.dosage = ft.TextField(
            label="Dosage",
            width=164,
            border_radius=10,
        )

        self.dosage_unit = ft.Dropdown(
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

        self.frequency = ft.TextField(
            label="Frequency",
            width=400,
            border_radius=10,
            hint_text="e.g., Once daily, Twice a day"
        )

        self.doctor_name = ft.TextField(
            label="Doctor's Name",
            width=400,
            border_radius=10,
        )   

        self.start_date = ft.TextField(
            label="Start Date",
            width=164,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        self.end_date = ft.TextField(
            label="End Date",
            width=164,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        self.quantity_limit = ft.TextField(
            label="Dispensing Quantity Limit",
            width=400, 
            border_radius=10,
            hint_text="Quantity"
        )

        def handle_save_prescription(e):
            # Collect prescription data
            prescription = {
                "medication": self.medication_name.value,
                "dosage": f"{self.dosage.value} {self.dosage_unit.value}",
                "frequency": self.frequency.value,
                "doctor": self.doctor_name.value,
                "start_date": self.start_date.value,
                "end_date": self.end_date.value,
                "quantity_limit": self.quantity_limit.value,
            }

            # Use prescription manager to save
            if self.prescription_manager.add_prescription(prescription):
                # Update prescription list
                self._update_prescription_list()

                # Clear input fields
                self._clear_prescription_inputs()

                # Toggle view
                self.toggle_view()
            else:
                # TODO: Add error handling (e.g., show error message)
                print("Failed to add prescription")

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
                    self.medication_name,
                    ft.Row(
                        controls=[self.dosage, self.dosage_unit],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.frequency,
                    ft.Row(
                        controls=[self.start_date, self.end_date],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.quantity_limit,
                    self.doctor_name,
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
    
    def _create_prescription_cards(self):
        """
        Create prescription cards from stored prescriptions
        """
        prescription_cards = []
        for prescription in self.prescription_manager.get_all_prescriptions():
            prescription_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.MEDICATION),
                                title=ft.Text(prescription["medication"]),
                                ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(f"Dosage: {prescription.get('dosage', 'N/A')}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Frequency: {prescription.get('frequency', 'N/A')}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Doctor: {prescription.get('doctor', 'N/A')}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Start Date: {prescription.get('start_date', 'N/A')}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"End Date: {prescription.get('end_date', 'N/A')}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Quantity Limit: {prescription.get('quantity_limit', 'N/A')}", weight=ft.FontWeight.BOLD),
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
                                        # TODO: Implement edit functionality
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_OUTLINED,
                                        icon_color="blue50",
                                        # TODO: Implement delete functionality
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                    ),
                    padding=10,
                )
            )
            prescription_cards.append(prescription_card)
        return prescription_cards

    def _update_prescription_list(self):
        """
        Update the prescription list view with current prescriptions
        """
        if self.prescription_list_view:
            # Clear existing controls
            self.prescription_list_view.controls.clear()

            # Add new prescription cards
            self.prescription_list_view.controls.extend(self._create_prescription_cards())

            # Update the page
            if self.page:
                self.page.update()

    def _clear_prescription_inputs(self):
        """
        Clear all input fields
        """
        self.medication_name.value = ""
        self.dosage.value = ""
        self.dosage_unit.value = None
        self.frequency.value = ""
        self.doctor_name.value = ""
        self.start_date.value = ""
        self.end_date.value = ""
        self.quantity_limit.value = ""

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

