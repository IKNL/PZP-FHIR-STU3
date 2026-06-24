"""
FHIR R4 to STU3 Organization Transformer

Organization is structurally identical between R4 and STU3, so this transformer
is essentially a pass-through: copy all fields, strip R4-specific Reference.type,
and map extension URLs. Implements:
http://hl7.org/fhir/StructureMap/Organization4to3
"""

from typing import Dict, Any, Optional
from .base_transformer import BaseTransformer


class OrganizationTransformer(BaseTransformer):
    """Transforms Organization resources from R4 to STU3."""

    # All Organization fields are unchanged between R4 and STU3.
    DIRECT_FIELDS = [
        "identifier", "active", "type", "name", "alias",
        "telecom", "address", "partOf", "contact", "endpoint",
    ]

    @property
    def resource_type(self) -> str:
        return "Organization"

    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.can_transform(r4_resource):
            return None

        # resourceType, id, meta, text/language/implicitRules
        stu3_resource = super().transform(r4_resource)

        for field in self.DIRECT_FIELDS:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]

        # Strip R4-specific Reference.type and map extension URLs (partOf, contact, etc.)
        stu3_resource = self.clean_references_in_object(stu3_resource)
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        return stu3_resource

    def get_transformation_summary(self) -> str:
        """Return a human-readable summary of the R4 -> STU3 mappings."""
        return ORGANIZATION_MAPPING_TABLE


# Mapping Documentation
ORGANIZATION_MAPPING_TABLE = """
Organization R4 to STU3 Transformations (StructureMap/Organization4to3):
+--------------------------+--------------------------+------------------------------------------+
| R4 Field                 | STU3 Field               | Transformation Notes                     |
+--------------------------+--------------------------+------------------------------------------+
| identifier               | identifier               | Direct mapping                           |
| active                   | active                   | Direct mapping                           |
| type                     | type                     | Direct mapping                           |
| name                     | name                     | Direct mapping                           |
| alias                    | alias                    | Direct mapping                           |
| telecom                  | telecom                  | Direct mapping                           |
| address                  | address                  | Direct mapping                           |
| partOf                   | partOf                   | Direct mapping + reference clean         |
| contact                  | contact                  | Direct mapping                           |
| endpoint                 | endpoint                 | Direct mapping + reference clean         |
+--------------------------+--------------------------+------------------------------------------+

Special Cases:
- Organization is structurally identical between R4 and STU3 (pure pass-through).
- Reference.type fields removed from all references (R4-specific, unsupported in STU3).
- Extension URLs mapped from R4 to STU3 equivalents globally.
"""

if __name__ == "__main__":
    print("Organization R4 to STU3 Transformer")
    print("=" * 50)
    print(ORGANIZATION_MAPPING_TABLE)
