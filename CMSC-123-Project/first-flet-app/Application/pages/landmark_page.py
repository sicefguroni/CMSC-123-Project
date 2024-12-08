import flet as ft
from pharmacies_db import pharmacies

class LandmarkPage:
    def __init__(self, page: ft.Page):
        # Expanded pharmacy database with more details
        self.pharmacies = pharmacies
        self.page = page
    
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
        """Create a card for each pharmacy"""
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
                    ])
                ], 
                spacing=5),
                padding=10
            ),
            elevation=2,
            width=360
        )
    
    def landmark_page(self):
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
            pharmacies_container.update()
        
        search_button = ft.SearchBar(
            bar_hint_text="Search Pharmacies", 
            on_change=search_pharmacies,
            width=350
        )
        
        # Main container
        landmark_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Pharmacy Finder", size=24, weight=ft.FontWeight.BOLD),
                            search_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10),
                        padding=20
                    ),
                    results_container
                ],
                spacing=0,
                expand=True
            ),
            width=400,
            visible=False
        )
        
        return landmark_container

# Usage in main app
def landmark_page():
    landmark = LandmarkPage(ft.Page)
    return landmark.landmark_page()