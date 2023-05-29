import tkinter.filedialog as fd
import tkinter as tk

class VisualInterface(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self , parent)
        self.parent = parent
        self.harcamalar = {}
        self.initUI()
        
    def initUI(self):
        
        self.lb = tk.Listbox(self, selectmode="single")
        self.lb.pack(fill=tk.BOTH, expand=True)

        self.buton_ekle = tk.Button(self, text="Aktar", command = self.liste_olustur)
        self.buton_secilisil = tk.Button(self, text="Secili Sil", command = self.secili_sil)
        self.buton_hepsinisil = tk.Button(self, text="Hepsini Sil", command = self.tumunu_sil)
        self.buton_ekle.pack(side=tk.LEFT)
        self.buton_secilisil.pack(side=tk.LEFT)
        self.buton_hepsinisil.pack(side=tk.LEFT)
        self.pack(fill=tk.BOTH, expand=True)

    def liste_olustur(self):
        self.liste_eleman_ekle()
        self.lb.pack(expand=True)
        self.pack(fill=tk.BOTH, expand=True)

    def liste_eleman_ekle(self):
        file_name = fd.askopenfilename()
        harcamalar = self.parse_yaml(file_name)
        for indeks, harcama in enumerate(harcamalar):
            self.harcamalar[indeks] = harcama
            self.lb.insert(indeks, harcama)

    def secili_sil(self):
        selected_indeks = self.lb.curselection()[0]
        try:
            self.harcamalar.pop(selected_indeks)
        except KeyError as e:
            print(e)
        self.lb.delete(selected_indeks)

    def tumunu_sil(self):
        self.lb.delete(0, tk.END)
        self.harcamalar.clear()

    def parse_yaml(self, file_name):
        """ Yaml dosyasini yukleyip bir sozluk yapisinda geri dondurur.
      
        """
        import yaml
        with open(file_name) as file:
            document = yaml.load(file,  Loader=yaml.FullLoader)

        return document["Butce_Girdileri"]
    





