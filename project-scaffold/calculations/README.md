# Calculations Directory

Engineering calculations organized by system.

## Creating a New Calculation

1. Copy template: `../templates/calculation-notebook-template.ipynb`
2. Import parameters: `from project_params import *`
3. Follow template structure
4. Include verification section

## Required Notebook Sections

- **Purpose**: What this calculation determines
- **Inputs**: Parameters used (reference project_params.py)
- **Assumptions**: Stated clearly with justification
- **Theory**: Equations with citations
- **Calculations**: Step-by-step work
- **Results**: Summary of outputs
- **Verification**: Cross-check or validation
- **Conclusions**: Engineering interpretation

## Organization

Create subfolders by system:
```
calculations/
├── system-name/
│   ├── calc-description.ipynb
│   └── results-summary.md
```

## Best Practices

- Always import from `project_params.py` - never hardcode values
- Include units in variable names or comments
- Document verification method for each calculation
