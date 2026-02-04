Instance: ACP-Encounter-29-07-2025-Pat1
InstanceOf: ACPEncounter
Title: "ACP Encounter 29-07-2025"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "2cd036c4-a147-4ed1-9d92-d5774fdeb74c"
* status = #finished
* class = $v3-ActCode#IMP "inpatient encounter"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* participant[0].individual = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* participant[=].individual.type = "PractitionerRole"
* participant[+].individual = Reference(ACP-ContactPerson-MichielHartman-Pat1) "ContactPerson, Michiel Hartman"
* participant[=].individual.type = "RelatedPerson"
* period.start = "2025-07-29"
* period.end = "2025-07-29"
* reasonReference = Reference(ACP-Procedure-29-07-2025-Pat1) "Procedure, ACP"
