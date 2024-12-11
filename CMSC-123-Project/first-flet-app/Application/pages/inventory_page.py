import flet as ft
from inventory_backend import MedicationInventory

########### TABLET MEDICATION INVENTORY ########

def inventory_page():
    inventory_backend = MedicationInventory()

    inventory = inventory_backend.get_tablet_inventory()
    fluid_inventory = inventory_backend.get_fluid_inventory()

    inventory_list = ft.Column(
        controls=[],
        visible=True
    )

    fluid_inventory_list = ft.Column(
        controls=[],
        visible=True
    )

    def add_item(e):
        nonlocal inventory
        try:
            name = tablet_name_input.value.strip()
            dosage = tablet_dosage_input.value.strip()
            stock = tablet_stock_input.value.strip()
        
            tablet_name_input.update()
            tablet_dosage_input.update()
            tablet_stock_input.update()
                
            inventory_backend.add_tablet_medication(name, int(dosage), int(stock))

            inventory = inventory_backend.get_tablet_inventory()

            tablet_name_input.value = ""
            tablet_dosage_input.value = ""
            tablet_stock_input.value = ""
            tablet_name_input.update()
            tablet_dosage_input.update()
            tablet_stock_input.update()
            update_inventory_list()
            add_tablet_dialog.open = False
            e.page.update()

            dlg_add = ft.AlertDialog(
                    content=ft.Text("Tablet medication added successfully!"),
                    on_dismiss=lambda e: None,
                )
            e.page.overlay.append(dlg_add)
            dlg_add.open = True
            e.page.update()

        except ValueError as ve:
            print(f"Error adding item: {ve}")
            error_snack = ft.SnackBar(content=ft.Text("Invalid input! Please enter valid data."))
            e.page.overlay.append(error_snack)
            error_snack.open = True
            e.page.update()

    def update_inventory_list():
        inventory_list.controls.clear()
        for idx, item in enumerate(inventory):
            inventory_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                # Medication details at the top
                                        ft.Text(f"{item['name']} - {item['dosage']}mg", weight=ft.FontWeight.BOLD, size=16),
                                        ft.Text(f"Stock: {item['stock']}", color=ft.colors.ON_SURFACE_VARIANT, size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                # Buttons row at the bottom
                                ft.Row(
                                    [
                                        # Left side: Stock adjustment buttons
                                        ft.Row(
                                            [
                                                ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    tooltip="Increase Stock",
                                                    on_click=lambda e, idx=idx: adjust_stock(idx, 1, e.page),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.REMOVE,
                                                    tooltip="Decrease Stock",
                                                    on_click=lambda e, idx=idx: adjust_stock(idx, -1, e.page),
                                                ),
                                            ]
                                        ),
                                        
                                        # Right side: Delete button
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Delete Medication",
                                            on_click=lambda e, idx=idx: confirm_delete_item(e, idx),
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                )
                            ],
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                    ),
                    elevation=2,
                )
            )
        inventory_list.visible = len(inventory) > 0

    def adjust_stock(idx, amount, page):
        nonlocal inventory
        try:    
            med = inventory[idx]

            inventory_backend.update_tablet_stock(med['name'], med['dosage'], amount)

            
            inventory = inventory_backend.get_tablet_inventory()

            update_inventory_list()
            snack = ft.SnackBar(content=ft.Text(f"Stock updated for {med['name']}"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except IndexError as ie:
            print(f"Error adjusting stock: {ie}")

    def confirm_delete_item(e, idx):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this medication?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(e, confirm_dialog)),
                ft.TextButton(
                    "Delete",
                    on_click=lambda e, idx=idx: delete_item(e, idx, confirm_dialog),
                ),
            ],
            modal=True,
        )
        e.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        e.page.update()

    def close_dialog(e, dialog):
        dialog.open = False
        e.page.update()

    def delete_item(e, idx, dialog):
        nonlocal inventory
        try:
            med = inventory[idx]

            inventory_backend.remove_tablet_medication(med['name'], med['dosage'])

            
            inventory = inventory_backend.get_tablet_inventory()

            update_inventory_list()
            dialog.open = False
            e.page.update()

            dlg_add = ft.AlertDialog(
                    content=ft.Text("Tablet medication deleted successfully!"),
                    on_dismiss=lambda e: None,
                )
            e.page.overlay.append(dlg_add)
            dlg_add.open = True
            e.page.update()

        except IndexError as ie:
            print(f"Error deleting item: {ie}")

    # Input fields for tablet medications
    tablet_name_input = ft.TextField(label="Tablet Name")
    tablet_dosage_input = ft.TextField(label="Dosage (mg)", keyboard_type=ft.KeyboardType.NUMBER)
    tablet_stock_input = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)

    add_tablet_button = ft.ElevatedButton(text="Add", on_click=add_item)
    cancel_tablet_button = ft.ElevatedButton(text="Cancel", on_click=lambda e: cancel_add(e, add_tablet_dialog))

    add_tablet_dialog = ft.AlertDialog(
        title=ft.Text("Add Tablet Medication", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            ft.Column(
                controls=[
                tablet_name_input,
                tablet_dosage_input,
                tablet_stock_input,
                ],
                spacing=20,
            ),
            width=200,
            height=200,
        ),
        actions=[add_tablet_button, cancel_tablet_button],
        modal=True,
    )

####### FLUID MEDICATION INVENTORY #######

    # Predefined valid fluid medications with valid dosages

    # Extract generic names for validation
   
    def add_fluid_item(e):
        nonlocal fluid_inventory
        try:
            name = fluid_name_input.value.strip()
            dosage = fluid_dosage_input.value.strip()
            stock = fluid_stock_input.value.strip()

            # Validate all fields before adding
            fluid_name_input.update()

            fluid_dosage_input.update()

            fluid_stock_input.update()

            # Add valid fluid medication to inventory
            # Use backend to add medication
            inventory_backend.add_fluid_medication(name, int(dosage), int(stock))
            
            # Update local fluid inventory list from backend
            fluid_inventory = inventory_backend.get_fluid_inventory()

            fluid_name_input.value = ""
            fluid_dosage_input.value = ""
            fluid_stock_input.value = ""
            fluid_name_input.update()
            fluid_dosage_input.update()
            fluid_stock_input.update()
            update_fluid_inventory_list()
            add_fluid_dialog.open = False
            e.page.update()

            dlg_add = ft.AlertDialog(
                    content=ft.Text("Fluid medicine added successfully!"),
                    on_dismiss=lambda e: None,
                )
            e.page.overlay.append(dlg_add)
            dlg_add.open = True
            e.page.update()
        
        except ValueError as ve:
            print(f"Error adding item: {ve}")
            error_snack = ft.SnackBar(content=ft.Text("Invalid input! Please enter valid data."))
            e.page.overlay.append(error_snack)
            error_snack.open = True
            e.page.update()

            

    def update_fluid_inventory_list():
        fluid_inventory_list.controls.clear()
        for idx, item in enumerate(fluid_inventory):
            fluid_inventory_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                # Medication details at the top
                                        ft.Text(f"{item['name']} - {item['dosage']}mg", weight=ft.FontWeight.BOLD, size=16),
                                        ft.Text(f"Stock: {item['stock']}", color=ft.colors.ON_SURFACE_VARIANT, size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                # Buttons row at the bottom
                                ft.Row(
                                    [
                                        # Left side: Stock adjustment buttons
                                        ft.Row(
                                            [
                                                ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    tooltip="Increase Stock",
                                                    on_click=lambda e, idx=idx: adjust_fluid_stock(idx, 1, e.page),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.REMOVE,
                                                    tooltip="Decrease Stock",
                                                    on_click=lambda e, idx=idx: adjust_fluid_stock(idx, -1, e.page),
                                                ),
                                            ]
                                        ),
                                        
                                        # Right side: Delete button
                                        ft.Row(
                                            [
                                                ft.IconButton(
                                                    icon=ft.icons.EDIT,
                                                    on_click=lambda e, idx=idx: open_edit_fluid_dialog(e, idx),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.DELETE,
                                                    tooltip="Delete Medication",
                                                    on_click=lambda e, idx=idx: confirm_delete_fluid_item(e, idx),
                                                )
                                            ]
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                )
                            ],
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                    ),
                    elevation=2,
                )
            )
        fluid_inventory_list.visible = len(fluid_inventory) > 0

    def adjust_fluid_stock(idx, amount, page):
        nonlocal fluid_inventory
        try:
            med = fluid_inventory[idx]

            inventory_backend.update_fluid_stock(med['name'], med['dosage'], amount)

            
            fluid_inventory = inventory_backend.get_fluid_inventory()
        # Update the stock by adding or subtracting based on dosage
            update_fluid_inventory_list()
            snack = ft.SnackBar(content=ft.Text(f"Stock updated for {med['name']}"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except IndexError as ie:
            print(f"Error adjusting fluid stock: {ie}")

    def open_edit_fluid_dialog(e, idx):
        global current_edit_idx  # Use a global variable to track the item index
        current_edit_idx = idx  # Save the index of the item being edited

        # Pre-fill the TextField with the current stock value
        edit_stock_input.value = str(fluid_inventory[idx]["stock"])
        
        # Ensure the dialog is attached to the page's overlay
        if edit_fluid_dialog not in e.page.overlay:
            e.page.overlay.append(edit_fluid_dialog)
        
        # Open the dialog
        edit_fluid_dialog.open = True
        e.page.update()

    def save_edited_fluid_stock(e):
        global current_edit_idx  # Access the global variable for the current index
        nonlocal fluid_inventory
        try:
            new_stock = int(edit_stock_input.value.strip())# Get the new stock value from the input field

            med = fluid_inventory[current_edit_idx]

            current_stock = med['stock']
            stock_change = new_stock - current_stock

            inventory_backend.update_fluid_stock(med['name'], med['dosage'], stock_change)

            
            fluid_inventory = inventory_backend.get_fluid_inventory()

            update_fluid_inventory_list()

            edit_fluid_dialog.open = False
            e.page.update()

            snack = ft.SnackBar(content=ft.Text("Fluid medication stock updated successfully!"))
            e.page.overlay.append(snack)
            snack.open = True
            e.page.update()
        
        except (ValueError, IndexError) as e:
            print(f"Error editing stock: {e}")
            error_snack = ft.SnackBar(content=ft.Text("Invalid input! Please enter a valid stock number."))
            e.page.overlay.append(error_snack)
            error_snack.open = True
            e.page.update()

    def confirm_delete_fluid_item(e, idx):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this fluid medication?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(e, confirm_dialog)),
                ft.TextButton(
                    "Delete",
                    on_click=lambda e, idx=idx: delete_fluid_item(e, idx, confirm_dialog),
                ),
            ],
            modal=True,
        )
        e.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        e.page.update()

    def delete_fluid_item(e, idx, dialog):
        nonlocal fluid_inventory
        try:
            med = fluid_inventory[idx]

            inventory_backend.remove_fluid_medication(med['name'], med['dosage'])
    
            
            fluid_inventory = inventory_backend.get_fluid_inventory()

            update_fluid_inventory_list()
            dialog.open = False
            e.page.update()
            
            dlg_add = ft.AlertDialog(
                    content=ft.Text("Fluid medication deleted successfully!"),
                    on_dismiss=lambda e: None,
                )
            e.page.overlay.append(dlg_add)
            dlg_add.open = True
            e.page.update()
        except IndexError as ie:
            print(f"Error deleting item: {ie}")

    def close_dialog(e, dialog):
        dialog.open = False
        e.page.update()

    # Input fields for fluid medications
    fluid_name_input = ft.TextField(label="Fluid Name")
    fluid_dosage_input = ft.TextField(label="Dosage (mL)")
    fluid_stock_input = ft.TextField(label="Stock (mL)")

    add_fluid_button = ft.ElevatedButton(text="Add", on_click=add_fluid_item)
    cancel_fluid_button = ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog(e, add_fluid_dialog))

    add_fluid_dialog = ft.AlertDialog(
        title=ft.Text("Add Fluid Medication", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            ft.Column(
                controls=[
                    fluid_name_input,
                    fluid_dosage_input,
                    fluid_stock_input,
                ],
                spacing=20,
            ),
            width=200,
            height=200,
        ),
        actions=[add_fluid_button, cancel_fluid_button],
        modal=True,
    )

    # Input field for editing stock
    edit_stock_input = ft.TextField(label="Edit Stock (mL)", autofocus=True)

    # Dialog for editing fluid stock
    edit_fluid_dialog = ft.AlertDialog(
        title=ft.Text("Edit Fluid Medication Stock", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            ft.Column(
                controls=[edit_stock_input
                ],
            ),
            width=200,
            height=200,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        actions=[
            ft.ElevatedButton(text="Save", on_click=save_edited_fluid_stock),
            ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog(e, edit_fluid_dialog)),
        ],
        modal=True,
    )

    # Fluid inventory list UI
    fluid_inventory_list = ft.Column()

######## Main Inventory UI #########
    
    inventory_list = ft.Column()
    fluid_inventory_list = ft.Column()

    add_tablet_med_button = ft.ElevatedButton(
        text="Add Tablet Medication",
        width=230,
        on_click=lambda e: open_add_dialog(e, add_tablet_dialog),
    )

    add_fluid_med_button = ft.ElevatedButton(
        text="Add Fluid Medication",
        width=230,
        on_click=lambda e: open_add_dialog(e, add_fluid_dialog),
    )

    ft.TextButton("Cancel", on_click=lambda e: close_dialog(e, fab_click_dialog))

    fab_click_dialog = ft.AlertDialog(
        title=ft.Text("Add to Inventory", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            ft.Column(
                controls=[
                    add_tablet_med_button,
                    add_fluid_med_button,
                ],
                spacing=25,
            ),
            width=120,
            height=100,
        ),
        actions=[ft.TextButton("Cancel", on_click=lambda e: close_dialog(e, fab_click_dialog))],
        modal=True,
    )

    fab = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        tooltip="Add Prescription",
        bgcolor=ft.colors.LIGHT_BLUE,
        on_click=lambda e: open_add_dialog(e, fab_click_dialog)
    )

    fab_container = ft.Container(
        content=fab,
        right=20,
        bottom=20,
        padding=10
    )

    def open_add_dialog(e, dialog):
        dialog.open = True
        if dialog not in e.page.overlay:
            e.page.overlay.append(dialog)
        e.page.update()

    def cancel_add(e, dialog):
        dialog.open = False
        e.page.update()

    
    update_inventory_list()
    update_fluid_inventory_list()

    # Main container for the entire inventory page
    inventory_container = ft.Column(
        controls=[
            inventory_list,
            fluid_inventory_list,
        ],
        visible=True  # Ensure the entire container is visible
    )
    
    return ft.Stack(
        controls=[
            ft.Container(
                content=inventory_container,
                padding=10,
                top=0,
                left=0,
                right=0,
                bottom=50,  # Leave space for FAB
            ),
            ft.Container(
                content=fab,
                right=20,
                bottom=20,
                padding=10
            )
        ],
        visible=False
    )
