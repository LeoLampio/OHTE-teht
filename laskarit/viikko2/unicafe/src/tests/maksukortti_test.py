import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortti_saldo_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_lataus_toimii(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 20.0)

    def test_saldo_vahenee(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_ota_true(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_ota_false(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)

    def test_to_string(self):
        self.assertEqual(self.maksukortti.__str__(), "Kortilla on rahaa 10.00 euroa")