import unittest

# Import test modules
import test_01_check_accessibility_wcag_only
import test_02_check_accessibility_all
import test_03_check_vulnerabilities

# Initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add test to the test suite
suite.addTest(loader.loadTestsFromModule(test_01_check_accessibility_wcag_only))
suite.addTest(loader.loadTestsFromModule(test_02_check_accessibility_all))
suite.addTest(loader.loadTestsFromModule(test_03_check_vulnerabilities))

# Initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
