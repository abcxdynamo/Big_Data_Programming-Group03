import sys
import io
import os
import unittest
from HtmlTestRunner import HTMLTestRunner
import performa_unit_test

# Ensure the standard output is set to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Monkey-patch HtmlTestRunner to use UTF-8 encoding
from HtmlTestRunner.result import HtmlTestResult
original_generate_file = HtmlTestResult.generate_file

def generate_file_utf8(self, testRunner, name, content):
    """Generate the HTML file with UTF-8 encoding."""
    filename = os.path.join(testRunner.output, f"{name}.html")
    with open(filename, 'w', encoding='utf-8') as report_file:
        report_file.write(content)

HtmlTestResult.generate_file = generate_file_utf8

# Load tests
test_suite = unittest.TestLoader().loadTestsFromModule(performa_unit_test)

if __name__ == "__main__":
    print("\nRunning tests...\n")

    # Ensure output directory exists
    report_dir = os.path.join('server', 'tests', 'reports')
    os.makedirs(report_dir, exist_ok=True)

    # Run tests
    runner = HTMLTestRunner(
        output=report_dir,
        report_name='Performa_UnitTest_Report',
        combine_reports=True,
        add_timestamp=True,
        open_in_browser=False,
        verbosity=2
    )
    
    runner.run(test_suite)