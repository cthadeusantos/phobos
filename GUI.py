import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFrame, QMenuBar, QMenu,  QToolBar, QLabel, QPushButton
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, pyqtSignal


class CustomFrame(QFrame):
    """ Frame personalizado que pode enviar sinais para os outros frames. """
    update_signal = pyqtSignal(str)  # Sinal que será emitido para atualizar outros frames

    def __init__(self, name, color):
        super().__init__()
        self.setStyleSheet(f"background-color: {color}; border: 2px solid black;")

        # Criar um layout interno
        self.layout = QVBoxLayout()
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Criar botão que emite o sinal
        self.button = QPushButton(f"Atualizar Frames")
        self.button.clicked.connect(self.send_update_signal)

        # Adicionar widgets ao layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def send_update_signal(self):
        """ Emite um sinal para os outros frames com um novo texto. """
        self.update_signal.emit(f"Atualizado por {self.label.text()}")


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 - Barra Flutuante e Layout Dinâmico")
        self.setGeometry(100, 100, 900, 600)

        # Criar barra de menu
        self.menu_bar = self.menuBar()
        self.create_menus()

        # Criar barra de ícones (toolbar) e permitir encaixe/removível
        self.toolbar = QToolBar("Barra de Ícones")
        self.toolbar.setMovable(True)
        self.create_toolbar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)  # Posição inicial à esquerda

        # Criar os frames personalizados
        self.frame1 = CustomFrame("Frame 1", "red")
        self.frame2 = CustomFrame("Frame 2", "green")
        self.frame3 = CustomFrame("Frame 3", "blue")

        # Conectar os sinais de cada frame para atualizar os outros
        self.frame1.update_signal.connect(self.update_frames)
        self.frame2.update_signal.connect(self.update_frames)
        self.frame3.update_signal.connect(self.update_frames)

        # Criar layout principal
        self.layout_principal = QHBoxLayout()
        self.layout_principal.addWidget(self.frame1)
        self.layout_principal.addWidget(self.frame2)
        self.layout_principal.addWidget(self.frame3)

        # Permitir que os frames se ajustem automaticamente ao tamanho da janela
        self.layout_principal.setStretch(0, 1)  # Expansível
        self.layout_principal.setStretch(1, 1)
        self.layout_principal.setStretch(2, 1)

        # Criar widget central e definir layout
        self.container = QWidget()
        self.container.setLayout(self.layout_principal)
        self.setCentralWidget(self.container)

        # Monitorar mudanças na barra de ferramentas
        self.toolBarAreaChanged.connect(self.update_layout)

    def create_menus(self):
        """Cria o menu com 5 opções, cada uma contendo 5 subopções."""
        for i in range(1, 6):
            menu = self.menu_bar.addMenu(f"Menu {i}")
            for j in range(1, 6):
                action = QAction(f"Submenu {i}.{j}", self)
                menu.addAction(action)

    def create_toolbar(self):
        """Cria uma barra de ícones com 10 ícones (inicialmente)."""
        for i in range(1, 11):
            action = QAction(QIcon(), f"Ícone {i}", self)
            self.toolbar.addAction(action)

    def update_frames(self, text):
        """ Atualiza o conteúdo dos frames quando um botão for pressionado. """
        self.frame1.label.setText(text)
        self.frame2.label.setText(text)
        self.frame3.label.setText(text)

    def update_layout(self):
        """ Atualiza a distribuição dos frames quando a barra de ferramentas é movida/removida. """
        self.layout_principal.setStretch(0, 1)
        self.layout_principal.setStretch(1, 1)
        self.layout_principal.setStretch(2, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
