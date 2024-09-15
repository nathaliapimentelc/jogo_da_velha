import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    select_icon = None

    def switch_player(icon: ft.Icon):
        players.controls.append(ft.Row([icon, ft.Text(icon.tooltip)]))
        players.update()
  
    page.pubsub.subscribe(switch_player)

    def select_player_click(e):
        if user.value != '':
            icon : ft.Icon = ft.Icon(
                name=e.control.icon,
                color=e.control.icon_color,
                size=e.control.icon_size,
                tooltip = user.value
            )            
            page.pubsub.send_all(icon)
            for icon in x_or_o.controls:
                if e.control.icon == icon.icon:
                    e.control.visible = False
            page.update()
        else:
            page.open(
                ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("Digite seu Nome"),
                )
            )
        
    players = ft.Column()
    

    user = ft.TextField(hint_text="seu nome")

    x_or_o = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.CIRCLE_OUTLINED,
                icon_color=ft.colors.GREEN_ACCENT_400,
                on_click=select_player_click
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE_OUTLINED,
                icon_color=ft.colors.RED,
                on_click=select_player_click
            ),
        ]
    )
    
    page.add(players, ft.Row([user, x_or_o]))


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)