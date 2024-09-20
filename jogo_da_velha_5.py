import flet as ft

def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
    
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

    _O_ = ft.Icon(ft.icons.CIRCLE_OUTLINED, color=ft.colors.GREEN_ACCENT_400, size=50)
    _X_ = ft.Icon(ft.icons.CLOSE_OUTLINED , color=ft.colors.BLUE_ACCENT_400 , size=50)
    
    def select_player(player):
        player_now = player.data
        for play in players.controls:
            color = ft.colors.RED if play.data == player_now else ft.colors.TRANSPARENT
            play.border = ft.border.all(width=2, color=color)
        page.update()


     # ==================== Stage 3 ====================

    def get_block(size):
        def click_me(e):
            print(f"user: {user.value} - play_now: {player_now} - CELL: {e.control.data}")

        return ft.Container(width=size, height=size, alignment=ft.alignment.center, bgcolor=ft.colors.WHITE, on_click=click_me)


    def create_board(items: str):
        p1_ID, p1_icon, p2_ID, p2_icon = items.split(':')
        p1_icon = _O_ if p1_icon == _O_.name else _X_
        player_1 = ft.Row([p1_icon, ft.Text("Player 1", size=size*0.1)], alignment=ft.MainAxisAlignment.CENTER)
        player_1 = ft.Container(player_1, data=p1_ID, width=size/1.5, border=ft.border.all(2, color=ft.colors.TRANSPARENT))

        p2_icon = _O_ if p2_icon == _O_.name else _X_
        player_2 = ft.Row([p2_icon, ft.Text("Player 2", size=size*0.1)], alignment=ft.MainAxisAlignment.CENTER)
        player_2 = ft.Container(player_2, data=p2_ID, width=size/1.5, border=ft.border.all(2, color=ft.colors.TRANSPARENT))
        line = ft.Column([player_1, player_2], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.controls[0] = ft.Container(content=line, width=size + (space*2))
        player_now = p1_ID

        board_content = ft.Row(controls=[], spacing=space)
        for i in range(3):
            col = ft.Column(controls=[], spacing=space)
            for j in range(3):
                block = get_block(size/3)
                block.data = f'{i} {j} {None}'
                col.controls.append(block)
            board_content.controls.append(col)

        board.visible = True
        board.content = board_content
        page.update()


     # ==================== Stage 2 ====================

    def get_players():
        player_1 = players.controls.pop(0)
        player_1_icon = player_1.controls[0].name
        player_1_name = player_1.controls[-1].value

        player_2 = players.controls.pop(0)
        player_2_icon = player_2.controls[0].name
        player_2_name = player_2.controls[-1].value

        return f"{player_1_name}:{player_1_icon}:{player_2_name}:{player_2_icon}"


    def switch_player(icon : str):
        name = "Player 1" if len(players.controls) == 0 else "Player 2"
        icon_ = _O_ if _O_.name == icon else _X_
        players.controls.append(ft.Row([icon_, ft.Text(name)]))
        
        index = 0 if x_or_o.controls[0].icon == icon else 1
        x_or_o.controls.pop(index)

        
        if len(players.controls) == 2:
            value = {
                'topic': 'create_board',
                'value': get_players()
            }
            page.pubsub.send_all(value)
        
        page.update()


     # ==================== Stage 1 ====================

    def select_player_click(e):
        user.icon = e.control.icon
        value = {
            'topic': 'switch_player',
            'value': e.control.icon
        }
        page.pubsub.send_all(value)
        page.controls.pop()
        page.update()


    x_or_o = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.CIRCLE_OUTLINED,
                icon_color=ft.colors.GREEN_ACCENT_400,
                icon_size=50,
                on_click=select_player_click,
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE_OUTLINED,
                icon_color=ft.colors.BLUE_ACCENT_400,
                icon_size=50,
                on_click=select_player_click,
            ),
        ]
    )


    def switch(arg):
        '''
            seleção de funcionalidade
        '''
        topic = arg.get('topic')
        value = arg.get('value')
        match topic:
            case "select_player":
                select_player(value)
            case "switch_player":
                switch_player(value)
            case "create_board":
                create_board(value)


    page.pubsub.subscribe(switch)

    user = ft.TextField(icon=None, value=page.session_id, visible=False)
    players = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    page.add(players, board, ft.Row([user, x_or_o], alignment=ft.MainAxisAlignment.CENTER))

if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)