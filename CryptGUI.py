"""Imports"""
import os
import sys
import cryptography.fernet as f
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
"""Start of code"""
class CryptGui(QDialog):
    def __init__(self,parent=None):
        """Initializes program"""
        super().__init__(parent)
        self.setWindowTitle('Encryptor')
        self.setWindowIcon(QtGui.QIcon('index.png'))
        self.msg = QLabel('')
        Dialog_layout = QVBoxLayout()
        Text_layout = QFormLayout()
        self.textbox1 = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        Text_layout.addRow('Enter Path:',self.textbox1)
        Text_layout.addRow('Enter key path:',self.textbox2)
        Text_layout.addRow('Path for key(Only use when generating key)',self.textbox3)
        Dialog_layout.addLayout(Text_layout)
        layout = QVBoxLayout()
        button = QPushButton('Encrypt')
        button2 = QPushButton('Decrypt')
        button3 = QPushButton('GenKey')
        button.clicked.connect(self.encrypt)
        layout.addWidget(button)
        button2.clicked.connect(self.decrypt)
        layout.addWidget(button2)
        button3.clicked.connect(self.gen_key)
        layout.addWidget(button3)
        layout.addWidget(self.msg)
        Dialog_layout.addLayout(layout)
        self.setLayout(Dialog_layout)

    def encrypt(self):
        if self.textbox1.text() == None:
            self.msg.setText('Specify a path!!!')
            return
        if self.textbox2.text() == None:
            self.msg.setText('Specify a key to use!!!')
            return
        path = self.textbox1.text()
        key_path = self.textbox2.text()
        if os.path.exists(key_path) and os.path.exists(path):
            try:
                _path = open(path,'r')
                contents = _path.read()
                key_path = open(key_path,'r')
                key_contents = key_path.read()
                k = f.Fernet(key_contents)
                encoded_contents = contents.encode()
                crypt = k.encrypt(encoded_contents)
                _clear = open(path,'wb')
                _clear.write(crypt)
                _clear.close()
                self.msg.setText(f'Encrypted file {path}')
                self.textbox1.setText('')
                self.textbox2.setText('')
                self.textbox3.setText('')
            except Exception as e:
                self.msg.setText(f'An error has occured {e}')
                self.textbox1.setText('')
                self.textbox2.setText('')
                self.textbox3.setText('')
                return
        else:
            self.msg.setText('That path does not exist')
            self.textbox1.setText('')
            self.textbox2.setText('')
            self.textbox3.setText('')
            return

    def decrypt(self):
        key = self.textbox2.text()
        path = self.textbox1.text()
        if os.path.exists(path):
            try: 
                k2 = f.Fernet(key)
                _path = open(path,"rb")
                contents = _path.read()
                _path.close()
                decrypt = k2.decrypt(contents)
                decoded = decrypt.decode()
                overwrite = open(path,'w+')
                overwrite.write(decoded)
                overwrite.close()
                self.msg.setText(f'Decrypted {path}')
                self.textbox1.setText('')
                self.textbox2.setText('')
                self.textbox3.setText('')
            except Exception as e:
                self.msg.setText(f'An error has occured {e}')
                self.textbox1.setText('')
                self.textbox2.setText('')
                self.textbox3.setText('')
        else:
            self.msg.setText('This path does not exist.')
    def gen_key(self):
        if self.textbox3 == None:
            self.msg.setText('You need to specify a path for where the key needs to go.')
            return
        try:
            key = f.Fernet.generate_key()
            g = open(self.textbox3.text(),'wb')
            g.write(key)
            g.close()
            path = self.textbox3.text()
            self.textbox1.setText('')
            self.textbox2.setText('')
            self.textbox3.setText('')
            self.msg.setText(f'Saved key to {path}')
        except Exception as e:
            print(f'An error has occured {e}')
            self.msg.setText(f'An error has occured {e}')
            self.textbox1.setText('')
            self.textbox2.setText('')
            self.textbox3.setText('')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Encrypt = CryptGui()
    Encrypt.show()
    sys.exit(app.exec_())
