from tkinter import Tk, Label, simpledialog
from pynput.keyboard import Key, Controller, Listener
import threading
import time

class AfkCasino:
    def __init__(self, root):
        self.keyboard = Controller()
        self.script_running = threading.Event()
        self.money = 0
        self.target_amount = 0
        self.cycle_time = 18  # Geschätzte Zeit für einen Zyklus in Sekunden
        self.cycle_earnings = 2497500  # Nettogewinn pro Zyklus
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Scoreboard")
        self.target_amount_label = Label(root, text="Zielbetrag: $0", font=("Arial", 18))
        self.target_amount_label.pack(pady=10)
        
        self.money_label = Label(root, text="Gefarmt: $0", font=("Arial", 24))
        self.money_label.pack(pady=20)
        
        self.remaining_label = Label(root, text="Verbleibt: $0", font=("Arial", 18))
        self.remaining_label.pack(pady=10)
        
        self.time_label = Label(root, text="Geschätzte verbleibende Zeit: 0s", font=("Arial", 18))
        self.time_label.pack(pady=10)

    def update_labels(self):
        self.target_amount_label.config(text=f"Zielbetrag: ${self.target_amount:,}")
        self.money_label.config(text=f"Gefarmt: ${self.money:,}")
        remaining = max(self.target_amount - self.money, 0)
        self.remaining_label.config(text=f"Verbleibt: ${remaining:,}")
        
        if remaining > 0 and self.cycle_earnings > 0:
            estimated_time = remaining / self.cycle_earnings * self.cycle_time
            self.time_label.config(text=f"Geschätzte verbleibende Zeit: {int(estimated_time)}s")
        else:
            self.time_label.config(text="Geschätzte verbleibende Zeit: 0s")
        self.root.update_idletasks()

    def press_sequence(self):
        while self.script_running.is_set() and self.money < self.target_amount:
            print('L wird gedrückt')
            self.keyboard.press('l')
            self.keyboard.release('l')
            time.sleep(1)

            print('Enter wird gedrückt (-$2,500)')
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            self.money -= 2500
            self.root.after(0, self.update_labels)
            time.sleep(7)

            if not self.script_running.is_set() or self.money >= self.target_amount:
                break

            print('P wird gedrückt')
            self.keyboard.press('p')
            self.keyboard.release('p')
            time.sleep(1)

            print('Enter wird gedrückt (+$2,500,000)')
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            self.money += 2500000
            self.root.after(0, self.update_labels)
            time.sleep(10)

            if self.money >= self.target_amount:
                print("Zielbetrag erreicht. Skript wird gestoppt...")
                self.script_running.clear()
                self.root.after(0, self.update_labels)  # Stelle sicher, dass Labels nach Beendigung aktualisiert werden

    def on_press(self, key):
        try:
            if key.char == 'o' or key.char == 'O':
                if not self.script_running.is_set():
                    self.root.after(0, self.ask_target_amount)
                else:
                    self.script_running.clear()
        except AttributeError:
            pass

    def ask_target_amount(self):
        print("Bitte gib den Zielbetrag im geöffneten Fenster ein.")
        self.target_amount = simpledialog.askinteger("Zielbetrag", "Wie viel Geld möchtest du farmen?", parent=self.root)
        if self.target_amount:
            print(f"Skript wird gestartet... Ziel: ${self.target_amount:,}")
            self.script_running.set()
            self.money = 0
            self.update_labels()
            threading.Thread(target=self.press_sequence, daemon=True).start()

if __name__ == "__main__":
    root = Tk()
    afk_casino = AfkCasino(root)
    listener = Listener(on_press=afk_casino.on_press)
    listener.start()
    root.mainloop()
