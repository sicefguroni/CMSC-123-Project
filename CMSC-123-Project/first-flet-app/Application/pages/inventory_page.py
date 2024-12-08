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
        "Acetylsalicylic- ": [30, 80, 100, 300, 325],
        "Aciclovir- ": [200, 400, 800],
        "Acitretin- ": [10, 17.5, 22.5, 25],
        "Adefovir- ": [10],
        "Allopurinol- ": [100, 300],
        "Baclofen- ": [10, 20, 25],
        "Bambuterol Hydochloride- ": [10],
        "Benazepril Hydrochloride- ": [5, 10, 20, 40],
        "Bicalutamide- ": [50, 150],
        "Bilastine- ": [20],
        "Bisacodyl- ": [5],
        "Bisoprolol- ": [2.5, 5, 10],
        "Bosentan- ": [62.5, 125],
        "Bromhexine Hydrochloride- ": [8, 16],
        "Butamirate Citrate- ": [50],
        "Candesartan Cilexetil- ": [2, 4, 8, 16, 32],
        "Capecitabine- ": [150, 500], 
        "Captopril- ": [25, 50],
        "Carbamazepine- ": [100, 200, 400],
        "Carbimazole- ": [5, 20], 
        "Carbocisteine- ": [200, 500],
        "Carvedilol- ": [3.125, 6.25, 12.25, 25],
        "Cefaclor- ": [250, 500],
        "Cefalexin- ": [250, 500, 750],
        "Cefixime- ": [100, 200, 400],
        "Danazol- ": [50, 100, 200],
        "Desloratadine- ": [5], 
        "Dexamethasone- ": [3, 4],
        "Diazepam- ": [5, 10],
        "Diclofenac Potassium- ": [12.5, 25, 50],
        "Dipyridamole- ": [25, 50, 75, 100],
        "Domperidone- ": [10],
        "Donepezil Hydrochloride- ": [5, 10, 23],
        "Doxofylline- ": [200, 400],
        "Dydrogesterone- ": [10], 
        "Efavirenz- ": [50, 100, 200, 600],
        "Empagliflozin- ": [10, 25],
        "Emtrcitabine- ": [200],
        "Enalapril maleate- ": [2.5, 5, 10, 20],
        "Entecavir- ": [1],
        "Enzalutamide- ": [40],
        "Eperisone hydrochloride- ": [50],
        "Eplerenone- ": [25, 50],
        "Erdosteine- ": [300],
        "Erythromycin stearate- ": [250, 500],
        "Famotidine- ": [10, 20, 40],
        "Febuxostat- ": [10, 20, 40, 80, 120],
        "Finasteride- ": [1, 5],
        "Flecainide acetate- ": [50, 100, 150],
        "Fluconazole- ": [50, 100, 150, 200],
        "Fludarabine Phosphate- ": [10],
        "Fluvoxamine Maleate- ": [50, 100],
        "Fosinopril Sodium- ": [10, 20],
        "Furazolidone- ": [100],
        "Furosemide- ": [20, 40, 80],
        "Gabapentin- ": [100, 300, 400, 600, 800],
        "Gabapentin enacarbil- ": [300],
        "Galantamine- ": [4, 8, 12],
        "Gefitinib- ": [250],
        "Gemfibrozil- ": [300, 600, 900],
        "Glibenclamide- ": [1.25, 1.5, 2.5, 3, 5, 6],
        "Gliclazide- ": [30, 60, 80],
        "Glimepiride- ": [1, 2, 3, 4],
        "Glipizide- ": [5, 10],
        "Guaifenesin- ": [200, 600],
        "Haloperidol- ": [2, 5, 10, 20],
        "Hydrochlorothiazide- ": [12.5, 25, 12.5],
        "Hydroxychloroquine sulfate- ": [200],
        "Hydroxycarbamide- ": [200, 300, 400, 500],
        "Hydroxyzine Hydrochloride- ": [10, 25],
        "Hyoscine butylbromide- ": [10],
        "Ibandronic Acid- ": [50, 150],
        "Ibuprofen- ": [200, 400, 600],
        "Imatinib- ": [100, 400],
        "Imidapril Hydrochloride- ": [5, 10, 20],
        "Indapamide- ": [2.5],
        "Indinavir- ": [200, 400],
        "Inosine acedoben dimepranol- ": [500],
        "Irbesartan- ": [75, 150, 300],
        "Isoniazid- ": [100, 300],
        "Isosorbide mononitrate- ": [10, 20, 30, 40],
        "Ketoprofen- ": [50, 100, 200],
        "Ketorolac trometamol- ": [10],
        "Ketotifen fumarate- ": [1, 2],
        "Lacidipine- ": [2, 4, 6],
        "Lacosamide- ": [50, 100, 150, 200],
        "Lamivudine- ": [100, 150, 300],
        "Lamotrigine- ": [2, 5, 25, 100],
        "Lansoprazole- ": [15, 30],
        "Lanthanum- ": [ 500, 750, 1000],
        "Lapatinib- ": [250],
        "Leflunomide- ": [10, 20, 100],
        "Lenalidomide- ": [2.5, 5, 7.5, 10, 15, 20, 25],
        "Letrozole- ": [2.5],
        "Losartan potassium- ": [12.5, 25, 50, 100],
        "Loratadine- ": [5, 10],
        "Mebendazole- ": [20, 50, 100],
        "Mefenamic Acid- ":[250, 500],
        "Megestrol acetate- ": [125, 160],
        "Meloxicam- ": [7.5, 15],
        "Mercaptopurine- ": [50],
        "Mesalazine- ": [250, 500],
        "Metformin hydrochloride- ": [500, 750, 850],
        "Methyldopa- ": [250, 500],
        "Mirtazapine- ": [15, 30, 45],
        "Modafinil- ":[100, 200],
        "Naproxen- ":[25, 375, 500],
        "Nateglinide- ":[120],
        "Nevirapine- ": [50, 100, 200, 400],
        "Nifedipine- ": [30, 60, 90],
        "Nifuroxazide- ": [200],
        "Nimodipine- ": [30],
        "Nitrofurantoin- ": [25, 50, 100],
        "Norfloxacin- ": [200, 400],
        "Ofloxacin- ": [200, 300, 400],
        "Olanzapine- ": [2.5, 5, 7.5, 10, 15, 20],
        "Olmesartan medoxomil- ": [5, 10, 20, 40],
        "Omeprazole- ": [10, 20, 40],
        "Ondansetron- ": [4, 8, 24],
        "Orlistat- ": [120],
        "Oxcarbazepine- ": [ 60, 150, 300, 600],
        "Oxycodone- ": [9, 13.5, 18, 27, 36], 
        "Paliperidone- ": [1.5, 3, 6, 9],
        "Paracetamol- ": [100, 120, 250, 325, 500], 
        "Pentoxifylline- ": [400],
        "Perampanel- ": [2, 4, 6, 8, 10, 12],
        "Piracetam- ": [800],
        "Piroxicam- ": [10, 20],
        "Posaconazole- ": [40, 100],
        "Pravastatin sodium- ": [20, 40, 80], 
        "Pyrantel embonate- ": [125, 250], 
        "Quetiapine- ": [25, 50, 100, 200, 300, 400],
        "Quinapril- ": [5, 10, 20, 40],
        "Quinine sulfate- ": [300, 324],
        "Rabeprazole Sodium- ": [5, 10, 20],
        "Raloxifene hydrochloride- ": [60],
        "Raltegravir- ": [25, 400, 600],
        "Ramelteon- ": [8],
        "Ramipril- ": [1.25, 2.5, 5, 10],
        "Ranitidine Hydrochloride- ": [75, 150, 300],
        "Ranolazine- ": [375, 500, 750, 1000],
        "Rebamipide- ": [100],
        "Regorafenib- ": [40],
        "Retigabine- ": [50, 100, 200, 300, 400],
        "Salbutamol Sulfate- ": [2],
        "Saxagliptin Hydrochloride- ": [2.5, 5],
        "Selegiline Hydrochloride- ": [1.25, 5, 10],
        "Sevelamer carbonate- ": [800],
        "Silodosin- ": [4, 8],
        "Simvastastin- ": [5, 10, 20, 40, 80],
        "Sirolimus- ": [1, 2],
        "Sofosbuvir- ": [400],
        "Spironolactone- ": [25, 50, 100],
        "Sulbutiamine- ": [200],
        "Tadalafil- ": [2.5, 5, 10, 20],
        "Tamoxifen Citrate- ": [10, 20, 40],
        "Tapentadol hydrochloride- ": [50, 75, 100],
        "Tedizolid Phosphate- ": [200],
        "Telmisartan- ": [20, 40, 80],
        "Temozolomide- ": [5, 20, 100, 140, 180, 250],
        "Tenofovir disoproxil fumarate- ": [200, 250, 300],
        "Tenoxicam- ": [20],
        "Terbutaline Sulfate- ": [2.5, 5],
        "Thalidomide- ": [50, 100, 150, 200],
        "Ulipristal Acetate- ": [5, 30],
        "Ursodeoxycholic Acid- ":[150, 250, 300, 500],
        "Valaciclovir Hydrochloride- ": [250, 500, 1000],
        "Valsartan- ": [40, 80, 160, 320],
        "Vardenafil Hydrochloride- ": [2.5, 5, 10, 20],
        "Vemurafenib- ": [240],
        "Verapamil Hydrochloride- ": [40, 80, 120],
        "Vildagliptin- ": [50],
        "Vinorelbine Tartrate- ": [20, 30, 80],
        "Vismodegib- ": [150],
        "Voriconazole- ": [50, 200],
        "Vortioxetine Hydrobromide- ": [5, 10, 15, 20],
        "Warfarin sodium- ": [1, 2, 2.5, 3, 4, 5, 6, 7.5, 10],
        "Zolmitriptan- ": [2.5, 5],
        "Zolpidem Tartrate- ": [5, 10],
        "Zonisamide- ": [25, 50, 100],
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

    # Predefined valid fluid medications with valid dosages
    valid_fluid_medications = {
        "Aciclovir- ": [5], 
        "Albendazole- ": [5], 
        "Amoxicillin- ": [5, 0.01],
        "Azithromycin- ": [5],
        "Azithromycin monohydrate- ": [5],
        "Carbamazepine- ": [5],
        "Carbocisteine- ": [5],
        "Cefaclor- ": [5, 0.05],
        "Cefadroxil- ":[5], 
        "Cefalexin- ": [5, 0.1],
        "Cefdinir- ": [5],
        "Cefixime- ": [5, 0.02],
        "Cefpodoxime proxetil- ": [5], 
        "Cefradine- ": [5],
        "Ceftibuten- ": [5],
        "Dasatinib- ": [10],
        "Diloxanide- ": [5],
        "Domperidone- ":[1, 5],
        "Doxycycline- ":[5],
        "Erdosteine- ": [5],
        "Erythromycin estolate- ": [5, 0.1], 
        "Erythromycin ethylsuccinate- ":[5],
        "Famotidine- ": [5],
        "Fexofenadine hydrochloride- ": [5],
        "Flucloxacillin- ":[5],
        "Fluconazole- ": [5, 0.01, 0.04], 
        "Furazolidone- ": [15],
        "Ibuprofen- ": [2.5, 5],
        "Linezolid- ": [5],
        "Mebendazole- ": [5, 0.02, 0.05],
        "Megestrol acetate- ": [0.125],
        "Methylphenidate hydrochloride- ":[5],
        "Metronidazole- ": [5, 0.025],
        "Mycophenolate mofetil- ": [0.2],
        "Naproxen- ": [0.025],
        "Nevirapine- ": [5],
        "Oseltamivir- ": [6, 12],
        "Oxcarbazepine- ": [0.06], 
        "Paracetamol- ": [0.1, 5],
        "Paroxetine- ": [5, 10],
        "Perampanel- ": [0.5],
        "Phenytoin sodium- ": [5],
        "Posaconazole- ": [0.04],
        "Prednisolone- ": [5],
        "Pyrantel embonate- ": [5],
        "Pyrazinamide- ": [5],
        "Rifampicin- ": [5],
        "Rufinamide- ": [0.04],
        "Simvastatin- ": [5],
        "Sucralfate- ": [5, 10],
        "Sultamicillin tosilate- ": [5],
        "Ursodeoxycholic Acid- ": [5],
        "Voriconazole- ": [0.04, 5],

    }

    # Extract generic names for validation
    fluid_generic_names = {key.split('-')[0].strip(): key for key in valid_fluid_medications}

    def validate_fluid_name(e):
        name = fluid_name_input.value.strip()

        # Ensure the entered name matches a key in the `fluid_generic_names`
        if name not in fluid_generic_names:
            fluid_name_input.error_text = "Invalid fluid medication name!"
        else:
            fluid_name_input.error_text = None
        fluid_name_input.update()

    def validate_fluid_dosage(e):
        # Retrieve and clean the input values
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()

        # Map the generic name to the full key in `valid_fluid_medications`
        if name in fluid_generic_names:
            full_name = fluid_generic_names[name]
        else:
            fluid_name_input.error_text = "Invalid medication name! Please select a valid name."
            fluid_name_input.update()
            return

        # Validate the dosage input
        if not dosage.isdigit():
            fluid_dosage_input.error_text = "Dosage must be numeric!"
            fluid_dosage_input.update()
            return

        # Convert the dosage input to a number
        dosage = int(dosage)

        # Retrieve valid dosages for the selected medication
        valid_dosages = valid_fluid_medications[full_name]

        # Check if the input dosage matches the valid dosage list
        if dosage not in valid_dosages:
            fluid_dosage_input.error_text = f"Invalid dosage! Valid dosages for {name}: {', '.join(map(str, valid_dosages))} mL."
        else:
            fluid_dosage_input.error_text = None  # Clear the error if valid

        # Update the UI component with the error or clear it
        fluid_dosage_input.update()


    def validate_fluid_stock(e):
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        if not stock.isdigit():
            fluid_stock_input.error_text = "Stock must be numeric!"
        elif dosage.replace('.', '', 1).isdigit() and float(dosage) >= int(stock):
            fluid_stock_input.error_text = "Stock must be greater than dosage!"
        else:
            fluid_stock_input.error_text = None

        fluid_stock_input.update()

    def add_fluid_item(e):
        name = fluid_name_input.value.strip()
        dosage = fluid_dosage_input.value.strip()
        stock = fluid_stock_input.value.strip()

        # Validate all fields before adding
        if name not in valid_fluid_medications:
            fluid_name_input.error_text = "Invalid medication name! Please select a valid name."
            fluid_name_input.update()
            return

        if not dosage.isdigit() or int(dosage) not in valid_fluid_medications[name]:
            fluid_dosage_input.error_text = f"Invalid dosage! Valid dosages for {name}: {', '.join(map(str, valid_fluid_medications[name]))}mL."
            fluid_dosage_input.update()
            return

        if not stock.isdigit() or int(dosage) >= int(stock):
            fluid_stock_input.error_text = "Stock must be numeric and greater than dosage!"
            fluid_stock_input.update()
            return

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
            row_color = ft.Colors.RED_50 if item["stock"] <= 3 else ft.Colors.TRANSPARENT
            fluid_inventory_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} - {item['dosage']}mL", expand=True),
                            ft.Text(f"Stock: {item['stock']}mL", expand=True),
                            # Plus button to add stock in increments of dosage
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                on_click=lambda e, idx=idx: adjust_fluid_stock(idx, item["dosage"]),
                            ),
                            # Minus button to subtract stock in increments of dosage
                            ft.IconButton(
                                icon=ft.Icons.REMOVE,
                                on_click=lambda e, idx=idx: adjust_fluid_stock(idx, -item["dosage"]),
                            ),
                            # Edit button to open dialog for stock editing
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, idx=idx: open_edit_fluid_dialog(e, idx),
                            ),
                            # Delete button for the item
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
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

        # Validate input: Must be numeric and greater than 0
        if not new_stock.isdigit() or int(new_stock) <= 0:  # Ensure it is a valid positive number
            snack = ft.SnackBar(content=ft.Text("Invalid stock value! Must be a positive number."))
            e.page.overlay.append(snack)
            snack.open = True
            e.page.update()
            return  # Invalid input, show a warning and do nothing

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
    fluid_name_input = ft.TextField(label="Fluid Name", on_change=validate_fluid_name)
    fluid_dosage_input = ft.TextField(label="Dosage (mL)", on_change=validate_fluid_dosage)
    fluid_stock_input = ft.TextField(label="Stock (mL)", on_change=validate_fluid_stock)

    add_fluid_button = ft.ElevatedButton(text="Add", on_click=add_fluid_item)
    cancel_fluid_button = ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog(e, add_fluid_dialog))

    add_fluid_dialog = ft.AlertDialog(
        title=ft.Text("Add Fluid Medication"),
        content=ft.Column(
            [
                fluid_name_input,
                fluid_dosage_input,
                fluid_stock_input,
            ],
            spacing=10,
        ),
        actions=[add_fluid_button, cancel_fluid_button],
        modal=True,
    )

    # Input field for editing stock
    edit_stock_input = ft.TextField(label="Edit Stock (mL)", autofocus=True)

    # Dialog for editing fluid stock
    edit_fluid_dialog = ft.AlertDialog(
        title=ft.Text("Edit Fluid Medication Stock"),
        content=ft.Column([edit_stock_input]),
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
