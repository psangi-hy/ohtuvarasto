import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_virheellinen_tilavuus(self):
        self.assertAlmostEqual(Varasto(0).tilavuus, 0)
        self.assertAlmostEqual(Varasto(-1).tilavuus, 0)
        self.assertAlmostEqual(Varasto(-2000).tilavuus, 0)

    def test_virheellinen_saldo(self):
        self.assertAlmostEqual(Varasto(10, -1).saldo, 0)
        self.assertAlmostEqual(Varasto(10, -2000).saldo, 0)

    def test_negatiivinen_lisays(self):
        vanha_saldo = self.varasto.saldo
        self.varasto.lisaa_varastoon(-2)
        # Saldon ei pitäisi muuttua.
        self.assertAlmostEqual(self.varasto.saldo, vanha_saldo)
        self.varasto.lisaa_varastoon(-4000)
        self.assertAlmostEqual(self.varasto.saldo, vanha_saldo)

    def test_lisaa_enemman_kuin_mahtuu(self):
        maara = self.varasto.paljonko_mahtuu() + 1
        self.varasto.lisaa_varastoon(maara)
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_negatiivinen_otto(self):
        self.varasto.lisaa_varastoon(5)
        vanha_saldo = self.varasto.saldo
        self.varasto.ota_varastosta(-1)
        # Saldon ei pitäisi muuttua.
        self.assertAlmostEqual(self.varasto.saldo, vanha_saldo)
        self.varasto.ota_varastosta(-2000)
        self.assertAlmostEqual(self.varasto.saldo, vanha_saldo)

    def test_ota_enemman_kuin_on(self):
        self.varasto.ota_varastosta(2)
        # Varastoon ei voi jäädä alle 0
        self.assertAlmostEqual(self.varasto.saldo, 0)
        self.varasto.lisaa_varastoon(5)
        self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_str(self):
        self.assertEqual(str(self.varasto), "saldo = 0, vielä tilaa 10")
        self.varasto.lisaa_varastoon(10)
        self.assertEqual(str(self.varasto), "saldo = 10, vielä tilaa 0")
        self.varasto.ota_varastosta(4.5)
        self.assertEqual(str(self.varasto), "saldo = 5.5, vielä tilaa 4.5")
