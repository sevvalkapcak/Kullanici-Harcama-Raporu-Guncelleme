from benim_exceptions import *


class Harcama:
    """ Harcama sinifi
    """

    def __init__(self, harcama_ismi, tarih, kategori, harcama_tutari):
        self.harcama_ismi = harcama_ismi
        self.tarih = tarih
        self.kategori = kategori
        self.harcama_tutari = harcama_tutari

    def __str__(self):
        return self.harcama_ismi + "," + self.tarih + "," + self.kategori + "," + str(self.harcama_tutari) + "\n"

    def __eq__(self, other):
        """ Bir Harcama nesnesi, eger butun elemanlari ayniysa baska bir harcama nesnesine esittir.
        """
        return (self.harcama_ismi == other.harcama_ismi and self.tarih == other.tarih and 
                self.kategori == other.kategori and self.harcama_tutari == other.harcama_tutari)


class Butce:
    """ Butce nesneleri icin baz sinif. 
    """

    def __init__(self, butce_ismi, butce_limiti, harcama_toplami = 0):
        self.butce_ismi = butce_ismi
        self.harcama_toplami = harcama_toplami
        self.butce_limiti = butce_limiti
        self.harcamalar = []

    def harcama_toplami_sifirla(self):
        self.harcama_toplami = 0.0


    def harcama_ekle(self, harcama: Harcama):
        """ Harcama sinifi ile cagirilan bir harcamayi toplama ekle

            Args:
                harcama: Eklenecek harcama sinifi
            
            Returns:
                True: Harcama tutari harcama limitinin altinda, False: Degil!
        """
        self.harcama_toplami += harcama.harcama_tutari
        self.harcamalar.append(harcama)
        return self.harcama_toplami <= self.butce_limiti

    def harcama_cikar(self, harcama: Harcama):
        """ Harcama sinifi ile cagirilan bir harcamayi toplamdan cikar

            Butce ustu harcamalari geri cikarmak icin kullanilabilir. Ya da iade olunan parayi geri yatirmak icin.
            Harcama toplami hicbir zaman sifirdan kucuk olamaz.

            Args:
                harcama: Eklenecek harcama sinifi
            
            Returns:
                True: Harcama tutari harcama limitinin altinda, False: Degil!
        """
        self.harcamalar.remove(harcama)
        self.harcama_toplami = max(0.0, self.harcama_toplami - harcama.harcama_tutari)
        

    def butce_ortalamasi(self):
        return self.harcama_toplami / self.butce_limiti

    def kalan_hesapla(self):
        return self.butce_limiti - self.harcama_toplami

    def __str__(self):
        to_str = ''
        for harcama in self.harcamalar:
            to_str += harcama.__str__()
        return to_str

class KategorikButce(Butce):
    ''' Kategorik butce sinifi: Butce sinifindan tureyerek kategori eklenmesini saglar
    '''

    def __init__(self, kategori, butce_limiti, butce_harcama = 0.0):
        super().__init__("Butce_"+kategori, butce_limiti, butce_harcama)
        self.kategori = kategori

    def __str__(self):
        to_str = "-"*30+"\n"
        to_str += "Kategori: {}, Butce_limiti: {}, Toplam Harcama: {}, Yuzde Kullanim: {}\n".format(
                                                self.kategori, self.butce_limiti, self.harcama_toplami, self.butce_ortalamasi())
        to_str += super().__str__()
        return to_str




class AylikButce(Butce):
    ''' Aylik butce sinifi: Butce sinifindan tureyerek kategoriler listesi barindirir.
    '''

    def __init__(self,  butce_limiti, butce_ay, kategorik_isimler = [], kategorik_yuzdeler= [], butce_harcama = 0.0 ):
         super().__init__("Toplam_Butce", butce_limiti, butce_harcama)
         # Aylik butce
         self.butce_ay = butce_ay
         self.butce_limiti = float(butce_limiti)
         
         # Kategorik butce nesnesi dict olustur
         self.kategorik_butceler = {}
         for i in range(len(kategorik_isimler)):

             self.kategorik_butceler[kategorik_isimler[i]] = KategorikButce(kategorik_isimler[i], 
                                                                            self.butce_limiti*kategorik_yuzdeler[i]/100)

    def harcama_toplami_sifirla(self):
        """ Tum kategorik butceleri ve kendini sifirlar
        """
        for key in self.kategorik_butceler.keys():
            self.kategorik_butceler[key].harcama_toplami_sifirla()
        self.harcama_toplami_sifirla()

    def harcama_ekle(self, harcama: Harcama):
        """ Kategorik butcelerde harcama sinifi uyan butcede harcama ekler.

        Args:
        harcama: Eklenecek harcama sinifi

        Returns:
        True: Harcama tutari harcama limitinin altinda, False: Degil!
        """
        try:
            self.kategorik_butceler[harcama.kategori]
        except KeyError:
            raise CategoryMismatchError("Harcama kategorisi {}, kategori sozlugunde bulunamadi {}".format(
                                                                                harcama.kategori, list(self.kategorik_butceler.keys())))

        

        if (not self.kategorik_butceler[harcama.kategori].harcama_ekle(harcama)):
            # Kategorik butce asildi!, degeri geri cikarip hata ver!
            self.kategorik_butceler[harcama.kategori].harcama_cikar(harcama)
            raise BudgetLimitExceededError("{} harcamasi, katgorik butce {} i asiyor. Harcama tutari: {}, Kategorik butce limiti {}, Kategorik Kullanilan Butce {}".format(
                                                harcama.harcama_ismi, harcama.kategori, 
                                                harcama.harcama_tutari, self.kategorik_butceler[harcama.kategori].butce_limiti,
                                                self.kategorik_butceler[harcama.kategori].harcama_toplami))
        else:
            super().harcama_ekle(harcama)

    def harcama_cikar(self, harcama):
        self.kategorik_butceler[harcama.kategori].harcama_cikar(harcama)
        return super().harcama_cikar(harcama)

    def __str__(self):
        to_str = "Butce Ayi: {}, Toplam Butce Limiti: {}, Butce Harcama Yuzdesi: {}\n".format(self.butce_ay, self.butce_limiti, self.butce_ortalamasi())

        for value in self.kategorik_butceler.values():
            to_str += value.__str__()
        
        to_str += "-"*30+"\n"
        to_str += "Kalan para: {}\n".format(self.kalan_hesapla())
        return to_str

        
