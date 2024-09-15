import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.add(ft.Row([ft.Icon(name=ft.icons.APPLE, size=35, color=ft.colors.BLACK)]))

ft.app(main)    