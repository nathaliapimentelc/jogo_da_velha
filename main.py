import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(ft.Row([ft.Icon(name=ft.icons.APPLE, size=35, color=ft.colors.BLACK)]))


if __name__ == "__main__":
    ft.app(main)