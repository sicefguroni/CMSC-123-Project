import flet as ft
from pages.prescription_page import PrescriptionPage
from pages.pharmacy_finder_page import pharmacy_finder_page
from pages.reminder_page import Reminder_Page # <ISA NEW>
from pages.inventory_page import inventory_page

##---------------------------------------------------------------------------------------------------##
#   Note to CEF:
#       Yo, click CTRL + F and type for "ISA NEW". Kana lang i-add sa very very main file XD
##---------------------------------------------------------------------------------------------------##


def main(page: ft.Page):
    # Set up the page  
    page.window_width = 414
    page.window_height = 736
    page.title = "Medion"

    selected_icon = "Prescription"

    # Create prescription module
    prescription_module = PrescriptionPage(page)
    prescription_pages = prescription_module.get_pages()

    # Load other pages
    pharmacy_finder = pharmacy_finder_page(page)
    reminder_instance = Reminder_Page(page)  # Create an instance of Reminder_Page <ISA NEW>
    reminder = reminder_instance.page_container  # Access its container <ISA NEW>
    inventory = inventory_page()

    # Create default app bar 
    page.appbar = ft.AppBar(
        leading=ft.Image(src="Medion-Logo.png", width=200, height=100),
        leading_width=50,
        title=ft.Text("Medion: Prescription", weight=ft.FontWeight.BOLD, size=20),
        title_spacing=0.0,
        center_title=False,
        actions=[
                ft.IconButton(ft.icons.HELP, tooltip=f"Help for Medion")
        ],
        toolbar_height=50,
    )

    # Function to handle navigation
    def on_navigation_click(e):
        nonlocal selected_icon  
        # Update the selected icon
        selected_icon = e.control.data  # Update the selected icon string

        page.appbar = ft.AppBar(
            leading=ft.Image(src=f"Medion-Logo.png", width=200, height=100),
            leading_width=50,
            title=ft.Text(f"Medion: {selected_icon}", weight=ft.FontWeight.BOLD, size=20),
            title_spacing=0.0,
            center_title=False,
            actions=[
                ft.IconButton(ft.icons.HELP, tooltip=f"Help for {selected_icon}")
            ],
            toolbar_height=50,
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
               # Reset prescription module views when leaving Prescription page
        if destination != "Presciption":
            # if current view is not already prescription, reset to prescription view
            if prescription_module.current_view != "prescription":
                prescription_module.current_view = "prescription"
                prescription_module.page_container.visible = True
                prescription_module.add_prescription_container.visible = False
                prescription_module.edit_prescription_container.visible = False

        # Ensure safe access to prescription pages
        if len(prescription_pages) >= 3:
            prescription_pages[0].visible = destination == "Prescription"
            prescription_pages[1].visible = destination == "Prescription" and prescription_module.current_view == "add_prescription"
            prescription_pages[2].visible = destination == "Prescription" and prescription_module.current_view == "edit_prescription"

        # Update visibility for all pages
        prescription_pages[0].visible = destination == "Prescription"
        prescription_pages[1].visible = destination == "Prescription" and prescription_module.current_view == "add_prescription"
        pharmacy_finder.visible = destination == "Pharmacy Finder"
        reminder.visible = destination == "Reminder"
        inventory.visible = destination == "Inventory"

        # Automatically show medicine intake reminders when navigating to the reminder page <ISA NEW>
        if destination == "Reminder":
            reminder_instance._show_view("Medicine Intake")

        # update all icons' appearances
        for icon in navigation_row.controls:
            if icon.data == destination:
                icon.bgcolor = ft.colors.BLUE_50
                icon.content.src = f"{icon.data}-Selected.png"
            else:
                icon.bgcolor = ft.colors.TRANSPARENT
                icon.content.src = f"{icon.data}-Default.png"
            icon.update()

    # Create navigation row
    navigation_row = ft.Row(
        [
            create_custom_icon("Prescription-Default.png", "Prescription-Selected.png", "Prescription", "Prescription"),
            create_custom_icon("Pharmacy Finder-Default.png", "Pharmacy Finder-Selected.png", "Pharmacy Finder", "Pharmacy Finder"),
            create_custom_icon("Reminder-Default.png", "Reminder-Selected.png", "Reminder", "Reminder"),
            create_custom_icon("Inventory-Default.png", "Inventory-Selected.png", "Inventory", "Inventory"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    top_navigation = ft.Container(
        content=navigation_row,
        padding=ft.padding.only(top=3, bottom=3),
    )

    content_area = ft.Container(
        content=ft.Stack(prescription_pages + [pharmacy_finder, reminder, inventory]),
        expand=True,
      
    )

    main_column = ft.Column(
        [
            ft.Divider(height=2, thickness=1),
            top_navigation,
            ft.Divider(height=2, thickness=1),
            content_area
        ],
        spacing=0,
        expand=True,
    )

    # Add the top navigation bar and body content to the page
    page.add(main_column)

    update_page_content(selected_icon)

ft.app(
    main,
    assets_dir="assets"  # Ensure this directory contains all icons
)