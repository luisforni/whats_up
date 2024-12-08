import flet as ft
import requests

BASE_URL = "http://127.0.0.1:8000/api/profiles"

def profile_view(page, user_id, navigate_to_posts):
    first_name = ft.TextField(label="Nombre")
    last_name = ft.TextField(label="Apellido")
    birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)")
    bio = ft.TextField(label="Biografía", multiline=True, max_length=500)

    profile_exists = False

    # Cargar los datos existentes del perfil
    def fetch_profile():
        nonlocal profile_exists
        print(f"Fetching profile for user_id: {user_id}")  # Debug
        response = requests.get(f"{BASE_URL}/{user_id}")
        print(f"Response: {response.status_code} - {response.text}")  # Debug
        if response.status_code == 200:
            profile = response.json()
            if isinstance(profile, dict):
                first_name.value = profile.get("first_name", "")
                last_name.value = profile.get("last_name", "")
                birth_date.value = profile.get("birth_date", "")
                bio.value = profile.get("bio", "")
                profile_exists = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Respuesta inválida del servidor"))
                page.snack_bar.open = True
        elif response.status_code == 404:
            profile_exists = False
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al cargar el perfil"))
            page.snack_bar.open = True
        page.update()

    # Guardar o actualizar el perfil
    def save_profile(e):
        if not all([first_name.value.strip(), last_name.value.strip(), birth_date.value.strip()]):
            page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        profile_data = {
            "user_id": user_id,
            "first_name": first_name.value,
            "last_name": last_name.value,
            "birth_date": birth_date.value,
            "bio": bio.value,
        }

        if profile_exists:
            # Actualizar perfil
            response = requests.put(f"{BASE_URL}/{user_id}", json=profile_data)
        else:
            # Crear perfil
            response = requests.post(BASE_URL, json=profile_data)

        if response.status_code in [200, 201]:
            navigate_to_posts()
        else:
            error_message = response.json().get("detail", "Error al guardar el perfil")
            page.snack_bar = ft.SnackBar(ft.Text(error_message))
            page.snack_bar.open = True
        page.update()

    # Cargar los datos al inicializar la vista
    fetch_profile()

    return ft.Column(
        [
            ft.Text("Completar o Modificar Perfil", size=24),
            first_name,
            last_name,
            birth_date,
            bio,
            ft.Row(
                [
                    ft.ElevatedButton("Guardar", on_click=save_profile),
                    ft.ElevatedButton("Home", on_click=lambda e: navigate_to_posts()),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ]
    )
