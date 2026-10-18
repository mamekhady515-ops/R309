import sys
import asyncio
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox
import qasync
import aiohttp

DOSSIER = Path(__file__).parent
LOGIN_URL = "http://localhost:4567/login"
VERIFY_URL = "http://localhost:4567/verify"


class Authentification(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification")
        self.resize(420, 320)
        self.token = None

        self.page_login = uic.loadUi(str(DOSSIER / "login.ui"))
        self.page_result = uic.loadUi(str(DOSSIER / "result.ui"))
        self.addWidget(self.page_login)
        self.addWidget(self.page_result)

        self.page_login.btnLogin.clicked.connect(self.connexion)
        self.page_login.editUser.returnPressed.connect(self.connexion)
        self.page_login.editPassword.returnPressed.connect(self.connexion)
        self.page_result.btnLogout.clicked.connect(self.deconnexion)

    def erreur(self, texte):
        boite = QMessageBox(QMessageBox.Icon.Warning, "Erreur", texte, parent=self)
        boite.open()

    @qasync.asyncSlot()
    async def connexion(self):
        user = self.page_login.editUser.text()
        pwd = self.page_login.editPassword.text()
        self.page_login.btnLogin.setEnabled(False)
        self.page_login.lblTitle.setText("Vérification en cours...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(LOGIN_URL, json={"user": user, "pwd": pwd}) as rep:
                    if rep.status != 200:
                        raise Exception(f"Erreur HTTP {rep.status} pour {LOGIN_URL}")
                    data = await rep.json()
                    self.token = data["token"]
                print("Token :", self.token)

                entete = {"Authorization": f"Bearer {self.token}"}
                async with session.get(VERIFY_URL, headers=entete) as rep:
                    data = await rep.json()
                print("Verify :", data)

            if data["valid"]:
                self.page_result.lblTitle.setText(f"Bienvenue {data['user']} !")
                self.setCurrentWidget(self.page_result)
            else:
                self.erreur(data["error"])
        except Exception as e:
            self.erreur(str(e))

        self.page_login.btnLogin.setEnabled(True)
        self.page_login.lblTitle.setText("Connexion")
        self.page_login.editPassword.clear()

    def deconnexion(self):
        self.page_login.editUser.clear()
        self.setCurrentWidget(self.page_login)


app = QApplication(sys.argv)
app.setStyleSheet((DOSSIER / "style-auth.qss").read_text())
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)
fenetre = Authentification()
fenetre.show()
with loop:
    loop.run_forever()