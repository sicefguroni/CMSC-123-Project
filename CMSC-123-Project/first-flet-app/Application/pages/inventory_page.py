import flet as ft
import re

def inventory_page():
    tablet_inventory = []
    fluid_inventory = []

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

    def update_tablet_inventory_list():
        tablet_list.controls.clear()
        for idx, item in enumerate(tablet_inventory):
            row_color = ft.colors.RED_50 if item["stock"] <= 3 else ft.colors.TRANSPARENT
            tablet_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} {item['dosage']}mg", expand=True),
                            ft.Text(f"Stock: {item['stock']}", expand=True),
                            ft.IconButton(
                                icon=ft.icons.REMOVE,
                                on_click=lambda e, idx=idx: adjust_stock(tablet_inventory, idx, -1),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda e, idx=idx: adjust_stock(tablet_inventory, idx, 1),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, idx=idx: confirm_delete_item(e, tablet_inventory, idx),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    bgcolor=row_color,
                    padding=10,
                    border_radius=5,
                )
            )
        tablet_list.update()

    def update_fluid_inventory_list():
        fluid_list.controls.clear()
        for idx, item in enumerate(fluid_inventory):
            row_color = ft.colors.RED_50 if item["stock"] <= 50 else ft.colors.TRANSPARENT
            fluid_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} {item['dosage']}mL", expand=True),
                            ft.Text(f"Stock: {item['stock']}mL", expand=True),
                            ft.IconButton(
                                icon=ft.icons.REMOVE,
                                on_click=lambda e, idx=idx: adjust_stock(fluid_inventory, idx, -10),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda e, idx=idx: adjust_stock(fluid_inventory, idx, 10),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, idx=idx: confirm_delete_item(e, fluid_inventory, idx),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    bgcolor=row_color,
                    padding=10,
                    border_radius=5,
                )
            )
        fluid_list.update()

    def validate_name(e):
        name = name_input.value.strip()
        if not re.match(r"^[A-Za-z\s]+$", name):
            name_input.error_text = "Invalid name! Use only letters."
            dosage_input.disabled = True
        elif name in generic_names:
            # Valid medication name
            name_input.error_text = None
            dosage_input.disabled = False
        else:
            # Invalid medication name
            name_input.error_text = "Invalid medication name!"
            dosage_input.disabled = True
        name_input.update()
        dosage_input.update()

    def validate_dosage(e):
        name = name_input.value.strip()
        dosage = dosage_input.value.strip()

        if name in generic_names:
            full_name = generic_names[name]
            valid_dosages = valid_a_medications[full_name]
            if not dosage.isdigit() or int(dosage) not in valid_dosages:
                dosage_input.error_text = f"Invalid dosage for {name}! Valid dosages: {', '.join(map(str, valid_dosages))}mg."
                stock_input.disabled = True
            else:
                dosage_input.error_text = None
                stock_input.disabled = False
        else:
            dosage_input.error_text = "Invalid dosage input!"
            stock_input.disabled = True
        dosage_input.update()
        stock_input.update()

    def validate_stock(e):
        if stock_input.value.isdigit():
            stock_input.error_text = None
        else:
            stock_input.error_text = "Stock must be numeric!"
        stock_input.update()

    def add_tablet_item(e):
        name = name_input.value.strip()
        dosage = dosage_input.value.strip()
        stock = stock_input.value.strip()

        # Validate medication name
        if name not in generic_names:
            name_input.error_text = "Invalid medication name!"
            name_input.update()
            return

        # Validate dosage
        full_name = generic_names[name]
        valid_dosages = valid_a_medications[full_name]
        if not dosage.isdigit() or int(dosage) not in valid_dosages:
            dosage_input.error_text = f"Invalid dosage for {name}! Valid dosages: {', '.join(map(str, valid_dosages))}mg."
            dosage_input.update()
            return

        # Validate stock
        if not stock.isdigit():
            stock_input.error_text = "Stock must be numeric!"
            stock_input.update()
            return

        stock_number = int(stock)
        if stock_number <= 3:
            snack = ft.SnackBar(content=ft.Text("Warning: Low stock (3 or less)!"))
            e.page.overlay.append(snack)
            snack.open = True

        tablet_inventory.append({
            "name": full_name,
            "dosage": int(dosage),
            "stock": stock_number,
        })
        name_input.value = ""
        dosage_input.value = ""
        stock_input.value = ""
        dosage_input.disabled = True
        stock_input.disabled = True
        name_input.update()
        dosage_input.update()
        stock_input.update()
        update_tablet_inventory_list()

        add_tablet_dialog.open = False
        e.page.update()

        snack = ft.SnackBar(content=ft.Text("Medication added successfully!"))
        e.page.overlay.append(snack)
        snack.open = True
        e.page.update()

    def validate_fluid_inputs(e):
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        if not re.match(r"^[A-Za-z\s]+$", name):
            fluid_name_input.error_text = "Invalid name! Use only letters."
        else:
            fluid_name_input.error_text = None

        if not dosage.isdigit():
            fluid_dosage_input.error_text = "Dosage must be numeric (in mL)!"
        else:
            fluid_dosage_input.error_text = None

        if not stock.isdigit():
            fluid_stock_input.error_text = "Stock must be numeric (in mL)!"
        else:
            fluid_stock_input.error_text = None

        fluid_name_input.update()
        fluid_dosage_input.update()
        fluid_stock_input.update()

    def add_fluid_item(e):
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        if not name or not dosage.isdigit() or not stock.isdigit():
            return

        fluid_inventory.append({
            "name": name,
            "dosage": int(dosage),
            "stock": int(stock),
        })
        fluid_name_input.value = ""
        fluid_dosage_input.value = ""
        fluid_stock_input.value = ""
        update_fluid_inventory_list()
        add_fluid_dialog.open = False
        e.page.update()

    def adjust_stock(inventory, idx, amount):
        inventory[idx]["stock"] = max(0, inventory[idx]["stock"] + amount)
        if inventory == tablet_inventory:
            update_tablet_inventory_list()
        elif inventory == fluid_inventory:
            update_fluid_inventory_list()

    # Dialogs and Buttons
    tablet_list = ft.Column()
    fluid_list = ft.Column()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tablet Inventory", weight=ft.FontWeight.BOLD),
                tablet_list,
                ft.Divider(),
                fluid_list,
            ]
