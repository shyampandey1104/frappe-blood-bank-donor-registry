"""Blood Bank Donor Registry, Component Separation & Cross-Match Reserve Engine."""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class BloodComponentUnit(BaseModel):
    unit_barcode: str
    donor_id: str
    blood_group: str        # A+, A-, B+, B-, O+, O-, AB+, AB-, Bombay_Oh
    component_type: str     # WHOLE_BLOOD, PRBC (Packed Red Cells), FFP (Fresh Frozen Plasma), PLATELETS
    collection_date: str    # YYYY-MM-DD
    expiry_date: str        # YYYY-MM-DD
    volume_ml: float
    storage_temp_celsius: float
    is_issued: bool = False
    cross_matched_patient_id: Optional[str] = None


class BloodBankManager:
    """Manages blood donor donations, component shelf-life separation, and cross-matching."""

    # Shelf Life Guidelines (NACO / DGHS India):
    # PRBC: 35-42 days at 2°C - 6°C
    # Platelets: 5 days at 20°C - 24°C with continuous agitation
    # Fresh Frozen Plasma (FFP): 365 days at -30°C
    # Whole Blood: 35 days (CPDA-1)
    SHELF_LIFE_DAYS = {
        "WHOLE_BLOOD": 35,
        "PRBC": 42,
        "PLATELETS": 5,
        "FFP": 365
    }

    def __init__(self):
        self.inventory: Dict[str, BloodComponentUnit] = {}

    def inward_donation(
        self,
        barcode: str,
        donor_id: str,
        blood_group: str,
        component_type: str,
        collection_date_str: str,
        volume_ml: float = 350.0
    ) -> BloodComponentUnit:
        comp = component_type.upper()
        if comp not in self.SHELF_LIFE_DAYS:
            raise ValueError(f"Unknown component type. Allowed: {list(self.SHELF_LIFE_DAYS.keys())}")

        d1 = datetime.strptime(collection_date_str, "%Y-%m-%d").date()
        shelf_days = self.SHELF_LIFE_DAYS[comp]
        exp_date = (d1 + timedelta(days=shelf_days)).strftime("%Y-%m-%d")

        temp = 4.0
        if comp == "PLATELETS":
            temp = 22.0
        elif comp == "FFP":
            temp = -30.0

        unit = BloodComponentUnit(
            unit_barcode=barcode,
            donor_id=donor_id,
            blood_group=blood_group.upper(),
            component_type=comp,
            collection_date=collection_date_str,
            expiry_date=exp_date,
            volume_ml=volume_ml,
            storage_temp_celsius=temp,
            is_issued=False
        )

        self.inventory[barcode] = unit
        return unit

    def find_compatible_unit(
        self,
        patient_blood_group: str,
        component_type: str,
        current_date_str: str
    ) -> Optional[BloodComponentUnit]:
        """Finds nearest-expiry compatible unit (FEFO) ensuring patient safety."""
        pt_group = patient_blood_group.upper()
        comp = component_type.upper()
        today = datetime.strptime(current_date_str, "%Y-%m-%d").date()

        # Simple compatibility matrix for RBC
        compatible_groups = [pt_group]
        if pt_group in ("A+", "B+", "AB+", "O+"):
            compatible_groups.append("O+")
        if pt_group not in compatible_groups:
            compatible_groups.append("O-")  # universal donor

        available = []
        for u in self.inventory.values():
            if not u.is_issued and u.component_type == comp and u.blood_group in compatible_groups:
                exp = datetime.strptime(u.expiry_date, "%Y-%m-%d").date()
                if exp >= today:
                    available.append((exp, u))

        if not available:
            return None

        # Sort by nearest expiry first (FEFO)
        available.sort(key=lambda x: x[0])
        return available[0][1]

    def cross_match_and_issue(self, unit_barcode: str, patient_id: str) -> Dict[str, Any]:
        unit = self.inventory.get(unit_barcode)
        if not unit:
            raise ValueError("Unit not found.")
        if unit.is_issued:
            raise ValueError("Unit has already been issued.")

        unit.is_issued = True
        unit.cross_matched_patient_id = patient_id

        return {
            "barcode": unit.unit_barcode,
            "blood_group": unit.blood_group,
            "component": unit.component_type,
            "issued_to_patient": patient_id,
            "status": "ISSUED_FOR_TRANSFUSION"
        }
