import flet as ft
from play import Play

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    player_1 = None
    player_2 = None
    player_now = None

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
        
        page.update()
        
        if len(players.controls) == 2:
            player_1 = players.controls.pop(0)
            player_1 = ft.Container(content=player_1, data=player_1.controls[-1].value)

            player_2 = players.controls.pop(0)
            player_2 = ft.Container(content=player_2, data=player_2.controls[-1].value)

            
            _play = Play(page, user.value, player_1, player_2)
            #page.controls.clear()
            page.controls.append(_play)
            page.pubsub.unsubscribe()
            #page.pubsub.subscribe(select_player)
            #page.update()
            #page.pubsub.send_all(player_1)
            page.update()
            
            






  
    page.pubsub.subscribe(switch_player)

    def select_player_click(e):
        if user.value != '':
            page.pubsub.send_all(f"{user.value} {e.control.icon}")
            page.controls.pop()
            # page.pubsub.send_all_on_topic("teste", icon)
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