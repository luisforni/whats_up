import flet as ft
import requests

BASE_URL = "http://127.0.0.1:8000/api/chat"
USERS_URL = "http://127.0.0.1:8000/api/users/nearby"

def chat_view(page: ft.Page, user_id, navigate_to_posts):
    chat_list = ft.Column()
    message_input = ft.TextField(label="Escribe tu mensaje", multiline=False)
    messages_list = ft.Column()
    current_chat_id = None  # Para rastrear el chat actual

    # Obtener la lista de chats del usuario
    def fetch_chats():
        response = requests.get(f"{BASE_URL}/chats/{user_id}")
        if response.status_code == 200:
            chats = response.json()
            chat_list.controls.clear()
            for chat in chats:
                chat_button = ft.ElevatedButton(
                    f"Chat con {chat['user2_id'] if chat['user1_id'] == user_id else chat['user1_id']}",
                    on_click=lambda e, chat_id=chat['id']: select_chat(chat_id),
                )
                chat_list.controls.append(chat_button)
            page.update()

    # Seleccionar un chat y obtener los mensajes
    def select_chat(chat_id):
        nonlocal current_chat_id
        current_chat_id = chat_id
        fetch_messages(chat_id)

    # Obtener los mensajes de un chat específico
    def fetch_messages(chat_id):
        response = requests.get(f"{BASE_URL}/messages/{chat_id}")
        if response.status_code == 200:
            messages = response.json()
            messages_list.controls.clear()
            for message in messages:
                messages_list.controls.append(ft.Text(f"{message['sender_id']}: {message['content']}"))
            page.update()

    # Enviar un mensaje
    def send_message(e):
        if current_chat_id is not None:
            response = requests.post(f"{BASE_URL}/messages", json={
                "chat_id": current_chat_id,
                "sender_id": user_id,
                "content": message_input.value
            })
            if response.status_code == 200:
                message_input.value = ""
                fetch_messages(current_chat_id)

    # Obtener usuarios cercanos
    def fetch_nearby_users():
        response = requests.get(f"{USERS_URL}?user_id={user_id}&latitude=40.7128&longitude=-74.0060&radius=2")
        if response.status_code == 200:
            users = response.json()
            return [ft.PopupMenuItem(text=f"{user['email']} ({user['distance']} km)") for user in users]
        else:
            return [ft.PopupMenuItem(text="No se encontraron usuarios cercanos")]

    # Inicializar la lista de chats al cargar la vista
    fetch_chats()

    # Botón de menú para usuarios cercanos
    nearby_users_button = ft.PopupMenuButton(
        items=fetch_nearby_users(),
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Chats", size=24),
                    ft.ElevatedButton("Home", on_click=lambda e: navigate_to_posts()),
                    nearby_users_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            chat_list,
            ft.Divider(),
            ft.Text("Mensajes", size=24),
            messages_list,
            message_input,
            ft.ElevatedButton("Enviar", on_click=send_message),
        ]
    )
