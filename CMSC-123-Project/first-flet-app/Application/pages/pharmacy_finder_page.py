import flet as ft
from pharmacies_db import pharmacies

class PharmacyFinderPage:
    def __init__(self, page: ft.Page):
        # Expanded pharmacy database with more details
        self.pharmacies = pharmacies
        self.page = page
        self.container = self.pharmacy_finder_page()
    
    def search_pharmacies(self, search_term):
        """Find pharmacies based on flexible search term"""
        # Convert search term to lowercase
        search_term = search_term.lower()
        
        # Filter pharmacies based on keywords, name, address, or city
        matching_pharmacies = []
        for pharmacy in self.pharmacies:
            # Check if search term matches any keywords, name, address, or city
            if (search_term in pharmacy['name'].lower() or
                search_term in pharmacy['address'].lower() or
                search_term in pharmacy['city'].lower() or
                any(search_term in keyword for keyword in pharmacy['keywords'])):
                matching_pharmacies.append(pharmacy)
        
        return matching_pharmacies
    
    def create_pharmacy_card(self, pharmacy):
        """Create a clickalble card for each pharmacy"""
        def create_details_dialog(p):
            def show_details(e):
                def handle_dialog_action(action):
                    def _action(e):
                        if action == 'close':
                            if hasattr(self.page, 'dialog'):
                                self.page.dialog.open = False
                                self.page.update()
                    return _action
                
                dlg = ft.AlertDialog(
                    icon=ft.Icon(name=ft.icons.LOCAL_PHARMACY, color=ft.colors.PRIMARY),
                    title=ft.Text(pharmacy['name'], weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                # Pharmacy Image (Placeholder or Custom)
                                ft.Container(
                                    content=ft.Image(
                                        src=pharmacy.get('image', '/api/placeholder/350/200'),
                                        width=300,
                                        height=230,
                                        fit=ft.ImageFit.FIT_HEIGHT
                                    ),
                                    padding=5
                                ),
                                # Detailed Information
                                
                                ft.Row([
                                    ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.LOCATION_ON, size=17),
                                            ft.Text(
                                                f"Address: {pharmacy['address']}", 
                                                size=17, 
                                                max_lines=2,  # Prevent overflow in long addresses
                                            ),
                                        ],
                                        scroll=ft.ScrollMode.AUTO),
                                        ft.Row([
                                            ft.Icon(ft.icons.ALARM, size=17),
                                            ft.Text(f"Hours: {pharmacy['hours']}", size=17),
                                        ]),
                                        ft.Row([
                                            ft.Icon(ft.icons.PHONE, size=17),
                                            ft.Text(f"Phone: {pharmacy['phone']}", size=17),
                                        ]),
                                        ft.Row([
                                            ft.Icon(ft.icons.DIRECTIONS, size=17),
                                            ft.Text(f"Distance: {pharmacy['distance']}", size=17),
                                        ]),
                                    ],
                                    spacing=17,)
                                ],
                                scroll=ft.ScrollMode.AUTO),
                        
                            ],
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO  # Enable scrolling for overflowing content
                        ),
                        width=350,  # Set a maximum width for the dialog
                        height=400,  # Set a maximum height for the dialog
                    ),
                    actions=[
                        ft.TextButton("Close", on_click=lambda e: handle_dialog_action('close')(e)),
                    ],
                    modal=True,  # Ensures the dialog captures focus
                )

                self.page.dialog = dlg
                dlg.open = True
                self.page.update()
            return show_details

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.LOCAL_PHARMACY, color=ft.colors.PRIMARY),
                        ft.Text(pharmacy['name'], weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.LOCATION_ON, size=16),
                        ft.Text(pharmacy['address'], size=12)
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.ALARM, size=16),
                        ft.Text(f"Hours: {pharmacy['hours']}", size=12)
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.PHONE, size=16),
                        ft.Text(pharmacy['phone'], size=12)
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.DIRECTIONS, size=16),
                        ft.Text(pharmacy['distance'], size=12)
                    ])
                ], 
                spacing=5),
                padding=10,
                on_click=create_details_dialog(pharmacy)
            ),
            elevation=2,
            width=360
        )
    
    def pharmacy_finder_page(self):
        # Pharmacies list 
        pharmacies_container = ft.Column(spacing=10)
        
        # Scrollable results container
        results_container = ft.Container(
            content=ft.Column(
                controls=[pharmacies_container],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            padding=10,
            expand=True
        )

        # Search button
        def search_pharmacies(e):
            search_term = search_button.value
            
            # Clear previous results
            pharmacies_container.controls.clear()
            
            # Find matching pharmacies
            matching_pharmacies = self.search_pharmacies(search_term)
            
            if matching_pharmacies:
                # Create pharmacy cards
                for pharmacy in matching_pharmacies:
                    pharmacies_container.controls.append(
                        self.create_pharmacy_card(pharmacy)
                    )
            else:
                pharmacies_container.controls.append(
                    ft.Text("No pharmacies found", color=ft.colors.RED)
                )
            
            # Update the UI
            self.page.update()
        
        search_button = ft.SearchBar(
            bar_hint_text="Search Pharmacies", 
            on_change=search_pharmacies,
            width=360
        )
        
        # Main container
        pharmacy_finder_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            search_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10
                    ),
                    results_container
                ],
                spacing=0,
                expand=True
            ),
            width=400,
            visible=False
        )
        
        return pharmacy_finder_container

# Usage in main app
def pharmacy_finder_page(page: ft.Page):
    pharmacy_finder = PharmacyFinderPage(page)
    return pharmacy_finder.pharmacy_finder_page()