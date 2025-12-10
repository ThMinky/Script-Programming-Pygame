import os
import sys
import subprocess

import globals


def showMenu():
    print("\n")

    if globals.played_once:
        if globals.won:
            print("|-----------------|")
            print("|    You Win!     |")
            print("|-----------------|")
            print("Do you want to beat them again? (y/n)")
        else:
            print("|-----------------|")
            print("|    You Lose!    |")
            print("|-----------------|")
            print("Do you want to redeem yourself? (y/n)")
    else:
        print("|------------------------------|")
        print("|  Do you want to play? (y/n)  |")
        print("|------------------------------|")


def main():
    baseDir = os.path.dirname(os.path.abspath(__file__))
    launcherPath = os.path.join(baseDir, "game.py")

    while True:
        showMenu()

        choice = input("  > ").strip().lower()

        if choice == "y":
            result = subprocess.run([sys.executable, launcherPath])

            globals.played_once = True
            globals.won = result.returncode == 1

        elif choice == "n":
            exit()
        else:
            print("Please choose y or n.")


if __name__ == "__main__":
    main()
