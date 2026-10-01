# Semiconductor Wafer Yield & Defect Density Analysis

A Monte Carlo-based semiconductor wafer yield analysis project developed using Python, NumPy, and Matplotlib. The project models random defect distribution across a circular semiconductor wafer, maps defects to individual dies, classifies defective dies, and analyzes wafer yield as a function of defect density.

## Project Overview

Semiconductor manufacturing yield is strongly affected by defect density and die area. This project uses Monte Carlo simulation to study the relationship between defect density, defective dies, and wafer yield.

The simulation includes:

- Circular wafer geometry
- Die grid generation
- Defect density modeling
- Random spatial defect generation
- Defect-to-die mapping
- Good and defective die classification
- Wafer yield calculation
- Monte Carlo statistical analysis
- Yield distribution analysis
- Yield versus defect density analysis
- Analytical yield validation using a Poisson model
  ## Wafer Defect Map

![Wafer Defect Map](<img width="1536" height="768" alt="defect map" src="https://github.com/user-attachments/assets/a9f5b786-f6e2-4c46-a13b-0010f32cca79" />
)

## Monte Carlo Yield Distribution

![Monte Carlo Yield Distribution](<img width="800" height="500" alt="Figure 2" src="https://github.com/user-attachments/assets/189a660d-de87-4ceb-af3d-e42e496b7f60" />
)

## Yield vs Defect Density

![Yield vs Defect Density](<img width="801" height="504" alt="Figure_1" src="https://github.com/user-attachments/assets/cb00aff7-81be-4fbd-8b39-b30ce0785843" />
)

## Technologies Used

- Python
- NumPy
- Matplotlib
- Monte Carlo Simulation
- Probability and Statistics

## Simulation Parameters

| Parameter | Value |
|---|---:|
| Wafer diameter | 150 mm |
| Wafer area | 176.71 cm² |
| Die size | 5 × 5 mm |
| Defect density | 0.1 defects/cm² |
| Usable dies | 648 |
| Monte Carlo trials | 5,000 |

## Methodology

The simulation follows the following flow:

```text
Defect Density
       ↓
Wafer Geometry
       ↓
Random Defect Generation
       ↓
Defect-to-Die Mapping
       ↓
Good / Bad Die Classification
       ↓
Wafer Yield Calculation
       ↓
Monte Carlo Statistical Analysis
       ↓
Yield vs Defect Density
