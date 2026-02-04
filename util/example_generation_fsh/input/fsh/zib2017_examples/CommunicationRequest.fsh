Instance: ACP-InformRelativesRequest-29-07-2025-Pat1
InstanceOf: ACPInformRelativesRequest
Title: "ACP InformRelativesRequest 29-07-2025 Pat1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "db919dcf-5fa0-428a-b9a9-f1d7d86532d7"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #completed
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* authoredOn = "2025-07-29"
* encounter = Reference(ACP-Encounter-29-07-2025-Pat1) "Encounter on 29-07-2025"
* requester = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* recipient = Reference(ACP-ContactPerson-MichielHartman-Pat1) "ContactPerson, Michiel Hartman"
* sender = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* reasonCode = $snomed#713603004 "advance care planning"


