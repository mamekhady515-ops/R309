import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QHBoxLayout, QVBoxLayout)


class Compteur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compteur")
        self.setMinimumSize(250, 180)
        self.valeur = 0

        # Les éléments de la fenêtre
        self.label = QLabel(str(self.valeur))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_moins = QPushButton("-")
        self.btn_plus = QPushButton("+")

        # La mise en page : les 2 boutons côte à côte, sous le label
        boutons = QHBoxLayout()
        boutons.addWidget(self.btn_moins)
        boutons.addWidget(self.btn_plus)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(boutons)


app = QApplication(sys.argv)
fenetre = Compteur()
fenetre.show()
sys.exit(app.exec())