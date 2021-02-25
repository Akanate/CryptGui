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
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
import time
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
        layout = QVBoxLayout()
        self.textbox1 = QLineEdit(self)
        self.path_button = QPushButton('Select Path to encrypt/decrypt')
        self.textbox2 = QLineEdit(self)
        self.key_button = QPushButton('Select Key Path')
        layout.addWidget(self.key_button)
        Text_layout.addRow('Path:',self.textbox1)
        Text_layout.addWidget(self.path_button)
        self.path_button.clicked.connect(self.select_path)
        Text_layout.addRow('Key Path:',self.textbox2)
        Text_layout.addWidget(self.key_button)
        self.key_button.clicked.connect(self.select_key_path)
        Dialog_layout.addLayout(Text_layout)
        self.gen_k = QPushButton("Automatically Select And Generate Key")
        button = QPushButton('Encrypt')
        button2 = QPushButton('Decrypt')
        self.gen_k.clicked.connect(self.generate_key)
        layout.addWidget(self.gen_k)
        button.clicked.connect(self.encrypt)
        layout.addWidget(button)
        button2.clicked.connect(self.decrypt)
        layout.addWidget(button2)
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
                key_path = open(key_path,'rb')
                key_contents = key_path.read()
                k = f.Fernet(key_contents)
                encoded_contents = contents.encode()
                crypt = k.encrypt(encoded_contents)
                _clear = open(path,'wb')
                _clear.write(crypt)
                _clear.close()
                self.msg.setText(f'Encrypted file {path}')
                self.textbox1.setText('')
            except Exception as e:
                self.msg.setText(f'An error has occured {e}')
                self.textbox1.setText('')
                return
        else:
            self.msg.setText('That path does not exist')
            self.textbox1.setText('')
            self.textbox2.setText('')
            return

    def decrypt(self):
        key = self.textbox2.text()
        path = self.textbox1.text()
        if os.path.exists(path):
            try: 
                _keypath = open(f'{key}','rb')
                key = _keypath.read()
                k2 = f.Fernet(key)
                _path = open(path,"r")
                contents = _path.read()
                _path.close()
                contents = contents.encode()
                decrypt = k2.decrypt(contents)
                decoded = decrypt.decode()
                overwrite = open(path,'w+')
                overwrite.write(decoded)
                overwrite.close()
                self.msg.setText(f'Decrypted {path}')
                self.textbox1.setText('')
                self.textbox2.setText('')
            except Exception as e:
                self.msg.setText(f'An error has occured {e}')
                self.textbox1.setText('')
        else:
            self.msg.setText('This path does not exist.')

    def select_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getOpenFileName(None, "Open a File", "","Text Files (*.txt)",options=options)
        self.textbox1.setText(filename)

    def select_key_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getOpenFileName(None, "Open a File", "","Text Files (*.txt)",options=options)
        self.textbox2.setText(filename)
    
    def generate_key(self):
        key = f.Fernet.generate_key()
        x = time.strftime("%Y%m%d-%H%M%S")
        file_name = f'Key-{str(x)}'
        with open(f'{file_name}.txt','wb') as e:
            e.write(key)
        self.msg.setText(f'Key Generated to file {file_name}.txt will automatically use this key unless new one generated.')
        self.textbox2.setText(f'{file_name}.txt')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Encrypt = CryptGui()
    Encrypt.show()
    sys.exit(app.exec_())

