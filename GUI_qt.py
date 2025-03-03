import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QToolBar,
    QWidget, QVBoxLayout, QFrame, QLabel, QPushButton
)
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 App com Menu e Barra de Ícones")
        self.setGeometry(100, 100, 800, 600)

        # Criar a barra de menus
        self.menu_bar = self.menuBar()
        self.criar_menu()
        self.criar_menu()

        # Criar a barra de ícones
        self.barra_icones = QToolBar("Barra de Ícones")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.barra_icones)  # Inicialmente à esquerda
        self.criar_barra_icones()

        # Criar layout principal com 3 frames
        self.container = QWidget()
        self.layout_principal = QVBoxLayout(self.container)

        self.frame1 = self.criar_frame("Frame 1")
        self.frame2 = self.criar_frame("Frame 2")
        self.frame3 = self.criar_frame("Frame 3")

        self.layout_principal.addWidget(self.frame1)
        self.layout_principal.addWidget(self.frame2)
        self.layout_principal.addWidget(self.frame3)

        self.setCentralWidget(self.container)

    def criar_menu(self):
        """Cria um menu com 5 opções e 5 subopções cada"""
        for i in range(1, 6):
            menu = self.menu_bar.addMenu(f"Menu {i}")
            for j in range(1, 6):
                acao = QAction(f"Opção {i}.{j}", self)
                acao.triggered.connect(lambda _, x=f"Opção {i}.{j}": self.mostrar_mensagem(x))
                menu.addAction(acao)

    def criar_barra_icones(self):
        """Cria uma barra de ícones inicial com 10 botões"""
        for i in range(1, 11):
            acao = QAction(QIcon(), f"Ícone {i}", self)  # Ícones vazios por enquanto
            acao.triggered.connect(lambda _, x=f"Ícone {i}": self.mostrar_mensagem(x))
            self.barra_icones.addAction(acao)

        self.barra_icones.setFloatable(True)  # Permite que a barra seja flutuante
        self.barra_icones.setMovable(True)  # Permite mover a barra pela tela

    def criar_frame(self, titulo):
        """Cria um QFrame que pode trocar informações"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout()

        label = QLabel(titulo)
        botao = QPushButton(f"Atualizar {titulo}")
        botao.clicked.connect(lambda: self.atualizar_frames(titulo))

        layout.addWidget(label)
        layout.addWidget(botao)
        frame.setLayout(layout)

        return frame

    def atualizar_frames(self, origem):
        """Simula troca de informações entre frames"""
        for frame in [self.frame1, self.frame2, self.frame3]:
            frame.findChild(QLabel).setText(f"Atualizado por {origem}")

    def mostrar_mensagem(self, texto):
        """Mostra qual item do menu ou barra foi clicado"""
        print(f"Clicado: {texto}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())
