import tkinter as tk
from tkinter import ttk, messagebox

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter App com Menu e Barra de Ícones")
        self.geometry("800x600")

        # Criar menu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.criar_menu()

        # Criar os frames principais
        self.frame1 = self.criar_frame("Frame 1", 0)
        self.frame2 = self.criar_frame("Frame 2", 1)
        self.frame3 = self.criar_frame("Frame 3", 2)

        # Criar barra de ícones flutuante
        self.barra_icones = IconBar(self)

    def criar_menu(self):
        """Cria um menu com 5 opções e 5 subopções cada"""
        for i in range(1, 6):
            menu = tk.Menu(self.menu_bar, tearoff=0)
            for j in range(1, 6):
                menu.add_command(label=f"Opção {i}.{j}", command=lambda x=f"Opção {i}.{j}": self.mostrar_mensagem(x))
            self.menu_bar.add_cascade(label=f"Menu {i}", menu=menu)

    def criar_frame(self, titulo, linha):
        """Cria um frame interativo"""
        frame = ttk.Frame(self, borderwidth=2, relief="groove")
        frame.grid(row=linha, column=0, padx=10, pady=10, sticky="nsew")

        label = ttk.Label(frame, text=titulo)
        label.pack(pady=5)

        botao = ttk.Button(frame, text=f"Atualizar {titulo}", command=lambda: self.atualizar_frames(titulo))
        botao.pack(pady=5)

        return frame

    def atualizar_frames(self, origem):
        """Atualiza os textos dos frames simulando troca de informações"""
        for frame in [self.frame1, self.frame2, self.frame3]:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.config(text=f"Atualizado por {origem}")

    def mostrar_mensagem(self, texto):
        """Mostra qual item do menu foi clicado"""
        messagebox.showinfo("Informação", f"Clicado: {texto}")


class IconBar(tk.Toplevel):
    """Janela flutuante contendo os ícones"""
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Barra de Ícones")
        self.geometry("200x400")  # Janela inicial menor
        self.resizable(True, True)  # Permite expansão
        self.attributes('-topmost', True)  # Mantém sempre à frente

        self.criar_icones()

    def criar_icones(self):
        """Cria 10 botões de ícones iniciais"""
        for i in range(1, 11):
            botao = ttk.Button(self, text=f"Ícone {i}", command=lambda x=f"Ícone {i}": self.mostrar_mensagem(x))
            botao.pack(pady=5, fill="x")

    def mostrar_mensagem(self, texto):
        """Mostra qual ícone foi clicado"""
        messagebox.showinfo("Ícone", f"Clicado: {texto}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
