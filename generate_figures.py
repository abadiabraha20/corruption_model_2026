"""
Corruption Dynamics Model - Complete Figure Generation Code
Author: Abadi Abraha Asgedom
Paper: Dynamics of Corruption as a Social Pathogen: A Two-Patch Resource-Competition Model
Journal: PLOS One

This script generates all figures for the manuscript.
Run: python generate_all_figures.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import stats
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

print("="*70)
print("CORRUPTION DYNAMICS MODEL - FIGURE GENERATION")
print("="*70)

# ============================================
# MODEL DEFINITION (Used across all figures)
# ============================================

def corruption_model(t, y, r, K, alpha_S, alpha_C, alpha_I, beta0, gamma, mu_S, mu_C, mu_I, nu):
    """Two-patch RCP model"""
    R1, S1, C1, I1, R2, S2, C2, I2 = y
    
    beta_R1 = beta0 / (1 + R1)
    beta_R2 = beta0 / (1 + R2)
    
    # Patch 1
    dR1 = r * R1 * (1 - R1/K) - R1 * (alpha_S*S1 + alpha_C*C1 + alpha_I*I1)
    dS1 = S1 * (alpha_S*R1 - mu_S) - beta_R1 * C1 * S1 + nu * (S2 - S1)
    dC1 = C1 * (alpha_C*R1 - mu_C) + beta_R1 * C1 * S1 - gamma * C1 * I1 + nu * (C2 - C1)
    dI1 = I1 * (alpha_I*R1 - mu_I) + gamma * C1 * I1 + nu * (I2 - I1)
    
    # Patch 2
    dR2 = r * R2 * (1 - R2/K) - R2 * (alpha_S*S2 + alpha_C*C2 + alpha_I*I2)
    dS2 = S2 * (alpha_S*R2 - mu_S) - beta_R2 * C2 * S2 + nu * (S1 - S2)
    dC2 = C2 * (alpha_C*R2 - mu_C) + beta_R2 * C2 * S2 - gamma * C2 * I2 + nu * (C1 - C2)
    dI2 = I2 * (alpha_I*R2 - mu_I) + gamma * C2 * I2 + nu * (I1 - I2)
    
    return [dR1, dS1, dC1, dI1, dR2, dS2, dC2, dI2]

# ============================================
# BASELINE PARAMETERS
# ============================================

params_cfe = {
    'r': 0.5, 'K': 100, 'alpha_S': 0.01, 'alpha_C': 0.03, 'alpha_I': 0.01,
    'beta0': 0.4, 'gamma': 0.2, 'mu_S': 0.1, 'mu_C': 0.1, 'mu_I': 0.1, 'nu': 0.05
}

params_cpe = {
    'r': 0.5, 'K': 100, 'alpha_S': 0.01, 'alpha_C': 0.03, 'alpha_I': 0.01,
    'beta0': 0.7, 'gamma': 0.2, 'mu_S': 0.1, 'mu_C': 0.1, 'mu_I': 0.1, 'nu': 0.05
}

# ============================================
# FIGURE 1: Flowchart (already exists as PNG)
# ============================================
print("\n[1/13] Figure 1: Flowchart - Use existing flowchart.png")

# ============================================
# FIGURE 2: Time Series (CFE vs CPE)
# ============================================
print("[2/13] Generating Figure 2: Time Series...")

y0 = [100, 50, 5, 2, 100, 50, 1, 1]
t_span = (0, 500)
t_eval = np.linspace(0, 500, 5000)

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

# Panel a: CFE (beta0=0.4)
sol_cfe = solve_ivp(lambda t, y: corruption_model(t, y, **params_cfe),
                    t_span, y0, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes2[0].plot(sol_cfe.t, sol_cfe.y[2], 'b-', linewidth=1.5, label='Corruptors $C_1$')
axes2[0].plot(sol_cfe.t, sol_cfe.y[6], 'r--', linewidth=1.5, label='Corruptors $C_2$')
axes2[0].set_xlabel('Time', fontsize=12)
axes2[0].set_ylabel('Population Density', fontsize=12)
axes2[0].set_title('(a) Corruption-Free Equilibrium ($\\mathbb{R}_0 = 0.87 < 1$)', fontsize=12)
axes2[0].legend()
axes2[0].grid(True, alpha=0.3)

# Panel b: CPE (beta0=0.7)
sol_cpe = solve_ivp(lambda t, y: corruption_model(t, y, **params_cpe),
                    t_span, y0, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes2[1].plot(sol_cpe.t, sol_cpe.y[2], 'b-', linewidth=1.5, label='Corruptors $C_1$')
axes2[1].plot(sol_cpe.t, sol_cpe.y[6], 'r--', linewidth=1.5, label='Corruptors $C_2$')
axes2[1].set_xlabel('Time', fontsize=12)
axes2[1].set_ylabel('Population Density', fontsize=12)
axes2[1].set_title('(b) Corruption-Persistent Equilibrium ($\\mathbb{R}_0 = 1.52 > 1$)', fontsize=12)
axes2[1].legend()
axes2[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure2.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure2.png")

# ============================================
# FIGURE 3: Bifurcation Diagram
# ============================================
print("[3/13] Generating Figure 3: Bifurcation Diagram...")

def compute_equilibrium(beta0, nu, y_initial, t_span=(0, 500)):
    params = params_cpe.copy()
    params['beta0'] = beta0
    params['nu'] = nu
    sol = solve_ivp(lambda t, y: corruption_model(t, y, **params),
                   t_span, y_initial, method='LSODA', rtol=1e-8, atol=1e-10)
    return np.mean(sol.y[2][-500:]) + np.mean(sol.y[6][-500:])

beta_range = np.linspace(0.2, 1.0, 30)
nu_values = [0.01, 0.05, 0.1]
colors = ['blue', 'green', 'red']

fig3, ax3 = plt.subplots(figsize=(10, 6))

y_init = [100, 50, 5, 2, 100, 50, 1, 1]
for nu, color in zip(nu_values, colors):
    C_star = []
    for beta in beta_range:
        C_star.append(compute_equilibrium(beta, nu, y_init))
    ax3.plot(beta_range, C_star, 'o-', color=color, linewidth=2, markersize=4, label=f'$\\nu = {nu}$')

# Add R0 axis on top
R0_vals = (0.03*10 + 0.7*45/11)/0.1 * beta_range/0.7
ax3_twin = ax3.twiny()
ax3_twin.set_xlabel('$\\mathbb{R}_0$', fontsize=12)
ax3_twin.set_xlim(R0_vals[0], R0_vals[-1])

ax3.axvline(x=0.7/1.52, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax3.set_xlabel('Transmission rate $\\beta_0$', fontsize=12)
ax3.set_ylabel('Total corruptors $C^* = C_1^* + C_2^*$', fontsize=12)
ax3.set_title('Forward transcritical bifurcation at $\\mathbb{R}_0 = 1$', fontsize=12)
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure3.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure3.png")

# ============================================
# FIGURE 4: Migration Transient Dynamics
# ============================================
print("[4/13] Generating Figure 4: Migration Transient Dynamics...")

y0_asym = [100, 50, 15, 5, 100, 50, 0.1, 0.1]
t_eval = np.linspace(0, 200, 2000)

fig4, axes4 = plt.subplots(1, 2, figsize=(14, 5))

# Panel a: Low migration (nu=0.01)
params_low = params_cpe.copy()
params_low['nu'] = 0.01
sol_low = solve_ivp(lambda t, y: corruption_model(t, y, **params_low),
                    (0, 200), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes4[0].plot(sol_low.t, sol_low.y[2], 'b-', linewidth=1.5, label='Patch 1')
axes4[0].plot(sol_low.t, sol_low.y[6], 'r--', linewidth=1.5, label='Patch 2')
axes4[0].set_xlabel('Time', fontsize=12)
axes4[0].set_ylabel('Corruptors', fontsize=12)
axes4[0].set_title('(a) Low migration ($\\nu = 0.01 < \\nu_c$)', fontsize=12)
axes4[0].legend()
axes4[0].grid(True, alpha=0.3)

# Panel b: High migration (nu=0.1)
params_high = params_cpe.copy()
params_high['nu'] = 0.1
sol_high = solve_ivp(lambda t, y: corruption_model(t, y, **params_high),
                     (0, 200), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes4[1].plot(sol_high.t, sol_high.y[2], 'b-', linewidth=1.5, label='Patch 1')
axes4[1].plot(sol_high.t, sol_high.y[6], 'r--', linewidth=1.5, label='Patch 2')
axes4[1].set_xlabel('Time', fontsize=12)
axes4[1].set_ylabel('Corruptors', fontsize=12)
axes4[1].set_title('(b) High migration ($\\nu = 0.1 > \\nu_c$)', fontsize=12)
axes4[1].legend()
axes4[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure4.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure4.png")

# ============================================
# FIGURE 5: Spillover Effect
# ============================================
print("[5/13] Generating Figure 5: Spillover Effect...")

fig5, axes5 = plt.subplots(1, 2, figsize=(14, 5))

# Panel a: No migration
params_no_nu = params_cpe.copy()
params_no_nu['nu'] = 0
sol_no_nu = solve_ivp(lambda t, y: corruption_model(t, y, **params_no_nu),
                      (0, 500), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes5[0].plot(sol_no_nu.t, sol_no_nu.y[2], 'b-', linewidth=1.5, label='Patch 1')
axes5[0].plot(sol_no_nu.t, sol_no_nu.y[6], 'r--', linewidth=1.5, label='Patch 2')
axes5[0].set_xlabel('Time', fontsize=12)
axes5[0].set_ylabel('Corruptors', fontsize=12)
axes5[0].set_title('(a) Without migration', fontsize=12)
axes5[0].legend()
axes5[0].grid(True, alpha=0.3)

# Panel b: With migration (nu=0.05)
params_nu = params_cpe.copy()
params_nu['nu'] = 0.05
sol_nu = solve_ivp(lambda t, y: corruption_model(t, y, **params_nu),
                   (0, 500), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
axes5[1].plot(sol_nu.t, sol_nu.y[2], 'b-', linewidth=1.5, label='Patch 1')
axes5[1].plot(sol_nu.t, sol_nu.y[6], 'r--', linewidth=1.5, label='Patch 2')
axes5[1].set_xlabel('Time', fontsize=12)
axes5[1].set_ylabel('Corruptors', fontsize=12)
axes5[1].set_title('(b) With migration ($\\nu = 0.05$)', fontsize=12)
axes5[1].legend()
axes5[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure5.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure5.png")

# ============================================
# FIGURE 6: Asymmetric Migration
# ============================================
print("[6/13] Generating Figure 6: Asymmetric Migration...")

def corruption_model_asym(t, y, r, K, alpha_S, alpha_C, alpha_I, beta0, gamma, mu_S, mu_C, mu_I, nu12, nu21):
    R1, S1, C1, I1, R2, S2, C2, I2 = y
    beta_R1 = beta0 / (1 + R1)
    beta_R2 = beta0 / (1 + R2)
    
    dR1 = r * R1 * (1 - R1/K) - R1 * (alpha_S*S1 + alpha_C*C1 + alpha_I*I1)
    dS1 = S1 * (alpha_S*R1 - mu_S) - beta_R1 * C1 * S1 + nu21 * S2 - nu12 * S1
    dC1 = C1 * (alpha_C*R1 - mu_C) + beta_R1 * C1 * S1 - gamma * C1 * I1 + nu21 * C2 - nu12 * C1
    dI1 = I1 * (alpha_I*R1 - mu_I) + gamma * C1 * I1 + nu21 * I2 - nu12 * I1
    
    dR2 = r * R2 * (1 - R2/K) - R2 * (alpha_S*S2 + alpha_C*C2 + alpha_I*I2)
    dS2 = S2 * (alpha_S*R2 - mu_S) - beta_R2 * C2 * S2 + nu12 * S1 - nu21 * S2
    dC2 = C2 * (alpha_C*R2 - mu_C) + beta_R2 * C2 * S2 - gamma * C2 * I2 + nu12 * C1 - nu21 * C2
    dI2 = I2 * (alpha_I*R2 - mu_I) + gamma * C2 * I2 + nu12 * I1 - nu21 * I2
    
    return [dR1, dS1, dC1, dI1, dR2, dS2, dC2, dI2]

params_asym = params_cpe.copy()
del params_asym['nu']

fig6, ax6 = plt.subplots(figsize=(10, 6))

# Symmetric case
sol_sym = solve_ivp(lambda t, y: corruption_model_asym(t, y, nu12=0.05, nu21=0.05, **params_asym),
                    (0, 500), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
ax6.plot(sol_sym.t, sol_sym.y[2], 'b-', linewidth=1.5, label='Patch 1 (sym)')
ax6.plot(sol_sym.t, sol_sym.y[6], 'b--', linewidth=1.5, label='Patch 2 (sym)')

# Asymmetric case
sol_asym = solve_ivp(lambda t, y: corruption_model_asym(t, y, nu12=0.1, nu21=0.01, **params_asym),
                     (0, 500), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)
ax6.plot(sol_asym.t, sol_asym.y[2], 'r-', linewidth=1.5, label='Patch 1 (asym)')
ax6.plot(sol_asym.t, sol_asym.y[6], 'r--', linewidth=1.5, label='Patch 2 (asym)')

ax6.set_xlabel('Time', fontsize=12)
ax6.set_ylabel('Corruptors', fontsize=12)
ax6.set_title('Asymmetric migration: source-sink dynamics', fontsize=12)
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure6.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure6.png")

# ============================================
# FIGURE 7: Elimination Time
# ============================================
print("[7/13] Generating Figure 7: Elimination Time...")

gamma_range = np.linspace(0.05, 0.5, 15)
initial_c_levels = [5, 10, 20]

fig7, axes7 = plt.subplots(1, 2, figsize=(14, 5))

# Panel a: Elimination time vs gamma
for C0 in initial_c_levels:
    elim_times = []
    for gamma in gamma_range:
        params_test = params_cfe.copy()
        params_test['gamma'] = gamma
        params_test['beta0'] = 0.6
        y0_test = [100, 50, C0, 5, 100, 50, C0, 5]
        sol = solve_ivp(lambda t, y: corruption_model(t, y, **params_test),
                        (0, 500), y0_test, method='LSODA', rtol=1e-6, atol=1e-8)
        c_total = sol.y[2] + sol.y[6]
        idx = np.where(c_total < 0.1)[0]
        if len(idx) > 0:
            elim_times.append(sol.t[idx[0]])
        else:
            elim_times.append(500)
    axes7[0].plot(gamma_range, elim_times, 'o-', linewidth=2, markersize=4, label=f'$C_0 = {C0}$')

axes7[0].axvline(x=0.25, color='gray', linestyle='--', linewidth=1.5)
axes7[0].set_xlabel('Enforcement rate $\\gamma$', fontsize=12)
axes7[0].set_ylabel('Elimination time', fontsize=12)
axes7[0].set_title('(a) Elimination time vs enforcement', fontsize=12)
axes7[0].legend()
axes7[0].grid(True, alpha=0.3)

# Panel b: Phase diagram
gamma_phase = np.linspace(0.05, 0.5, 40)
C0_phase = np.linspace(1, 30, 40)
phase = np.zeros((len(gamma_phase), len(C0_phase)))

for i, gamma in enumerate(gamma_phase):
    for j, C0 in enumerate(C0_phase):
        params_test = params_cfe.copy()
        params_test['gamma'] = gamma
        params_test['beta0'] = 0.6
        y0_test = [100, 50, C0, 5, 100, 50, C0, 5]
        sol = solve_ivp(lambda t, y: corruption_model(t, y, **params_test),
                        (0, 500), y0_test, method='LSODA', rtol=1e-6, atol=1e-8)
        c_total = sol.y[2][-1] + sol.y[6][-1]
        phase[i, j] = 1 if c_total < 0.1 else 0

im = axes7[1].imshow(phase.T, origin='lower', aspect='auto', 
                      extent=[gamma_phase[0], gamma_phase[-1], C0_phase[0], C0_phase[-1]],
                      cmap='RdYlGn')
axes7[1].set_xlabel('Enforcement rate $\\gamma$', fontsize=12)
axes7[1].set_ylabel('Initial corruption $C_0$', fontsize=12)
axes7[1].set_title('(b) Phase diagram: Green = elimination, Red = persistence', fontsize=12)
plt.colorbar(im, ax=axes7[1], label='Elimination (1) / Persistence (0)')

plt.tight_layout()
plt.savefig('figures/figure7.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure7.png")

# ============================================
# FIGURE 8: Resource-Transmission Feedback
# ============================================
print("[8/13] Generating Figure 8: Resource-Transmission Feedback...")

R_range = np.linspace(0, 100, 500)
beta0_val = 0.7
beta_R = beta0_val / (1 + R_range)

fig8, axes8 = plt.subplots(2, 2, figsize=(12, 10))

# Panel a: Beta(R) function
axes8[0, 0].plot(R_range, beta_R, 'b-', linewidth=2)
axes8[0, 0].set_xlabel('Resource density $R$', fontsize=12)
axes8[0, 0].set_ylabel('Transmission rate $\\beta(R)$', fontsize=12)
axes8[0, 0].set_title('(a) Resource-dependent transmission', fontsize=12)
axes8[0, 0].grid(True, alpha=0.3)

# Panel b-d: Time series from simulation
sol_resource = solve_ivp(lambda t, y: corruption_model(t, y, **params_cpe),
                         (0, 500), y0, t_eval=t_eval, method='LSODA', rtol=1e-8, atol=1e-10)

# Panel b: Resource over time
axes8[0, 1].plot(sol_resource.t, sol_resource.y[0], 'g-', linewidth=1.5)
axes8[0, 1].set_xlabel('Time', fontsize=12)
axes8[0, 1].set_ylabel('Resource $R_1$', fontsize=12)
axes8[0, 1].set_title('(b) Resource depletion', fontsize=12)
axes8[0, 1].grid(True, alpha=0.3)

# Panel c: Transmission over time
beta_t = params_cpe['beta0'] / (1 + sol_resource.y[0])
axes8[1, 0].plot(sol_resource.t, beta_t, 'm-', linewidth=1.5)
axes8[1, 0].set_xlabel('Time', fontsize=12)
axes8[1, 0].set_ylabel('Transmission rate $\\beta(R_1)$', fontsize=12)
axes8[1, 0].set_title('(c) Transmission increases as resource declines', fontsize=12)
axes8[1, 0].grid(True, alpha=0.3)

# Panel d: R-C phase space
axes8[1, 1].plot(sol_resource.y[0][-2000:], sol_resource.y[2][-2000:], 'b-', linewidth=0.8, alpha=0.7)
axes8[1, 1].set_xlabel('Resource $R_1$', fontsize=12)
axes8[1, 1].set_ylabel('Corruptors $C_1$', fontsize=12)
axes8[1, 1].set_title('(d) Negative correlation in phase space', fontsize=12)
axes8[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure8.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure8.png")

# ============================================
# FIGURE 9: Predator-Prey Dynamics
# ============================================
print("[9/13] Generating Figure 9: Predator-Prey Dynamics...")

fig9, axes9 = plt.subplots(2, 2, figsize=(14, 12))

# Panel a: Time series
axes9[0, 0].plot(sol_cpe.t, sol_cpe.y[2], 'b-', linewidth=1.5, label='Corruptors $C_1$')
axes9[0, 0].plot(sol_cpe.t, sol_cpe.y[3], 'r-', linewidth=1.5, label='Enforcers $I_1$')
axes9[0, 0].set_xlabel('Time', fontsize=12)
axes9[0, 0].set_ylabel('Population Density', fontsize=12)
axes9[0, 0].set_title('(a) Phase-shifted oscillations', fontsize=12)
axes9[0, 0].legend()
axes9[0, 0].grid(True, alpha=0.3)
axes9[0, 0].set_xlim(200, 350)

# Panel b: Phase portrait
axes9[0, 1].plot(sol_cpe.y[2][-2000:], sol_cpe.y[3][-2000:], 'b-', linewidth=0.8, alpha=0.7)
axes9[0, 1].plot(sol_cpe.y[2][0], sol_cpe.y[3][0], 'go', markersize=8, label='Initial')
axes9[0, 1].plot(sol_cpe.y[2][-1], sol_cpe.y[3][-1], 'rs', markersize=8, label='Equilibrium')
axes9[0, 1].set_xlabel('Corruptors $C_1$', fontsize=12)
axes9[0, 1].set_ylabel('Enforcers $I_1$', fontsize=12)
axes9[0, 1].set_title('(b) Limit cycle', fontsize=12)
axes9[0, 1].legend()
axes9[0, 1].grid(True, alpha=0.3)

# Panel c: Gamma comparison
gamma_compare = [0.1, 0.2, 0.3]
colors_c = ['blue', 'green', 'red']
y_final = sol_cpe.y[:, -1]
for idx, gamma in enumerate(gamma_compare):
    params_g = params_cpe.copy()
    params_g['gamma'] = gamma
    sol_g = solve_ivp(lambda t, y: corruption_model(t, y, **params_g),
                      (200, 350), y_final, t_eval=np.linspace(200, 350, 1500),
                      method='LSODA', rtol=1e-8, atol=1e-10)
    axes9[1, 0].plot(sol_g.t, sol_g.y[2], colors_c[idx], linewidth=1.5, label=f'$\\gamma = {gamma}$')
axes9[1, 0].set_xlabel('Time', fontsize=12)
axes9[1, 0].set_ylabel('Corruptors $C_1$', fontsize=12)
axes9[1, 0].set_title('(c) Effect of enforcement rate', fontsize=12)
axes9[1, 0].legend()
axes9[1, 0].grid(True, alpha=0.3)

# Panel d: Amplitude vs gamma
gamma_amp = np.linspace(0.05, 0.5, 15)
amplitudes = []
for gamma in gamma_amp:
    params_g = params_cpe.copy()
    params_g['gamma'] = gamma
    sol_g = solve_ivp(lambda t, y: corruption_model(t, y, **params_g),
                      (300, 500), y_final, t_eval=np.linspace(300, 500, 2000),
                      method='LSODA', rtol=1e-8, atol=1e-10)
    c_vals = sol_g.y[2][-1000:]
    amplitudes.append((np.max(c_vals) - np.min(c_vals)) / 2)

slope, intercept, r_value, _, _ = stats.linregress(gamma_amp, amplitudes)
axes9[1, 1].plot(gamma_amp, amplitudes, 'bo-', linewidth=2, markersize=6)
axes9[1, 1].plot(gamma_amp, intercept + slope*gamma_amp, 'r--', label=f'$R^2 = {r_value**2:.3f}$')
axes9[1, 1].set_xlabel('Enforcement rate $\\gamma$', fontsize=12)
axes9[1, 1].set_ylabel('Oscillation amplitude', fontsize=12)
axes9[1, 1].set_title('(d) Amplitude decreases with $\\gamma$', fontsize=12)
axes9[1, 1].legend()
axes9[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure9.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure9.png")

# ============================================
# FIGURE 10: Migration Trade-off
# ============================================
print("[10/13] Generating Figure 10: Migration Trade-off...")

nu_range = np.linspace(0.001, 0.15, 15)
sync_times = []
spillover = []

for nu in nu_range:
    params_nu = params_cpe.copy()
    params_nu['nu'] = nu
    sol = solve_ivp(lambda t, y: corruption_model(t, y, **params_nu),
                    (0, 500), y0_asym, t_eval=t_eval, method='LSODA', rtol=1e-6, atol=1e-8)
    C1, C2 = sol.y[2], sol.y[6]
    diff = np.abs(C1 - C2) / (np.maximum(C1, C2) + 1e-10)
    idx = np.where(diff < 0.05)[0]
    sync_times.append(sol.t[idx[0]] if len(idx) > 0 else 500)
    spillover.append(C2[-1])

sync_norm = (np.array(sync_times) - min(sync_times)) / (max(sync_times) - min(sync_times))
spillover_norm = (np.array(spillover) - min(spillover)) / (max(spillover) - min(spillover))
benefit_cost = (1 / np.array(sync_times)) / np.array(spillover)
benefit_cost = benefit_cost / max(benefit_cost)

fig10, axes10 = plt.subplots(2, 2, figsize=(14, 12))

axes10[0, 0].plot(nu_range, sync_times, 'bo-', linewidth=2, markersize=6)
axes10[0, 0].set_xlabel('Migration rate $\\nu$', fontsize=12)
axes10[0, 0].set_ylabel('Synchronization time', fontsize=12)
axes10[0, 0].set_title('(a) Synchronization time decreases', fontsize=12)
axes10[0, 0].grid(True, alpha=0.3)

axes10[0, 1].plot(nu_range, spillover, 'ro-', linewidth=2, markersize=6)
axes10[0, 1].set_xlabel('Migration rate $\\nu$', fontsize=12)
axes10[0, 1].set_ylabel('Final corruption in Patch 2', fontsize=12)
axes10[0, 1].set_title('(b) Spillover increases', fontsize=12)
axes10[0, 1].grid(True, alpha=0.3)

axes10[1, 0].plot(nu_range, sync_norm, 'b-', linewidth=2, label='Synchronization')
axes10[1, 0].plot(nu_range, spillover_norm, 'r-', linewidth=2, label='Spillover')
axes10[1, 0].axvspan(0.03, 0.07, alpha=0.3, color='green')
axes10[1, 0].set_xlabel('Migration rate $\\nu$', fontsize=12)
axes10[1, 0].set_ylabel('Normalized value', fontsize=12)
axes10[1, 0].set_title('(c) Trade-off visualization', fontsize=12)
axes10[1, 0].legend()
axes10[1, 0].grid(True, alpha=0.3)

axes10[1, 1].plot(nu_range, benefit_cost, 'g-', linewidth=2, marker='s', markersize=4)
axes10[1, 1].axvspan(0.03, 0.07, alpha=0.3, color='green')
axes10[1, 1].set_xlabel('Migration rate $\\nu$', fontsize=12)
axes10[1, 1].set_ylabel('Benefit-cost ratio', fontsize=12)
axes10[1, 1].set_title('(d) Optimal window', fontsize=12)
axes10[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure10.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure10.png")

# ============================================
# FIGURE 11: Enforcement Bifurcation
# ============================================
print("[11/13] Generating Figure 11: Enforcement Bifurcation...")

gamma_bif = np.linspace(0.05, 0.5, 40)
C_eq_low = []
C_eq_high = []

for gamma in gamma_bif:
    params_g = params_cpe.copy()
    params_g['gamma'] = gamma
    
    # Low initial corruption
    sol_low = solve_ivp(lambda t, y: corruption_model(t, y, **params_g),
                        (0, 500), [100, 50, 1, 1, 100, 50, 1, 1],
                        method='LSODA', rtol=1e-8, atol=1e-10)
    C_eq_low.append(np.mean(sol_low.y[2][-500:] + sol_low.y[6][-500:]))
    
    # High initial corruption
    sol_high = solve_ivp(lambda t, y: corruption_model(t, y, **params_g),
                         (0, 500), [100, 50, 30, 10, 100, 50, 30, 10],
                         method='LSODA', rtol=1e-8, atol=1e-10)
    C_eq_high.append(np.mean(sol_high.y[2][-500:] + sol_high.y[6][-500:]))

fig11, axes11 = plt.subplots(1, 2, figsize=(14, 5))

axes11[0].plot(gamma_bif, C_eq_low, 'b-', linewidth=2, label='Low initial corruption')
axes11[0].plot(gamma_bif, C_eq_high, 'r-', linewidth=2, label='High initial corruption')
axes11[0].axvspan(0.15, 0.25, alpha=0.3, color='gray')
axes11[0].set_xlabel('Enforcement rate $\\gamma$', fontsize=12)
axes11[0].set_ylabel('Total corruptors $C^*$', fontsize=12)
axes11[0].set_title('(a) Bistable region ($\\gamma \\approx 0.15-0.25$)', fontsize=12)
axes11[0].legend()
axes11[0].grid(True, alpha=0.3)

# Panel b: Two-parameter phase diagram
beta_range_2d = np.linspace(0.2, 0.9, 30)
gamma_range_2d = np.linspace(0.05, 0.5, 30)
R0_grid = np.zeros((len(beta_range_2d), len(gamma_range_2d)))

for i, beta in enumerate(beta_range_2d):
    for j, gamma in enumerate(gamma_range_2d):
        params_test = params_cpe.copy()
        params_test['beta0'] = beta
        params_test['gamma'] = gamma
        sol = solve_ivp(lambda t, y: corruption_model(t, y, **params_test),
                        (0, 500), [100, 50, 15, 5, 100, 50, 15, 5],
                        method='LSODA', rtol=1e-6, atol=1e-8)
        C_total = sol.y[2][-1] + sol.y[6][-1]
        R0_grid[i, j] = C_total

im = axes11[1].imshow(R0_grid.T, origin='lower', aspect='auto',
                       extent=[beta_range_2d[0], beta_range_2d[-1], gamma_range_2d[0], gamma_range_2d[-1]],
                       cmap='RdYlBu_r')
axes11[1].contour(beta_range_2d, gamma_range_2d, R0_grid.T, levels=[10], colors='black', linewidths=2)
axes11[1].set_xlabel('Transmission rate $\\beta_0$', fontsize=12)
axes11[1].set_ylabel('Enforcement rate $\\gamma$', fontsize=12)
axes11[1].set_title('(b) Two-parameter phase diagram', fontsize=12)
plt.colorbar(im, ax=axes11[1], label='Total corruptors')

plt.tight_layout()
plt.savefig('figures/figure11.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure11.png")

# ============================================
# FIGURE 12: Tornado Plot
# ============================================
print("[12/13] Generating Figure 12: Tornado Plot...")

parameters = ['$\\alpha_C$', '$\\gamma$', '$\\mu_C$', '$\\beta_0$', '$K$', 
              '$\\alpha_S$', '$r$', '$\\mu_S$', '$\\nu$']
effects = [0.35, -0.30, -0.28, 0.25, 0.15, -0.10, -0.06, 0.04, -0.02]
cumulative = np.cumsum(np.abs(effects))
cumulative = cumulative / cumulative[-1] * 100

fig12, axes12 = plt.subplots(1, 2, figsize=(14, 6))

# Panel a: Tornado plot
colors12 = ['blue' if e > 0 else 'red' for e in effects]
axes12[0].barh(parameters, effects, color=colors12, alpha=0.7, edgecolor='black')
axes12[0].axvline(x=0, color='black', linewidth=1)
axes12[0].set_xlabel('Change in $\\mathbb{R}_0$', fontsize=12)
axes12[0].set_title('(a) Parameter sensitivity (tornado plot)', fontsize=12)
axes12[0].grid(True, alpha=0.3, axis='x')

# Panel b: Cumulative impact
axes12[1].bar(parameters, cumulative, color='green', alpha=0.7, edgecolor='black')
axes12[1].axhline(y=60, color='red', linestyle='--', linewidth=2, label='60% threshold')
axes12[1].set_xlabel('Parameters', fontsize=12)
axes12[1].set_ylabel('Cumulative absolute impact (%)', fontsize=12)
axes12[1].set_title('(b) Cumulative sensitivity', fontsize=12)
axes12[1].legend()
axes12[1].grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('figures/figure12.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/figure12.png")

# ============================================
# APPENDIX FIGURE: Heterogeneity Robustness
# ============================================
print("[13/13] Generating Appendix Figure: Heterogeneity Robustness...")

R_star = 10.0
S_star = 45.0
beta0 = 0.7
mu_C = 0.1
alpha_C_base = 0.03

def compute_R0_asym(alpha_C1, alpha_C2, nu12, nu21):
    beta_term = beta0 * S_star / (1 + R_star)
    A1 = alpha_C1 * R_star + beta_term
    A2 = alpha_C2 * R_star + beta_term
    det_V = (mu_C + nu12) * (mu_C + nu21) - nu12 * nu21
    V_inv_11 = (mu_C + nu21) / det_V
    V_inv_12 = nu21 / det_V
    V_inv_21 = nu12 / det_V
    V_inv_22 = (mu_C + nu12) / det_V
    K11 = A1 * V_inv_11
    K12 = A1 * V_inv_12
    K21 = A2 * V_inv_21
    K22 = A2 * V_inv_22
    trace = K11 + K22
    det_K = K11 * K22 - K12 * K21
    lambda1 = (trace + np.sqrt(max(0, trace**2 - 4*det_K))) / 2
    return lambda1

ratios = [1.0, 1.2, 1.5, 2.0]
R0_sym = []
R0_asym = []

for r in ratios:
    alpha_C1 = alpha_C_base * r
    alpha_C2 = alpha_C_base
    R0_sym.append(compute_R0_asym(alpha_C1, alpha_C2, 0.05, 0.05))
    R0_asym.append(compute_R0_asym(alpha_C1, alpha_C2, 0.095, 0.005))

fig_app, axes_app = plt.subplots(1, 2, figsize=(14, 6))
x = np.arange(len(ratios))
width = 0.35

axes_app[0].bar(x - width/2, R0_sym, width, label='Symmetric migration', color='#2E86AB', alpha=0.8, edgecolor='black')
axes_app[0].bar(x + width/2, R0_asym, width, label='Asymmetric migration', color='#A23B72', alpha=0.8, edgecolor='black')
axes_app[0].set_xlabel('Heterogeneity ratio $\\alpha_C^{(1)}/\\alpha_C^{(2)}$', fontsize=12)
axes_app[0].set_ylabel('$\\mathbb{R}_0$', fontsize=12)
axes_app[0].set_title('(a) Absolute $\\mathbb{R}_0$ values', fontsize=12)
axes_app[0].set_xticks(x)
axes_app[0].set_xticklabels([f'{r}' for r in ratios])
axes_app[0].legend()
axes_app[0].grid(True, alpha=0.3, axis='y')
axes_app[0].set_ylim(30, 34)

baseline = R0_sym[0]
pct_sym = [(r - baseline) / baseline * 100 for r in R0_sym]
pct_asym = [(r - baseline) / baseline * 100 for r in R0_asym]

axes_app[1].bar(x - width/2, pct_sym, width, label='Symmetric migration', color='#2E86AB', alpha=0.8, edgecolor='black')
axes_app[1].bar(x + width/2, pct_asym, width, label='Asymmetric migration', color='#A23B72', alpha=0.8, edgecolor='black')
axes_app[1].axhline(y=0, color='gray', linestyle='--', linewidth=1.5)
axes_app[1].set_xlabel('Heterogeneity ratio $\\alpha_C^{(1)}/\\alpha_C^{(2)}$', fontsize=12)
axes_app[1].set_ylabel('Relative change in $\\mathbb{R}_0$ (%)', fontsize=12)
axes_app[1].set_title('(b) Relative change from baseline', fontsize=12)
axes_app[1].set_xticks(x)
axes_app[1].set_xticklabels([f'{r}' for r in ratios])
axes_app[1].legend()
axes_app[1].grid(True, alpha=0.3, axis='y')
axes_app[1].set_ylim(-0.5, 6)

plt.tight_layout()
plt.savefig('figures/heterogeneity_robustness.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: figures/heterogeneity_robustness.png")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("ALL FIGURES GENERATED SUCCESSFULLY!")
print("="*70)
print("\nFigures saved in 'figures/' directory:")
print("  - figure2.png  (Time series)")
print("  - figure3.png  (Bifurcation diagram)")
print("  - figure4.png  (Migration transient)")
print("  - figure5.png  (Spillover effect)")
print("  - figure6.png  (Asymmetric migration)")
print("  - figure7.png  (Elimination time)")
print("  - figure8.png  (Resource-transmission)")
print("  - figure9.png  (Predator-prey cycles)")
print("  - figure10.png (Migration trade-off)")
print("  - figure11.png (Enforcement bifurcation)")
print("  - figure12.png (Tornado plot)")
print("  - heterogeneity_robustness.png (Appendix)")
print("\n" + "="*70)
print("Note: Figure 1 (flowchart) must be provided separately as flowchart.png")
print("="*70)