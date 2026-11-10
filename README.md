# Frappe Blood Bank & Component Transfusion Registry 🩸🏥

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise blood bank management, blood component separation (PRBC, Platelets, FFP), strict FEFO expiration tracking, and emergency cross-match transfusion system for **Frappe Healthcare & Hospital Information Systems (HIS)**.

---

## 🚀 Key Features

- **Component Separation Life-Cycle**: Tracks shelf lives adhering to National AIDS Control Organisation (NACO) guidelines (Platelets 5 days, PRBC 42 days, FFP 365 days).
- **First-Expiry First-Out (FEFO) Dispatch**: Prioritizes nearest-expiry units to eliminate critical blood product wastage.
- **Cross-Matching Compatibility Engine**: Automates ABO and Rh compatibility checks for emergency transfusions.
- **Storage Temperature Cold-Chain Alarms**: Continuous monitoring of platelet agitators (22°C) and deep-freeze plasma units (-30°C).

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/frappe-blood-bank-donor-registry.git
cd frappe-blood-bank-donor-registry
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from bloodbank.engine import BloodBankManager

manager = BloodBankManager()

# Inward whole blood donation & packed red cell separation
unit = manager.inward_donation(
    barcode="BB-4001",
    donor_id="DNR-102",
    blood_group="O+",
    component_type="PRBC",
    collection_date_str="2026-06-01",
    volume_ml=300.0
)

# Search compatible unit for emergency surgery patient
compatible = manager.find_compatible_unit("B+", "PRBC", "2026-06-10")
if compatible:
    issue = manager.cross_match_and_issue(compatible.unit_barcode, patient_id="PAT-ICU-88")
    print(f"Transfusion Unit Dispatched: {issue['barcode']} to Patient: {issue['issued_to_patient']}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
