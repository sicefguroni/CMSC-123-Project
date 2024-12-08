import flet as ft
import re


########### TABLET MEDICATION INVENTORY ########

def inventory_page():
    inventory = []  # Combined inventory for tablets and fluids
    fluid_inventory = []  # Separate inventory for fluids

    # List of valid tablet medications and their corresponding valid dosages
    valid_a_medications = {
        "Abacavir (as sulfate)-300mg Tablet": [300],
        "Abiraterone Acetate - ": [250, 500],
        "Acarbose- ": [25, 50, 100],
        "Aceclofenac- ": [100],
        "Acetazolamide- ": [250],
    }

    # Extract generic names for validation
    generic_names = {key.split('-')[0].strip(): key for key in valid_a_medications}

    def validate_name(e):
        name = tablet_name_input.value.strip()
        if name not in generic_names:
            tablet_name_input.error_text = "Invalid medication name!"
        else:
            tablet_name_input.error_text = None
        tablet_name_input.update()

    def validate_dosage(e):
        name = tablet_name_input.value.strip()
        dosage = tablet_dosage_input.value.strip()
        if not dosage.isdigit():
            tablet_dosage_input.error_text = "Dosage must be numeric!"
        elif name in generic_names:
            valid_dosages = valid_a_medications[generic_names[name]]
            if int(dosage) not in valid_dosages:
                tablet_dosage_input.error_text = f"Invalid dosage! Allowed: {', '.join(map(str, valid_dosages))}mg"
            else:
                tablet_dosage_input.error_text = None
        else:
            tablet_dosage_input.error_text = "Enter a valid medication name first!"
        tablet_dosage_input.update()

    def validate_stock(e):
        if not tablet_stock_input.value.isdigit():
            tablet_stock_input.error_text = "Stock must be numeric!"
        else:
            tablet_stock_input.error_text = None
        tablet_stock_input.update()

    def add_item(e):
        name = tablet_name_input.value.strip()
        dosage = tablet_dosage_input.value.strip()
        stock = tablet_stock_input.value.strip()

        # Validate all fields before adding
        if not name or name not in generic_names:
            tablet_name_input.error_text = "Invalid medication name!"
            tablet_name_input.update()
            return

        if not dosage.isdigit() or int(dosage) not in valid_a_medications[generic_names[name]]:
            tablet_dosage_input.error_text = "Invalid dosage!"
            tablet_dosage_input.update()
            return

        if not stock.isdigit():
            tablet_stock_input.error_text = "Stock must be numeric!"
            tablet_stock_input.update()
            return

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

    def update_inventory_list():
        inventory_list.controls.clear()
        for idx, item in enumerate(inventory):
            row_color = ft.Colors.RED_50 if item["stock"] <= 3 else ft.Colors.TRANSPARENT
            inventory_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} {item['dosage']}mg", expand=True),
                            ft.Text(f"Stock: {item['stock']}", expand=True),
                            ft.IconButton(
                                icon=ft.Icons.REMOVE,
                                on_click=lambda e, idx=idx: adjust_stock(idx, -1),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                on_click=lambda e, idx=idx: adjust_stock(idx, 1),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, idx=idx: confirm_delete_item(e, idx),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    bgcolor=row_color,
                    padding=10,
                    border_radius=5,
                )
            )
        inventory_list.update()

    def adjust_stock(idx, amount):
        if 0 <= inventory[idx]["stock"] + amount:
            inventory[idx]["stock"] += amount
            update_inventory_list()

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
        inventory.pop(idx)
        update_inventory_list()
        dialog.open = False
        e.page.update()

    # Input fields for tablet medications
    tablet_name_input = ft.TextField(label="Tablet Name", on_change=validate_name)
    tablet_dosage_input = ft.TextField(label="Dosage (mg)", on_change=validate_dosage)
    tablet_stock_input = ft.TextField(label="Stock", on_change=validate_stock)

    add_tablet_button = ft.ElevatedButton(text="Add", on_click=add_item)
    cancel_tablet_button = ft.ElevatedButton(text="Cancel", on_click=lambda e: cancel_add(e, add_tablet_dialog))

    add_tablet_dialog = ft.AlertDialog(
        title=ft.Text("Add Tablet Medication"),
        content=ft.Column(
            [
                tablet_name_input,
                tablet_dosage_input,
                tablet_stock_input,
            ],
            spacing=10,
        ),
        actions=[add_tablet_button, cancel_tablet_button],
        modal=True,
    )

####### FLUID MEDICATION INVENTORY #######

# Sample data structure for fluid medications
fluid_inventory = [
    {"name": "Fluid A", "dosage": 20, "stock": 100},
    {"name": "Fluid B", "dosage": 50, "stock": 200},
]

def adjust_fluid_stock(idx, amount):
    """Adjust stock based on dosage and amount (+1 for adding, -1 for subtracting)."""
    dosage = fluid_inventory[idx]["dosage"]
    new_stock = fluid_inventory[idx]["stock"] + (dosage * amount)

    if new_stock >= 0:
        fluid_inventory[idx]["stock"] = new_stock
        update_fluid_inventory_list()
    else:
        snack = ft.SnackBar(content=ft.Text("Stock cannot go below 0!"))
        e.page.overlay.append(snack)
        snack.open = True
        e.page.update()

def edit_fluid_stock(idx):
    """Open a dialog to directly edit stock."""
    def save_new_stock(e):
        new_stock_value = edit_stock_input.value.strip()
        if not new_stock_value.isdigit() or int(new_stock_value) < 0:
            edit_stock_input.error_text = "Stock must be a positive number!"
            edit_stock_input.update()
        else:
            fluid_inventory[idx]["stock"] = int(new_stock_value)
            edit_dialog.open = False
            update_fluid_inventory_list()
            e.page.update()

    # Dialog for editing stock
    edit_stock_input = ft.TextField(
        label="New Stock (mL)", value=str(fluid_inventory[idx]["stock"])
    )
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit Stock"),
        content=edit_stock_input,
        actions=[
            ft.TextButton("Save", on_click=save_new_stock),
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(e, edit_dialog)),
        ],
        modal=True,
    )
    e.page.overlay.append(edit_dialog)
    edit_dialog.open = True
    e.page.update()

def update_fluid_inventory_list():
    """Update the inventory list UI to reflect changes."""
    fluid_inventory_list.controls.clear()

    for idx, item in enumerate(fluid_inventory):
        row_color = ft.Colors.RED_50 if item["stock"] <= 3 else ft.Colors.TRANSPARENT
        fluid_inventory_list.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"{item['name']} {item['dosage']}mL", expand=True),
                        ft.Text(f"Stock: {item['stock']}mL", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            tooltip="Subtract Stock",
                            on_click=lambda e, idx=idx: adjust_fluid_stock(idx, -1),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Edit Stock",
                            on_click=lambda e, idx=idx: edit_fluid_stock(idx),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            tooltip="Add Stock",
                            on_click=lambda e, idx=idx: adjust_fluid_stock(idx, 1),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Delete Medication",
                            on_click=lambda e, idx=idx: confirm_delete_fluid_item(e, idx),
                        ),
                    ],
                    alignment="spaceBetween",
                ),
                bgcolor=row_color,
                padding=10,
                border_radius=5,
            )
        )
    fluid_inventory_list.update()

def add_fluid_medication(e):
    """Add a new fluid medication to the inventory."""
    name = fluid_name_input.value.strip()
    dosage = fluid_dosage_input.value.strip()
    stock = fluid_stock_input.value.strip()

    if not name or not dosage.isdigit() or not stock.isdigit():
        # Handle invalid input
        return

    new_item = {
        "name": name,
        "dosage": int(dosage),
        "stock": int(stock),
    }
    fluid_inventory.append(new_item)
    fluid_name_input.value = ""
    fluid_dosage_input.value = ""
    fluid_stock_input.value = ""

    # Update the inventory list UI
    update_fluid_inventory_list()
    e.page.update()

# UI components for adding fluid medication
fluid_name_input = ft.TextField(label="Medication Name")
fluid_dosage_input = ft.TextField(label="Dosage (mL)")
fluid_stock_input = ft.TextField(label="Stock (mL)")

add_fluid_button = ft.ElevatedButton("Add Fluid Medication", on_click=add_fluid_medication)

# Fluid inventory list UI
fluid_inventory_list = ft.Column()

def main(e):
    """Main function to set up the UI."""
    update_fluid_inventory_list()

    e.page.add(
        ft.Column(
            [
                fluid_name_input,
                fluid_dosage_input,
                fluid_stock_input,
                add_fluid_button,
                fluid_inventory_list,
            ]
        )
    )

ft.app(target=main)

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

    def open_add_dialog(e, dialog):
        dialog.open = True
        if dialog not in e.page.overlay:
            e.page.overlay.append(dialog)
        e.page.update()

    def cancel_add(e, dialog):
        dialog.open = False
        e.page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tablet Medications", size=20, weight=ft.FontWeight.BOLD),
                add_tablet_med_button,
                inventory_list,
                ft.Text("Fluid Medications", size=20, weight=ft.FontWeight.BOLD),
                add_fluid_med_button,
                fluid_inventory_list,
            ],
            spacing=10,
        ),
    )
