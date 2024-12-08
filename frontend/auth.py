import flet as ft
import requests

BASE_URL = "http://127.0.0.1:8000/api/auth"

def signup_view(page: ft.Page, on_show_login):
    email = ft.TextField(label="Correo electrónico")
    password = ft.TextField(label="Contraseña", password=True)

    def signup_action(e):
        response = requests.post(f"{BASE_URL}/signup", json={
            "email": email.value,
            "password": password.value
        })
        if response.status_code == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Registro exitoso"))
            page.snack_bar.open = True
            on_show_login()  # Navega al login tras el registro exitoso
        else:
            error_message = response.json().get("detail", "Error en el registro")
            page.snack_bar = ft.SnackBar(ft.Text(error_message))
            page.snack_bar.open = True
        page.update()

    return ft.Column(
        [
            ft.Text("Registro", size=24),
            email,
            password,
            ft.ElevatedButton("Registrar", on_click=signup_action),
            ft.TextButton("¿Ya tienes una cuenta? Inicia sesión", on_click=lambda e: on_show_login()),
        ]
    )

def login_view(page: ft.Page, on_login, on_show_signup):
    email = ft.TextField(label="Correo electrónico")
    password = ft.TextField(label="Contraseña", password=True)

    def login_action(e):
        response = requests.post(f"{BASE_URL}/login", json={
            "email": email.value,
            "password": password.value
        })
        if response.status_code == 200:
            user = response.json()  # Asegúrate de que este JSON contiene la clave 'id'
            on_login(user)
        else:
            error_message = response.json().get("detail", "Credenciales incorrectas")
            page.snack_bar = ft.SnackBar(ft.Text(error_message))
            page.snack_bar.open = True
        page.update()

    return ft.Column(
        [
            ft.Text("Iniciar Sesión", size=24),
            email,
            password,
            ft.ElevatedButton("Iniciar Sesión", on_click=login_action),
            ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda e: on_show_signup()),
        ]
    )
