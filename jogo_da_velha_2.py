import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    player_1 = None
    player_2 = None
    player_now = None

    def switch(arg):
        topic = arg.get('topic')
        value = arg.get('value')
        match topic:
            case "select_player":
                select_player(value)
            case "switch_player":
                switch_player(value)

    def select_player(player):
        player_now = player.data
        for play in players.controls:
            color = ft.colors.RED if play.data == player_now else ft.colors.TRANSPARENT
            play.border = ft.border.all(width=2, color=color)
        page.update()


    def switch_player(item : str):
        name, icon = item.split()
        icon_color = ft.colors.GREEN_ACCENT_400 if ft.icons.CIRCLE_OUTLINED == icon else ft.colors.BLUE_ACCENT_400
        players.controls.append(ft.Row(
            [
                ft.Icon(name=icon, size=50, tooltip=name, color=icon_color),
                ft.Text(name)
            ]
        ))
        select_icon(icon)
        
        if len(players.controls) == 2:
            player_1 = players.controls.pop(0)
            player_now = player_1.controls[-1].value 
            player_1 = ft.Container(content=player_1, bgcolor=ft.colors.RED, data=player_1.controls[-1].value)

            player_2 = players.controls.pop(0)
            player_2 = ft.Container(content=player_2, bgcolor=ft.colors.GREY, data=player_2.controls[-1].value)

            players.controls.append(player_1)
            players.controls.append(player_2)
            value = {
                'topic': 'select_player',
                'value': player_1
            }
            page.pubsub.send_all(value)

        page.update()
  
    page.pubsub.subscribe(switch)

    def select_player_click(e):
        if user.value != '':
            value = {
                'topic': 'switch_player',
                'value': f"{user.value} {e.control.icon}"
            }
            page.pubsub.send_all(value)
            page.controls.pop()
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
                on_click=select_player_click,
                icon_size=50,
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE_OUTLINED,
                icon_color=ft.colors.BLUE_ACCENT_400,
                on_click=select_player_click,
                icon_size=50
            ),
        ]
    )

    def select_icon(icon_):
        index = 0
        for item in x_or_o.controls:
            if item.icon == icon_:
                x_or_o.controls.pop(index)
                break
            index += 1
    
    def line(icon):
       icon.color = ft.colors.ORANGE
       players.controls.append(ft.Row([icon], alignment=ft.MainAxisAlignment.CENTER))
       page.update()
    
    # page.pubsub.subscribe_topic('teste', line)



    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(players, ft.Row([user, x_or_o], alignment=ft.MainAxisAlignment.CENTER))


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)