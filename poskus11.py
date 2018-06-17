from tkinter import *
import random 


class Kocke:
    def __init__(self, okno):
        frame = Frame(okno)
        frame.pack(fill=Y, expand=False)
        self.gumb = Button(frame, text='MET KOCKE', command=self.met_dveh_kock)
        self.gumb.grid(row=0, column=0)

        self.platno = Canvas(frame, width=800, height=164) # height=436
        self.platno.grid(row=8, column=0, columnspan=4)


        Label(frame, text='PRVA KOCKA').grid(row=1, column=0)
        self.kocka1 = IntVar(frame)
        izpis = Entry(frame, textvariable=self.kocka1).grid(row=1, column=1)
        Label(frame, text='DRUGA KOCKA').grid(row=2, column=0)
        self.kocka2 = IntVar(frame)
        izpis = Entry(frame, textvariable=self.kocka2).grid(row=2, column=1)

        Label(frame, text='NAMEN IGRE: uganiti, kateri igralec in v koliko metih bo prvi prišel na cilj.').grid(row=0, column=2)
        self.minimum = IntVar(frame)
        Label(frame, text='PREMIK').grid(row=5, column=0)
        Entry(frame, textvariable=self.minimum).grid(row=5, column=1)

        self.na_potezi = StringVar(frame)
        Label(frame, text='NA POTEZI JE').grid(row=4, column=0)
        Entry(frame, textvariable=self.na_potezi).grid(row=4, column=1)
        self.kdo_je_na_potezi()
        self.stevilo_potez = IntVar(frame)
        Label(frame, text='ŠTEVILO POTEZ').grid(row=6, column=0)
        Entry(frame, textvariable=self.stevilo_potez).grid(row=6, column=1)
        self.zgodilo_se_je = StringVar(frame)
        Label(frame, text='KAJ SE JE ZGODILO').grid(row=7, column=0)
        Entry(frame, textvariable=self.zgodilo_se_je).grid(row=7, column=1)

        Label(frame, text='Kateri igrablec bo zmagal (PRVI ali DRUGI)?').grid(row=1, column=2)
        self.zmaga = Entry(frame)
        self.zmaga.grid(row=1, column=3)
        Label(frame, text='V koliko potezah bo prišel na cilj?').grid(row=2, column=2)
        self.cilj = Entry(frame)
        self.cilj.grid(row=2, column=3)
        self.zmagovalec = StringVar(frame)
        Label(frame, text='ZMAGOVALEC JE').grid(row=3, column=2)
        Entry(frame, textvariable=self.zmagovalec).grid(row=3, column=3)
        self.rezultat = StringVar(frame)
        Label(frame, text='REZULTAT').grid(row=4, column=2)
        Entry(frame, textvariable=self.rezultat, width=42).grid(row=4, column=3)


        self.slika = PhotoImage(file='kocke.gif') #kocke = ime datoteke
        self.platno.create_image(360,150, image=self.slika) #cifri sta središče, velikost slike= 880 x 212 slike

        prvi = self.platno.create_oval(50, 30, 70, 50, fill='plum2')
        drugi = self.platno.create_oval(50, 135, 70, 155, fill='aquamarine2')
            
    
        self.polozaj = [0, 0] # [1. igralec, 2.]
        self.caka = [0, 0]
        self.poteze = [0, 0]
        self.id = [prvi, drugi]

        self.premiki = [0, 2, 0, 0, 1, 0, 3, -4, -8, 0]
        self.cakaj = [0, 0, 0, 2, 0, 0, 0, 0, 0, 0]

    
              

    def kdo_je_na_potezi(self):
        igra = random.randint(0, 1)
        self.igralec = igra
        if igra == 0:
            self.na_potezi.set('PRVI IGRALEC')
        else:
            self.na_potezi.set('DRUGI IGRALEC')

        


    def met_dveh_kock(self):
        kocka1 = random.randint(1, 6)
        kocka2 = random.randint(1, 6)
        minimum = min(kocka1, kocka2)
        self.kocka1.set(kocka1)
        self.kocka2.set(kocka2)
        self.minimum.set(minimum)
        
        
        if self.caka[self.igralec] > 0:
            self.caka[self.igralec] -= 1
            self.zgodilo_se_je.set('igralec čaka')
        else:
            self.polozaj[self.igralec] += min(minimum, 9 - self.polozaj[self.igralec])
            while self.premiki[self.polozaj[self.igralec]] != 0:
                self.polozaj[self.igralec] += self.premiki[self.polozaj[self.igralec]]
            self.zgodilo_se_je.set('igralec se je premaknil')
            self.caka[self.igralec] = self.cakaj[self.polozaj[self.igralec]]

            self.poteze[self.igralec] += 1
            self.stevilo_potez.set(self.poteze[self.igralec])
            
            x = self.polozaj[self.igralec] * 65 + 45
            y = 30 if self.igralec == 0 else 135
            self.platno.coords(self.id[self.igralec], x, y, x + 20, y + 20)

            if self.polozaj[self.igralec] == 9:
                self.konec_igre()
                return

        self.igralec = 1 - self.igralec
        kdo_igra = ['PRVI IGRALEC', 'DRUGI IGRALEC']
        self.na_potezi.set(kdo_igra[self.igralec])

        
    def konec_igre(self):
        self.gumb.config(state=DISABLED)
        #self.zmagovalec.set("jaz")
        self.zmagovalec.set(self.na_potezi.get())
        self.na_potezi.set("")
        napoved_zmagovalca = self.zmaga.get() + ' IGRALEC'
        napoved_potez = int(self.cilj.get())
        if napoved_zmagovalca != self.zmagovalec.get():
            self.rezultat.set('Več sreče prihodnjič.')
        else:
            if napoved_potez == self.poteze[self.igralec]:
                self.rezultat.set('ČESTITAMO! Uspelo Vam je napovedati izid igre.')
            else:
                self.rezultat.set('Bili ste blizu. Najbolje, da ponovno poskusite.')
       


okno = Tk()
app = Kocke(okno)
okno.mainloop()
