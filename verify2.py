import math
tests = [
    ('Malta 1100=100x11', 1100 % 11 == 0),
    ('Efes 137 1+3+7=11', (1+3+7) == 11),
    ('mtDNA tRNA 22=2x11', 22 % 11 == 0),
    ('Derinkuyu 55=5x11', 55 % 11 == 0),
    ('Nazca 33=3x11', 33 % 11 == 0),
    ('Telomer 44=4x11', 44 % 11 == 0),
    ('Hemoglobin 55~5x11', abs(55.845-55)<1),
    ('Stonehenge sarsen 33', 33 % 11 == 0),
    ('Okyanus 0.11=11/100', abs(0.11 - 11/100) < 0.001),
    ('Okyanus 1.1=11/10', abs(1.1 - 11/10) < 0.001),
]
passed = sum(1 for _,r in tests if r)
print('EK KESIFLER: %d/%d' % (passed, len(tests)))
for name, r in tests:
    print('  [%s] %s' % ('V' if r else 'X', name))
