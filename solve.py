import pandas as pd
import numpy as np
from scipy.optimize import minimize

def solve_parameters():
  
    try:
        data = pd.read_csv('xy_data.csv')
        x_data = data['x'].values
        y_data = data['y'].values
    except FileNotFoundError:
        print("Error: 'xy_data.csv' not found. Please upload the file.")
        return

    def objective_function(params):
        theta_rad, M, X = params

        x_prime = x_data - X
        y_prime = y_data - 42.0
        
        cos_theta = np.cos(theta_rad)
        sin_theta = np.sin(theta_rad)

        t_calc = x_prime * cos_theta + y_prime * sin_theta

        v_calc = -x_prime * sin_theta + y_prime * cos_theta

        v_expected = np.exp(M * np.abs(t_calc)) * np.sin(0.3 * t_calc)

        error = np.sum((v_calc - v_expected)**2)

        t_below_penalty = np.sum(np.maximum(0, 6.0 - t_calc)**2)
        t_above_penalty = np.sum(np.maximum(0, t_calc - 60.0)**2)

        t_range_penalty = 1e6 * (t_below_penalty + t_above_penalty)
        
        return error + t_range_penalty


    theta_min_rad = np.deg2rad(0.0) + 1e-6  
    theta_max_rad = np.deg2rad(50.0) - 1e-6 
    
    bounds = [
        (theta_min_rad, theta_max_rad), 
        (-0.05 + 1e-6, 0.05 - 1e-6),    
        (0.0 + 1e-6, 100.0 - 1e-6)      
    ]

    initial_guess = [np.deg2rad(25), 0.0, 50.0]
    
    print("🚀 Starting optimization...")

    result = minimize(
        objective_function,
        initial_guess,
        method='L-BFGS-B',
        bounds=bounds,
        options={'disp': True, 'ftol': 1e-15} 
    )

    if result.success:
        theta_rad_opt, M_opt, X_opt = result.x
        theta_deg_opt = np.rad2deg(theta_rad_opt)
        
        print("\n✅ Optimization Successful!")
        print("-----------------------------------")
        print(f"  Final Error (L2): {result.fun: .2e}")
        print("-----------------------------------")
        print("🎉 Found Parameters:")
        print(f"  theta (deg): {theta_deg_opt: .6f}")
        print(f"  theta (rad): {theta_rad_opt: .6f}")
        print(f"  M:           {M_opt: .6f}")
        print(f"  X:           {X_opt: .6f}")
        print("-----------------------------------")

        x_prime = x_data - X_opt
        y_prime = y_data - 42.0
        cos_theta = np.cos(theta_rad_opt)
        sin_theta = np.sin(theta_rad_opt)
        t_final = x_prime * cos_theta + y_prime * sin_theta
        
        print("Constraint Check:")
        print(f"  Min 't' calculated: {np.min(t_final):.2f} (Constraint: > 6)")
        print(f"  Max 't' calculated: {np.max(t_final):.2f} (Constraint: < 60)")

    else:
        print("\n❌ Optimization failed to converge.")
        print(result.message)

solve_parameters()
