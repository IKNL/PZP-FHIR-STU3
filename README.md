# PZP FHIR Implementation Guide

This repository contains Implementation Guides (IG) in both FHIR STU3 that support the Advance Care Planning (ACP) information standard (Dutch: Proactieve Zorgplanning) for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the [Netherlands Comprehensive Cancer Organisation](https://iknl.nl/en) (Dutch: Integraal kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR to exchange ACP data. It builds on top of the Dutch Core STU3 profiles.

## Published Implementation Guides

- **R4**: https://api.iknl.nl/docs/pzp/r4/index.html
- **STU3**: https://api.iknl.nl/docs/pzp/stu3/index.html

Main source for issue tracking is at the R4 repo.

## Quick Start

This project uses the HL7 FHIR Publisher to build the implementation guides. The [PZP FHIR R4 repo](https://github.com/IKNL/PZP-FHIR-R4/) version uses FHIR Shorthand (FSH) for profile definitions. Which are used as basis to convert to STU3 profiles and examples. 


## Utility Tools

The `/util/` folder contains specialized tools for maintaining this STU3 implementation guide:

- **R4 to STU3 Transformer** (`/util/r4_to_stu3_transformer/`) - Converts FHIR resources from R4 to STU3 format
- **STU3 Mapping Generator** (`/util/stu3_mapping_generator/`) - Generates ZIB mapping tables from StructureDefinitions  
- **Example Generation FSH** (`/util/example_generation_fsh/`) - FSH-based example generation to be converted to STU3

Run the batch files in each utility folder for standard workflows. See [GitHub Copilot instructions](.github/copilot-instructions.md) for detailed usage.
