# CryptGui
## Disclaimer
This program is used to encrypt files, use it at your own risk. Any damages done is not the fault of the owner or any other parties involved in the creation of this program.
## Requirements
- Python3
## How to use 
- Make sure to install requirements.txt by doing `pip install -r requirements.txt` this will give you the required modules you need for this program.
## Update Log
##### Version 1.00
- Updated the program so now it gets the contents of the file you put in for the key instead of you having to copy and paste the key out of the file.
##### Version 1.0.1
- Generation of key is more automatic now you can click a button and it will generate and select the key for you.
- You now have the option to select a path via a button which takes you to a nice file explorer gui where you can select any text file.
##### Version 1.0.2
- Removed the other gen button I left on accident.
##### Version 1.0.3
- Made it so then the encryption key text box no longer gets reset when you encrypt or decrypt a file.
##### Version 1.0.4
- You can now select multiple files to encrypt and decrypt.
##### Version 1.0.5
- Bug fix where when you cancel out of selecting a file it would put a newline in, instead this would cause an error where it says that "the path does not exist". Ive also done some changes to the code to make it a bit easier to read.
##### Version 1.0.6
- Fixed an issue where when selecting the same path multiple times over even though it would not appear in the text box and not be encrypted N times over it would still register as there so when it says "Encrypted n files" n would be wrong.
