import sqlite3
from tkinter import *
from tkinter import messagebox

# Klase, kurā tiek turēti metodi lai stradāt ar datubazei
class Datubaze:
    # Veido databaze ja ta neeksistē. 
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS dalas (id INTEGER PRIMARY KEY, dala text, klients text, veikals text, cena text)")
        self.conn.commit()

    # "Fetch" ir metode lai lasīt un atrast informāciju
    def fetch(self):
        self.cur.execute("SELECT * FROM dalas")
        rindas = self.cur.fetchall()
        return rindas

    #" Insert" ir metode lai pievienot jaunu informaciju
    def insert(self, dala, klients, veikals, cena):
        self.cur.execute("INSERT INTO dalas VALUES (NULL, ?, ?, ?, ?)",
                        (dala, klients, veikals, cena))
        self.conn.commit()
    
    # "Remove" ir metode lai noņemt informaciju
    def remove(self, id):
        self.cur.execute("DELETE FROM dalas WHERE id=?", (id,))
        self.conn.commit()

    # "Update" ir metode lai nomainīt informāciju
    def update(self, id, dala, klients, veikals, cena):
        self.cur.execute("UPDATE dalas SET dala = ?, klients = ?, veikals = ?, cena = ? WHERE id = ?",
                         (dala, klients, veikals, cena, id))
        self.conn.commit()

    # Metode, lai beigt darbu ar datubazei.
    def __del__(self):
        self.conn.close()

# Databazes veidošana nosaucitā mapē.
db = Datubaze('./store.db')

# Funkcija, lai mainit datus sarakstā
def datu_lasisana():
    dalas_saraksts.delete(0, END)
    for rinda in db.fetch():
        dalas_saraksts.insert(END, rinda)

# Funkcija, lai pievienot jaunu daļu programmā
def pievienot_dalu():
    #Kļudas logs jā kāda no logam nav aizpildīta
    if dala_teksts.get() == '' or klients_teksts.get() == '' or veikals_teksts.get() == '' or cena_teksts.get() == '':
        messagebox.showerror('ERROR', 'Lūdzu aizpildīti visus laukus.')
        return
    db.insert(dala_teksts.get(), klients_teksts.get(),
              veikals_teksts.get(), cena_teksts.get())
    dalas_saraksts.delete(0, END)
    dalas_saraksts.insert(END, (dala_teksts.get(), klients_teksts.get(),
                            veikals_teksts.get(), cena_teksts.get()))
    
    notirit_tekstu()
    datu_lasisana()


# Funkcija, kura ievada informaciju par daļam, kad lietotais izvelē jebkuru no saraksta
def izvele_dalu():
    try:
        global izveleta_dala
        indeksa = dalas_saraksts.curselection()[0]
        izveleta_dala = dalas_saraksts.get(indeksa)

        dalas_ieraksts.delete(0, END)
        dalas_ieraksts.insert(END, izveleta_dala[1])
        klienta_ieraksts.delete(0, END)
        klienta_ieraksts.insert(END, izveleta_dala[2])
        veikala_ieraksts.delete(0, END)
        veikala_ieraksts.insert(END, izveleta_dala[3])
        cenas_ieraksts.delete(0, END)
        cenas_ieraksts.insert(END, izveleta_dala[4])
    except IndexError:
        pass

# Funkcija, lai noņemt daļu no datubāzes
def nonemt_dalu():
    db.remove(izveleta_dala[0])
    notirit_tekstu()
    datu_lasisana()

# Funkcija, lai izlabot informaciju par kādu daļu
def mainit_dalu():
    db.update(izveleta_dala[0], dala_teksts.get(), klients_teksts.get(),
              veikals_teksts.get(), cena_teksts.get())
    datu_lasisana()

# Funkcija, kura noņema visu informaciju no laukiem
def notirit_tekstu():
    dalas_ieraksts.delete(0, END)
    klienta_ieraksts.delete(0, END)
    veikala_ieraksts.delete(0, END)
    cenas_ieraksts.delete(0, END)


# Izveido jaunu logu ar GUI, izmantojot TKinteru
logs = Tk()

# Daļas informacija
dala_teksts = StringVar()

dalas_vards = Label(logs, text='Daļas Vards', font=('bold', 14), pady=20)
dalas_vards.grid(row=0, column=0, sticky=W)

dalas_ieraksts = Entry(logs, textvariable=dala_teksts)
dalas_ieraksts.grid(row=0, column=1)

# Klientu informacija
klients_teksts = StringVar()

klientu_vards = Label(logs, text='Klients', font=('bold', 14))
klientu_vards.grid(row=0, column=2, sticky=W)

klienta_ieraksts = Entry(logs, textvariable=klients_teksts)
klienta_ieraksts.grid(row=0, column=3)

# Veikala informacija
veikals_teksts = StringVar()

veikala_vards = Label(logs, text='Veikals', font=('bold', 14))
veikala_vards.grid(row=1, column=0, sticky=W)

veikala_ieraksts = Entry(logs, textvariable=veikals_teksts)
veikala_ieraksts.grid(row=1, column=1)

# Cenas Informacija
cena_teksts = StringVar()

cenu_vards = Label(logs, text='Cena  (EUR)', font=('bold', 14))
cenu_vards.grid(row=1, column=2, sticky=W)

cenas_ieraksts = Entry(logs, textvariable=cena_teksts)
cenas_ieraksts.grid(row=1, column=3)

# Daļas Saraksts (Listbox)
dalas_saraksts = Listbox(logs, height=8, width=50, border=0)
dalas_saraksts.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# Ritjosla (Scrollbar)
ritjosla = Scrollbar(logs)
ritjosla.grid(row=3, column=3)

# Pievieno ritjoslu pie sarakstu
dalas_saraksts.configure(yscrollcommand=ritjosla.set)
ritjosla.configure(command=dalas_saraksts.yview)

# Pievieno izvele pie sarakstu
dalas_saraksts.bind('<<ListboxSelect>>', lambda e: izvele_dalu())

# Pogas
pievieno_poga = Button(logs, text='Pievieno Daļu', width=12, command=pievienot_dalu)
pievieno_poga.grid(row=2, column=0, pady=20)

nonemt_poga = Button(logs, text='Noņemt Daļu', width=12, command=nonemt_dalu)
nonemt_poga.grid(row=2, column=1)

mainit_poga = Button(logs, text='Mainīt Daļu', width=12, command=mainit_dalu)
mainit_poga.grid(row=2, column=2)

iztuksot_poga = Button(logs, text='Notīrīt Ievadi', width=12, command=notirit_tekstu)
iztuksot_poga.grid(row=2, column=3)

#Logu vārds un izmērs
logs.title('Daļas Noliktāva')
logs.geometry('500x350')

# Funkcija, kura ievada datus, kas lietotajs sāk programmu
datu_lasisana()

# TKintera galvenais cikls, kurš vada GUI procesus
logs.mainloop()