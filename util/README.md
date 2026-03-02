# util/ — Helper Scripts & Tools

Standalone Python utilities for the IKNL PZP FHIR STU3 Implementation Guide.
None of these scripts are required by the IG build itself — they automate
common development, analysis, and transformation tasks.

Each script contains full documentation (usage, examples, configuration) in
its module docstring.  **Check the configuration constants at the top of each
file** — you may need to adjust paths or URLs for your local setup.

All scripts require **Python 3.8+** and use only the standard library.

## Scripts

| Script | Purpose |
|---|---|
| `stu3_mapping_generator/stu3_mapping_table_generator.py` | Generates a Markdown mapping table from STU3 StructureDefinition mappings and an ART-DECOR JSON dataset export. |
| `questionnaire_item_prefix_populator.py` | Moves detected prefixes (a), 1., etc.) from `item.text` to `item.prefix` in Questionnaire resources, and strips them from QuestionnaireResponse resources for FHIR compliance. |
| `questionnaire_item_code_remover.py` | Removes all `code` elements from Questionnaire items at every nesting level. |

## Subfolders

| Folder | Purpose |
|---|---|
| `r4_to_stu3_transformer/` | Transforms FHIR resources from R4 format to STU3 using resource-specific transformers. Includes a batch script (`transform_r4_to_stu3.bat`) and auto-discovered transformer classes. |
| `stu3_mapping_generator/` | Contains the mapping table generator and its batch script (`generate_stu3_mappings.bat`). |
| `example_generation_fsh/` | FSH (FHIR Shorthand) project for generating additional example resources via SUSHI. |

## Data Flow

```
R4 Repository → FSH Generation → STU3 Transformation → Prefix / Code Cleanup → Mapping Generation → STU3 IG Build
```
