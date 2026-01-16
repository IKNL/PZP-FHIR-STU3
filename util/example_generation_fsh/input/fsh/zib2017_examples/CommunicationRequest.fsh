Instance: P1-ACP-InformRelativesRequest-29-07-2025
InstanceOf: ACPInformRelativesRequest
Title: "P1 ACP InformRelativesRequest"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "db919dcf-5fa0-428a-b9a9-f1d7d86532d7"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #completed
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* authoredOn = "2025-07-29"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter on 29-07-2025"
* requester = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* recipient = Reference(P1-ACP-ContactPerson-MichielHartman) "ContactPerson, Michiel Hartman"
* sender = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* reasonCode = $snomed#713603004 "advance care planning"


