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
from PyQt5.QtWidgets import QPlainTextEdit
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
        self.resize(500,200)
        self.file_array = []
        self.array_count = 0
        self.Dialog_layout = QVBoxLayout()
        self.Text_layout = QFormLayout()
        self.layout = QVBoxLayout()
        self.textbox1 = QPlainTextEdit(self)
        self.textbox1.setReadOnly(True)
        self.textbox1.resize(20,20)
        self.path_button = QPushButton('Select Path to encrypt/decrypt')
        self.textbox2 = QLineEdit(self)
        self.key_button = QPushButton('Select Key Path')
        self.init_widgets()

    def init_widgets(self):
        self.layout.addWidget(self.key_button)
        self.Text_layout.addRow('Path:',self.textbox1)
        self.Text_layout.addWidget(self.path_button)
        self.clear_button = QPushButton('Clear Paths')
        self.clear_button.clicked.connect(self.clear)
        self.Text_layout.addWidget(self.clear_button)
        self.path_button.clicked.connect(self.select_path)
        self.Text_layout.addRow('Key Path:',self.textbox2)
        self.Text_layout.addWidget(self.key_button)
        self.key_button.clicked.connect(self.select_key_path)
        self.Dialog_layout.addLayout(self.Text_layout)
        self.gen_k = QPushButton("Automatically Select And Generate Key")
        button = QPushButton('Encrypt')
        button2 = QPushButton('Decrypt')
        self.gen_k.clicked.connect(self.generate_key)
        self.layout.addWidget(self.gen_k)
        button.clicked.connect(self.encrypt)
        self.layout.addWidget(button)
        button2.clicked.connect(self.decrypt)
        self.layout.addWidget(button2)
        self.layout.addWidget(self.msg)
        self.Dialog_layout.addLayout(self.layout)
        self.setLayout(self.Dialog_layout)


    def encrypt(self):
        if self.file_array == []:
            self.msg.setText('Specify a path!!!')
            return
        if self.textbox2.text() == None:
            self.msg.setText('Specify a key to use!!!')
            return
        key_path = self.textbox2.text()
        if os.path.exists(key_path) == False:
            self.msg.setText('The Encryption Key Path Does Not Exist')
        print(self.file_array)
        for i in range(len(self.file_array)):
            print(i)
            if os.path.exists(self.file_array[i]):
                try:
                    _path = open(self.file_array[i],'r')
                    contents = _path.read()
                    key_path = open(self.textbox2.text(),'rb')
                    key_contents = key_path.read()
                    k = f.Fernet(key_contents)
                    encoded_contents = contents.encode()
                    crypt = k.encrypt(encoded_contents)
                    _clear = open(self.file_array[i],'wb')
                    _clear.write(crypt)
                    _clear.close()
                    x=[i+'\n' for i in self.file_array]
                    t=''.join(x)
                    self.msg.setText(f'Encrypted file {t}')
                    print('Hit')
                    self.textbox1.setPlainText('')
                except Exception as e:
                    self.msg.setText(f'An error has occured {e}')
                    return
            else:
                self.msg.setText('That path does not exist')
                self.textbox1.setPlainText('')
                self.file_array = []
                return
        self.msg.setText(f'Encrypted {self.array_count} files')
        self.file_array = []
        self.textbox1.setPlainText('')

    def decrypt(self):
        if self.file_array == []:
            self.msg.setText('Specify a path!!!')
            return
        if self.textbox2.text() == None:
            self.msg.setText('Specify a key to use!!!')
            return
        print(self.file_array)
        key = self.textbox2.text()
        if os.path.exists(key) == False:
            self.msg.setText('The Encryption Key Path Does Not Exist')
        for i in range(len(self.file_array)):
            print(i)
            if os.path.exists(self.file_array[i]):
                try: 
                    _keypath = open(f'{key}','rb')
                    key1 = _keypath.read()
                    k2 = f.Fernet(key1)
                    _path = open(self.file_array[i],"r")
                    contents = _path.read()
                    _path.close()
                    contents = contents.encode()
                    decrypt = k2.decrypt(contents)
                    decoded = decrypt.decode()
                    overwrite = open(self.file_array[i],'w+')
                    overwrite.write(decoded)
                    overwrite.close()
                    self.msg.setText(f'Decrypted {self.file_array[i]}')
                except Exception as e:
                    self.msg.setText(f'An error has occured {e}')
                    self.textbox1.setPlainText('')
            else:
                self.msg.setText('This path does not exist.')
                return
        self.msg.setText(f'Decrypted {self.array_count} files')
        self.textbox1.setPlainText('')
        self.file_array = []

    def select_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename,_ = QFileDialog.getOpenFileName(None, "Open a File", "","Text Files (*.txt)",options=options)
        if filename == '':
            return
        self.file_array.append(str(filename))
        x = [i for i in self.file_array]
        setted_x = set(x)
        self.array_count = len(setted_x)
        joined_x = '\n'.join(setted_x)
        self.textbox1.setPlainText(joined_x)

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
    
    def clear(self):
        self.textbox1.setPlainText('')
        self.file_array = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Encrypt = CryptGui()
    Encrypt.show()
    sys.exit(app.exec_())
