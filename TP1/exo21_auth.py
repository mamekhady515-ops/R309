import sys
import hashlib
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox

DOSSIER = Path(__file__).parent


def charger_utilisateurs(fichier):
    users = {}
    for ligne in open(fichier):
        ligne = ligne.strip()
        if ligne:
            nom, empreinte = ligne.split(":")
            users[nom] = empreinte
    return users


class Authentification(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.resize(420, 320)
        self.users = charger_utilisateurs(DOSSIER / "users.sha256")

        self.page_login = uic.loadUi(str(DOSSIER / "login.ui"))
        self.page_result = uic.loadUi(str(DOSSIER / "result.ui"))
        self.addWidget(self.page_login)
        self.addWidget(self.page_result)

        self.page_login.btnLogin.clicked.connect(self.connexion)
        self.page_login.editUser.returnPressed.connect(self.connexion)
        self.page_login.editPassword.returnPressed.connect(self.connexion)
        self.page_result.btnLogout.clicked.connect(self.deconnexion)

    def connexion(self):
        user = self.page_login.editUser.text()
        mdp = self.page_login.editPassword.text()
        empreinte = hashlib.sha256(mdp.encode()).hexdigest()

        if self.users.get(user) == empreinte:
            self.page_result.lblTitle.setText(f"Bienvenue {user} !")
            self.setCurrentWidget(self.page_result)
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")
        self.page_login.editPassword.clear()

    def deconnexion(self):
        self.page_login.editUser.clear()
        self.setCurrentWidget(self.page_login)


app = QApplication(sys.argv)
app.setStyleSheet((DOSSIER / "style-auth.qss").read_text())
fenetre = Authentification()
fenetre.show()
sys.exit(app.exec())