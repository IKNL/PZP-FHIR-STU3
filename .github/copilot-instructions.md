# GitHub Copilot Instructions - PZP FHIR STU3

This repository contains the STU3 version of the PZP (Proactieve Zorgplanning) FHIR Implementation Guide. The codebase includes several utility tools for transforming and generating FHIR resources.

## Project Structure

- **Main IG files**: Located in `/input/` directory (profiles, examples, pages)
- **Utilities**: Located in `/util/` directory with specialized transformation tools
- **Output**: Generated IG files in `/output/` directory

## Utility Tools (`/util/` folder)

### 1. R4 to STU3 Transformer (`/util/r4_to_stu3_transformer/`)

**Purpose**: Transforms FHIR resources from R4 format to STU3 format using resource-specific transformers.

**Key Files**:
- `fhir_r4_to_stu3_transformer.py` - Main orchestrator script
- `transform_r4_to_stu3.bat` - Convenience batch script for PZP project
- `transformers/` - Directory containing resource-specific transformer classes

**Usage**:
```bash
# Using the batch file (recommended for PZP project)
transform_r4_to_stu3.bat

# Direct Python usage
python fhir_r4_to_stu3_transformer.py input_dir1 input_dir2 output_dir [--resources ResourceType]
```

**Input Sources**:
- R4 repository: `C:\git\IKNL\iknl-pzp-fhir-r4\fsh-generated\resources`
- STU3 FSH examples: `C:\git\IKNL\iknl-pzp-fhir-stu3\util\example_generation_fsh\fsh-generated\resources`

**Configuration**: Update paths in `transform_r4_to_stu3.bat` if your directory structure differs.

**Features**:
- Automatically discovers available transformers
- Supports multiple input directories
- Handles PractitionerRole reference resolution across resources
- Skips non-convertible resources (ValueSet, StructureDefinition, etc.)

### 2. STU3 Mapping Generator (`/util/stu3_mapping_generator/`)

**Purpose**: Generates mapping tables from STU3 StructureDefinition JSON files to ZIB concepts.

**Key Files**:
- `stu3_mapping_table_generator.py` - Main script for generating mapping tables
- `generate_stu3_mappings.bat` - Convenience batch script

**Usage**:
```bash
# Using the batch file
generate_stu3_mappings.bat

# Direct Python usage
python stu3_mapping_table_generator.py
```

**Output**: Creates `input/includes/zib2017_stu3_mappings.md` with mapping tables.

### 3. Example Generation FSH (`/util/example_generation_fsh/`)

**Purpose**: Contains FSH (FHIR Shorthand) configuration for generating additional examples.

**Key Files**:
- `sushi-config.yaml` - SUSHI configuration for FSH compilation
- `input/` - FSH source files
- `fsh-generated/` - Generated FHIR resources from FSH

**Dependencies**:
- R4 PZP implementation guide
- Dutch Core profiles
- ZIB 2020 profiles

## Development Workflow

1. **Building R4 sources**: Ensure the R4 repository is built first
2. **Generating FSH examples**: Run SUSHI on the example generation FSH project
3. **Transforming to STU3**: Use the R4 to STU3 transformer to convert resources
4. **Generating mappings**: Create mapping tables using the STU3 mapping generator
5. **Building STU3 IG**: Run the FHIR publisher to generate the final implementation guide

## Important Notes

- **Path Configuration**: Update directory paths in batch files if your setup differs from the default
- **Dependencies**: This STU3 repository depends on content from the R4 repository
- **Resource Types**: Not all FHIR resource types are converted (see transformer code for supported types)
- **Reference Resolution**: PractitionerRole references are automatically resolved during transformation

## Code Patterns

When working with the transformers:
- Each resource type has its own transformer class inheriting from `BaseTransformer`
- Transformers are automatically discovered by the main orchestrator
- Use the batch files for standard PZP project workflows
- Use direct Python scripts for custom transformations or different directory structures

## Data Flow

```
R4 Repository → FSH Generation → STU3 Transformation → Mapping Generation → STU3 IG Build
```

This workflow ensures that the STU3 implementation guide stays synchronized with the R4 version while maintaining STU3-specific adaptations and mappings.