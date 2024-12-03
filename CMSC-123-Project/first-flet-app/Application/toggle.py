import flet as ft

def main(page: ft.Page):
    def on_submit(e):
        if not username.value.strip():
            username.error_text = "Username cannot be empty!"
        else:
            username.error_text = None
        if len(password.value) < 6:
            password.error_text = "Password must be at least 6 characters long!"
        else:
            password.error_text = None
        
        # Update the UI after setting error_text
        username.update()
        password.update()
        
        # If no errors, show a success message
        if username.error_text is None and password.error_text is None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Form submitted successfully!"),
                open=True
            )
            page.update()

    # TextFields
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, width=300)

    # Submit Button
    submit_btn = ft.ElevatedButton("Submit", on_click=on_submit)

    # Add components to the page
    page.add(username, password, submit_btn)

# Start the app
ft.app(main)
