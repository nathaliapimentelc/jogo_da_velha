import flet as ft
from play import Play

_O_ = ft.Icon(ft.icons.CIRCLE_OUTLINED, color=ft.colors.GREEN_ACCENT_400, size=50)
_X_ = ft.Icon(ft.icons.CLOSE_OUTLINED , color=ft.colors.BLUE_ACCENT_400 , size=50)


def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    player_1 = None
    player_2 = None
    player_now = None
    size = page.height/2
    space = 10
    board = ft.Container(
        width=size + (space*2),
        height=size + (space*2),
        bgcolor=ft.colors.GREY,
        visible=False
    )
    

    def switch(arg):
        topic = arg.get('topic')
        value = arg.get('value')
        match topic:
            case "select_player":
                select_player(value)
            case "switch_player":
                switch_player(value)
            case "create_board":
                create_board(value)

    def select_player(player):
        player_now = player.data
        for play in players.controls:
            color = ft.colors.RED if play.data == player_now else ft.colors.TRANSPARENT
            play.border = ft.border.all(width=2, color=color)
        page.update()


    def get_block(size):
        def click_me(e):
            print(f"user: {user.value} - play_now: {player_now} - CELL: {e.control.data}")

        return ft.Container(width=size, height=size, alignment=ft.alignment.center, bgcolor=ft.colors.WHITE, on_click=click_me)


    def create_board(items: str):
        p1_name, p1_icon, p2_name, p2_icon = items.split()
        p1_icon = _O_ if p1_icon == ft.icons.CIRCLE_OUTLINED else _X_
        p2_icon = _O_ if p2_icon == ft.icons.CIRCLE_OUTLINED else _X_
        player_1 = ft.Container(ft.Row([p1_icon, ft.Text(p1_name, size=50)]), data=p1_name, width=size/2, border=ft.border.all(2))
        player_2 = ft.Container(ft.Row([p2_icon, ft.Text(p2_name, size=50)]), data=p2_name, width=size/2, border=ft.border.all(2))
        line = ft.Row([player_1, player_2], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        page.controls[0] = ft.Container(content=line, width=size + (space*2))
        player_now = p1_name
        board.visible = True
        page.update()

        line = ft.Row(controls=[], spacing=space)
        for i in range(3):
            col = ft.Column(controls=[], spacing=space)
            for j in range(3):
                block = get_block(size/3)
                block.data = f'{i} {j} {None}'
                col.controls.append(block)
            line.controls.append(col)

        board.content = line
        page.update()



        


    def select_icon(icon_):
        index = 0
        for item in x_or_o.controls:
            if item.icon == icon_:
                x_or_o.controls.pop(index)
                break
            index += 1

    def get_players():
        player_1 = players.controls.pop(0)
        player_1_icon = player_1.controls[0].name
        player_1_name = player_1.controls[-1].value

        player_2 = players.controls.pop(0)
        player_2_icon = player_2.controls[0].name
        player_2_name = player_2.controls[-1].value

        return f"{player_1_name} {player_1_icon} {player_2_name} {player_2_icon}"


    def switch_player(item : str):
        name, icon = item.split()
        icon_ = _O_ if ft.icons.CIRCLE_OUTLINED == icon else _X_
        players.controls.append(ft.Row([icon_, ft.Text(name)]))
        select_icon(icon)

        
        if len(players.controls) == 2:
            value = {
                'topic': 'create_board',
                'value': get_players()
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



    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(players, board, ft.Row([user, x_or_o], alignment=ft.MainAxisAlignment.CENTER))


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)