import flet as ft
import chess
from PIL import Image, ImageDraw
import io, base64

def render_board(board):
    square_size = 60
    board_size = square_size * 8
    img = Image.new("RGB", (board_size, board_size), "white")
    draw = ImageDraw.Draw(img)

    light = (240, 217, 181)
    dark = (181, 136, 99)

    for rank in range(8):
        for file in range(8):
            x0 = file * square_size
            y0 = rank * square_size
            x1 = x0 + square_size
            y1 = y0 + square_size
            color = light if (rank + file) % 2 == 0 else dark
            draw.rectangle([x0, y0, x1, y1], fill=color)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.square_file(square)
            rank = 7 - chess.square_rank(square)
            x = file * square_size + 15
            y = rank * square_size + 15
            draw.text((x, y), piece.symbol(), fill="black")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def Jugar(page: ft.Page, jugador1="Jugador 1", jugador2="Jugador 2"):
    board = chess.Board()

    img = ft.Image(src=f"data:image/png;base64,{render_board(board)}", width=480, height=480)
    move_input = ft.TextField(label="Movimiento (ej: e2e4)", width=200)

    turn_text = ft.Text(value=f"Turno: {jugador1} (Blancas)", size=20, weight="bold")
    status_text = ft.Text(value="", size=18, color="red")

    def make_move(e):
        try:
            move = chess.Move.from_uci(move_input.value)
            if move in board.legal_moves:
                board.push(move)
                img.src = f"data:image/png;base64,{render_board(board)}"

                # Actualizar turno
                if board.turn == chess.WHITE:
                    turn_text.value = f"Turno: {jugador1} (Blancas)"
                else:
                    turn_text.value = f"Turno: {jugador2} (Negras)"

                # Revisar estado del juego
                if board.is_checkmate():
                    ganador = jugador1 if board.turn == chess.BLACK else jugador2
                    perdedor = jugador2 if ganador == jugador1 else jugador1
                    # Mostrar mensaje en pantalla
                    status_text.value = f"Victoria de {ganador} sobre {perdedor}"
                    # Guardar frase completa en archivo
                    f = open("ganadores.txt", "a")
                    f.write(f"Victoria de {ganador} sobre {perdedor}\n")
                    f.close()

                elif board.is_stalemate():
                    # Mostrar mensaje en pantalla
                    status_text.value = f"Empate entre {jugador1} y {jugador2}"
                    # Guardar frase completa en archivo
                    f = open("ganadores.txt", "a")
                    f.write(f"Empate entre {jugador1} y {jugador2}\n")
                    f.close()
      

                elif board.is_check():
                    status_text.value = "¡Jaque!"
                else:
                    status_text.value = ""

                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Movimiento ilegal"))
                page.snack_bar.open = True
                page.update()
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Formato incorrecto"))
            page.snack_bar.open = True
            page.update()

    play_button = ft.ElevatedButton(
        content=ft.Text("Mover"),
        on_click=make_move
    )

    page.controls.clear()
    page.add(img, move_input, play_button, turn_text, status_text)
    page.update()
