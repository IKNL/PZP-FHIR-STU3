Instance: ACP-MedicalDevice-ICD-Pat1
InstanceOf: ACP-MedicalDevice
Title: "ACP MedicalDevice ICD Pat 1"
Usage: #example
* extension[healthProfessional].valueReference = Reference(ACP-HealthProfessional-PractitionerRole-Santos-Pat1) "Healthcare professional, Santos"
// * extension[location].valueReference = Reference(ACP-Healthcareprovider-Location) "Healthcare provider (location), Zorginstelling F"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "19f6c62e-dc54-46ff-b350-99f1e7a5a566"
* status = #active
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* device = Reference(ACP-MedicalDevice.Product-ICD-Pat1)
// What to do with reference to problem as in test script? --> check with Esther
* bodySite = $snomed#80891009 "structuur van cor"
* bodySite.extension[laterality].valueCodeableConcept = $snomed#7771000 "links"
* timingPeriod.start = "2020-05-19"
