import sqlite3
import sys
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog,QLabel,QHBoxLayout,QMessageBox, QWidget)

conn = sqlite3.connect("Liste.db")
c = conn.cursor()
c.execute(
"""
CREATE TABLE IF NOT EXISTS personne
(
    prenom text,
    nom text
            
)
""")

conn.commit()
conn.close()


class DB(QDialog):

    def __init__(self, parent=None):
        super(DB, self).__init__(parent)
        # Create widgets
        # self.setWindowTitle('BTS SNIR2')
        self.label1 = QLabel("Nom ")
        self.label2 = QLabel("Prénom")
        self.label3 = QLabel("Nom")
        self.label4 = QLabel("Prénom")
        self.label5 = QLabel("")
        self.label6 = QLabel("")

        self.edit1 = QLineEdit()
        self.edit2 = QLineEdit()
        
        self.button = QPushButton("Enregistrer")
        self.button2 = QPushButton("Afficher")
        self.button3 = QPushButton("Quitter")
        self.button4 = QPushButton("Supprimer Enregistrement")
        self.button5 = QPushButton("Supprimer table")
        self.button6 = QPushButton("Mettre à jour")
        # Create layout and add widgets
        layoutVer = QVBoxLayout()
        layoutHor1 = QHBoxLayout()
        layoutHor2 = QHBoxLayout()
        layoutHor3 = QHBoxLayout()
        layoutHor4 = QHBoxLayout()
        layoutHor5 = QHBoxLayout()
        layoutHor6 = QHBoxLayout()
        layoutHor7 = QHBoxLayout()
        layoutHor8 = QHBoxLayout()


        layoutHor1.addWidget(self.label1)
        layoutHor1.addWidget(self.edit1)

        layoutHor2.addWidget(self.label2)
        layoutHor2.addWidget(self.edit2)

        layoutHor3.addWidget(self.button)
        layoutHor3.addWidget(self.button2)

        layoutHor5.addWidget(self.button3)
        layoutHor5.addWidget(self.button4)

        layoutHor6.addWidget(self.button5)
        layoutHor6.addWidget(self.button6)

        layoutHor7.addWidget(self.label3)
        layoutHor7.addWidget(self.label4)

        layoutHor8.addWidget(self.label5)
        layoutHor8.addWidget(self.label6)

        # layoutVer.addWidget(self.edit2)
        layoutVer.addLayout(layoutHor1)
        layoutVer.addLayout(layoutHor2)
        layoutVer.addLayout(layoutHor3)
        layoutVer.addLayout(layoutHor4)
        layoutVer.addLayout(layoutHor5)
        layoutVer.addLayout(layoutHor6)
        layoutVer.addLayout(layoutHor7)
        layoutVer.addLayout(layoutHor8)

        # layoutVer.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layoutVer)

        # Add button signal to greetings slot
        self.button.clicked.connect(self.Enregistrer)
        self.button2.clicked.connect(self.Afficher)
        self.button3.clicked.connect(self.close)
        self.button4.clicked.connect(self.SupprimerEnregistrer)
        self.button5.clicked.connect(self.SupprimerTable)
        self.button6.clicked.connect(self.MettreàJour)
        self.messagebox = QMessageBox()
        self.messagebox.setText("Attention! au moin un champ est vide")
        validator= QRegularExpressionValidator(QRegularExpression("[A-Za-z]+"))
        self.edit1.setValidator(validator)
        self.edit2.setValidator(validator)

    # Greets the user    
    def Enregistrer(self):

        if(self.edit1.text()=="" or self.edit2.text()==""):
            self.messagebox.show()
            self.edit1.setText("")
            self.edit2.setText("") 
        else:
            conn = sqlite3.connect("Liste.db")
            c = conn.cursor()


            c.execute("""INSERT INTO personne (nom,prenom)  VALUES(?, ?)""", (self.edit1.text(), self.edit2.text()))

            conn.commit()
            conn.close()
        
            self.edit1.setText("")
            self.edit2.setText("")  

    def Afficher(self):

        conn = sqlite3.connect("Liste.db")
        c = conn.cursor()

        c.execute("""SELECT nom, prenom FROM personne""")

        liste = c.fetchall()
        # for row in liste :

        #     nom = row[0] 
        #     prenom = row[1] 
        global nom
        nom = liste[-1][0] 
        global prenom
        prenom = liste[-1][1] 
        

        self.label5.setText(nom)
        self.label6.setText(prenom)
        conn.commit()
        conn.close()
    
    def SupprimerEnregistrer(self):
        
        conn = sqlite3.connect("Liste.db")
        c = conn.cursor()

        c.execute("""DELETE FROM personne WHERE nom = ? and prenom = ? """,(self.edit1.text(),self.edit2.text()))

        self.label5.setText("")
        self.label6.setText("")
        self.edit1.setText("")
        self.edit2.setText("") 
        conn.commit()
        conn.close()
        print("L'enregistrement a été supprimée") 
        
    def SupprimerTable(self):

        conn = sqlite3.connect("Liste.db")
        c = conn.cursor()

        c.execute("DROP TABLE personne")

        conn.commit()
        conn.close()

        print("La table a été supprimée")
        self.close()

    def MettreàJour(self):
        conn = sqlite3.connect("Liste.db")
        c = conn.cursor()

        c.execute("""UPDATE personne SET nom = ? WHERE prenom = ? """, (self.edit1.text(), self.edit2.text()))

        conn.commit()
        conn.close()
        print("La table a été mise à jour")


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = DB()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
