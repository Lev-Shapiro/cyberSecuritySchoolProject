import os
import typer
from PyInquirer import prompt
from rich import print as rprint
from directory_retriever import DirectoryRetriever
from dict_string_converter import DictStringConverter
from directory_synchronizer import DirectorySynchronizer
from vigenere_cipher import VigenereCipher
from vigenere_hack import VigenereHack

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main():
    rprint("[green]👋 Welcome![/green]\n")

    questions = [
        {
            "type": "list",
            "name": "action",
            "message": "What would you like to do?",
            "choices": [
                "Encrypt",
                "Decrypt",
                "Hack"
            ],
        },
    ]

    answers = prompt(questions)
    action = answers["action"]

    if action == "Encrypt":
        encrypt()
    elif action == "Decrypt":
        decrypt()
    elif action == "Hack":
        hack()

@app.command("encrypt")
def encrypt():
    rprint("[yellow]=============================================[yello]\n")
    rprint("[red]CYBERSECURITY[/red] - [yellow]FINAL PROJECT[yello]")
    rprint("\n[yellow]=============================================[yello]\n")

    folder_name = typer.prompt("Give the path you'd like to encrypt")

    # Check if the folder exists
    if not os.path.exists(folder_name):
        rprint(f"[red]❌ Folder not found[/red]")
        exit()
    else:
        rprint(f"[green]✅ Folder found[/green]")

    key = typer.prompt("Specify encryption key")

    # Check if the key is valid
    if len(key) == 0:
        rprint("[red]❌ Key cannot be empty.[/red]")
        exit()
    else:
        rprint("[green]✅ Key is valid[/green]")

    # Encrypt the folder
    cipher = VigenereCipher(key)
    retriever = DirectoryRetriever(folder_name)

    data = retriever.retrieve_all(folder_name)
    converted_text = DictStringConverter.convertToStr(data)

    encrypted = cipher.encrypt(converted_text)

    # save the encrypted data
    with open("encrypted_data.txt", "w") as f:
        f.write(encrypted)

    rprint("\n[yellow]=============================================[yello]\n")

    rprint("[blue]You can view the encrypted data at encrypted_data.txt[/blue]")


@app.command("load")
def decrypt():
    rprint("[yellow]=============================================[yello]\n")
    rprint("[red]Cyber Security[/red] - [yellow]Final Project[yello]")
    rprint("\n[yellow]=============================================[yello]\n")

    # Search for the file
    if os.path.exists("encrypted_data.txt"):
        rprint(f"[green]✅ File found[/green]")
        with open("encrypted_data.txt", "r") as f:
            encrypted = f.read()
    else:
        rprint(f"[red]❌ File not found[/red]")
        exit()

    key = typer.prompt("Specify encryption key")

    # Check if the key is valid
    if len(key) == 0:
        rprint("[red]❌ Key cannot be empty.[/red]")
        exit()

    cipher = VigenereCipher(key)
    decrypted = cipher.decrypt(encrypted)

    rprint("\n[yellow]=============================================[yello]\n")

    try:
        # string to dictionary
        converted_dist = DictStringConverter.convertToDict(decrypted)
        synchronizer = DirectorySynchronizer('result')


        synchronizer.synchronize(converted_dist)

        rprint("[green]Saved at[/green] [blue]/result[/blue] [green]folder[/green]")
    except:
        rprint("[red]❌ Key is not valid[/red]")
        exit()

@app.command("hack")
def hack():
    if os.path.exists("encrypted_data.txt"):
        rprint(f"[green]✅ Encrypted file found. Hacking... [/green]")
        with open("encrypted_data.txt", "r") as f:
            encrypted = f.read()
    else:
        rprint(f"[red]❌ File not found[/red]")
        exit()

    hackerAgent = VigenereHack(encrypted)

    # NOT NECESSARILY ACCURATE! The longer the encrypted data is - the better algorithm works (because more data for analysis)
    estimatedKey = hackerAgent.find_key()

    vigenereCipher = VigenereCipher(estimatedKey)
    estimatedContent = vigenereCipher.decrypt(encrypted)

    # Save the decrypted data
    with open("hacked.txt", "w") as f:
        f.write(estimatedContent)

    rprint("\n[yellow]=============================================[yello]\n")

    rprint("[blue]You can view the decrypted data at hacked.txt[/blue]")
    rprint(f"[green]ESTIMATED KEY: {estimatedKey}[/green]")
    # NOTIFY THAT IT MAY BE NOT ACCURATE
    rprint(f"[red]THE KEY MAY BE NOT ACCURATE: LONGER KEYS = LESS ACCURATE, LONGER ENCRYPTED CONTENT = MORE ACCURATE! [/red]")

    rprint("\n[yellow]=============================================[yello]\n")

if __name__ == "__main__":
    app()
