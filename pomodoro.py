import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import math

# Definindo constantes de cores e tempos
PINK = "#e2979c"
RED = "#e7305b"
MUSTARD = "#ffba3f"
BLUE = "#2c456b"
BEGE = "#ece0d1"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Contadores
reps = 1
timer = None
timer_running = False
remaining_time = None

# Função para exibir mensagem de alerta ao redefinir o temporizador
def reset_timer():
    if messagebox.askokcancel("Reset Timer", "Tem certeza que deseja reiniciar o temporizador?"):
        stop_timer()
        canvas.itemconfig(timer_text, text="00:00")
        title_label.config(text="Timer")
        check_marks.config(text="")
        global reps, timer_running
        reps = 1
        timer_running = False
        start_button.config(text="Start", command=start_timer)

# Função para parar o temporizador
def stop_timer():
    app.after_cancel(timer)

# Função para reproduzir o som do alarme
def play_alarm():
    try:
        playsound("assets/bell.mp3", block=False)
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao reproduzir o som do alarme: {e}")

# Função para atualizar o temporizador
def count_down(count):
    minutos, segundos = divmod(count, 60)
    if segundos < 10:
        segundos = f"0{segundos}"
    canvas.itemconfig(timer_text, text=f"{minutos}:{segundos}")

    if count > 0:
        global timer
        timer = app.after(1000, count_down, count - 1)
    else:
        global reps, timer_running
        play_alarm()
        reps += 1
        start_timer()
        marks = 0
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += 1
        check_marks.config(text=f"{marks} sprint(s)")

        start_timer()


# Função para iniciar o temporizador
def start_timer():
    global timer_running, remaining_time
    timer_running = not timer_running

    if timer_running:
        start_button.config(text="Pause")
        continue_timer()
    else:
        start_button.config(text="Play")
        pause_timer()

# Função para pausar o temporizador
def pause_timer():
    global timer_running, remaining_time
    timer_running = False
    start_button.config(text="Play")
    app.after_cancel(timer)
    remaining_time = get_remaining_time()

# Função para obter o tempo restante do temporizador
def get_remaining_time():
    current_time_str = canvas.itemcget(timer_text, "text")
    current_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time_str.split(":"))))
    return current_time

# Função para continuar o temporizador
def continue_timer():
    global reps, remaining_time, timer_running
    if timer_running:
        if reps % 8 == 0:
            if remaining_time is not None and remaining_time != 0:  
                count_down(remaining_time)
            else:
                count_down(LONG_BREAK_MIN * 60)  
            title_label.config(text="Break", fg=RED)

        elif reps % 2 == 1:  # Ajuste para iniciar o temporizador após o foco e ao inicio
            if remaining_time is not None and remaining_time != 0:  
                count_down(remaining_time)
            else:
                count_down(WORK_MIN * 60)  
            title_label.config(text="Focus", fg=BLUE)

        else:
            if remaining_time is not None and remaining_time != 0:  
                count_down(remaining_time)
            else:
                count_down(SHORT_BREAK_MIN * 60)  
            title_label.config(text="Break", fg=PINK)

# Inicialização da interface gráfica
app = tk.Tk()
app.resizable(False, False)
app.title("Pomodoro")
app.config(padx=25, pady=25, bg=BEGE)

# Label do título
title_label = tk.Label(text="Timer", fg=BLUE, bg=BEGE, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0)

# Canvas para o temporizador
canvas = tk.Canvas(width=200, height=224, bg=BEGE, highlightthickness=0)
stopwatch_img = tk.PhotoImage(file='assets/watch.png')
canvas.create_image(100, 75, image=stopwatch_img)
timer_text = canvas.create_text(100, 150, text="00:00", fill=MUSTARD, font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1, row=1)

# Botão para iniciar o temporizador
start_button = tk.Button(text="Start", highlightthickness=0, command=start_timer, width=10, font=(FONT_NAME, 10))
start_button.grid(column=0, row=2)

# Botão para redefinir o temporizador
reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer, width=10, font=(FONT_NAME, 10))
reset_button.grid(column=2, row=2)

# Label para exibir marcações
check_marks = tk.Label(text="", fg=BLUE, bg=BEGE, font=(FONT_NAME, 15))
check_marks.grid(column=1, row=3)

# Iniciar o loop principal da interface gráfica
app.mainloop()
