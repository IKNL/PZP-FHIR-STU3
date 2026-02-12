Instance: ACP-HealthProfessional-Practitioner-DrVanHuissen-Pat1
InstanceOf: ACPHealthProfessionalPractitioner
Title: "ACP HealthProfessional Practitioner - Dr. van Huissen - Pat 1"
Usage: #example
* identifier.system = "http://fhir.nl/fhir/NamingSystem/agb-z"
* identifier.value = "000002222"
* name.use = #official
* name.text = "Marleen van Huissen"
* name.family = "van Huissen"
* name.family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name.family.extension[=].valueString = "van"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension[=].valueString = "Huissen"
* name[nameInformation-GivenName].use = #usual
* name[nameInformation-GivenName].given = "Marleen"


Instance: ACP-HealthProfessional-Practitioner-Gerrits-Pat1
InstanceOf: ACPHealthProfessionalPractitioner
Title: "ACP HealthProfessional Practitioner - Gerrits - Pat 1"
Usage: #example
* name.use = #official
* name.text = "Adam Gerrits"