import flet as ft
import requests

BASE_URL = "http://127.0.0.1:8000/api/posts"

def posts_view(page, user_id, navigate_to_profile, navigate_to_chat, on_logout):
    post_input = ft.TextField(label="Escribe tu post", multiline=True, max_length=500)
    posts_list = ft.Column()

    # Obtener las publicaciones
    def fetch_posts(e=None):  # Maneja el argumento `e` aunque no se utilice
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                posts = response.json()
                posts_list.controls.clear()
                for post in posts:
                    posts_list.controls.append(ft.Text(f"{post['user_id']}: {post['content']}"))
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al cargar publicaciones"))
                page.snack_bar.open = True
                page.update()
        except requests.RequestException as err:
            print(f"Error al conectar al backend: {err}")
            page.snack_bar = ft.SnackBar(ft.Text("Error de conexión con el servidor"))
            page.snack_bar.open = True

    # Crear una nueva publicación
    def create_post(e):
        content = post_input.value.strip()
        if not content:
            page.snack_bar = ft.SnackBar(ft.Text("El contenido del post no puede estar vacío"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            response = requests.post(BASE_URL, json={"user_id": user_id, "content": content})
            if response.status_code == 201:
                post_input.value = ""  # Limpiar el campo de entrada
                fetch_posts()  # Actualizar la lista de publicaciones
            else:
                # Este caso no debería ocurrir si el código 201 se maneja correctamente
                print(f"Error al crear el post: {response.text}")
                page.snack_bar = ft.SnackBar(ft.Text("Error inesperado al crear el post"))
                page.snack_bar.open = True
        except requests.RequestException as err:
            print(f"Error en la solicitud: {err}")
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo conectar al servidor"))
            page.snack_bar.open = True
        page.update()

    # Botones de navegación
    profile_button = ft.ElevatedButton(
        "Modificar Perfil", on_click=lambda e: navigate_to_profile()
    )
    chat_button = ft.ElevatedButton(
        "Chat", on_click=lambda e: navigate_to_chat()
    )
    logout_button = ft.ElevatedButton(
        "Cerrar Sesión", on_click=lambda e: on_logout()
    )

    # Inicializar publicaciones
    fetch_posts()

    return ft.Column(
        [
            ft.Text("Publicaciones", size=24),
            post_input,
            ft.ElevatedButton("Publicar", on_click=create_post),
            ft.Row([profile_button, chat_button, logout_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Divider(),
            posts_list,
        ]
    )
