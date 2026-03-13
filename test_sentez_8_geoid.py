#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TEST SENTEZ-8 GEOID MATRIX VERIFICATION
DÜNYA GEOİT MATRİSİ VE PİRAMİDAL ÇARPANLAR (22-66-88)
================================================================================
Purpose: Verify SENTEZ-8 Geoid Matrix calculations:
  - Lambda from Geoid: 88 × 74 = 6512 ≈ 6.52 MHz
  - Gravity from Geoid: 88 / 2.99² = 9.843 ≈ g (9.81 m/s²)
  - Cyclic Matrix: 66 / 2.99 = 22, 22 × 2.99 = 66
  - Pi_11 Light Speed: 2.99 × 100000 = 299000 ≈ C_REAL
  - Cross-references with Sentez 1-7 constants

Date: March 13, 2026
Status: SENTEZ-8 Integration Test
================================================================================
"""

import sys
import math
from datetime import datetime

# Import SENTEZ-8 class from simulasyon_11.py
try:
    from simulasyon_11 import (
        Geoid_Matrix_22_66_88,
        verify_sentez8_geoid_matrix,
        Sentez7_MasterConstants,
        Colors
    )
except ImportError as e:
    print(f"❌ ERROR: Could not import SENTEZ-8 classes: {e}")
    sys.exit(1)

# Import Levhi Mahfuz for cross-validation
try:
    from levhi_mahfuz import LevhiMahfuzConstants as LMC
    from levhi_mahfuz import KarTopuSentezConstants as KTS
except ImportError:
    LMC = None
    KTS = None


# ==============================================================================
# TEST RUNNER: SENTEZ-8 GEOID MATRIX
# ==============================================================================

class TestSentez8GeoidMatrix:
    """Complete test suite for SENTEZ-8 Geoid Matrix constants and formulas"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.timestamp = datetime.now().isoformat()
        self.gm = Geoid_Matrix_22_66_88()
        
    def header(self):
        """Print test header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("=" * 80)
        print("SENTEZ-8 GEOID MATRIX VERIFICATION TEST SUITE")
        print("Dünya Geoit Matrisi (22-66-88) + Pi_11 Entegrasyonu")
        print("=" * 80)
        print(f"{Colors.ENDC}")
        print(f"{Colors.GOLD}Execution Time: {self.timestamp}{Colors.ENDC}\n")
    
    def _record_result(self, name, passed, details=""):
        """Record test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = f"{Colors.GREEN}✅ PASSED{Colors.ENDC}"
        else:
            self.failed_tests += 1
            status = f"{Colors.RED}❌ FAILED{Colors.ENDC}"
        
        self.test_results.append({
            "name": name,
            "passed": passed,
            "details": details
        })
        print(f"  → {name}: {status} {details}")
    
    # ==========================================================================
    # TEST 1: CONSTANTS VERIFICATION
    # ==========================================================================
    def test_constants(self):
        """Test all Geoid Matrix constants"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 1] Geoid Matrix Constants Verification{Colors.ENDC}")
        print(f"{Colors.CYAN}Purpose: Verify all 22-66-88 constants are correct{Colors.ENDC}\n")
        
        try:
            # Core constants
            self._record_result(
                "GEOIT_FARK = 22",
                self.gm.GEOIT_FARK == 22
            )
            self._record_result(
                "GEOIT_OMURGA = 66",
                self.gm.GEOIT_OMURGA == 66
            )
            self._record_result(
                "GEOIT_TOPLAM = 88",
                self.gm.GEOIT_TOPLAM == 88
            )
            self._record_result(
                "GEOIT_CARPIM = 127776 (22×66×88)",
                self.gm.GEOIT_CARPIM == 22 * 66 * 88
            )
            self._record_result(
                "PI_11 = 2.99",
                self.gm.PI_11 == 2.99
            )
            self._record_result(
                "LAMBDA_GEOIT = 6512 (88×74)",
                self.gm.LAMBDA_GEOIT == 88 * 74
            )
            self._record_result(
                "GEOIT_FARK + GEOIT_OMURGA = GEOIT_TOPLAM",
                self.gm.GEOIT_FARK + self.gm.GEOIT_OMURGA == self.gm.GEOIT_TOPLAM
            )
            
        except Exception as e:
            self._record_result("Constants Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 2: LAMBDA FROM GEOID (88 × 74 = 6512 ≈ 6.52 MHz)
    # ==========================================================================
    def test_lambda_from_geoid(self):
        """Test Lambda frequency derivation from Geoid constants"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 2] Lambda from Geoid Verification{Colors.ENDC}")
        print(f"{Colors.CYAN}Formula: Λ_geoid = 88 × 74 (Halley) = 6512 ≈ 6.52 MHz{Colors.ENDC}\n")
        
        try:
            result = self.gm.verify_lambda_from_geoid()
            
            self._record_result(
                "88 × 74 = 6512",
                result['lambda_value'] == 6512
            )
            self._record_result(
                "Lambda ≈ 6.52 MHz (deviation < 1%)",
                result['deviation_percent'] < 1.0,
                f"(deviation: {result['deviation_percent']:.4f}%)"
            )
            self._record_result(
                "Yol1 = Yol2 (176×37 = 6512)",
                result['yol1_match']
            )
            
            # Cross-check with SENTEZ-7
            sentez7_lambda = Sentez7_MasterConstants.LAMBDA_BREAK_FREQ
            lambda_diff = abs(result['lambda_mhz'] - sentez7_lambda)
            self._record_result(
                f"Sentez-7 Lambda match ({sentez7_lambda} MHz)",
                lambda_diff < 0.05,
                f"(diff: {lambda_diff:.3f} MHz)"
            )
            
        except Exception as e:
            self._record_result("Lambda Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 3: GRAVITY FROM GEOID (88 / 2.99² = 9.843 ≈ g)
    # ==========================================================================
    def test_gravity_from_geoid(self):
        """Test gravity derivation from Geoid and Pi_11"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 3] Gravity from Geoid Verification{Colors.ENDC}")
        print(f"{Colors.CYAN}Formula: g = 88 / 2.99² = 88 / 8.9401 = 9.843 ≈ 9.81{Colors.ENDC}\n")
        
        try:
            result = self.gm.gravity_from_geoid()
            
            self._record_result(
                "g_geoid ≈ 9.81 (deviation < 1%)",
                result['deviation_percent'] < 1.0,
                f"(g={result['g_geoid']:.6f}, deviation: {result['deviation_percent']:.4f}%)"
            )
            
            # Direct calculation check
            g_calc = 88 / (2.99 ** 2)
            self._record_result(
                "Direct: 88/2.99² = 9.843",
                abs(g_calc - 9.843) < 0.01,
                f"(calculated: {g_calc:.6f})"
            )
            
            # Pi_11² × 11 ≈ g × 10
            pi11_sq_x11 = (2.99 ** 2) * 11
            g_x_10 = 9.80665 * 10
            self._record_result(
                "Pi_11² × 11 ≈ g × 10",
                abs(pi11_sq_x11 - g_x_10) < 1.0,
                f"({pi11_sq_x11:.2f} ≈ {g_x_10:.2f})"
            )
            
        except Exception as e:
            self._record_result("Gravity Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 4: CYCLIC MATRIX (66/2.99=22, 22×2.99=66)
    # ==========================================================================
    def test_cyclic_matrix(self):
        """Test cyclic matrix proof"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 4] Cyclic Matrix Verification{Colors.ENDC}")
        print(f"{Colors.CYAN}Cycle: 66→22→66→22 (Pi_11 döngüsel matris){Colors.ENDC}\n")
        
        try:
            result = self.gm.cyclic_matrix_test()
            
            # 66 / 2.99 ≈ 22
            self._record_result(
                "66 / 2.99 ≈ 22",
                result['cycle_forward_int'] == 22,
                f"(actual: {result['cycle_forward']:.4f})"
            )
            
            # 22 × 2.99 ≈ 66
            self._record_result(
                "22 × 2.99 ≈ 66",
                result['cycle_reverse_int'] == 66,
                f"(actual: {result['cycle_reverse']:.4f})"
            )
            
            # Cyclic proof
            self._record_result(
                "Cyclic loop verified (66→22→66)",
                result['is_cyclic']
            )
            
            # Orbital velocity
            self._record_result(
                "88/2.99 ≈ 29.78 km/s (Earth orbital)",
                result['orbital_deviation_pct'] < 2.0,
                f"(velocity: {result['orbital_velocity_kms']:.2f} km/s, deviation: {result['orbital_deviation_pct']:.2f}%)"
            )
            
            # 11² dimension lock
            self._record_result(
                "363/2.99 ≈ 121 = 11²",
                result['dimension_deviation_pct'] < 1.0,
                f"(ratio: {result['year_pi11_ratio']:.2f}, deviation: {result['dimension_deviation_pct']:.2f}%)"
            )
            
        except Exception as e:
            self._record_result("Cyclic Matrix Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 5: PI_11 LIGHT SPEED BRIDGE
    # ==========================================================================
    def test_pi11_light_speed(self):
        """Test Pi_11 connection to light speed"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 5] Pi_11 Light Speed Bridge{Colors.ENDC}")
        print(f"{Colors.CYAN}Formula: Pi_11 × 100000 = 299000 ≈ C_REAL{Colors.ENDC}\n")
        
        try:
            pi_11 = self.gm.PI_11
            c_real = 299792.458  # km/s (CODATA)
            
            c_pi11 = pi_11 * 100_000  # 299000
            deviation = abs(c_pi11 - c_real) / c_real * 100
            
            self._record_result(
                "Pi_11 × 100K ≈ C_REAL",
                deviation < 1.0,
                f"({c_pi11:.0f} vs {c_real:.3f}, deviation: {deviation:.4f}%)"
            )
            
            # Pi_11 = C_REAL / 100000
            pi_from_c = c_real / 100_000
            self._record_result(
                "C_REAL / 100K ≈ Pi_11",
                abs(pi_from_c - pi_11) < 0.01,
                f"({pi_from_c:.5f} ≈ {pi_11})"
            )
            
        except Exception as e:
            self._record_result("Pi_11 Light Speed Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 6: CROSS-REFERENCE WITH SENTEZ 1-7
    # ==========================================================================
    def test_cross_references(self):
        """Test cross-references with existing constants"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 6] Cross-Reference with Sentez 1-7{Colors.ENDC}")
        print(f"{Colors.CYAN}Purpose: Validate Geoid constants against all prior discoveries{Colors.ENDC}\n")
        
        try:
            # GEOIT_OMURGA = VERTEBRAE_TOTAL (from levhi_mahfuz)
            if LMC:
                self._record_result(
                    "GEOIT_OMURGA = VERTEBRAE_TOTAL (66)",
                    self.gm.GEOIT_OMURGA == LMC.VERTEBRAE_TOTAL
                )
                
                # WGS84 radius difference
                wgs84_diff = LMC.EARTH_RADIUS_EQUATORIAL - LMC.EARTH_RADIUS_POLAR
                self._record_result(
                    f"WGS84 Ekvator-Kutup farkı ≈ 22 km",
                    abs(wgs84_diff - 22) < 1.0,
                    f"(actual: {wgs84_diff:.3f} km)"
                )
                
                # Halley period validation
                self._record_result(
                    "HALLEY_PERIOD = 74 (ideal 11T)",
                    LMC.HALLEY_PERIOD_IDEAL == 74
                )
            
            # KarTopuSentezConstants cross-check
            if KTS:
                self._record_result(
                    "KTS.LAMBDA_FREQ_MHZ ≈ LAMBDA_GEOIT/1000",
                    abs(KTS.LAMBDA_FREQ_MHZ - self.gm.LAMBDA_GEOIT / 1000) < 0.05,
                    f"({KTS.LAMBDA_FREQ_MHZ} vs {self.gm.LAMBDA_GEOIT/1000:.3f})"
                )
                
                # Geoid constants in KTS
                if hasattr(KTS, 'GEOIT_FARK'):
                    self._record_result(
                        "KTS SENTEZ-8 constants present",
                        KTS.GEOIT_FARK == 22 and KTS.PI_11 == 2.99
                    )
            
            # Full analysis
            self.gm.cross_reference_analysis()
            
        except Exception as e:
            self._record_result("Cross-Reference Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # TEST 7: QUICK VERIFICATION FUNCTION
    # ==========================================================================
    def test_quick_verify(self):
        """Test the verify_sentez8_geoid_matrix() function"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST 7] Quick Verification Function{Colors.ENDC}")
        print(f"{Colors.CYAN}Purpose: Test verify_sentez8_geoid_matrix() integrity{Colors.ENDC}\n")
        
        try:
            result = verify_sentez8_geoid_matrix()
            
            self._record_result(
                "lambda_check passed",
                result['checks']['lambda_check']
            )
            self._record_result(
                "gravity_check passed",
                result['checks']['gravity_check']
            )
            self._record_result(
                "cyclic_check passed",
                result['checks']['cyclic_check']
            )
            self._record_result(
                "light_speed_check passed",
                result['checks']['light_speed_check']
            )
            self._record_result(
                "dimension_lock passed",
                result['checks']['dimension_lock']
            )
            self._record_result(
                "ALL CHECKS PASSED",
                result['all_passed'],
                result['status']
            )
            
        except Exception as e:
            self._record_result("Quick Verify Test", False, f"ERROR: {e}")
    
    # ==========================================================================
    # DETAILED ANALYSIS OUTPUT
    # ==========================================================================
    def run_detailed_analysis(self):
        """Run detailed analysis of all Geoid Matrix components"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
        print(f"SENTEZ-8 DETAILED FREQUENCY ANALYSIS")
        print(f"{'='*60}{Colors.ENDC}")
        
        gm = self.gm
        
        print(f"\n{Colors.BOLD}Geoid Matrix Constants:{Colors.ENDC}")
        print(f"  • GEOIT_FARK:   {Colors.GREEN}{gm.GEOIT_FARK}{Colors.ENDC}")
        print(f"  • GEOIT_OMURGA: {Colors.GREEN}{gm.GEOIT_OMURGA}{Colors.ENDC}")
        print(f"  • GEOIT_TOPLAM: {Colors.GREEN}{gm.GEOIT_TOPLAM}{Colors.ENDC}")
        print(f"  • GEOIT_CARPIM: {Colors.GREEN}{gm.GEOIT_CARPIM}{Colors.ENDC}")
        print(f"  • PI_11:        {Colors.GREEN}{gm.PI_11}{Colors.ENDC}")
        print(f"  • LAMBDA_GEOIT: {Colors.GREEN}{gm.LAMBDA_GEOIT}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Derived Values:{Colors.ENDC}")
        print(f"  • Pi_11²:          {gm.PI_11_SQUARED:.4f}")
        print(f"  • g from Geoid:    {gm.GRAVITY_FROM_GEOID:.6f} m/s²")
        print(f"  • Cyclic 66→22:    {gm.CYCLIC_PROOF:.4f}")
        print(f"  • Cyclic 22→66:    {gm.REVERSE_CYCLIC:.4f}")
        print(f"  • Orbital v:       {gm.ORBITAL_VELOCITY:.4f} km/s")
        print(f"  • C from Pi_11:    {gm.LIGHT_SPEED_PI11:.0f} km/s")
        print(f"  • 363/Pi_11:       {gm.YEAR_PI11_RATIO:.4f} ≈ 11²={11**2}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Key Relationships:{Colors.ENDC}")
        print(f"  • Lambda: 88 × 74 = {88*74} → {88*74/1000:.3f} MHz (target: 6.52 MHz)")
        print(f"  • Gravity: 88 / 2.99² = {88/(2.99**2):.6f} (target: 9.81)")
        print(f"  • Light: 2.99 × 100K = {2.99*100000:.0f} (target: 299792)")
        
        s7 = Sentez7_MasterConstants
        print(f"\n{Colors.BOLD}{Colors.CYAN}Sentez-7 ↔ Sentez-8 Bridge:{Colors.ENDC}")
        print(f"  • S7 Lambda: {s7.LAMBDA_BREAK_FREQ} MHz | S8 Lambda: {gm.LAMBDA_GEOIT/1000:.3f} MHz")
        print(f"  • S7 G_i: {s7.G_I_GRAVITY} | S8 g_geoid: {gm.GRAVITY_FROM_GEOID:.6f}")
        print(f"  • S7 V_Universe: {s7.V_UNIVERSE} | S8 Piramidal/11³: {gm.PIRAMIDAL_VOLUME:.1f}")
    
    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    def print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("=" * 80)
        print("SENTEZ-8 GEOID MATRIX TEST SUMMARY")
        print("=" * 80)
        print(f"{Colors.ENDC}")
        
        print(f"  Total Tests:  {self.total_tests}")
        print(f"  Passed:       {Colors.GREEN}{self.passed_tests}{Colors.ENDC}")
        print(f"  Failed:       {Colors.RED}{self.failed_tests}{Colors.ENDC}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        if success_rate == 100:
            print(f"\n  {Colors.GREEN}{Colors.BOLD}SUCCESS RATE: {success_rate:.0f}% — ALL TESTS PASSED ✅{Colors.ENDC}")
        elif success_rate >= 80:
            print(f"\n  {Colors.WARNING}SUCCESS RATE: {success_rate:.1f}% — MOSTLY PASSED ⚠️{Colors.ENDC}")
        else:
            print(f"\n  {Colors.RED}SUCCESS RATE: {success_rate:.1f}% — FAILURES DETECTED ❌{Colors.ENDC}")
        
        print(f"\n  {Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"  {Colors.GOLD}SENTEZ-8 GEOID MATRIX: {'OPERATIONAL ✅' if success_rate == 100 else 'NEEDS REVIEW ⚠️'}{Colors.ENDC}")
        print(f"  {Colors.GOLD}22-66-88 × Pi_11 = DÖNGÜSEL KİLİT{Colors.ENDC}")
        print(f"  {Colors.BOLD}{'='*60}{Colors.ENDC}\n")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    test_runner = TestSentez8GeoidMatrix()
    test_runner.header()
    
    # Run all tests
    test_runner.test_constants()
    test_runner.test_lambda_from_geoid()
    test_runner.test_gravity_from_geoid()
    test_runner.test_cyclic_matrix()
    test_runner.test_pi11_light_speed()
    test_runner.test_cross_references()
    test_runner.test_quick_verify()
    
    # Detailed analysis
    test_runner.run_detailed_analysis()
    
    # Summary
    test_runner.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if test_runner.failed_tests == 0 else 1)
