# Parametric-curve-solver

This repository contains the solution and code for finding the unknown variables in a given parametric equation based on a set of `(x, y)` data points.

## Final Equation 

Here is the final parametric equation in the required LaTeX format:

x = (t * cos(0.523598) - exp(0.03 * abs(t)) * sin(0.3 * t) * sin(0.523598) + 55.0) y = (42 + t * sin(0.523598) + exp(0.03 * abs(t)) * sin(0.3 * t) * cos(0.523598))

\left(t*\cos(0.523598)-e^{0.03\left|t\right|}\cdot\sin(0.3t)\sin(0.523598)\ +55.0, 42+\ t*\sin(0.523598)+e^{0.03\left|t\right|}\cdot\sin(0.3t)\cos(0.523598)\right)

### Discovered Parameters

* **$\theta$**: $30^\circ$ (or $0.523598$ radians)
* **$M$**: $0.03$
* **$X$**: $55.0$

---

## Solution Process and Explanation

Here is a step-by-step breakdown of the process followed to find these parameters.

### 1. Analyze the Equations (The Key Insight)

First, I analyzed the structure of the parametric equations:
$$x(t) = t \cdot \cos(\theta) - e^{M|t|} \cdot \sin(0.3t) \cdot \sin(\theta) + X$$
$$y(t) = 42 + t \cdot \sin(\theta) + e^{M|t|} \cdot \sin(0.3t) \cdot \cos(\theta)$$

The primary challenge is that we have $(x, y)$ data points but don't know the corresponding parameter $t$ for each point.

The key insight comes from recognizing this as a **geometric transformation**. If we define a new variable $v = e^{M|t|} \cdot \sin(0.3t)$ and "un-translate" the coordinates by $X$ and $42$, we get:

* $x' = x - X = t \cdot \cos(\theta) - v \cdot \sin(\theta)$
* $y' = y - 42 = t \cdot \sin(\theta) + v \cdot \cos(\theta)$

This is the standard formula for **rotating** a point $(t, v)$ by an angle $\theta$.

### 2. Apply the Inverse Transformation

Since we have the rotated coordinates $(x', y')$ from the data, we can apply the **inverse rotation** (by angle $-\theta$) to find the *original* coordinates $(t, v)$:

* $t_{\text{calc}} = x' \cos(\theta) + y' \sin(\theta)$
* $v_{\text{calc}} = -x' \sin(\theta) + y' \cos(\theta)$

By substituting $x' = x - X$ and $y' = y - 42$, we get equations for $t$ and $v$ based *only* on the data and our unknown parameters:

* $t_{\text{calc}} = (x - X) \cos(\theta) + (y - 42) \sin(\theta)$
* $v_{\text{calc}} = -(x - X) \sin(\theta) + (y - 42) \cos(\theta)$

### 3. Formulate the Optimization Problem

Now we have two separate relationships that must be consistent. We have $v_{\text{calc}}$ (calculated from the data) and the "expected" value of $v$ from its definition, $v_{\text{expected}} = e^{M|t_{\text{calc}}|} \cdot \sin(0.3 t_{\text{calc}})$.

For the correct parameters, these two must be equal:
$v_{\text{calc}} = v_{\text{expected}}$

This allows us to define an **error (or loss) function** to minimize. We want to find the parameters $(\theta, M, X)$ that make the squared difference between these two values as close to zero as possible for all data points:

$$Loss = \sum_{i} \left( v_{\text{calc}, i} - v_{\text{expected}, i} \right)^2$$

### 4. Define Constraints and Solve

I then used a numerical optimization algorithm (`scipy.optimize.minimize` with the `L-BFGS-B` method) to find the parameters $(\theta, M, X)$ that minimize this loss function.

I applied the following constraints as bounds for the optimizer, as given in the problem:
1.  **$\theta$:** $0 < \theta < 50^\circ$ (converted to $0 < \theta_{\text{rad}} < 0.8727$)
2.  **$M$:** $-0.05 < M < 0.05$
3.  **$X$:** $0 < X < 100$

I also added a strong penalty to the loss function if any calculated $t_{\text{calc}}$ values fell outside the given range of $6 < t < 60$.

### 5. The Result

The optimization algorithm successfully converged to a near-zero error (`1.87e-08`), giving the final parameters:
* **$\theta$:** $0.523598...$ radians, which is **$30^\circ$**
* **$M$:** **$0.03$**
* **$X$:** **$55.0$**

All three values are well within their specified ranges. The calculated $t$ values for the provided data points also fell perfectly within the $6 < t < 60$ range (from $6.05$ to $60.00$), confirming the solution's validity.

---

## Code

The `solve.py` file contains the Python script used to perform this optimization.

### Dependencies

* Python 3.x
* pandas
* numpy
* scipy

You can install the dependencies using pip:
```sh
pip install pandas numpy scipy
