# Corruption Dynamics Model: A Spatial Resource-Competition-Pathogen (SRCP) Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SciPy](https://img.shields.io/badge/SciPy-1.10+-green.svg)](https://scipy.org/)

Python implementation of a novel two-patch compartmental model for corruption dynamics, integrating renewable resource competition, resource-dependent transmission, predator-prey enforcement, and spatial connectivity via migration.

## 📚 Citation

If you use this code in your research, please cite:

```bibtex
@article{asgedom2026corruption,
  title={Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model with Endogenous Enforcement and Migration},
  author={Asgedom, Abadi Abraha and Kefela, Yohannes Yirga and Welu, Hailu Tkue},
  journal={Applied Mathematics and Computation},
  year={2026}
}
📖 Overview
This repository contains the complete simulation code, parameter sets, and figure generation scripts for the manuscript "Dynamics of Corruption as a Social Pathogen". The model frames corruption as a pathogenic social strategy within a biological resource-competition framework, incorporating:

Renewable resource dynamics with logistic growth

Resource-dependent transmission of corrupt behavior

Predator-prey enforcement dynamics between corruptors and enforcers

Spatial connectivity via symmetric migration between two patches

Key Features
Full ODE system implementation for two-patch dynamics

Computation of basic reproduction number 
R
0
R 
0
​
 

Bifurcation analysis with respect to transmission and enforcement parameters

Critical migration threshold calculations

PRCC global sensitivity analysis

Complete figure generation for all manuscript figures

🚀 Getting Started
Prerequisites
Python 3.9 or higher

Required packages (see requirements.txt)

Installation
Clone the repository:

bash
git clone https://github.com/abadiabraha20/corruption_model_2026.git
cd corruption_model_2026
Install dependencies:

bash
pip install -r requirements.txt
📁 Repository Structure
text
corruption_model_2026/
├── src/
│   ├── __init__.py
│   ├── model.py              # ODE system definition
│   ├── simulation.py         # Simulation utilities
│   └── analysis.py           # R0, bifurcation, sensitivity analysis
├── scripts/
│   ├── generate_figures.py   # Generate all manuscript figures
│   ├── figure2.py            # Time series (CFE vs CPE)
│   ├── figure3.py            # Bifurcation diagram (beta0)
│   ├── figure4.py            # Migration effect
│   ├── figure5.py            # Spillover effect
│   ├── figure6.py            # R0 heatmap
│   ├── figure7.py            # Elimination time
│   ├── figure8.py            # Resource-transmission relationship
│   ├── figure9.py            # Predator-prey cycles
│   ├── figure10.py           # Migration trade-off
│   ├── figure11.py           # Enforcement bifurcation
│   └── figure12.py           # Tornado plot (sensitivity)
├── params/
│   ├── baseline_params.json  # Baseline parameter values
│   └── prcc_params.json      # PRCC analysis parameter ranges
├── figures/                  # Generated figures (PNG)
├── notebooks/                # Jupyter notebooks for exploration
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # This file
🔧 Usage
Basic Simulation
python
from src.model import corruption_model
from src.simulation import simulate
import numpy as np

# Define parameters
params = [0.5, 100, 0.01, 0.03, 0.01, 0.7, 0.2, 0.1, 0.1, 0.1, 0.05]
#          r    K    aS    aC    aI    b0    g    mS   mC   mI   nu

# Initial conditions
y0 = [10, 45, 0.5, 0.1, 10, 45, 0.5, 0.1]

# Run simulation
t, y = simulate(params, y0, t_max=500)

# Plot results
import matplotlib.pyplot as plt
plt.plot(t, y[:, 2] + y[:, 6], 'r-', label='Total Corruptors')
plt.xlabel('Time (years)')
plt.ylabel('Population Density')
plt.legend()
plt.show()
Compute Reproduction Number
python
from src.analysis import compute_R0

params = [0.5, 100, 0.01, 0.03, 0.01, 0.7, 0.2, 0.1, 0.1, 0.1, 0.05]
R0 = compute_R0(params)
print(f"R0 = {R0:.3f}")
Generate All Figures
To reproduce all figures from the manuscript:

bash
python scripts/generate_figures.py
Figures will be saved to the figures/ directory.

Run Bifurcation Analysis
python
from src.analysis import bifurcation_analysis

# Analyze with respect to beta0
results = bifurcation_analysis('beta0', 0.1, 1.2, n_points=30)
📊 Model Description
State Variables
Variable	Description
R
i
R 
i
​
 	Renewable resource density in Patch 
i
i
S
i
S 
i
​
 	Cooperators (sustainable users) in Patch 
i
i
C
i
C 
i
​
 	Corruptors (unsustainable exploiters) in Patch 
i
i
I
i
I 
i
​
 	Enforcers (suppressors) in Patch 
i
i
Parameters
Parameter	Description	Typical Range
r
r	Resource growth rate	0.1–1.0
K
K	Resource carrying capacity	50–200
α
S
α 
S
​
 	Cooperator consumption rate	0.005–0.02
α
C
α 
C
​
 	Corruptor consumption rate	0.02–0.05
α
I
α 
I
​
 	Enforcer consumption rate	0.005–0.02
β
0
β 
0
​
 	Baseline transmission rate	0.1–0.8
γ
γ	Enforcement rate	0.05–0.3
μ
S
,
μ
C
,
μ
I
μ 
S
​
 ,μ 
C
​
 ,μ 
I
​
 	Mortality rates	0.05–0.15
ν
ν	Migration rate	0–0.1
📈 Results Reproduction
All numerical results presented in the manuscript can be reproduced using the provided code:

Figure 2: Time series (CFE vs CPE) → scripts/figure2.py

Figure 3: Bifurcation diagram (β₀) → scripts/figure3.py

Figure 4: Migration effect → scripts/figure4.py

Figure 5: Spillover effect → scripts/figure5.py

Figure 6: R₀ heatmap → scripts/figure6.py

Figure 7: Elimination time → scripts/figure7.py

Figure 8: Resource-transmission → scripts/figure8.py

Figure 9: Predator-prey cycles → scripts/figure9.py

Figure 10: Migration trade-off → scripts/figure10.py

Figure 11: Enforcement bifurcation → scripts/figure11.py

Figure 12: Tornado plot → scripts/figure12.py

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📧 Contact
For questions or feedback, please contact:

Abadi Abraha Asgedom - abadi.abraha@mu.edu.et

🙏 Acknowledgments
This work was supported by the Department of Mathematics, Mekelle University, Ethiopia. The authors thank the anonymous reviewers for their valuable feedback.

Note: This repository is actively maintained. If you encounter any issues or have suggestions for improvement, please open an issue on GitHub.

text

---

## Additional Files to Create

### requirements.txt
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0

text

### .gitignore
Python
pycache/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env
.venv

Jupyter Notebook
.ipynb_checkpoints/
*.ipynb

Figures
figures/.png
figures/.pdf

IDE
.vscode/
.idea/

OS
.DS_Store
Thumbs.db

text

### LICENSE (MIT)
MIT License

Copyright (c) 2026 Abadi Abraha Asgedom, Yohannes Yirga Kefela, Hailu Tkue Welu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

text

---

This README provides a complete, professional documentation for your repository that will help users understand, use, and cite your work. Would you like me to help you with any other files?
