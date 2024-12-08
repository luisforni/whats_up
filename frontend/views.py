from profile import profile_view
from posts import posts_view

def navigate_to_profile(page, user_id, on_login, show_signup):
    page.views.clear()
    page.views.append(ft.View("/profile", [profile_view(page, user_id, on_login, show_signup)]))
    page.update()

def navigate_to_posts(page, user_id, on_login, show_signup):
    page.views.clear()
    page.views.append(ft.View("/posts", [posts_view(page, user_id, on_login, show_signup)]))
    page.update()
