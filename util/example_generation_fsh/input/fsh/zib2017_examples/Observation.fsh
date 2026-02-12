Instance: ACP-SpecificCareWishes-2025-Pat1
InstanceOf: ACPSpecificCareWishes
Title: "ACP Specific Care Wishes - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d2a5de51-c409-4ade-846a-9b81d1f29a26"
* status = #final
* code =  $snomed#153851000146100 "wensen en verwachtingen met betrekking tot uitkomst van behandeling"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* encounter = Reference(ACP-Encounter-2025-Pat1) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* valueString = "Broer Michiel is erg betrokken bij het proces van Hendrik. Het gaat de laatste tijd een stuk slechter en Hendrik denkt vaker na over de dood. Hij is niet bang, maar vindt het lastig om zijn familie achter te laten."
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg" 


Instance: ACP-PreferredPlaceOfDeath-2025-Pat1
InstanceOf: ACPPreferredPlaceOfDeath
Title: "ACP Preferred Place of Death - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "253b44be-bfad-4ad6-a1d6-2011f1db8a98"
* status = #final
* code =  $snomed#395091006 "Preferred place of death"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* encounter = Reference(ACP-Encounter-2025-Pat1) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#264362003 "thuis"
* note.text = "Het liefst rustig thuis"


Instance: ACP-PositionRegardingEuthanasia-2025-Pat1
InstanceOf: ACPPositionRegardingEuthanasia
Title: "ACP Position Regarding Euthanasia - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d3269776-a4dd-4f77-835e-9a17f5fb048b"
* status = #final
* code =  $snomed#340171000146104 "standpunt ten opzichte van euthanasie"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* encounter = Reference(ACP-Encounter-2025-Pat1) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#340201000146103 "wil geen euthanasie"


Instance: ACP-OrganDonationChoiceRegistration-2025-Pat1
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "ACP Organ Donation Choice Registration in Donor Register - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ec6d52d0-4ebc-4904-bf8b-8610d049be24"
* status = #final
* code = $snomed#570801000146104 "geregistreerd in orgaan donorregister" 
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* encounter = Reference(ACP-Encounter-2025-Pat1) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#373066001 "ja"


Instance: ACP-SenseOfPurpose-2025-Pat1
InstanceOf: ACPSenseOfPurpose
Title: "ACP Sense of Purpose - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "8d2ba0a3-1a15-4066-9d6a-af596c826cbe"
* status = #final
* code =  $snomed#247751003 "gevoel van zingeving"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* encounter = Reference(ACP-Encounter-2025-Pat1) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* valueString = "Hendrik wordt erg vrolijk van tulpen"
