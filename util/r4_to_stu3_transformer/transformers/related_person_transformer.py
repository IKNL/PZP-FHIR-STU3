"""
FHIR R4 to STU3 RelatedPerson Transformer

This module handles the transformation of RelatedPerson resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/RelatedPerson4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class RelatedPersonTransformer(BaseTransformer):
    """Transforms RelatedPerson resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "RelatedPerson"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single RelatedPerson resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming RelatedPerson resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'RelatedPerson'
        if 'id' in r4_resource:
            stu3_resource['id'] = r4_resource['id']
        
        # 2. Meta (early)
        if 'meta' in r4_resource:
            stu3_resource['meta'] = self.transform_meta(r4_resource['meta'])
            
        # 3. Basic structural elements
        if 'text' in r4_resource:
            stu3_resource['text'] = r4_resource['text']
        if 'contained' in r4_resource:
            stu3_resource['contained'] = r4_resource['contained']
        
        try:
            # Apply RelatedPerson-specific transformations
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally  
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed RelatedPerson: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming RelatedPerson {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "active", 
            "patient",
            "name",
            "telecom",
            "gender",
            "birthDate",
            "address",
            "photo",
            "period"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
        
        # Handle relationship field separately:
        # R4 relationship (0..*) splits into STU3 relationship (0..1) and
        # nl-core-relatedperson-role extensions based on the coding system.
        if 'relationship' in r4_resource:
            self._transform_relationship(r4_resource['relationship'], stu3_resource)
    
    # Systems whose codes stay on RelatedPerson.relationship in STU3
    RELATIONSHIP_SYSTEMS = {
        "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
        "http://terminology.hl7.org/CodeSystem/v3-NullFlavor",
    }

    ROLE_EXTENSION_URL = "http://fhir.nl/fhir/StructureDefinition/nl-core-relatedperson-role"

    def _is_relationship_concept(self, codeable_concept: Dict[str, Any]) -> bool:
        """Return True if any coding in the CodeableConcept belongs to a relationship system."""
        for coding in codeable_concept.get("coding", []):
            if coding.get("system") in self.RELATIONSHIP_SYSTEMS:
                return True
        return False

    def _transform_relationship(
        self,
        r4_relationship: List[Dict[str, Any]],
        stu3_resource: Dict[str, Any],
    ) -> None:
        """
        Transform R4 relationship (0..*) into STU3 relationship (0..1) plus
        nl-core-relatedperson-role extensions.

        Categorisation logic:
        - CodeableConcepts with a coding from v3-RoleCode or v3-NullFlavor
          are mapped to RelatedPerson.relationship (STU3 single CodeableConcept).
        - All other CodeableConcepts are mapped to separate
          nl-core-relatedperson-role extensions on the resource root.

        If multiple CodeableConcepts qualify for relationship, only the first
        is used and a warning is logged about the discarded ones.
        """
        if not r4_relationship:
            return

        relationship_concepts: List[Dict[str, Any]] = []
        role_concepts: List[Dict[str, Any]] = []

        for concept in r4_relationship:
            if self._is_relationship_concept(concept):
                relationship_concepts.append(concept)
            else:
                role_concepts.append(concept)

        # --- STU3 relationship (0..1) ---
        if relationship_concepts:
            stu3_resource["relationship"] = relationship_concepts[0]
            if len(relationship_concepts) > 1:
                discarded = relationship_concepts[1:]
                logger.warning(
                    f"RelatedPerson has {len(relationship_concepts)} relationship "
                    f"CodeableConcepts qualifying for STU3 relationship, but only "
                    f"1 is supported. Taking the first and discarding: "
                    f"{[rc.get('coding', rc) for rc in discarded]}"
                )

        # --- nl-core-relatedperson-role extensions ---
        if role_concepts:
            if "extension" not in stu3_resource:
                stu3_resource["extension"] = []
            for concept in role_concepts:
                stu3_resource["extension"].append({
                    "url": self.ROLE_EXTENSION_URL,
                    "valueCodeableConcept": concept,
                })
            logger.info(
                f"Mapped {len(role_concepts)} role CodeableConcept(s) to "
                f"nl-core-relatedperson-role extension(s)."
            )
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "RelatedPerson",
            "base_mapping": "http://hl7.org/fhir/StructureMap/RelatedPerson4to3",
            "key_transformations": {
                "Reference.type": "Removed from all Reference objects (R4-specific)",
                "relationship": (
                    "R4 relationship (0..*) is split by coding system. "
                    "v3-RoleCode / v3-NullFlavor codes stay on relationship (0..1). "
                    "All other codes move to nl-core-relatedperson-role extensions."
                ),
            },
            "direct_mappings": "identifier, active, patient, name, telecom, gender, birthDate, address, photo, period"
        }


# Mapping Documentation
RELATED_PERSON_MAPPING_TABLE = """
┌─────────────────────────┬──────────────────────────────────────────┬───────────────────────────────────────────────────┐
│ R4 Field                │ STU3 Field                               │ Transformation Notes                              │
├─────────────────────────┼──────────────────────────────────────────┼───────────────────────────────────────────────────┤
│ identifier              │ identifier                               │ Direct mapping                                    │
│ active                  │ active                                   │ Direct mapping                                    │
│ patient                 │ patient                                  │ Direct mapping                                    │
│ relationship (0..*)     │ relationship (0..1) +                    │ Split by coding system (see below)                │
│                         │ ext:nl-core-relatedperson-role (0..*)    │                                                   │
│ name                    │ name                                     │ Direct mapping                                    │
│ telecom                 │ telecom                                  │ Direct mapping                                    │
│ gender                  │ gender                                   │ Direct mapping                                    │
│ birthDate               │ birthDate                                │ Direct mapping                                    │
│ address                 │ address                                  │ Direct mapping                                    │
│ photo                   │ photo                                    │ Direct mapping                                    │
│ period                  │ period                                   │ Direct mapping                                    │
└─────────────────────────┴──────────────────────────────────────────┴───────────────────────────────────────────────────┘

Critical Transformations:
1. RELATIONSHIP SPLIT BY CODING SYSTEM:
   - R4: relationship is an array of CodeableConcepts (0..*)
   - Each CodeableConcept is categorised by its coding system:
     a) v3-RoleCode / v3-NullFlavor  → STU3 RelatedPerson.relationship (0..1)
        Only the first qualifying concept is used; extras are discarded with a warning.
     b) All other systems              → extension nl-core-relatedperson-role
        Each concept becomes a separate extension with valueCodeableConcept. 
        This is currenlty a bit of a catch-all category that is not production grade, but fine for our purposes.
   - Extension URL: http://fhir.nl/fhir/StructureDefinition/nl-core-relatedperson-role

2. Reference.type fields are removed (R4-specific, not supported in STU3)

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: patient reference
"""

if __name__ == "__main__":
    print("RelatedPerson R4 to STU3 Transformer")
    print("=" * 50)
    print(RELATED_PERSON_MAPPING_TABLE)
