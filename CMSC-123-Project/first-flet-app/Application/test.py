import flet as ft


class GPSMockApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.grid_size = 10  # Define the road grid size (10x10)
        self.grid = []  # Store the grid cells
        self.start_pin = None
        self.end_pin = None

    def create_road_grid(self):
        """Creates a road grid layout resembling streets."""
        grid_container = ft.Column(spacing=0)

        for row in range(self.grid_size):
            row_cells = ft.Row(spacing=0)
            for col in range(self.grid_size):
                # Default road style (gray background, border for streets)
                cell = ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.BLUE,
                    border=ft.border.all(1, ft.colors.BLACK),
                    alignment=ft.alignment.center,
                )
                self.grid.append((row, col, cell))
                row_cells.controls.append(cell)
            grid_container.controls.append(row_cells)

        return grid_container

    def place_pin(self, location, pin_type):
        """Places a pin on the road grid."""
        try:
            # Convert the location to grid coordinates
            row, col = map(int, location.split(","))
            if row < 0 or col < 0 or row >= self.grid_size or col >= self.grid_size:
                raise ValueError("Invalid location")

            # Find the cell in the grid
            for r, c, cell in self.grid:
                if r == row and c == col:
                    # Update pin style based on type
                    if pin_type == "start":
                        cell.content = ft.Icon(name=ft.icons.LOCATION_ON, color=ft.colors.GREEN, size=30)
                        self.start_pin = (row, col)
                    elif pin_type == "end":
                        cell.content = ft.Icon(name=ft.icons.FLAG, color=ft.colors.RED, size=30)
                        self.end_pin = (row, col)
                    cell.update()
                    break
        except Exception as e:
            print(f"Error placing pin: {e}")

    def draw_route(self):
        """Draws a route between start and end pins."""
        if not self.start_pin or not self.end_pin:
            print("Both start and end pins must be set.")
            return

        start_row, start_col = self.start_pin
        end_row, end_col = self.end_pin

        # Draw a simple route
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1

        current_row, current_col = start_row, start_col
        while current_row != end_row:
            current_row += row_step
            for r, c, cell in self.grid:
                if r == current_row and c == start_col:
                    cell.bgcolor = ft.colors.YELLOW
                    cell.update()

        while current_col != end_col:
            current_col += col_step
            for r, c, cell in self.grid:
                if r == end_row and c == current_col:
                    cell.bgcolor = ft.colors.YELLOW
                    cell.update()

    def run(self):
        """Runs the main UI."""
        def set_start(e):
            self.place_pin(start_input.value, "start")

        def set_end(e):
            self.place_pin(end_input.value, "end")

        def draw_path(e):
            self.draw_route()

        # Input fields
        start_input = ft.TextField(label="Start Location (row,col)", width=200)
        end_input = ft.TextField(label="End Location (row,col)", width=200)

        # Buttons
        set_start_button = ft.ElevatedButton("Set Start", on_click=set_start)
        set_end_button = ft.ElevatedButton("Set End", on_click=set_end)
        draw_path_button = ft.ElevatedButton("Show Route", on_click=draw_path)

        # Layout
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Mock GPS App", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(controls=[start_input, set_start_button]),
                    ft.Row(controls=[end_input, set_end_button]),
                    ft.Row(controls=[draw_path_button]),
                    self.create_road_grid(),
                ],
                spacing=10,
                expand=True,
            )
        )


# Run the app
def main(page: ft.Page):
    app = GPSMockApp(page)
    app.run()


ft.app(target=main)
