import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Основное окно
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x450")
window.resizable(False, False)
window.configure(bg="#f0f0f0")

# Переменные игры
current_player = "X"
player_symbol = "X"
computer_symbol = "0"
buttons = []
x_wins = 0
o_wins = 0
game_active = True

# Стили
style = ttk.Style()
style.configure("TButton", font=("Arial", 16), padding=10)
style.configure("Title.TLabel", font=("Arial", 18, "bold"), background="#f0f0f0")
style.configure("Score.TLabel", font=("Arial", 12), background="#f0f0f0")

# Фреймы
title_frame = ttk.Frame(window)
title_frame.pack(pady=10)

score_frame = ttk.Frame(window)
score_frame.pack(pady=5)

board_frame = ttk.Frame(window)
board_frame.pack(pady=10)

control_frame = ttk.Frame(window)
control_frame.pack(pady=10)

# Элементы интерфейса
title_label = ttk.Label(title_frame, text="Крестики-Нолики", style="Title.TLabel")
title_label.pack()

x_score_label = ttk.Label(score_frame, text="X: 0", style="Score.TLabel")
x_score_label.pack(side=tk.LEFT, padx=10)

o_score_label = ttk.Label(score_frame, text="O: 0", style="Score.TLabel")
o_score_label.pack(side=tk.RIGHT, padx=10)

def create_board():
    global buttons
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24),
                width=3,
                height=1,
                bg="#ffffff",
                relief="ridge",
                borderwidth=2,
                command=lambda r=i, c=j: on_click(r, c)
            )
            btn.grid(row=i, column=j, padx=5, pady=5)
            row.append(btn)
        buttons.append(row)


def reset_game():
    global current_player, game_active
    current_player = "X"
    game_active = True
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="#ffffff")
    update_turn_indicator()


def check_winner():
    # Проверка строк и столбцов
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            highlight_winner(i, 0, i, 1, i, 2)
            return buttons[i][0]['text']
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            highlight_winner(0, i, 1, i, 2, i)
            return buttons[0][i]['text']

    # Проверка диагоналей
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        highlight_winner(0, 0, 1, 1, 2, 2)
        return buttons[0][0]['text']
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        highlight_winner(0, 2, 1, 1, 2, 0)
        return buttons[0][2]['text']

    # Проверка на ничью
    if all(btn['text'] != "" for row in buttons for btn in row):
        return "draw"

    return None


def highlight_winner(r1, c1, r2, c2, r3, c3):
    buttons[r1][c1].config(bg="#a5d6a7")
    buttons[r2][c2].config(bg="#a5d6a7")
    buttons[r3][c3].config(bg="#a5d6a7")


def update_score():
    x_score_label.config(text=f"X: {x_wins}")
    o_score_label.config(text=f"O: {o_wins}")


def update_turn_indicator():
    title_label.config(text=f"Крестики-Нолики (Ход: {current_player})")


def on_click(row, col):
    global current_player, game_active, x_wins, o_wins

    if not game_active or buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player
    buttons[row][col].config(fg="#333333")

    winner = check_winner()

    if winner:
        game_active = False
        if winner == "X":
            x_wins += 1
            messagebox.showinfo("Победа!", "Игрок X победил!")
        elif winner == "0":
            o_wins += 1
            messagebox.showinfo("Победа!", "Игрок O победил!")
        else:
            messagebox.showinfo("Ничья!", "Игра окончена вничью!")

        update_score()

        if x_wins >= 3 or o_wins >= 3:
            final_winner = "X" if x_wins >= 3 else "O"
            messagebox.showinfo("Конец игры!", f"Игрок {final_winner} выиграл серию до 3 побед!")
            x_wins = 0
            o_wins = 0
            update_score()

        window.after(1000, reset_game)
    else:
        current_player = "0" if current_player == "X" else "X"
        update_turn_indicator()


def choose_symbol(symbol):
    global player_symbol, computer_symbol, current_player
    player_symbol = symbol
    computer_symbol = "0" if symbol == "X" else "X"
    current_player = "X"  # X всегда ходит первым
    symbol_window.destroy()
    update_turn_indicator()


def show_symbol_chooser():
    global symbol_window
    symbol_window = tk.Toplevel(window)
    symbol_window.title("Выбор символа")
    symbol_window.geometry("350x450")
    symbol_window.resizable(False, False)

    label = ttk.Label(symbol_window, text="Выберите, чем будете играть:", font=("Arial", 12))
    label.pack(pady=10)

    x_btn = ttk.Button(symbol_window, text="Крестики (X)", command=lambda: choose_symbol("X"))
    x_btn.pack(pady=5)

    o_btn = ttk.Button(symbol_window, text="Нолики (O)", command=lambda: choose_symbol("0"))
    o_btn.pack(pady=5)


# Кнопки управления
reset_btn = ttk.Button(control_frame, text="Новая игра", command=reset_game)
reset_btn.pack(side=tk.LEFT, padx=5)

symbol_btn = ttk.Button(control_frame, text="Выбор символа", command=show_symbol_chooser)
symbol_btn.pack(side=tk.RIGHT, padx=5)

# Инициализация игры
create_board()
update_turn_indicator()
show_symbol_chooser()

window.mainloop()