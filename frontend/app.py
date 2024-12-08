import flet as ft
import requests
from auth import login_view, signup_view
from posts import posts_view
from profile import profile_view
from chat import chat_view

BASE_URL = "http://127.0.0.1:8000/api/profiles"


def main(page: ft.Page):
    user_id = None

    def show_snack_bar(message):
        snack_bar = ft.SnackBar(ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def navigate_to_login():
        page.views.clear()
        page.views.append(ft.View("/login", [login_view(page, on_login, navigate_to_signup)]))
        page.update()

    def navigate_to_signup():
        page.views.clear()
        page.views.append(ft.View("/signup", [signup_view(page, navigate_to_login)]))
        page.update()

    def navigate_to_posts():
        page.views.clear()
        page.views.append(
            ft.View("/posts", [posts_view(page, user_id, navigate_to_profile, navigate_to_chat, on_logout)])
        )
        page.update()

    def navigate_to_profile():
        page.views.clear()
        page.views.append(ft.View("/profile", [profile_view(page, user_id, navigate_to_posts)]))
        page.update()

    def navigate_to_chat():
        page.views.clear()
        page.views.append(ft.View("/chat", [chat_view(page, user_id, navigate_to_posts)]))
        page.update()

    def on_logout():
        nonlocal user_id
        user_id = None
        navigate_to_login()

    def on_login(user):
        nonlocal user_id
        user_id = user["id"]

        # Verificar si el perfil existe
        response = requests.get(f"{BASE_URL}/{user_id}")
        if response.status_code == 200:
            # Si el perfil existe, ir a publicaciones
            navigate_to_posts()
        elif response.status_code == 404:
            # Si el perfil no existe, redirigir a completar perfil
            navigate_to_profile()
        else:
            # Mostrar error en caso de fallo inesperado
            show_snack_bar("Error al verificar el perfil")

    navigate_to_login()


ft.app(target=main)
