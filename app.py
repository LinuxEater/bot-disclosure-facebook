import facebook
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FacebookBot:
    def __init__(self, master):
        self.master = master
        master.title("Facebook Bot")

        # Token de acesso
        self.access_token_label = ttk.Label(master, text="Token de Acesso:")
        self.access_token_label.grid(row=0, column=0, padx=5, pady=5)
        self.access_token_entry = ttk.Entry(master, width=50)
        self.access_token_entry.grid(row=0, column=1, padx=5, pady=5)

        # Mensagem
        self.message_label = ttk.Label(master, text="Mensagem:")
        self.message_label.grid(row=1, column=0, padx=5, pady=5)
        self.message_text = tk.Text(master, height=5, width=40)
        self.message_text.grid(row=1, column=1, padx=5, pady=5)

        # Data e hora
        self.date_label = ttk.Label(master, text="Data (AAAA-MM-DD):")
        self.date_label.grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(master)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.time_label = ttk.Label(master, text="Hora (HH:MM):")
        self.time_label.grid(row=3, column=0, padx=5, pady=5)
        self.time_entry = ttk.Entry(master)
        self.time_entry.grid(row=3, column=1, padx=5, pady=5)

        # Botão de postagem
        self.post_button = ttk.Button(master, text="Postar", command=self.post)
        self.post_button.grid(row=4, column=0, columnspan=2, pady=10)

    def post(self):
        access_token = self.access_token_entry.get()
        message = self.message_text.get("1.0", tk.END)
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()

        try:
            post_date = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data ou hora inválido.")
            return

        try:
            graph = facebook.GraphAPI(access_token)
            graph.put_object('me', 'feed', message=message, scheduled_publish_time=post_date.timestamp())
            messagebox.showinfo("Sucesso", "Postagem agendada com sucesso!")
        except facebook.GraphAPIError as e:
            messagebox.showerror("Erro", f"Erro na API do Facebook: {e}")

root = tk.Tk()
bot = FacebookBot(root)
root.mainloop()