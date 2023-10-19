# coding: utf-8

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time  # Para simular a atualização das variáveis
from datetime import timedelta  # Importe timedelta


def read_task_log():
    import time
    import pandas as pd
    while True:
        try:
            df = pd.read_csv('task_log.csv')
            # Processa os dados ou faz o que for necessário
            return df
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

def update_data():

    global date_time_trabalhado_hoje, date_time_trabalhado_semana, date_time_trabalhado_mensal
    df = read_task_log()
    date_time_trabalhado_hoje, date_time_trabalhado_semana, date_time_trabalhado_mensal = work_summary(df)

class VariableDisplay(tk.Tk):
    def __init__(self, monitoramento, horas_hoje, horas_semana, horas_mensal):
        super().__init__()
        self.title("Monitoramento de Horas")
        self.geometry("250x200")
        self.configure(bg="#f0f0f0")

        # Atribui as variáveis fornecidas
        self.monitoramento = monitoramento
        self.horas_hoje = self.format_time(horas_hoje)
        self.horas_semana = self.format_time(horas_semana)
        self.horas_mensal = self.format_time(horas_mensal)

        # Crie e estilize os labels
        ttk.Label(self, text="Monitoramento:", font=("Arial", 12)).pack(pady=5)
        self.monitoramento_label = ttk.Label(self, text=self.monitoramento, font=("Arial", 12, "bold"))
        self.monitoramento_label.pack(pady=5)

        ttk.Label(self, text="Horas hoje:", font=("Arial", 12)).pack(pady=5)
        self.horas_hoje_label = ttk.Label(self, text=self.horas_hoje, font=("Arial", 12, "bold"))
        self.horas_hoje_label.pack(pady=5)

        ttk.Label(self, text="Horas semana:", font=("Arial", 12)).pack(pady=5)
        self.horas_semana_label = ttk.Label(self, text=self.horas_semana, font=("Arial", 12, "bold"))
        self.horas_semana_label.pack(pady=5)

        ttk.Label(self, text="Horas mensal:", font=("Arial", 12)).pack(pady=5)
        self.horas_mensal_label = ttk.Label(self, text=self.horas_mensal, font=("Arial", 12, "bold"))
        self.horas_mensal_label.pack(pady=5)

        self.refresh_display()


    def format_time(self, td):
        """Converte um objeto timedelta em uma string no formato hh:mm."""
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours:02}:{minutes:02}"

    
    def refresh_display(self):
            """Atualiza os labels com os valores mais recentes das variáveis."""
            update_data()  # Atualiza os dados
            self.horas_hoje_label.config(text=self.format_time(date_time_trabalhado_hoje))
            self.horas_semana_label.config(text=self.format_time(date_time_trabalhado_semana))
            self.horas_mensal_label.config(text=self.format_time(date_time_trabalhado_mensal))
            self.after(10000, self.refresh_display)  # Atualiza a cada 10 segundos


def update_variables():
    """Função para simular a atualização das variáveis."""
    global horas_hoje
    while True:
        horas_hoje += timedelta(minutes=1)  # Adiciona 1 minuto
        time.sleep(10)  # Aguarda 10 segundos antes de atualizar novamente




import pandas as pd
import pytz
from datetime import datetime, timedelta

def work_summary(df):
    # Define o timezone
    pt = pytz.timezone('America/Los_Angeles')
    
    # Converte a coluna 'date' para datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Determina o "hoje" em America/Los_Angeles
    today = datetime.now(pt).date()
    
    # Filtra os dados de hoje
    today_data = df[df['date'] == pd.Timestamp(today)]

    
    # Ajusta a definição de semana para começar no domingo
    if today.weekday() == 6:  # Se for domingo
        start_week = today
    else:
        start_week = today - timedelta(days=today.weekday() + 1)
    end_week = start_week + timedelta(days=6)
    
    # Filtra os dados da semana corrente
    week_data = df[(df['date'] >= pd.Timestamp(start_week)) & (df['date'] <= pd.Timestamp(end_week))]

    
    # Determina o mês corrente
    current_month = today.month
    month_data = df[df['date'].dt.month == current_month]

    
    hours_today = timedelta(hours=today_data['elapsed_time'].sum() / 3600)
    hours_week = timedelta(hours=week_data['elapsed_time'].sum() / 3600)
    hours_month = timedelta(hours=month_data['elapsed_time'].sum() / 3600)
    
    return hours_today, hours_week, hours_month

# Lê o CSV
df = pd.read_csv('task_log.csv')

# Chama a função
date_time_trabalhado_hoje, date_time_trabalhado_semana, date_time_trabalhado_mensal = work_summary(df)


# Exemplo de como instanciar e executar a janela
monitoramento = "Não implementado"

# Inicia a GUI em uma thread separada
gui_thread = threading.Thread(target=lambda: VariableDisplay(monitoramento, date_time_trabalhado_hoje, date_time_trabalhado_semana, date_time_trabalhado_mensal).mainloop())
gui_thread.start()
