# Corruption Dynamics Model: A Spatial Resource-Competition-Pathogen (SRCP) Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SciPy](https://img.shields.io/badge/SciPy-1.10+-green.svg)](https://scipy.org/)

Python implementation of a two-patch compartmental model for corruption dynamics with resource competition, resource-dependent transmission, predator-prey enforcement, and spatial connectivity via migration.

## Citation

@article{asgedom2026corruption,
  title={Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model with Endogenous Enforcement and Migration},
  author={Asgedom, Abadi Abraha and Kefela, Yohannes Yirga and Welu, Hailu Tkue},
  journal={Applied Mathematics and Computation},
  year={2026}
}

## Overview

This repository contains simulation code for the manuscript "Dynamics of Corruption as a Social Pathogen". The model incorporates:
- Renewable resource dynamics with logistic growth
- Resource-dependent transmission of corrupt behavior
- Predator-prey enforcement dynamics
- Spatial connectivity via symmetric migration between two patches

## Installation

git clone https://github.com/abadiabraha20/corruption_model_2026.git
cd corruption_model_2026
pip install -r requirements.txt

## Repository Structure

corruption_model_2026/
├── src/                    # Source code (model, simulation, analysis)
├── scripts/                # Figure generation scripts (figure2.py to figure12.py)
├── params/                 # Parameter configuration files
├── notebooks/              # Jupyter notebooks
├── figures/                # Generated figures
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
└── README.md               # This file

## Usage

### Basic Simulation

from scipy.integrate import solve_ivp
import numpy as np

def corruption_model(t, y, params):
    r, K, aS, aC, aI, b0, g, mS, mC, mI, nu = params
    R1, S1, C1, I1, R2, S2, C2, I2 = y
    dR1 = r * R1 * (1 - R1/K) - R1 * (aS * S1 + aC * C1 + aI * I1)
    dS1 = S1 * (aS * R1 - mS) - (b0 * C1 * S1) / (1 + R1) + nu * (S2 - S1)
    dC1 = C1 * (aC * R1 - mC) + (b0 * C1 * S1) / (1 + R1) - g * C1 * I1 + nu * (C2 - C1)
    dI1 = I1 * (aI * R1 - mI) + g * C1 * I1 + nu * (I2 - I1)
    dR2 = r * R2 * (1 - R2/K) - R2 * (aS * S2 + aC * C2 + aI * I2)
    dS2 = S2 * (aS * R2 - mS) - (b0 * C2 * S2) / (1 + R2) + nu * (S1 - S2)
    dC2 = C2 * (aC * R2 - mC) + (b0 * C2 * S2) / (1 + R2) - g * C2 * I2 + nu * (C1 - C2)
    dI2 = I2 * (aI * R2 - mI) + g * C2 * I2 + nu * (I1 - I2)
    return [dR1, dS1, dC1, dI1, dR2, dS2, dC2, dI2]

params = [0.5, 100, 0.01, 0.03, 0.01, 0.7, 0.2, 0.1, 0.1, 0.1, 0.05]
R_star = 0.1 / 0.01
S_star = (0.5 / 0.01) * (1 - 0.1/(0.01 * 100))
y0 = [R_star, S_star, 0.5, 0.1, R_star, S_star, 0.5, 0.1]
t = np.linspace(0, 500, 2000)
sol = solve_ivp(corruption_model, (0, 500), y0, t_eval=t, args=(params,), method='LSODA')
total_C = sol.y[2] + sol.y[6]

### Compute Reproduction Number

def compute_R0(params):
    r, K, aS, aC, aI, b0, g, mS, mC, mI, nu = params
    R_star = mS / aS
    S_star = (r / aS) * (1 - mS/(aS * K))
    return (aC * R_star + b0 * S_star / (1 + R_star)) / mC

R0 = compute_R0(params)  # Output: 1.524

### Generate Figures

python scripts/generate_figures.py

## Model Description

State Variables:
- R_i : Resource density in Patch i
- S_i : Cooperators in Patch i
- C_i : Corruptors in Patch i
- I_i : Enforcers in Patch i

Key Parameters:
- r : Resource growth rate (0.1-1.0)
- K : Carrying capacity (50-200)
- aC : Corruptor consumption rate (0.02-0.05)
- b0 : Baseline transmission rate (0.1-0.8)
- g : Enforcement rate (0.05-0.3)
- mC : Corruptor mortality (0.05-0.15)
- nu : Migration rate (0-0.1)

## Reproducing Results

| Figure | Description | Script |
|--------|-------------|--------|
| Fig. 2 | Time series (CFE vs CPE) | scripts/figure2.py |
| Fig. 3 | Bifurcation diagram (b0) | scripts/figure3.py |
| Fig. 4 | Migration effect | scripts/figure4.py |
| Fig. 5 | Spillover effect | scripts/figure5.py |
| Fig. 6 | R0 heatmap | scripts/figure6.py |
| Fig. 7 | Elimination time | scripts/figure7.py |
| Fig. 8 | Resource-transmission | scripts/figure8.py |
| Fig. 9 | Predator-prey cycles | scripts/figure9.py |
| Fig. 10 | Migration trade-off | scripts/figure10.py |
| Fig. 11 | Enforcement bifurcation | scripts/figure11.py |
| Fig. 12 | Tornado plot | scripts/figure12.py |

## License

MIT License - see LICENSE file.

## Contact

Abadi Abraha Asgedom - abadi.abraha@mu.edu.et

## Acknowledgments

Department of Mathematics, Mekelle University, Ethiopia.
