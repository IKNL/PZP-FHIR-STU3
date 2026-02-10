Instance: ACP-Procedure-2025-Pat1
InstanceOf: ACPProcedure
Title: "ACP Procedure - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "6b384331-b19f-42a8-a7d7-2e5837d136e9"
* status = #completed
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer[0].actor = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-MichielHartman-Pat1) "ContactPerson, Michiel Hartman"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2025-07-29"
* performedPeriod.end = "2025-07-29"
* code = $snomed#713603004 "advance care planning"



