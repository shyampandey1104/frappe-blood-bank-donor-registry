import unittest
from bloodbank.engine import BloodBankManager


class TestBloodBankManager(unittest.TestCase):
    def setUp(self):
        self.manager = BloodBankManager()

    def test_component_inward_and_compatibility(self):
        # Inward 2 units of PRBC
        u1 = self.manager.inward_donation(
            barcode="BB-001",
            donor_id="DNR-901",
            blood_group="O+",
            component_type="PRBC",
            collection_date_str="2026-06-01",
            volume_ml=280.0
        )
        self.assertEqual(u1.expiry_date, "2026-07-13")  # +42 days
        self.assertEqual(u1.storage_temp_celsius, 4.0)

        # Inward platelets (5-day expiry)
        u2 = self.manager.inward_donation(
            barcode="BB-002",
            donor_id="DNR-902",
            blood_group="B+",
            component_type="PLATELETS",
            collection_date_str="2026-06-01",
            volume_ml=60.0
        )
        self.assertEqual(u2.expiry_date, "2026-06-06")

        # Find compatible PRBC unit for A+ patient
        match = self.manager.find_compatible_unit("A+", "PRBC", "2026-06-05")
        self.assertIsNotNone(match)
        self.assertEqual(match.blood_group, "O+")  # O+ is compatible with A+

        # Issue for transfusion
        res = self.manager.cross_match_and_issue(match.unit_barcode, "PAT-7712")
        self.assertEqual(res["status"], "ISSUED_FOR_TRANSFUSION")
        self.assertTrue(self.manager.inventory["BB-001"].is_issued)


if __name__ == "__main__":
    unittest.main()
