# Introduction
As part of my Cybersecurity studies I was asked to make a final project related to cybersecurity.

This project can encrypt whole directories (including their content) with a special key that the user provides. To restore the directory on another computer you'll need to have the key and run `python3 main.py load` to load the encrypted directories (it will ask for the key)

## COMMANDS
`python3 main.py encrypt` - will encrypt the directory that you'll specify with a key that you'll provide

`python3 main.py load` - will load the encrypted directories using the key and encrypted_data.txt (which is generated by the previous command)

`python3 main.py` - opens an radio button to select whether you want to encrypt or load the directory.

## USED PACKAGES

#### Install Everything Together
`pip install -r requirements.txt`

#### Install Every Library Separately
Typer: `pip install "typer[all]"`

PyInquirer: `pip install PyInquirer`

Rich: `pip install rich`