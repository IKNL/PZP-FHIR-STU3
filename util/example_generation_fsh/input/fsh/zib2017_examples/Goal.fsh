Instance: ACP-MedicalPolicyGoal-2025-Pat1
InstanceOf: ACPMedicalPolicyGoal
Title: "ACP Medical Policy Goal - 2025 - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ecd53b68-d9d2-4945-b1f0-0eccb07f48a3"
* lifecycleStatus = #active
* description = $snomed#713148004 "voorkomen en behandelen van symptomen"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* statusDate = "2025-07-29"
* note.text = "De behandeling van Hendrik is na verslechtering en gesprekken hierover bijgesteld van levensverlenging naar symptoomgericht"