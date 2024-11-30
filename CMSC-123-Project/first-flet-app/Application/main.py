import flet as ft
from pages.prescription_page import PrescriptionPage
from pages.landmark_page import landmark_page
from pages.reminder_page import reminder_page
from pages.inventory_page import inventory_page

def main(page: ft.Page):
    # Set up the page
    page.window_width = 414
    page.window_height = 736
    page.title = "Medion"
    
    selected_icon = "Prescription"  # default landing page

    # Create prescription module
    prescription_module = PrescriptionPage(page)
    prescription_pages = prescription_module.get_pages()

    # Load other pages
    landmark = landmark_page()
    reminder = reminder_page()
    inventory = inventory_page()

    # Create default app bar 
    page.appbar = ft.AppBar(
        leading=ft.Image(src="Medion-Logo.png", width=32, height=32),
        leading_width=50,
        title=ft.Text("Medion"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(ft.icons.HELP, tooltip=f"Help for Medion")
        ],
    )

    # Function to handle navigation
    def on_navigation_click(e):
        nonlocal selected_icon  
        # Update the selected icon
        selected_icon = e.control.data  # Update the selected icon string

        page.appbar = ft.AppBar(
            leading=ft.Image(src="Medion-Logo.png", width=32, height=32),
            leading_width=50,
            title=ft.Text(f"Medion: {selected_icon}"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.HELP, tooltip=f"Help for {selected_icon}")
            ],
        )
        # update visible content
        update_page_content(selected_icon)
        page.update()  # Refresh the UI

    def create_custom_icon(default_icon, selected_icon_path, tooltip, data):
        container = ft.Container(
            content=ft.Image(
                src=default_icon,
                width=24,
                height=24,
            ),
            tooltip=tooltip,
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(5),
            bgcolor=ft.colors.TRANSPARENT,
            ink=True,
            data=data,
            on_click=on_navigation_click,
        )

        def on_hover(e):
            is_hovered = e.data == "true"
            # Update image source based on hover and selection state
            if selected_icon == data:
                container.content.src = selected_icon_path
            else:
                container.content.src = selected_icon_path if is_hovered else default_icon
            # update background color
            container.bgcolor = (
                ft.colors.BLUE_50 if selected_icon == data
                else ft.colors.BLUE_50 if is_hovered
                else ft.colors.TRANSPARENT
            )
            container.update()

        container.on_hover = on_hover
        return container
    
    def update_page_content(destination):
        # Update visibility for all pages
        prescription_pages[0].visible = destination == "Prescription"
        prescription_pages[1].visible = destination == "Prescription" and prescription_module.current_view == "add_prescription"
        landmark.visible = destination == "Landmark"
        reminder.visible = destination == "Reminder"
        inventory.visible = destination == "Inventory"

        # update all icons' appearances
        for icon in navigation_row.controls:
            if icon.data == destination:
                icon.bgcolor = ft.colors.LIGHT_BLUE
                icon.content.src = f"{icon.data}-Selected.png"
            else:
                icon.bgcolor = ft.colors.TRANSPARENT
                icon.content.src = f"{icon.data}-Default.png"
            icon.update()

    # Create navigation row
    navigation_row = ft.Row(
        [
            create_custom_icon("Prescription-Default.png", "Prescription-Selected.png", "Prescription", "Prescription"),
            create_custom_icon("Landmark-Default.png", "Landmark-Selected.png", "Landmark", "Landmark"),
            create_custom_icon("Reminder-Default.png", "Reminder-Selected.png", "Reminder", "Reminder"),
            create_custom_icon("Inventory-Default.png", "Inventory-Selected.png", "Inventory", "Inventory"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    top_navigation = ft.Container(
        content=navigation_row,
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=ft.padding.only(top=5, bottom=5),
    )

    content_area = ft.Container(
        content=ft.Stack(prescription_pages + [landmark, reminder, inventory]),
        expand=True,
        padding=ft.padding.only(top=10),
    )

    main_column = ft.Column(
        [
            top_navigation,
            content_area
        ],
        spacing=0,
        expand=True,
    )

    # Add the top navigation bar and body content to the page
    page.add(main_column)

ft.app(
    main,
    assets_dir="assets"  # Ensure this directory contains all icons
)
