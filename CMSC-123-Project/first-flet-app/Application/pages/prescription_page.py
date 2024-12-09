import flet as ft
from prescription_backend import PrescriptionManager

class PrescriptionPage:
    def __init__(self, page: ft.Page):
        # Main page reference for global access if needed
        self.page = page

        # Initialize Prescription
        self.prescription_manager = PrescriptionManager()

        # Create prescription list view first
        self.prescription_list_view = self._create_prescription_list()

        # Create main prescription page container
        self.page_container = self._create_prescription_page()

        # Create add prescription page container
        self.add_prescription_container = self.create_add_prescription_page()

        # Create edit prescription page container
        self.edit_prescription_container = self.create_edit_prescription_page()

        # Current view tracking
        self.current_view = "prescription"

        self.current_edit_prescription = None

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
            width=173,
            border_radius=10,
        )

        self.dosage_unit = ft.Dropdown(
            label="Dosage Unit",
            width=173,
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
            width=173,
            border_radius=10,
            hint_text="e.g., Once daily",
        )

        self.time_interval = ft.TextField(
            label="Time Interval",
            width=173,
            border_radius=10,
            hint_text="e.g., 6 hours",
        )

        self.doctor_name = ft.TextField(
            label="Doctor's Name",
            width=400,
            border_radius=10,
        )   

        self.start_date = ft.TextField(
            label="Start Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY",
        )   

        self.end_date = ft.TextField(
            label="End Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY",
        )   

        self.appointment_date= ft.TextField(
            label="Appointment Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY",
        )

        self.appointment_time= ft.TextField(
            label="Appointment Time",
            width=173,
            border_radius=10,
            hint_text="HH:MM",
        )

        self.quantity_limit = ft.TextField(
            label="Dispensing Quantity Limit",
            width=400, 
            border_radius=10,
        )

        def handle_save_prescription(e):
            # Fields to validate
            fields_to_validate = [
                self.medication_name,
                self.dosage,
                self.dosage_unit,
                self.frequency,
                self.time_interval,
                self.doctor_name,
                self.start_date,
                self.end_date,
                self.appointment_date,
                self.appointment_time,
                self.quantity_limit,
            ]

            # Validate fields
            if self._validate_fields(fields_to_validate):
                prescription = {
                    "medication": self.medication_name.value,
                    "dosage": f"{self.dosage.value} {self.dosage_unit.value}",
                    "frequency": self.frequency.value,
                    "time_interval": self.time_interval.value,
                    "doctor": self.doctor_name.value,
                    "start_date": self.start_date.value,
                    "end_date": self.end_date.value,
                    "appointment_date": self.appointment_date.value,
                    "appointment_time": self.appointment_time.value,
                    "quantity_limit": self.quantity_limit.value,
                }

                dlg_add = ft.AlertDialog(
                    content=ft.Text("Added prescription successfully!"),
                    on_dismiss=lambda e: None,
                )

                # Use prescription manager to save
                if self.prescription_manager.add_prescription(prescription):
                    # Update prescription list
                    self._update_prescription_list()

                    # Clear input fields
                    self._clear_prescription_inputs()

                    # Show success dialog
                    self.page.dialog = dlg_add
                    dlg_add.open = True 
                    self.page.update()

                    # Toggle view
                    self.toggle_view()
                else:
                    # TODO: Add error handling (e.g., show error message)
                    print("Failed to add prescription")
            else:
                # Trigger UI to update error messages
                self.page.update()

        def handle_back_add(e):
            # Simply toggle back to prescription view
            self._clear_prescription_inputs()
            self.toggle_view()

        add_prescription_container = ft.Container(
            expand=True,
            visible=False,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.IconButton(icon=ft.icons.ARROW_BACK_OUTLINED, on_click=handle_back_add),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Text("Add New Prescription", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=5), # spacer
                    self.medication_name,
                    ft.Row(
                        controls=[self.dosage, self.dosage_unit],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[self.frequency, self.time_interval],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[self.start_date, self.end_date],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.quantity_limit,
                    self.doctor_name,
                    ft.Row(
                        controls=[self.appointment_date, self.appointment_time],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=15),
                    ft.ElevatedButton(
                        "Save Prescription",
                        on_click=handle_save_prescription,
                        width=400,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
            alignment=ft.alignment.center,
        )

        return add_prescription_container

    def create_edit_prescription_page(self):
        # Similar to add_prescription_page, but with pre-filled values
        self.edit_medication_name = ft.TextField(
            label="Medication Name",
            width=400,
            border_radius=10
        )

        # dosage input
        self.edit_dosage = ft.TextField(
            label="Dosage",
            width=173,
            border_radius=10
        )

        self.edit_dosage_unit = ft.Dropdown(
            label="Dosage Unit",
            width=173,
            options=[
                ft.dropdown.Option("mg"),
                ft.dropdown.Option("ml"),
                ft.dropdown.Option("mcg"),
                ft.dropdown.Option("tablet"),
                ft.dropdown.Option("capsule"),
            ],
        )

        self.edit_frequency = ft.TextField(
            label="Frequency",
            width=173,
            border_radius=10,
            hint_text="e.g., 1/day, 2/week"
        )

        self.edit_time_interval = ft.TextField(
            label="Time Interval",
            width=173,
            border_radius=10,
            hint_text="e.g., 6 hours"
        )

        self.edit_doctor_name = ft.TextField(
            label="Doctor's Name",
            width=400,
            border_radius=10
        )   

        self.edit_start_date = ft.TextField(
            label="Start Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        self.edit_end_date = ft.TextField(
            label="End Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )   

        self.edit_appointment_date = ft.TextField(
            label="Appointment Date",
            width=173,
            border_radius=10,
            hint_text="MM/DD/YYYY"
        )

        self.edit_appointment_time = ft.TextField(
            label="Appointment Time",
            width=173,
            border_radius=10,
            hint_text="HH:MM"
        )

        self.edit_quantity_limit = ft.TextField(
            label="Dispensing Quantity Limit",
            width=400, 
            border_radius=10,
        )

        def handle_save_edit(e):
            # Fields to validate
            fields_to_validate = [
                self.edit_medication_name,
                self.edit_dosage,
                self.edit_dosage_unit,
                self.edit_frequency,
                self.edit_time_interval,
                self.edit_doctor_name,
                self.edit_start_date,
                self.edit_end_date,
                self.edit_appointment_date,
                self.edit_appointment_time,
                self.edit_quantity_limit
            ]

            dlg_edit = ft.AlertDialog(
                content=ft.Text("Updated prescription successfully!"),
                on_dismiss=lambda e: None,
            )

            # Validate fields
            if self._validate_fields(fields_to_validate):
                updated_prescription = {
                    "medication": self.edit_medication_name.value,
                    "dosage": f"{self.edit_dosage.value} {self.edit_dosage_unit.value}",
                    "frequency": self.edit_frequency.value,
                    "time_interval": self.edit_time_interval.value,
                    "doctor": self.edit_doctor_name.value,
                    "start_date": self.edit_start_date.value,
                    "end_date": self.edit_end_date.value,
                    "appointment_date": self.edit_appointment_date.value,
                    "appointment_time": self.edit_appointment_time.value,
                    "quantity_limit": self.edit_quantity_limit.value,
                }

                # Use prescription manager to update
                if self.current_edit_prescription and self.prescription_manager.update_prescription(
                    self.current_edit_prescription['id'], 
                    updated_prescription
                    ):
                    # Update prescription list
                    self._update_prescription_list()

                    # Clear input fields
                    self._clear_edit_inputs()

                    # Show success dialog
                    self.page.dialog = dlg_edit
                    dlg_edit.open = True
                    self.page.update()

                    # Toggle view
                    self.toggle_view()
                else:
                    # TODO: Add error handling (e.g., show error message)
                    print("Failed to update prescription")
            else:
                self.page.update()

        def handle_back_edit(e):
            #Simply toggle back to prescription view
            self._clear_edit_inputs()
            self.current_edit_prescription = None
            self.toggle_view()

        edit_prescription_container = ft.Container(
            expand=True,
            visible=False,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.IconButton(icon=ft.icons.ARROW_BACK_OUTLINED, on_click=handle_back_edit),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Text("Edit Prescription", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=5), # spacer
                    self.edit_medication_name,
                    ft.Row(
                        controls=[self.edit_dosage, self.edit_dosage_unit],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[self.edit_frequency, self.edit_time_interval],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[self.edit_start_date, self.edit_end_date],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.edit_quantity_limit,
                    self.edit_doctor_name,
                    ft.Row(
                        controls=[self.edit_appointment_date, self.edit_appointment_time],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=15),
                    ft.ElevatedButton(
                        "Save Changes",
                        on_click=handle_save_edit,
                        width=400,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
            alignment=ft.alignment.center,
        )

        return edit_prescription_container

    def _create_prescription_cards(self, search_term=''):
            """
            Create prescription cards from stored prescriptions
            Supports filtering by search term
            """
            prescription_cards = []

            # Get all prescriptions from the manager
            all_prescriptions = self.prescription_manager.get_all_prescriptions()

            # Filter prescriptions based on search term
            filtered_prescriptions = [
                prescription for prescription in self.prescription_manager.get_all_prescriptions()
                if not search_term or search_term.lower() in prescription.get('medication', '').lower()
            ]

            # Debugger
            print(f"Total prescriptions: {len(all_prescriptions)}")
            print(f"Filtered prescriptions: {len(filtered_prescriptions)}")

            for prescription in filtered_prescriptions:
                def create_details_dialog(p):
                    def show_details(e):
                        def handle_dialog_action(action):
                            def _action(e):
                                if action == 'close':
                                    self.page.dialog.open = False
                                elif action == 'edit':
                                    self.page.dialog.open = False
                                    self.start_edit_prescription(p)
                                self.page.update()
                            return _action

                        dlg = ft.AlertDialog(
                            icon=ft.Icon(name=ft.icons.MEDICATION, size=30),
                            title=ft.Text(p["medication"], weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                            content=ft.Container(
                                ft.Column(
                                    controls=[
                                        ft.Text(f"Dosage: {p.get('dosage', 'N/A')}", size=17),
                                        ft.Text(f"Frequency: {p.get('frequency', 'N/A')}", size=17),
                                        ft.Text(f"Time Interval: {p.get('time_interval', 'N/A')}", size=17),
                                        ft.Text(f"Doctor: {p.get('doctor', 'N/A')}", size=17),
                                        ft.Text(f"Next Appointment: {p.get('appointment_date', 'N/A')} - {p.get('appointment_time', 'N/A')}", size=17),
                                        ft.Text(f"Start Date: {p.get('start_date', 'N/A')}", size=17),
                                        ft.Text(f"End Date: {p.get('end_date', 'N/A')}", size=17),
                                        ft.Text(f"Quantity Limit: {p.get('quantity_limit', 'N/A')}", size=17),
                                    ],
                                    spacing=25,
                                ),
                                width=350,
                                height=330,
                            ),
                            actions=[
                                ft.TextButton("Close", on_click=handle_dialog_action('close')),
                                ft.TextButton("Edit", on_click=handle_dialog_action('edit')),
                            ],
                        )
                        self.page.dialog = dlg
                        dlg.open = True
                        self.page.update()
                    return show_details

                prescription_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICATION),
                                    title=ft.Text(prescription["medication"]),
                                    subtitle=ft.Text(f"Dosage: {prescription.get('dosage', 'N/A')}"),
                                ),
                                ft.ListTile(
                                    leading=ft.IconButton(
                                        icon=ft.icons.EDIT_OUTLINED,
                                        icon_color="black",
                                        on_click=lambda e, p=prescription: self.start_edit_prescription(p)
                                    ),
                                    trailing=ft.IconButton(
                                        icon=ft.icons.DELETE_OUTLINED,
                                        icon_color="black",
                                        on_click=lambda e, p=prescription: self.delete_prescription(p)
                                    ),
                                ),
                            ],
                        ),
                        padding=10,
                        on_click=create_details_dialog(prescription)
                    ),
                    elevation=2,
                    width=350
                )
                prescription_cards.append(prescription_card)
            return prescription_cards
    
    def start_edit_prescription(self, prescription):
        """
        Prepare edit form with existing prescription details
        """
        # Store current prescription being edited
        self.current_edit_prescription = prescription

        # Pre-fill edit fields
        dosage, unit = prescription.get('dosage', ' ').split(' ', 1)
        self.edit_medication_name.value = prescription.get('medication', '')
        self.edit_dosage.value = dosage
        self.edit_dosage_unit.value = unit
        self.edit_frequency.value = prescription.get('frequency', '')
        self.edit_time_interval.value = prescription.get('time_interval', '')
        self.edit_doctor_name.value = prescription.get('doctor', '')
        self.edit_appointment_date.value = prescription.get('appointment_date', '')
        self.edit_appointment_time.value = prescription.get('appointment_time', '')
        self.edit_start_date.value = prescription.get('start_date', '')
        self.edit_end_date.value = prescription.get('end_date', '')
        self.edit_quantity_limit.value = prescription.get('quantity_limit', '')

        # Toggle to edit view
        self.page_container.visible = False
        self.add_prescription_container.visible = False
        self.edit_prescription_container.visible = True
        self.current_view = "edit_prescription"
        
        # Trigger page update
        if self.page:
            self.page.update()

    def delete_prescription(self, prescription):
        """
        Delete a prescription
        """
        # Use prescription manager to delete
        if self.prescription_manager.delete_prescription(prescription['id']):
            # Update prescription list
            self._update_prescription_list()
        else:
            # TODO: Add error handling
            print("Failed to delete prescription")

    def _clear_edit_inputs(self):
        """
        Clear all edit input fields
        """
        self.edit_medication_name.value = ""
        self.edit_dosage.value = ""
        self.edit_dosage_unit.value = None
        self.edit_frequency.value = ""
        self.edit_time_interval.value = ""
        self.edit_doctor_name.value = ""
        self.edit_appointment_date.value = ""
        self.edit_appointment_time.value = ""
        self.edit_start_date.value = ""
        self.edit_end_date.value = ""
        self.edit_quantity_limit.value = ""
    
    def _validate_fields(self, fields):
        """
        Validate a list of fields and update their error_text if invalid.
        Returns True if all fields are valid, otherwise False.
        """
        is_valid = True
        for field in fields:
            if isinstance(field, ft.TextField) and not field.value.strip():
                field.error_text = f"{field.label} is required"
                is_valid = False
            elif isinstance(field, ft.Dropdown) and not field.value:
                field.error_text = f"{field.label} is required"
                is_valid = False
            else:
                field.error_text = None
        return is_valid

    def _create_prescription_list(self):
        """
        Create prescription list view from stored prescriptions
        """
        # Explicitly get all prescriptions from the manager
        prescriptions = self.prescription_manager.get_all_prescriptions()

        # Create list view with prescription cards
        prescription_list_view = ft.ListView(
            controls=self._create_prescription_cards(),
            spacing=10,
            height=300,
            expand=True
        )
        return prescription_list_view

    def _create_prescription_page(self):
        """
        Modify the prescription page to include search functionality
        """
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

        # search bar with functionality
        def on_search_change(e):
            # Update prescription list based on search term
            search_term = anchor.value
            self.prescription_list_view.controls.clear()
            self.prescription_list_view.controls.extend(self._create_prescription_cards(search_term))
            self.page.update()

        # search bar
        anchor = ft.SearchBar(
            width=360,
            view_elevation=4,
            bar_hint_text="Search Prescriptions",
            divider_color=ft.colors.AMBER,
            on_change=on_search_change
        )

        self.prescription_list_view = ft.ListView(
            controls=self._create_prescription_cards(),
            spacing=10,
            expand=True
        )

        # Scrollable results
        results_container = ft.Container(
            content=self.prescription_list_view,  # Directly use the ListView
            padding=10,
            expand=True
        )

        # Main container
        prescription_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            anchor,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10
                    ),
                    results_container
                ],
                spacing=0,
                expand=True
            ),
            expand=True,
        )

        fab_container = ft.Container(
            content=fab,
            alignment=ft.alignment.bottom_right,
            right=20,
            bottom=20,
            padding=10
        )

        # Overlay FAB
        page_container.content = ft.Stack(
            controls=[
                prescription_container,
                fab_container
            ],
            expand=True
        )

        return page_container

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
        self.time_interval.value = ""
        self.doctor_name.value = ""
        self.appointment_date.value = ""
        self.appointment_time.value = ""
        self.start_date.value = ""
        self.end_date.value = ""
        self.quantity_limit.value = ""

    def toggle_view(self):
        # Toggle between prescription and add prescription views
        if self.current_view == "prescription":
            self.page_container.visible = False
            self.add_prescription_container.visible = True
            self.current_view = "add_prescription"
        elif self.current_view == "add_prescription":
            self.page_container.visible = True
            self.add_prescription_container.visible = False
            self.current_view = "prescription"
        elif self.current_view == "edit_prescription":
            self.page_container.visible = True
            self.edit_prescription_container.visible = False
            self.current_view = "prescription"
        
        # Trigger page update
        if self.page:
            self.page.update()
    
    def get_pages(self):
        # Return both page containers for use in main app
        return [self.page_container, 
                self.add_prescription_container,
                self.edit_prescription_container
        ]   