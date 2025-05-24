import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import datetime
import holidays


ORE_AL_GIORNO = 8
anno_corrente = datetime.datetime.now().year
festivita_italiane = holidays.IT(years=anno_corrente)

def è_bisestile(anno):
    return calendar.isleap(anno)

# Calcolo giorni lavorativi del mese selezionato
def get_giorni_lavorativi(mese):
    num_giorni = calendar.monthrange(anno_corrente, mese)[1]
    giorni = []
    for giorno in range(1, num_giorni + 1):
        data = datetime.date(anno_corrente, mese, giorno)
        if data.weekday() < 5 and data not in festivita_italiane:
            giorni.append(data)
    return giorni

# Quando l’utente preme “Avanti”
def apri_finestra_ore():
    mese = mese_var.get()
    if not mese:
        messagebox.showerror("Errore", "Seleziona un mese.")
        return

    numero_mese = list(calendar.month_name).index(mese)
    giorni_lavorativi = get_giorni_lavorativi(numero_mese)

    finestra_ore = tk.Toplevel(root)
    finestra_ore.title(f"Inserisci ore per {mese}")
    finestra_ore.geometry("500x700")  # Larghezza fissa e altezza gestita dinamicamente  
    inputs = {}

    for i, data in enumerate(giorni_lavorativi):
        label = tk.Label(finestra_ore, text=f"{data.day:02d} {data.strftime('%A')}")
        label.grid(row=i, column=0, sticky="w", padx=4,  pady=4)
        entry = tk.Entry(finestra_ore, width=10)
        entry.grid(row=i, column=1, padx=10)
        inputs[data] = entry

    def calcola_risultato():
        ore_effettive = 0
        for data, entry in inputs.items():
            try:
                ore = float(entry.get() or 0)
                ore_effettive += ore
            except ValueError:
                messagebox.showerror("Errore", f"Valore non valido per il giorno {data.day}")
                return

        ore_previste = len(giorni_lavorativi) * ORE_AL_GIORNO
        diff = ore_previste - ore_effettive

        msg = (
            f"Mese: {mese}\n"
            f"Giorni lavorativi: {len(giorni_lavorativi)}\n"
            f"Ore previste: {ore_previste}\n"
            f"Ore effettive: {ore_effettive}\n"
        )
        if diff > 0:
            msg += f"⛔ Assenza: {diff} ore"
        elif diff < 0:
            msg += f"✅ Ore extra: {abs(diff)} ore"
        else:
            msg += "🎯 Hai lavorato esattamente il previsto"

        messagebox.showinfo("Riepilogo", msg)

    bottone_calcola = tk.Button(finestra_ore, text="Calcola", command=calcola_risultato)
    bottone_calcola.grid(row=len(giorni_lavorativi)+1, column=0, columnspan=2, pady=20, )

# === GUI PRINCIPALE ===
root = tk.Tk()
root.title("Gestione Ore Lavoro")
root.geometry("400x300")

tk.Label(root, text="Seleziona un mese").pack(pady=10)
mese_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=mese_var, values=list(calendar.month_name)[1:])
combo.pack()

btn_avanti = tk.Button(root, text="Avanti", command=apri_finestra_ore)
btn_avanti.pack(pady=20)

if è_bisestile(anno_corrente):
    tk.Label(root, text="✔️ Anno bisestile").pack()
else:
    tk.Label(root, text="❌ Anno non bisestile").pack()

root.mainloop()
