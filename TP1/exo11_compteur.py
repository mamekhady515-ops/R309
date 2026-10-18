import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class Compteur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compteur")
        self.setMinimumSize(250, 180)
        self.valeur = 0

        self.label = QLabel("0")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_moins = QPushButton("-")
        self.btn_plus = QPushButton("+")

        boutons = QHBoxLayout()
        boutons.addWidget(self.btn_moins)
        boutons.addWidget(self.btn_plus)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(boutons)

        self.btn_plus.clicked.connect(self.plus)
        self.btn_moins.clicked.connect(self.moins)

    def plus(self):
        if self.valeur < 100:
            self.valeur += 1
            self.label.setText(str(self.valeur))

    def moins(self):
        if self.valeur > 0:
            self.valeur -= 1
            self.label.setText(str(self.valeur))


app = QApplication(sys.argv)
app.setStyleSheet(Path(__file__).with_name("compteur.qss").read_text())
fenetre = Compteur()
fenetre.show()
sys.exit(app.exec())