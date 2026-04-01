# Corruption Dynamics Model: A Spatial Resource-Competition-Pathogen (SRCP) Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SciPy](https://img.shields.io/badge/SciPy-1.10+-green.svg)](https://scipy.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.21+-brightgreen.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-orange.svg)](https://matplotlib.org/)

Python implementation of a two-patch compartmental model for corruption dynamics with resource competition, resource-dependent transmission, predator-prey enforcement, and spatial connectivity via migration.

---

## 📚 Citation

If you use this code in your research, teaching, or any other work, please cite:

```bibtex
@article{asgedom2026corruption,
  title={Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model with Endogenous Enforcement and Migration},
  author={Asgedom, Abadi Abraha and Kefela, Yohannes Yirga and Welu, Hailu Tkue},
  journal={Applied Mathematics and Computation},
  year={2026}
}
📖 Overview
This repository contains the complete simulation code, parameter sets, and figure generation scripts for the manuscript "Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model with Endogenous Enforcement and Migration".

The model frames corruption as a pathogenic social strategy within a biological resource-competition framework, incorporating:

Renewable resource dynamics with logistic growth

Resource-dependent transmission of corrupt behavior

Predator-prey enforcement dynamics between corruptors and enforcers

Spatial connectivity via symmetric migration between two patches

Key Features
Feature	Description
Full ODE System	8-dimensional coupled ODE system for two-patch dynamics
Reproduction Number	Computation of 
R
0
R 
0
​
  via next-generation matrix method
Bifurcation Analysis	Forward transcritical bifurcation in 
β
0
β 
0
​
 ; bistability in 
γ
γ
Migration Thresholds	Critical migration rate 
ν
c
ν 
c
​
  for synchronization
Sensitivity Analysis	PRCC global sensitivity analysis with Latin Hypercube Sampling
Figure Generation	Complete scripts for reproducing all 12 manuscript figures















