# Corruption Dynamics Model: A Spatial Resource-Competition-Pathogen (SRCP) Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SciPy](https://img.shields.io/badge/SciPy-1.10+-green.svg)](https://scipy.org/)

Python implementation of a two-patch compartmental model for corruption dynamics with resource competition, resource-dependent transmission, predator-prey enforcement, and migration.

---

## 📚 Citation

If you use this code, please cite:

```bibtex
@article{asgedom2026corruption,
  title={Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model with Endogenous Enforcement and Migration},
  author={Asgedom, Abadi Abraha and Kefela, Yohannes Yirga and Welu, Hailu Tkue},
  journal={Applied Mathematics and Computation},
  year={2026}
}
📖 Overview
This repository contains the simulation code for the manuscript "Dynamics of Corruption as a Social Pathogen". The model incorporates:

Renewable resource dynamics with logistic growth

Resource-dependent transmission of corrupt behavior

Predator-prey enforcement dynamics

Spatial connectivity via symmetric migration between two patches
git clone https://github.com/abadiabraha20/corruption_model_2026.git
cd corruption_model_2026
pip install -r requirements.txt
corruption_model_2026/
├── src/                    # Source code
│   ├── model.py            # ODE system
│   ├── simulation.py       # Simulation utilities
│   └── analysis.py         # R0, bifurcation, sensitivity
├── scripts/                # Figure generation
│   ├── generate_figures.py # Generate all figures
│   └── figure2.py ...      # Individual figure scripts
├── params/                 # Parameter files
├── figures/                # Generated figures
├── notebooks/              # Jupyter notebooks
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
└── README.md               # This file
from src.model import corruption_model
from scipy.integrate import solve_ivp
import numpy as np

# Parameters: r, K, aS, aC, aI, b0, g, mS, mC, mI, nu
params = [0.5, 100, 0.01, 0.03, 0.01, 0.7, 0.2, 0.1, 0.1, 0.1, 0.05]

# Initial conditions
y0 = [10, 45, 0.5, 0.1, 10, 45, 0.5, 0.1]

# Run simulation
t = np.linspace(0, 500, 2000)
sol = solve_ivp(corruption_model, (0, 500), y0, t_eval=t, args=(params,), method='LSODA')

# Total corruptors
total_C = sol.y[2] + sol.y[6]
from src.analysis import compute_R0

R0 = compute_R0(params)
print(f"R0 = {R0:.3f}")  # Output: 1.524
python scripts/generate_figures.py
📊 Model Description
State Variables
Variable	Description
R
i
R 
i
​
 	Resource density in Patch 
i
i
S
i
S 
i
​
 	Cooperators in Patch 
i
i
C
i
C 
i
​
 	Corruptors in Patch 
i
i
I
i
I 
i
​
 	Enforcers in Patch 
i
i
Parameters
Parameter	Description	Typical Range
r
r	Resource growth rate	0.1–1.0
K
K	Carrying capacity	50–200
α
S
α 
S
​
 	Cooperator consumption	0.005–0.02
α
C
α 
C
​
 	Corruptor consumption	0.02–0.05
α
I
α 
I
​
 	Enforcer consumption	0.005–0.02
β
0
β 
0
​
 	Transmission rate	0.1–0.8
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
📈 Reproducing Results
Figure	Description	Script
Fig. 2	Time series (CFE vs CPE)	figure2.py
Fig. 3	Bifurcation diagram (β₀)	figure3.py
Fig. 4	Migration effect	figure4.py
Fig. 5	Spillover effect	figure5.py
Fig. 6	R₀ heatmap	figure6.py
Fig. 7	Elimination time	figure7.py
Fig. 8	Resource-transmission	figure8.py
Fig. 9	Predator-prey cycles	figure9.py
Fig. 10	Migration trade-off	figure10.py
Fig. 11	Enforcement bifurcation	figure11.py
Fig. 12	Tornado plot	figure12.py
📄 License
MIT License - see LICENSE file.

📧 Contact
Abadi Abraha Asgedom - abadi.abraha@mu.edu.et
🙏 Acknowledgments
Department of Mathematics, Mekelle University, Ethiopia.

---

## Supporting Files

### requirements.txt
```plaintext
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
__pycache__/
*.pyc
venv/
env/
figures/*.png
.DS_Store
.ipynb_checkpoints/
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
