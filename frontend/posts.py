import flet as ft
import requests

BASE_URL = "http://127.0.0.1:8000/api/posts"

def posts_view(page, user_id, navigate_to_profile, navigate_to_chat, on_logout):
    post_input = ft.TextField(label="Escribe tu post", multiline=True, max_length=500)
    posts_list = ft.Column()

    def fetch_posts():
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            posts = response.json()
            posts_list.controls.clear()
            for post in posts:
                posts_list.controls.append(ft.Text(f"{post['user_id']}: {post['content']}"))
            page.update()

    profile_button = ft.ElevatedButton(
        "Modificar Perfil", on_click=lambda e: navigate_to_profile()
    )
    chat_button = ft.ElevatedButton(
        "Chat", on_click=lambda e: navigate_to_chat()
    )
    logout_button = ft.ElevatedButton(
        "Cerrar Sesión", on_click=lambda e: on_logout()
    )

    fetch_posts()

    return ft.Column(
        [
            ft.Text("Publicaciones", size=24),
            post_input,
            ft.ElevatedButton("Publicar", on_click=fetch_posts),
            ft.Row([profile_button, chat_button, logout_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Divider(),
            posts_list,
        ]
    )
