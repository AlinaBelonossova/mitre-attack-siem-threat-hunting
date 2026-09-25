import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from process_iocs import normalize_indicator, process_rows


class TestIOCProcessing(unittest.TestCase):
    def test_domain_normalization(self):
        self.assertEqual(
            normalize_indicator("Example-Malicious.COM.", "domain"),
            "example-malicious.com",
        )

    def test_url_canonicalization(self):
        self.assertEqual(
            normalize_indicator(
                "HTTPS://Example-Malicious.com:443/login#section",
                "url",
            ),
            "https://example-malicious.com/login",
        )

    def test_duplicate_correlation(self):
        rows = [
            {
                "indicator": "Example-Malicious.com",
                "type": "domain",
                "source": "Shodan",
                "confidence": "70",
                "description": "first",
                "tags": "osint",
            },
            {
                "indicator": "example-malicious.com.",
                "type": "hostname",
                "source": "VirusTotal",
                "confidence": "90",
                "description": "second",
                "tags": "malware",
            },
        ]

        accepted, rejected, stats = process_rows(rows)

        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(rejected), 0)
        self.assertEqual(stats["correlated_duplicate_records"], 1)
        self.assertEqual(accepted[0]["confidence"], 90)
        self.assertEqual(accepted[0]["sightings_count"], 2)
        self.assertIn("Shodan", accepted[0]["sources"])
        self.assertIn("VirusTotal", accepted[0]["sources"])

    def test_low_confidence_filter(self):
        rows = [{
            "indicator": "192.0.2.10",
            "type": "ip-dst",
            "source": "OSINT",
            "confidence": "20",
            "description": "",
            "tags": "",
        }]

        accepted, rejected, stats = process_rows(rows, min_confidence=50)

        self.assertEqual(len(accepted), 0)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(stats["rejected_low_confidence"], 1)

    def test_invalid_ip_rejected(self):
        rows = [{
            "indicator": "999.999.999.999",
            "type": "ip",
            "source": "OSINT",
            "confidence": "90",
            "description": "",
            "tags": "",
        }]

        accepted, rejected, stats = process_rows(rows)

        self.assertEqual(len(accepted), 0)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(stats["rejected_invalid"], 1)


if __name__ == "__main__":
    unittest.main()
