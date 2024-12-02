import flet as ft
import re

def inventory_page():
    inventory = []

    # List of valid medications starting with 'A' and their corresponding dosages
    valid_a_medications = {
        "Abacavir (as sulfate)-300mg Tablet": [300],
        "Abacavir (as sulfate) +Lamivudine - 600mg/300mgTablet": [600, 300],
        "Abacavir (as sulfate) +Lamivudine +Zidovudine - 300mg/150mg/300mg Tablet": [300, 150, 300],
        "Abacavir (as sulfate) +Dolutegravir (as sodium) +Lamivudine- 600mg/50mg/300mg Tablet": [600, 50, 300],
        "Abiraterone Acetate - 250mg Tablet/500mg Tablet": [250, 500],
        "Acarbose- 25mg Tablet/50mg Tablet/100mg Tablet": [25, 50, 100],
        "Aceclofenac- 100mg Film-Coated Tablet": [100],
        "Acetazolamide- 250mg Tablet": [250],
    }

    def update_inventory_list():
        inventory_list.controls.clear()
        for idx, item in enumerate(inventory):
            row_color = ft.colors.RED_50 if item["stock"] <= 3 else ft.colors.TRANSPARENT
            inventory_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} {item['dosage']}mg", expand=True),
                            ft.Text(f"Stock: {item['stock']}", expand=True),
                            ft.IconButton(
                                icon=ft.icons.REMOVE,
                                on_click=lambda e, idx=idx: adjust_stock(idx, -1),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda e, idx=idx: adjust_stock(idx, 1),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                on_click=lambda e, idx=idx: confirm_delete_item(idx),
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

    def validate_name(e):
        name = name_input.value.strip()
        if not re.match(r"^[A-Za-z\s]+$", name):
            name_input.error_text = "Invalid medication name"
            dosage_input.disabled = True
        elif name.startswith("A"):
            # Check if the name is in the list of valid medications
            if name not in valid_a_medications:
                name_input.error_text = "Invalid medication name"
                dosage_input.disabled = True
            else:
                name_input.error_text = None
                dosage_input.disabled = False
        else:
            name_input.error_text = None
            dosage_input.disabled = False
        name_input.update()
        dosage_input.update()

    def validate_dosage(e):
        name = name_input.value.strip()
        dosage = dosage_input.value.strip()

        if name.startswith("A") and name in valid_a_medications:
            # Validate dosage for the specific medication
            valid_dosages = valid_a_medications[name]
            if not dosage.isdigit() or int(dosage) not in valid_dosages:
                dosage_input.error_text = f"Invalid dosage for {name}! Valid dosages: {', '.join(map(str, valid_dosages))}mg."
                stock_input.disabled = True
            else:
                dosage_input.error_text = None
                stock_input.disabled = False
        else:
            dosage_input.error_text = None
            stock_input.disabled = True
        dosage_input.update()
        stock_input.update()

    def validate_stock(e):
        if stock_input.value.isdigit():
            stock_input.error_text = None
        else:
            stock_input.error_text = "Stock must be numeric!"
        stock_input.update()

    def add_item(e):
        name = name_input.value.strip()
        dosage = dosage_input.value.strip()
        stock = stock_input.value.strip()

        if not re.match(r"^[A-Za-z\s]+$", name):
            name_input.error_text = "Invalid medication name"
            name_input.update()
            return

        if name.startswith("A") and name not in valid_a_medications:
            name_input.error_text = "Invalid medication name"
            name_input.update()
            return

        if name.startswith("A") and dosage.isdigit():
            valid_dosages = valid_a_medications[name]
            if int(dosage) not in valid_dosages:
                dosage_input.error_text = f"Invalid dosage for {name}! Valid dosages: {', '.join(map(str, valid_dosages))}mg."
                dosage_input.update()
                return

        if not stock.isdigit():
            stock_input.error_text = "Stock must be numeric!"
            stock_input.update()
            return

        stock_number = int(stock)
        if stock_number <= 3:
            snack = ft.SnackBar(content=ft.Text("Warning: Low stock!"))
            e.page.overlay.append(snack)
            snack.open = True

        inventory.append({
            "name": name,
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
        update_inventory_list()

        add_dialog.open = False
        e.page.update()

        snack = ft.SnackBar(content=ft.Text("Medication added successfully!"))
        e.page.overlay.append(snack)
        snack.open = True
        e.page.update()

    def adjust_stock(idx, amount):
        if 0 <= inventory[idx]["stock"] + amount:
            inventory[idx]["stock"] += amount
            update_inventory_list()

            if inventory[idx]["stock"] <= 3:
                snack = ft.SnackBar(content=ft.Text(f"Warning: Low stock for '{inventory[idx]['name']}'!"))
                snack.open = True
                e.page.overlay.append(snack)
                e.page.update()

    def confirm_delete_item(idx):
        def delete_confirmed(e):
            inventory.pop(idx)
            update_inventory_list()
            confirm_dialog.open = False
            snack = ft.SnackBar(content=ft.Text("Medication deleted successfully!"))
            e.page.overlay.append(snack)
            snack.open = True
            e.page.update()

        def cancel_delete(e):
            confirm_dialog.open = False
            e.page.update()

        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{inventory[idx]['name']}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton("Delete", on_click=delete_confirmed),
            ],
            modal=True,
        )
        e.page.dialog = confirm_dialog
        confirm_dialog.open = True
        e.page.update()

    # Input fields
    name_input = ft.TextField(label="Medication Name", on_change=validate_name)
    dosage_input = ft.TextField(label="Dosage (mg)", on_change=validate_dosage, disabled=True)
    stock_input = ft.TextField(label="Stock Number", on_change=validate_stock, disabled=True)

    add_button = ft.ElevatedButton(text="Add", on_click=add_item)

    # Pop-up for adding medication
    add_dialog = ft.AlertDialog(
        title=ft.Text("Add Medication"),
        content=ft.Column(
            [
                name_input,
                dosage_input,
                stock_input,
            ],
            spacing=10,
        ),
        actions=[add_button],
        modal=True,
    )

    # Main Inventory UI
    inventory_list = ft.Column()
    add_med_button = ft.ElevatedButton(
        text="Add Medication",
        on_click=lambda e: open_add_dialog(e),
    )

    def open_add_dialog(e):
        add_dialog.open = True
        e.page.dialog = add_dialog
        e.page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to Inventory Page!", size=20, weight=ft.FontWeight.BOLD),
                add_med_button,
                ft.Divider(),
                inventory_list,
            ],
            spacing=10,
        ),
    )
