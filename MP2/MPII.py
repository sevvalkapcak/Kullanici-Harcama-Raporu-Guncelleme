import tkinter.filedialog as fd
import tkinter as tk
import dbm
import pyexcel as pe
import tkinter.messagebox as msgbox
from labII_siniflar_v2 import Harcama, AylikButce
from LabIV import PlotEkrani
from LabIII import VisualInterface as VI
from benim_exceptions import BudgetBaseException



class ListeEkrani(VI):

    def __init__(self, parent, butce):
        super().__init__(parent)
        self.butce = butce
        self.plt = PlotEkrani(parent, 600, 300)

    def plot_butce(self):
        self.plt.canvas_bg.delete('all')
        butce_yuzdeleri = []
        for kategori, butce_ in self.butce.kategorik_butceler.items():
            butce_yuzdeleri.append(butce_.butce_ortalamasi()*100)
        self.plt.bar_diagram(butce_yuzdeleri)

    def liste2harcama(self, liste_elemani):
        tarih, isim, kategori, miktar = liste_elemani.split(',')
        return Harcama(
            isim.strip(), tarih.strip(), kategori.strip(), float(miktar))

    def liste_eleman_ekle(self):
        ''' Listeye eleman ekleme icin once VI sinifindaki yapiyi, sonrasinda ise self.butce.harcama fonksiyonunu kullaniyoruz.
        '''
        super().liste_eleman_ekle()
        for harcama in self.harcamalar.values():
            harcama_nesne = self.liste2harcama(harcama)
            try:
                self.butce.harcama_ekle(harcama_nesne)
            except BudgetBaseException as error:
                # Bekledigimiz bir hata gelirse (mantiksal hata), kullaniciya uyari ver!
                msgbox.showerror(title="Butce Asmasi", message=error)

        self.plot_butce()
        

    def secili_sil(self):
        ''' Secili nesneyi hem gorsel olarak hem de butce sinifindan cikar
        '''
        secili = self.harcamalar[self.lb.curselection()[0]]
        harcama_nesne = self.liste2harcama(secili)
        self.butce.harcama_cikar(harcama_nesne)
        super().secili_sil()
        self.plot_butce()

    def tumunu_sil(self):
        # burce.harcamalar listesi for dongusu icinde degistigi icin donguyu onun kopyalanmis hali ile gezmemiz gerekiyor
        # Alternatif olarak VisualInterface sinifinin harcamalar listesi ile de dolasilabilirdi
        butceharcamalari_derinkopya = list(self.butce.harcamalar)
        for harcama in butceharcamalari_derinkopya:
            try:
                self.butce.harcama_cikar(harcama)
            except:
                print("Harcama {} zaten silinmis".format(harcama))
        super().tumunu_sil()
        self.plot_butce()

def __main__():

    try:
        butce = AylikButce(
            10000, 'mart', ["Yiyecek", "Icecek", "Giyim", "Elektronik", "Ev"], [25, 5, 15, 20, 35])
    except BudgetBaseException as error:
        msgbox.showerror(title="Butce Asmasi", message=error)


    root = tk.Tk()
    root.title("Harcama Raporu")
    root.geometry("650x650+400+100")
    
    ListeEkrani(root, butce)
    
   
    root.mainloop()


__main__()
