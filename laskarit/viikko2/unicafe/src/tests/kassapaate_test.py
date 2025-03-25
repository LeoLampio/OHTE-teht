import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kp = Kassapaate()
        self.kort = Maksukortti(1000)

    def test_correct_constructor(self):
        self.assertEqual(self.kp.kassassa_rahaa, 100000)
        self.assertEqual(self.kp.edulliset, 0)
        self.assertEqual(self.kp.maukkaat, 0)

    def test_edullinen_maksu_raha(self):
        v = self.kp.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kp.kassassa_rahaa, 100240)
        self.assertEqual(v, 760)
    def test_edullinen_maara(self):
        self.kp.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kp.edulliset, 1)
    def test_edullinen_ei_riita(self):
        v = self.kp.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kp.kassassa_rahaa, 100000)
        self.assertEqual(v, 100)
        self.assertEqual(self.kp.edulliset, 0)

    def test_maukas_maksu_raha(self):
        v = self.kp.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kp.kassassa_rahaa, 100400)
        self.assertEqual(v, 600)
    def test_maukas_maara(self):
        self.kp.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kp.maukkaat, 1)
    def test_maukas_ei_riita(self):
        v = self.kp.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kp.kassassa_rahaa, 100000)
        self.assertEqual(v, 100)
        self.assertEqual(self.kp.maukkaat, 0)
    
    def test_edullinen_maksu_raha_kortti(self):
        b = self.kp.syo_edullisesti_kortilla(self.kort)
        self.assertEqual(self.kort.saldo, 760)
        self.assertEqual(b, True)
    def test_edullinen_maara_kortti(self):
        self.kp.syo_edullisesti_kortilla(self.kort)
        self.assertEqual(self.kp.edulliset, 1)
    def test_edullinen_ei_riita_kortti(self):
        k = Maksukortti(100)
        b = self.kp.syo_edullisesti_kortilla(k)
        self.assertEqual(k.saldo, 100)
        self.assertEqual(b, False)
        self.assertEqual(self.kp.edulliset, 0)
    def test_edullinen_kassa_ei_muutu(self):
        self.kp.syo_edullisesti_kortilla(self.kort)
        self.assertEqual(self.kp.kassassa_rahaa, 100000)

    def test_maukas_maksu_raha_kortti(self):
        b = self.kp.syo_maukkaasti_kortilla(self.kort)
        self.assertEqual(self.kort.saldo, 600)
        self.assertEqual(b, True)
    def test_maukas_maara_kortti(self):
        self.kp.syo_maukkaasti_kortilla(self.kort)
        self.assertEqual(self.kp.maukkaat, 1)
    def test_maukas_ei_riita_kortti(self):
        k = Maksukortti(100)
        b = self.kp.syo_maukkaasti_kortilla(k)
        self.assertEqual(k.saldo, 100)
        self.assertEqual(b, False)
        self.assertEqual(self.kp.maukkaat, 0)
    def test_maukas_kassa_ei_muutu(self):
        self.kp.syo_maukkaasti_kortilla(self.kort)
        self.assertEqual(self.kp.kassassa_rahaa, 100000)

    def test_kortti_lataus(self):
        self.kp.lataa_rahaa_kortille(self.kort, 100)
        self.assertEqual(self.kp.kassassa_rahaa, 100100)
        self.assertEqual(self.kort.saldo, 1100)
    def test_kortti_lataus_neg(self):
        self.kp.lataa_rahaa_kortille(self.kort, -100)
        self.assertEqual(self.kp.kassassa_rahaa, 100000)
        self.assertEqual(self.kort.saldo, 1000)
    
    def test_kassa_eurot(self):
        self.assertEqual(self.kp.kassassa_rahaa_euroina(), 1000.0)