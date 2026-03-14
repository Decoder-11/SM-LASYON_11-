#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
İSTATİSTİKSEL ANALİZ TEST MODÜLü
================================================================================
Tarih: 2026-03-14
Amaç: istatistiksel_analiz.py modülü için birim testleri
================================================================================
"""

import unittest
import math
import os
import json
import sys

# Modülü import et
try:
    from istatistiksel_analiz import (
        VerifiedConstants,
        SimulationConstants,
        SignificanceLevel,
        StatisticalResult,
        MonteCarloAnalyzer,
        BayesianAnalyzer,
        BenfordAnalyzer,
        CorrelationAnalyzer,
        HypothesisTester,
        StatisticalValidationEngine,
        Colors,
        SCIPY_AVAILABLE
    )
    MODULE_AVAILABLE = True
except ImportError as e:
    MODULE_AVAILABLE = False
    print(f"UYARI: istatistiksel_analiz modülü import edilemedi: {e}")


class TestVerifiedConstants(unittest.TestCase):
    """NASA/CODATA doğrulanmış sabitler testleri."""
    
    def test_speed_of_light_ms(self):
        """Işık hızı (m/s) doğru mu?"""
        self.assertEqual(VerifiedConstants.SPEED_OF_LIGHT_MS, 299_792_458)
    
    def test_speed_of_light_kms(self):
        """Işık hızı (km/s) doğru mu?"""
        self.assertAlmostEqual(VerifiedConstants.SPEED_OF_LIGHT_KMS, 299792.458, places=3)
    
    def test_gravitational_constant(self):
        """Evrensel çekim sabiti doğru mu?"""
        self.assertAlmostEqual(VerifiedConstants.GRAVITATIONAL_CONSTANT, 6.67430e-11, places=16)
    
    def test_planck_constant(self):
        """Planck sabiti doğru mu?"""
        self.assertEqual(VerifiedConstants.PLANCK_CONSTANT, 6.62607015e-34)
    
    def test_earth_radius_mean(self):
        """Dünya ortalama yarıçapı doğru mu?"""
        self.assertEqual(VerifiedConstants.EARTH_RADIUS_MEAN, 6371.0)
    
    def test_moon_mean_distance(self):
        """Ay ortalama uzaklığı doğru mu?"""
        self.assertEqual(VerifiedConstants.MOON_MEAN_DISTANCE, 384400.0)
    
    def test_giza_latitude(self):
        """Giza enlemi doğru mu?"""
        self.assertAlmostEqual(VerifiedConstants.GIZA_LATITUDE, 29.9792, places=4)
    
    def test_fine_structure_inverse(self):
        """İnce yapı sabiti tersi (~137) doğru mu?"""
        self.assertAlmostEqual(VerifiedConstants.FINE_STRUCTURE_INVERSE, 137.036, places=2)


class TestSimulationConstants(unittest.TestCase):
    """Simülasyon sabitleri testleri."""
    
    def test_base_11(self):
        """Baz 11 doğru mu?"""
        self.assertEqual(SimulationConstants.BASE_11, 11)
    
    def test_r11(self):
        """R11 repunit doğru mu?"""
        self.assertEqual(SimulationConstants.R11, 11111111111)
    
    def test_r11_factors(self):
        """R11 faktörleri çarpılınca R11 vermeli."""
        result = SimulationConstants.R11_FACTOR_1 * SimulationConstants.R11_FACTOR_2
        self.assertEqual(result, SimulationConstants.R11)
    
    def test_ideal_year(self):
        """İdeal yıl 363 gün mü?"""
        self.assertEqual(SimulationConstants.IDEAL_YEAR, 363)
    
    def test_simulation_duration(self):
        """Simülasyon süresi 11111 yıl mı?"""
        self.assertEqual(SimulationConstants.SIMULATION_DURATION, 11111)
    
    def test_drift_per_year(self):
        """Yıllık sapma doğru mu?"""
        expected_drift = SimulationConstants.REAL_YEAR - SimulationConstants.IDEAL_YEAR
        self.assertAlmostEqual(SimulationConstants.DRIFT_PER_YEAR, expected_drift, places=2)
    
    def test_halley_cycle_extended(self):
        """Halley genişletilmiş döngüsü 11 × 74 mı?"""
        self.assertEqual(SimulationConstants.HALLEY_CYCLE_EXTENDED, 11 * 74)


class TestStatisticalResult(unittest.TestCase):
    """İstatistiksel sonuç sınıfı testleri."""
    
    def test_highly_significant(self):
        """p < 0.0001 için yüksek anlamlılık."""
        result = StatisticalResult(
            test_name="Test",
            statistic=10.0,
            p_value=0.00001
        )
        self.assertEqual(result.significance_level, SignificanceLevel.HIGHLY_SIGNIFICANT)
        self.assertTrue(result.is_significant())
    
    def test_significant(self):
        """p < 0.01 için anlamlılık."""
        result = StatisticalResult(
            test_name="Test",
            statistic=5.0,
            p_value=0.005
        )
        self.assertEqual(result.significance_level, SignificanceLevel.SIGNIFICANT)
        self.assertTrue(result.is_significant())
    
    def test_not_significant(self):
        """p >= 0.05 için anlamsızlık."""
        result = StatisticalResult(
            test_name="Test",
            statistic=1.0,
            p_value=0.10
        )
        self.assertEqual(result.significance_level, SignificanceLevel.NOT_SIGNIFICANT)
        self.assertFalse(result.is_significant())
    
    def test_to_dict(self):
        """Sözlük dönüşümü çalışıyor mu?"""
        result = StatisticalResult(
            test_name="Test",
            statistic=5.0,
            p_value=0.01
        )
        d = result.to_dict()
        self.assertEqual(d["test_name"], "Test")
        self.assertEqual(d["statistic"], 5.0)
        self.assertEqual(d["p_value"], 0.01)


class TestMonteCarloAnalyzer(unittest.TestCase):
    """Monte Carlo analizci testleri."""
    
    def setUp(self):
        """Test için Monte Carlo analizci oluştur."""
        self.mc = MonteCarloAnalyzer(iterations=1000, seed=42)
    
    def test_haversine_distance(self):
        """Haversine formülü doğru mu?"""
        # Ekvator üzerinde 0° - 90° arası ≈ 10007.5 km
        distance = self.mc._haversine_distance(0, 0, 0, 90)
        self.assertAlmostEqual(distance, 10007.5, delta=1)
    
    def test_haversine_poles(self):
        """Kuzey-Güney kutup mesafesi ≈ 20015 km."""
        distance = self.mc._haversine_distance(90, 0, -90, 0)
        self.assertAlmostEqual(distance, 20015.1, delta=1)
    
    def test_giza_light_speed_test_runs(self):
        """Giza-ışık hızı testi çalışıyor mu?"""
        result = self.mc.giza_light_speed_correlation()
        self.assertIsInstance(result, StatisticalResult)
        self.assertGreaterEqual(result.p_value, 0)
        self.assertLessEqual(result.p_value, 1)
    
    def test_sirius_frequency_test_runs(self):
        """Sirius frekansı testi çalışıyor mu?"""
        result = self.mc.sirius_frequency_validation()
        self.assertIsInstance(result, StatisticalResult)
        self.assertGreaterEqual(result.p_value, 0)
        self.assertLessEqual(result.p_value, 1)
    
    def test_run_all_tests(self):
        """Tüm testler çalışıyor mu?"""
        results = self.mc.run_all_tests()
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertIsInstance(r, StatisticalResult)


class TestBayesianAnalyzer(unittest.TestCase):
    """Bayesian analizci testleri."""
    
    def setUp(self):
        """Test için Bayesian analizci oluştur."""
        self.bayes = BayesianAnalyzer(prior_h1=0.01)
    
    def test_initial_prior(self):
        """Başlangıç öncülü doğru mu?"""
        self.assertEqual(self.bayes.prior_h1, 0.01)
        self.assertEqual(self.bayes.posterior_h1, 0.01)
    
    def test_update_increases_posterior(self):
        """Yüksek uyum posterior'u artırmalı."""
        initial = self.bayes.posterior_h1
        self.bayes.update("Test", 100, 100, 0.05)  # Mükemmel eşleşme
        self.assertGreater(self.bayes.posterior_h1, initial)
    
    def test_bayes_factor_interpretation(self):
        """Bayes faktörü yorumlaması çalışıyor mu?"""
        interp = self.bayes._interpret_bayes_factor(150)
        self.assertEqual(interp, "Kesin Kanıt (H1)")
        
        interp = self.bayes._interpret_bayes_factor(0.005)
        self.assertEqual(interp, "Çok Güçlü Kanıt (H0)")
    
    def test_comprehensive_analysis_runs(self):
        """Kapsamlı analiz çalışıyor mu?"""
        result = self.bayes.run_comprehensive_analysis()
        self.assertIn("final_posterior_h1", result)
        self.assertIn("updates", result)
        self.assertIn("conclusion", result)


class TestBenfordAnalyzer(unittest.TestCase):
    """Benford analizci testleri."""
    
    def test_first_digit(self):
        """İlk basamak tespiti doğru mu?"""
        benford = BenfordAnalyzer([123, 456, 789])
        self.assertEqual(benford._first_digit(123.45), 1)
        self.assertEqual(benford._first_digit(9.99), 9)
        self.assertEqual(benford._first_digit(0.00123), 1)
    
    def test_observed_frequencies(self):
        """Gözlenen frekanslar doğru mu?"""
        data = [1, 2, 3, 10, 20, 30, 100, 200, 300]
        benford = BenfordAnalyzer(data)
        freq = benford.observed_frequencies()
        self.assertEqual(freq[1], 3)  # 1, 10, 100
        self.assertEqual(freq[2], 3)  # 2, 20, 200
        self.assertEqual(freq[3], 3)  # 3, 30, 300
    
    def test_benford_expected_sum(self):
        """Benford beklenen oranları toplamı ~100 mü?"""
        total = sum(BenfordAnalyzer.BENFORD_EXPECTED.values())
        self.assertAlmostEqual(total, 100, places=0)


@unittest.skipIf(not SCIPY_AVAILABLE, "scipy gerekli")
class TestCorrelationAnalyzer(unittest.TestCase):
    """Korelasyon analizci testleri (scipy gerekli)."""
    
    def setUp(self):
        """Test için korelasyon analizci oluştur."""
        self.corr = CorrelationAnalyzer()
    
    def test_perfect_positive_correlation(self):
        """Mükemmel pozitif korelasyon r = 1."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]  # y = 2x
        result = self.corr.pearson_correlation(x, y)
        self.assertAlmostEqual(result.statistic, 1.0, places=5)
    
    def test_perfect_negative_correlation(self):
        """Mükemmel negatif korelasyon r = -1."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]  # y = -2x + 12
        result = self.corr.pearson_correlation(x, y)
        self.assertAlmostEqual(result.statistic, -1.0, places=5)
    
    def test_spearman_correlation(self):
        """Spearman korelasyonu çalışıyor mu?"""
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]  # y = x²
        result = self.corr.spearman_correlation(x, y)
        self.assertIsInstance(result, StatisticalResult)
        self.assertAlmostEqual(result.statistic, 1.0, places=5)


@unittest.skipIf(not SCIPY_AVAILABLE, "scipy gerekli")
class TestHypothesisTester(unittest.TestCase):
    """Hipotez test sınıfı testleri (scipy gerekli)."""
    
    def setUp(self):
        """Test için hipotez test sınıfı oluştur."""
        self.tester = HypothesisTester()
    
    def test_one_sample_t_test_same_mean(self):
        """Aynı ortalama için H0 kabul edilmeli."""
        # Küçük varyans ile ortalama ~10
        data = [9.9, 10.0, 10.1, 10.0, 9.95, 10.05]
        result = self.tester.one_sample_t_test(data, 10)
        # p-değeri yüksek olmalı (H0 kabul)
        self.assertGreater(result.p_value, 0.05)
    
    def test_one_sample_t_test_different_mean(self):
        """Farklı ortalama için H0 reddedilmeli."""
        import numpy as np
        np.random.seed(42)
        data = list(np.random.normal(100, 5, 100))  # Ortalama ≈ 100
        result = self.tester.one_sample_t_test(data, 50)  # 50 ile karşılaştır
        # p-değeri düşük olmalı (H0 red)
        self.assertLess(result.p_value, 0.05)


class TestStatisticalValidationEngine(unittest.TestCase):
    """Ana doğrulama motoru testleri."""
    
    def test_engine_initialization(self):
        """Motor düzgün başlatılıyor mu?"""
        engine = StatisticalValidationEngine(monte_carlo_iterations=100)
        self.assertEqual(engine.monte_carlo.iterations, 100)
        self.assertIsNotNone(engine.bayesian)
        self.assertIsNotNone(engine.correlation)
        self.assertIsNotNone(engine.hypothesis)
    
    def test_engine_runs(self):
        """Motor çalışıyor mu?"""
        engine = StatisticalValidationEngine(monte_carlo_iterations=100)
        summary = engine.run_comprehensive_validation()
        
        self.assertIn("timestamp", summary)
        self.assertIn("total_tests", summary)
        self.assertIn("significant_tests", summary)
        self.assertIn("conclusion", summary)
    
    def test_json_export(self):
        """JSON export çalışıyor mu?"""
        engine = StatisticalValidationEngine(monte_carlo_iterations=100)
        filepath = "/tmp/test_istatistiksel_sonuclar.json"
        engine.export_json(filepath)
        
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.assertIn("timestamp", data)
        self.assertIn("all_results", data)
        
        # Temizle
        os.remove(filepath)


class TestIntegration(unittest.TestCase):
    """Entegrasyon testleri."""
    
    def test_full_pipeline(self):
        """Tam pipeline çalışıyor mu?"""
        # Küçük iterasyon sayısı ile hızlı test
        engine = StatisticalValidationEngine(monte_carlo_iterations=100)
        summary = engine.run_comprehensive_validation()
        
        # Temel kontroller
        self.assertGreater(summary["total_tests"], 0)
        self.assertGreaterEqual(summary["significant_tests"], 0)
        self.assertLessEqual(summary["significant_tests"], summary["total_tests"])
        self.assertIn("conclusion", summary)
    
    def test_levhi_mahfuz_integration(self):
        """Levhi Mahfuz sabitleri ile entegrasyon."""
        try:
            from levhi_mahfuz import LevhiMahfuzConstants as LMC
            
            # Sabitler karşılaştırması
            self.assertEqual(LMC.BASE_SYSTEM, SimulationConstants.BASE_11)
            self.assertEqual(LMC.R11, SimulationConstants.R11)
            
        except ImportError:
            self.skipTest("levhi_mahfuz modülü mevcut değil")


def run_tests():
    """Testleri çalıştır."""
    print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}İSTATİSTİKSEL ANALİZ BİRİM TESTLERİ{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"scipy mevcut: {SCIPY_AVAILABLE}")
    print()
    
    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tüm test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestVerifiedConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulationConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalResult))
    suite.addTests(loader.loadTestsFromTestCase(TestMonteCarloAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestBayesianAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestBenfordAnalyzer))
    
    if SCIPY_AVAILABLE:
        suite.addTests(loader.loadTestsFromTestCase(TestCorrelationAnalyzer))
        suite.addTests(loader.loadTestsFromTestCase(TestHypothesisTester))
    
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticalValidationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Özet
    print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}TEST ÖZETİ{Colors.ENDC}")
    print(f"{'=' * 80}")
    print(f"Toplam Test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print(f"Atlanan: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print(f"\n{Colors.GREEN}✓ TÜM TESTLER BAŞARILI{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}✗ BAZI TESTLER BAŞARISIZ{Colors.ENDC}")
    
    return result


if __name__ == "__main__":
    if MODULE_AVAILABLE:
        run_tests()
    else:
        print("Modül import edilemedi, testler çalıştırılamıyor.")
        sys.exit(1)
