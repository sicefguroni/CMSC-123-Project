import flet as ft

def create_add_prescription_page(toggle_view_callback=None):
    # medication name input
    medication_name = ft.TextField(
        label="Medication Name",
        width=400,
        border_radius=10,
    )

    # dosage input
    dosage = ft.TextField(
        label="Dosage",
        width=400,
        border_radius=10,
    )

    dosage_unit = ft.Dropdown(
        label="Dosage Unit",
        width=400,
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

    # start date picker
    start_date = ft.TextField(
        label="Start Date",
        width=190,
        read_only=True,
    )

    # end date picker
    end_date = ft.TextField(
        label="End Date",
        width=190,
        read_only=True,
    )

    # Date Pickers
    def format_date(d):
        return d.strftime("%Y-%m-%d") if d else ""

    start_date_picker = ft.DatePicker(
        on_change=lambda e: setattr(start_date, 'value', format_date(e.control.value))
    )

    end_date_picker = ft.DatePicker(
        on_change=lambda e: setattr(end_date, 'value', format_date(e.control.value))
    )

    def pick_start_date(e):
        start_date_picker.show()

    def pick_end_date(e):
        end_date_picker.show()

    start_date.on_focus = pick_start_date
    end_date.on_focus = pick_end_date

    def handle_save_prescription(e):
        # implement prescription saving logic
        print("Saving prescription...")
        print(f"Medication: {medication_name.value}")
        print(f"Dosage: {dosage.value} {dosage_unit.value}")
        print(f"Frequency: {frequency.value}")
        print(f"Start Date: {start_date.value}")
        print(f"End Date: {end_date.value}")

        # add your validation and saving logic here
        if toggle_view_callback:
            toggle_view_callback()

    add_prescription_container = ft.Container(
        expand=True,
        visible=False,
        content=ft.Column(
            controls=[
                ft.Text("Add New Prescription", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=20), # spacer
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
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Save Prescription",
                    on_click=handle_save_prescription,
                    width=400,
                ),
                # add date pickers to the control
                start_date_picker,
                end_date_picker 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=20,
        alignment=ft.alignment.center,
    )

    return add_prescription_container

def prescription_page(toggle_view_callback=None):
    #Main container for the prescription page
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

    # floating action button
    fab = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        tooltip="Add Prescription",
        on_click=lambda e: toggle_view_callback() if toggle_view_callback else None,
        bgcolor=ft.colors.LIGHT_BLUE,   
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