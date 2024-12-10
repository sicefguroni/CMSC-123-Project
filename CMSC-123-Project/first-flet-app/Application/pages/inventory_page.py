import flet as ft

########### TABLET MEDICATION INVENTORY ########

def inventory_page():
    inventory = []  # Combined inventory for tablets and fluids
    fluid_inventory = []  # Separate inventory for fluids

    inventory_list = ft.Column(
        controls=[],
        visible=True
    )

    fluid_inventory_list = ft.Column(
        controls=[],
        visible=True
    )

    def add_item(e):
        try:
            name = tablet_name_input.value.strip()
            dosage = tablet_dosage_input.value.strip()
            stock = tablet_stock_input.value.strip()
        
            tablet_name_input.update()
            tablet_dosage_input.update()
            tablet_stock_input.update()
                
            inventory.append({
                "name": name,
                "dosage": int(dosage),
                "stock": int(stock),
            })
            tablet_name_input.value = ""
            tablet_dosage_input.value = ""
            tablet_stock_input.value = ""
            tablet_name_input.update()
            tablet_dosage_input.update()
            tablet_stock_input.update()
            update_inventory_list()
            add_tablet_dialog.open = False
            e.page.update()

            snack = ft.SnackBar(content=ft.Text("Tablet medication added successfully!"))
            e.page.overlay.append(snack)
            snack.open = True
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
                                                    on_click=lambda e, idx=idx: adjust_stock(idx, 1),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.REMOVE,
                                                    tooltip="Decrease Stock",
                                                    on_click=lambda e, idx=idx: adjust_stock(idx, -1),
                                                ),
                                            ]
                                        ),
                                        
                                        # Right side: Delete button
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Delete Medication",
                                            icon_color=ft.colors.ERROR,
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
        inventory_list.update()

    def adjust_stock(idx, amount):
        try:
            if 0 <= inventory[idx]["stock"] + amount:
                inventory[idx]["stock"] += amount
                update_inventory_list()
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
        try:
            inventory.pop(idx)
            update_inventory_list()
            dialog.open = False
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
                spacing=10,
            ),
            width=200,
            height=200,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        actions=[add_tablet_button, cancel_tablet_button],
        modal=True,
    )

####### FLUID MEDICATION INVENTORY #######

    # Predefined valid fluid medications with valid dosages

    # Extract generic names for validation
    def validate_fluid_name(e):
        name = fluid_name_input.value.strip()

        fluid_name_input.update()

    def validate_fluid_dosage(e):
        # Retrieve and clean the input values
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()

        fluid_name_input.update()
        fluid_dosage_input.update()

        # Convert the dosage input to a number
        dosage = int(dosage)
        
        # Update the UI component with the error or clear it
        fluid_dosage_input.update()


    def validate_fluid_stock(e):
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        fluid_stock_input.update()

    def add_fluid_item(e):
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        # Validate all fields before adding
        fluid_name_input.update()

        fluid_dosage_input.update()

        fluid_stock_input.update()

        # Add valid fluid medication to inventory
        fluid_inventory.append({
            "name": name,
            "dosage": int(dosage),
            "stock": int(stock),
        })
        fluid_name_input.value = ""
        fluid_dosage_input.value = ""
        fluid_stock_input.value = ""
        fluid_name_input.update()
        fluid_dosage_input.update()
        fluid_stock_input.update()
        update_fluid_inventory_list()
        add_fluid_dialog.open = False
        e.page.update()

        snack = ft.SnackBar(content=ft.Text("Fluid medication added successfully!"))
        e.page.overlay.append(snack)
        snack.open = True
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
                                                    on_click=lambda e, idx=idx: adjust_fluid_stock(idx, 1),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.REMOVE,
                                                    tooltip="Decrease Stock",
                                                    on_click=lambda e, idx=idx: adjust_fluid_stock(idx, -1),
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
                                                    icon_color=ft.colors.ERROR,
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
        fluid_inventory_list.update()

    def adjust_fluid_stock(idx, adjustment):
        # Update the stock by adding or subtracting based on dosage
        new_stock = fluid_inventory[idx]["stock"] + adjustment
        if new_stock >= 0:
            fluid_inventory[idx]["stock"] = new_stock
            update_fluid_inventory_list()

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
        new_stock = edit_stock_input.value.strip()  # Get the new stock value from the input field

        
        e.page.update()

        # Update the stock value in the selected fluid medication
        fluid_inventory[current_edit_idx]["stock"] = int(new_stock)
        
        # Refresh the inventory list to reflect the updated stock
        update_fluid_inventory_list()

        # Close the dialog after saving
        edit_fluid_dialog.open = False
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
        fluid_inventory.pop(idx)
        update_fluid_inventory_list()
        dialog.open = False
        e.page.update()

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
                spacing=10,
            ),
            width=200,
            height=200,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
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
        on_click=lambda e: open_add_dialog(e, add_tablet_dialog),
    )

    add_fluid_med_button = ft.ElevatedButton(
        text="Add Fluid Medication",
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
                spacing=10,
            ),
            width=200,
            height=200,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
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
        alignment=ft.alignment.bottom_right,
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
