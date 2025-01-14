import flet as ft



def main(page: ft.Page):
    page.title = "DashDog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
    matriz = []
    player_1 = None
    player_2 = None
    player_now = None
    size = page.height/2
    space = 10
    board_content = ft.Row(controls=[], spacing=space)
    
    def get_block(size, data):
        def click_me(e):
            global player_now
            if user.icon == player_now :
                value = {
                    'topic': 'select_block',
                    'value': e.control.data
                }
                page.pubsub.send_all(value)

        return ft.Container(
            width=size,
            height=size, 
            alignment=ft.alignment.center, 
            bgcolor=ft.colors.WHITE,
            content=ft.IconButton(
                on_click=click_me,
                data=data,
                icon_size=size*0.9,
                icon=ft.icons.SWIPE_DOWN, 
                icon_color=ft.colors.TRANSPARENT
            )
        )
    
    for i in range(3):
        col = ft.Column(controls=[], spacing=space)
        for j in range(3):
            block = get_block(size/3, f'{i} {j}')
            col.controls.append(block)
        board_content.controls.append(col)
    board = ft.Container(
        content = board_content,
        width=size + (space*2),
        height=size + (space*2),
        bgcolor=ft.colors.GREY,
        visible=False
    )

    _O_ = ft.Icon(ft.icons.CIRCLE_OUTLINED, color=ft.colors.GREEN_ACCENT_400, size=50)
    _X_ = ft.Icon(ft.icons.CLOSE_OUTLINED , color=ft.colors.BLUE_ACCENT_400 , size=50)
    
    def select_player(player):
        global player_now
        player_now = player
        for play in page.controls[0].content.controls:
            color = ft.colors.RED if play.data == player_now else ft.colors.TRANSPARENT
            play.border = ft.border.all(width=2, color=color)
        page.update()

    def select_block(lin, col):
        global player_now, matriz
        matriz[lin][col] = 'O' if player_now == _O_.name else 'X'
        
        content = _O_ if player_now == _O_.name else _X_
        container = page.controls[1].content.controls[lin].controls[col]
        container.content = content
        container.on_click = False
        container.update()

        prox = _X_.name if player_now == _O_.name else _O_.name
        value = {
            'topic': 'select_player',
            'value': prox
        }
        page.pubsub.send_all(value)


     # ==================== Stage 3 ====================



    def create_board(items: str):
        global player_now, player_1, player_2, matriz
        p1_ID, p1_icon, p2_ID, p2_icon = items.split(':')
        icon1 = p1_icon
        icon2 = p2_icon
        player_now = p1_icon
        p1_icon = _O_ if p1_icon == _O_.name else _X_
        player_1 = ft.Row([p1_icon, ft.Text(p1_ID, size=size*0.1)], alignment=ft.MainAxisAlignment.CENTER)
        player_1 = ft.Container(player_1, data=icon1, width=size/1.5, border=ft.border.all(2, color=ft.colors.TRANSPARENT))

        p2_icon = _O_ if p2_icon == _O_.name else _X_
        player_2 = ft.Row([p2_icon, ft.Text(p2_ID, size=size*0.1)], alignment=ft.MainAxisAlignment.CENTER)
        player_2 = ft.Container(player_2, data=icon2, width=size/1.5, border=ft.border.all(2, color=ft.colors.TRANSPARENT))
        line = ft.Column([player_1, player_2], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.controls[0] = ft.Container(content=line, width=size + (space*2))

        board.visible = True
        page.update()
        select_player(player_now)

        matriz = [[None, None, None],
                  [None, None, None],
                  [None, None, None]]

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
            case "select_block":
                lin, col = map(int, str(value).split())
                select_block(lin, col)

    page.pubsub.subscribe(switch)

    user = ft.TextField(icon=None, value=page.session_id, visible=False)
    players = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
    page.add(players, board, ft.Row([user, x_or_o], alignment=ft.MainAxisAlignment.CENTER))

if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER,port=8080)