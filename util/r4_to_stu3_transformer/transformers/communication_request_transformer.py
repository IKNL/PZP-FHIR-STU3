"""
FHIR R4 to STU3 CommunicationRequest Transformer

This module handles the transformation of CommunicationRequest resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/CommunicationRequest4to3

Author: AI Assistant  
Date: 2025-12-19
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class CommunicationRequestTransformer(BaseTransformer):
    """Transforms CommunicationRequest resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "CommunicationRequest"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single CommunicationRequest resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming CommunicationRequest resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'CommunicationRequest'
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
            # Apply CommunicationRequest-specific transformations
            self._transform_instantiates_canonical(r4_resource, stu3_resource)
            self._transform_status_and_not_done(r4_resource, stu3_resource)
            self._transform_encounter_to_context(r4_resource, stu3_resource)
            self._transform_occurrence(r4_resource, stu3_resource)
            self._transform_authored_on(r4_resource, stu3_resource)
            self._transform_requester(r4_resource, stu3_resource)
            self._transform_payload(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed CommunicationRequest: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming CommunicationRequest {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_instantiates_canonical(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform instantiatesCanonical to definition field."""
        
        if "instantiatesCanonical" in r4_resource:
            stu3_resource["definition"] = r4_resource["instantiatesCanonical"]
    
    def _transform_status_and_not_done(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform status field - CommunicationRequest doesn't use 'not-done' like Communication does."""
        
        r4_status = r4_resource.get("status")
        if r4_status:
            # Direct mapping for CommunicationRequest status
            # Valid values: draft | active | suspended | cancelled | completed | entered-in-error | unknown
            stu3_resource["status"] = r4_status
    
    def _transform_encounter_to_context(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform encounter field to context field."""
        
        if "encounter" in r4_resource:
            stu3_resource["context"] = r4_resource["encounter"]
    
    def _transform_occurrence(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform occurrence[x] field with polymorphic type handling."""
        
        # Handle polymorphic occurrence field
        if "occurrenceDateTime" in r4_resource:
            stu3_resource["occurrenceDateTime"] = r4_resource["occurrenceDateTime"]
        elif "occurrencePeriod" in r4_resource:
            stu3_resource["occurrencePeriod"] = r4_resource["occurrencePeriod"]
    
    def _transform_authored_on(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform authoredOn field."""
        
        if "authoredOn" in r4_resource:
            stu3_resource["authoredOn"] = r4_resource["authoredOn"]
    
    def _transform_requester(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform requester field from R4 Reference to STU3 requester.agent structure.
        
        In R4, requester is a simple Reference.
        In STU3, requester is a BackboneElement with:
        - requester.agent: Reference (the actual requester)
        - requester.onBehalfOf: Reference (optional)
        
        Note: PractitionerRole resolution is handled later by the main transformer's
        process_practitioner_role_references_in_object() method, which will:
        1. Resolve PractitionerRole to Practitioner reference
        2. Store original PractitionerRole in extension
        """
        
        if "requester" not in r4_resource:
            return
        
        r4_requester = r4_resource["requester"]
        
        # Simply wrap the requester reference in the agent structure
        # PractitionerRole resolution will be handled automatically by the base transformer
        stu3_resource["requester"] = {
            "agent": r4_requester
        }
    
    def _transform_payload(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform payload array with polymorphic content handling."""
        
        if "payload" not in r4_resource:
            return
            
        stu3_payloads = []
        
        for r4_payload in r4_resource["payload"]:
            stu3_payload = {}
            
            # Handle polymorphic content field
            if "contentString" in r4_payload:
                stu3_payload["contentString"] = r4_payload["contentString"]
            elif "contentAttachment" in r4_payload:
                stu3_payload["contentAttachment"] = r4_payload["contentAttachment"]
            elif "contentReference" in r4_payload:
                stu3_payload["contentReference"] = r4_payload["contentReference"]
            elif "content" in r4_payload:
                # Direct content field (less common)
                stu3_payload["content"] = r4_payload["content"]
            
            # Copy any other payload fields
            for field in r4_payload:
                if field not in ["contentString", "contentAttachment", "contentReference", "content"]:
                    stu3_payload[field] = r4_payload[field]
            
            stu3_payloads.append(stu3_payload)
        
        if stu3_payloads:
            stu3_resource["payload"] = stu3_payloads
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "basedOn",
            "replaces",
            "groupIdentifier",
            "statusReason",
            "category",
            "priority",
            "doNotPerform",
            "medium",
            "subject",
            "about",
            "recipient",
            "sender",
            "reasonCode",
            "reasonReference",
            "note"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "CommunicationRequest",
            "base_mapping": "http://hl7.org/fhir/StructureMap/CommunicationRequest4to3",
            "key_transformations": {
                "instantiatesCanonical": "Mapped to 'definition' field in STU3",
                "encounter": "Mapped to 'context' field in STU3",
                "requester": "Wrapped in requester.agent structure; PractitionerRole resolved to Practitioner with extension",
                "occurrence[x]": "Polymorphic handling (DateTime/Period)",
                "payload.content": "Polymorphic content handling (string/Attachment/Reference)",
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "polymorphic_fields": {
                "occurrence": "Supports DateTime, Period",
                "payload.content": "Supports string, Attachment, Reference"
            },
            "direct_mappings": "identifier, basedOn, replaces, groupIdentifier, status, statusReason, category, priority, doNotPerform, medium, subject, about, recipient, sender, reasonCode, reasonReference, note, authoredOn, requester"
        }


# Mapping Documentation
COMMUNICATION_REQUEST_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ instantiatesCanonical   │ definition              │ Field name change                       │
│ basedOn                 │ basedOn                 │ Direct mapping                          │
│ replaces                │ replaces                │ Direct mapping                          │
│ groupIdentifier         │ groupIdentifier         │ Direct mapping                          │
│ status                  │ status                  │ Direct mapping                          │
│ statusReason            │ statusReason            │ Direct mapping                          │
│ category                │ category                │ Direct mapping                          │
│ priority                │ priority                │ Direct mapping                          │
│ doNotPerform            │ doNotPerform            │ Direct mapping                          │
│ medium                  │ medium                  │ Direct mapping                          │
│ subject                 │ subject                 │ Direct mapping                          │
│ about                   │ about                   │ Direct mapping                          │
│ encounter               │ context                 │ Field name change                       │
│ occurrenceDateTime      │ occurrenceDateTime      │ Direct mapping (polymorphic)            │
│ occurrencePeriod        │ occurrencePeriod        │ Direct mapping (polymorphic)            │
│ authoredOn              │ authoredOn              │ Direct mapping                          │
│ requester               │ requester.agent         │ Wrapped in BackboneElement structure    │
│ requester (PractitionerRole)│ requester.agent     │ Resolved to Practitioner + extension    │
│                         │ + extension             │ preserves PractitionerRole reference    │
│ recipient               │ recipient               │ Direct mapping                          │
│ sender                  │ sender                  │ Direct mapping                          │
│ reasonCode              │ reasonCode              │ Direct mapping                          │
│ reasonReference         │ reasonReference         │ Direct mapping                          │
│ payload                 │ payload                 │ Polymorphic content mapping             │
│ payload.contentString   │ payload.contentString   │ Direct mapping                          │
│ payload.contentAttachment│ payload.contentAttachment│ Direct mapping                         │
│ payload.contentReference│ payload.contentReference│ Direct mapping                          │
│ note                    │ note                    │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

Special Transformations:
1. requester → requester.agent (BackboneElement structure)
   - PractitionerRole references resolved to Practitioner
   - Original PractitionerRole preserved in extension
4. occurrence[x] polymorphic handling (DateTime, Period)
5. payload.content[x] polymorphic handling (string, Attachment, Reference)
6. occurrence[x] polymorphic handling (DateTime, Period)
4. payload.content[x] polymorphic handling (string, Attachment, Reference)
5. Reference.type fields removed (R4-specific)

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: basedOn, replaces, subject, about, recipient, sender, requester, 
  reasonReference, payload.contentReference

Key Differences from Communication:
- CommunicationRequest does not use 'not-done' status handling
- Has 'priority', 'doNotPerform', 'about' fields
- Uses 'occurrence[x]' instead of 'sent/received'
- Has 'requester' instead of separate sender/recipient tracking
- Has 'authoredOn' for creation timestamp
"""

if __name__ == "__main__":
    print("CommunicationRequest R4 to STU3 Transformer")
    print("=" * 50)
    print(COMMUNICATION_REQUEST_MAPPING_TABLE)
