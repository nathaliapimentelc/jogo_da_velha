import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT

    def on_message(msg):
        messages.controls.append(ft.Text(msg))
        page.update()
    
    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(f"{user.value}: {message.value}")
        message.value = ""
        page.update()
    
    
    messages = ft.Column()
    user = ft.TextField(hint_text="seu nome")
    message = ft.TextField(hint_text="sua mensagem...", expand=True)
    send = ft.ElevatedButton(text="Enviar", on_click=send_click)
    page.add(messages, ft.Row([user, message, send]))


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)