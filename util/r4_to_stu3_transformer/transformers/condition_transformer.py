"""
FHIR R4 to STU3 Condition Transformer

Implements http://hl7.org/fhir/StructureMap/Condition4to3

Key R4 -> STU3 changes:
- clinicalStatus:     CodeableConcept (R4) -> code (STU3)
- verificationStatus: CodeableConcept (R4) -> code (STU3); 'unconfirmed' -> 'provisional'
- encounter           -> context (field rename)
- recordedDate        -> assertedDate (field rename)
- recorder            dropped (STU3 Condition has no recorder)
- stage.type          dropped (R4-only on Condition.stage)
"""

from typing import Dict, Any, Optional
from .base_transformer import BaseTransformer

# R4 verificationStatus 'unconfirmed' has no STU3 equivalent; map to 'provisional'.
VERIFICATION_STATUS_MAP = {"unconfirmed": "provisional"}


class ConditionTransformer(BaseTransformer):
    """Transforms Condition resources from R4 to STU3."""

    DIRECT_FIELDS = [
        "identifier", "category", "severity", "code", "bodySite",
        "subject", "asserter", "evidence", "note",
    ]

    @property
    def resource_type(self) -> str:
        return "Condition"

    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.can_transform(r4_resource):
            return None

        # resourceType, id, meta, text/language/implicitRules
        stu3_resource = super().transform(r4_resource)
        if "contained" in r4_resource:
            stu3_resource["contained"] = r4_resource["contained"]

        # CodeableConcept -> code
        clinical = self._first_code(r4_resource.get("clinicalStatus"))
        if clinical:
            stu3_resource["clinicalStatus"] = clinical

        verification = self._first_code(r4_resource.get("verificationStatus"))
        if verification:
            stu3_resource["verificationStatus"] = VERIFICATION_STATUS_MAP.get(verification, verification)

        # Field renames
        if "encounter" in r4_resource:
            stu3_resource["context"] = r4_resource["encounter"]
        if "recordedDate" in r4_resource:
            stu3_resource["assertedDate"] = r4_resource["recordedDate"]

        # onset[x] / abatement[x] map by prefix (onsetDateTime, abatementBoolean, ...)
        for key, value in r4_resource.items():
            if key.startswith("onset") or key.startswith("abatement"):
                stu3_resource[key] = value

        # stage: drop the R4-only 'type' element on each stage entry
        if "stage" in r4_resource:
            stu3_resource["stage"] = [
                {k: v for k, v in stage.items() if k != "type"}
                for stage in r4_resource["stage"]
            ]

        for field in self.DIRECT_FIELDS:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]

        stu3_resource = self.clean_references_in_object(stu3_resource)
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        return stu3_resource

    @staticmethod
    def _first_code(codeable_concept: Optional[Dict[str, Any]]) -> Optional[str]:
        """Extract the first coding.code from a CodeableConcept."""
        if not isinstance(codeable_concept, dict):
            return None
        for coding in codeable_concept.get("coding", []):
            if "code" in coding:
                return coding["code"]
        return None

    def get_transformation_summary(self) -> str:
        """Return a human-readable summary of the R4 -> STU3 mappings."""
        return CONDITION_MAPPING_TABLE


# Mapping Documentation
CONDITION_MAPPING_TABLE = """
Condition R4 to STU3 Transformations (StructureMap/Condition4to3):
+--------------------------+--------------------------+------------------------------------------+
| R4 Field                 | STU3 Field               | Transformation Notes                     |
+--------------------------+--------------------------+------------------------------------------+
| identifier               | identifier               | Direct mapping                           |
| clinicalStatus (CC)      | clinicalStatus (code)    | First coding.code extracted              |
| verificationStatus (CC)  | verificationStatus (code)| First coding.code; 'unconfirmed' ->      |
|                          |                          | 'provisional' (no STU3 equivalent)       |
| category                 | category                 | Direct mapping                           |
| severity                 | severity                 | Direct mapping                           |
| code                     | code                     | Direct mapping                           |
| bodySite                 | bodySite                 | Direct mapping                           |
| subject                  | subject                  | Direct mapping                           |
| encounter                | context                  | Field name change                        |
| onset[x]                 | onset[x]                 | Direct mapping (by prefix)               |
| abatement[x]             | abatement[x]             | Direct mapping (by prefix)               |
| recordedDate             | assertedDate             | Field name change                        |
| recorder                 | (dropped)                | STU3 Condition has no recorder           |
| asserter                 | asserter                 | Direct mapping                           |
| stage                    | stage                    | R4-only stage.type element dropped       |
| evidence                 | evidence                 | Direct mapping                           |
| note                     | note                     | Direct mapping                           |
+--------------------------+--------------------------+------------------------------------------+

Special Cases:
- clinicalStatus / verificationStatus collapse from CodeableConcept to a plain code.
- verificationStatus 'unconfirmed' (R4-only) maps to 'provisional'.
- Reference.type fields removed from all references (R4-specific, unsupported in STU3).
- Extension URLs mapped from R4 to STU3 equivalents globally.
"""

if __name__ == "__main__":
    print("Condition R4 to STU3 Transformer")
    print("=" * 50)
    print(CONDITION_MAPPING_TABLE)
