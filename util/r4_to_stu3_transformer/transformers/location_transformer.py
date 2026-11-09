"""
FHIR R4 to STU3 Location Transformer

In zib2020 (R4) the zib HealthcareProvider is split over a Location profile
(zib-HealthcareProvider / nl-core-HealthcareProvider, the focal resource) and an
Organization profile. In zib2017 (STU3) the zib HealthcareProvider is a single
Organization (nl-core-organization), and STU3 references to a healthcare provider,
such as DeviceUseStatement.extension:zib-MedicalDevice-Organization, point to an
Organization.

This transformer therefore converts R4 HealthcareProvider Locations into STU3
Organizations with the same id. References to these Locations are rewritten to
Organization/<id> by the transformers of the referring resources (see
DeviceUseStatementTransformer). Locations with any other profile are not converted.
"""

from typing import Dict, Any, Optional
from .base_transformer import BaseTransformer


HEALTHCARE_PROVIDER_LOCATION_PROFILES = {
    "http://nictiz.nl/fhir/StructureDefinition/zib-HealthcareProvider",
    "http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthcareProvider",
}

STU3_ORGANIZATION_PROFILE = "http://fhir.nl/fhir/StructureDefinition/nl-core-organization"


def is_healthcare_provider_location(resource: Dict[str, Any]) -> bool:
    """True if the resource is an R4 Location that represents a zib HealthcareProvider."""
    if resource.get("resourceType") != "Location":
        return False
    profiles = resource.get("meta", {}).get("profile", [])
    return any(p.split("|")[0] in HEALTHCARE_PROVIDER_LOCATION_PROFILES for p in profiles)


class LocationTransformer(BaseTransformer):
    """Transforms R4 HealthcareProvider Location resources into STU3 Organization resources."""

    # Location fields that have the same name and type on STU3 Organization.
    DIRECT_FIELDS = ["identifier", "name", "alias", "telecom"]

    @property
    def resource_type(self) -> str:
        return "Location"

    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.can_transform(r4_resource):
            return None
        if not is_healthcare_provider_location(r4_resource):
            raise ValueError(
                "Only zib HealthcareProvider Locations are supported "
                "(meta.profile zib-HealthcareProvider or nl-core-HealthcareProvider)"
            )

        # resourceType, id, meta, text/language/implicitRules
        stu3_resource = super().transform(r4_resource)
        stu3_resource["resourceType"] = "Organization"
        stu3_resource.setdefault("meta", {})["profile"] = [STU3_ORGANIZATION_PROFILE]

        if "extension" in r4_resource:
            stu3_resource["extension"] = r4_resource["extension"]

        for field in self.DIRECT_FIELDS:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]

        # Location.status (active | suspended | inactive) -> Organization.active
        if "status" in r4_resource:
            stu3_resource["active"] = r4_resource["status"] == "active"

        # Location.address (0..1) -> Organization.address (0..*)
        if "address" in r4_resource:
            stu3_resource["address"] = [r4_resource["address"]]

        # Organizational hierarchy: the managing organization, or else the parent
        # Location (itself converted to an Organization with the same id).
        if "managingOrganization" in r4_resource:
            stu3_resource["partOf"] = r4_resource["managingOrganization"]
        elif "partOf" in r4_resource:
            stu3_resource["partOf"] = location_to_organization_reference(r4_resource["partOf"])

        stu3_resource = self.clean_references_in_object(stu3_resource)
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        return stu3_resource

    def get_transformation_summary(self) -> str:
        """Return a human-readable summary of the R4 -> STU3 mappings."""
        return LOCATION_MAPPING_TABLE


def location_to_organization_reference(reference: Dict[str, Any]) -> Dict[str, Any]:
    """Rewrite a Reference to Location/<id> into a Reference to Organization/<id>."""
    result = dict(reference)
    ref = result.get("reference", "")
    if ref.startswith("Location/"):
        result["reference"] = "Organization/" + ref[len("Location/"):]
    elif "/Location/" in ref:
        result["reference"] = ref.replace("/Location/", "/Organization/")
    if result.get("type") == "Location":
        result["type"] = "Organization"
    return result


# Mapping Documentation
LOCATION_MAPPING_TABLE = """
Location (zib-HealthcareProvider, R4) to Organization (nl-core-organization, STU3):
+--------------------------+--------------------------+------------------------------------------+
| R4 Location Field        | STU3 Organization Field  | Transformation Notes                     |
+--------------------------+--------------------------+------------------------------------------+
| id                       | id                       | Same id, resourceType Organization       |
| meta.profile             | meta.profile             | nl-core-organization                     |
| identifier               | identifier               | Direct mapping                           |
| name                     | name                     | Direct mapping                           |
| alias                    | alias                    | Direct mapping                           |
| telecom                  | telecom                  | Direct mapping                           |
| address (0..1)           | address (0..*)           | Wrapped in a list                        |
| status                   | active                   | active -> true, otherwise false          |
| managingOrganization     | partOf                   | Direct mapping + reference clean         |
| partOf (Location)        | partOf (Organization)    | Only without managingOrganization;       |
|                          |                          | Location/<id> -> Organization/<id>       |
+--------------------------+--------------------------+------------------------------------------+

Special Cases:
- Only Locations with meta.profile zib-HealthcareProvider or nl-core-HealthcareProvider
  are converted; other Locations raise an error and stay R4.
- Other Location fields (type, physicalType, position, mode, hoursOfOperation, ...)
  have no Organization equivalent and are dropped.
- Referring resources must rewrite Location/<id> to Organization/<id>; the
  DeviceUseStatement transformer does this for ext-MedicalDevice.Location.
"""

if __name__ == "__main__":
    print("Location R4 to STU3 Transformer")
    print("=" * 50)
    print(LOCATION_MAPPING_TABLE)
