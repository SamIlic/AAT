# RUN TIME - ~ 2 min

import matplotlib.pyplot as plt 
import numpy as np
import pymc3
import scipy.stats as stats


plt.style.use("ggplot")

### Specify & Sample Model

# Set prior parameters
# Parameter values for prior and analytic posterior
n = 50 # number of coin flips
z = 10 # number of observed heads
alpha = 12 # beggining num heads
beta = 12 # beginning num tails
alpha_post = 22 # end num heads
beta_post = 52 # end num tails

# How many iterations of the Metropolis algorithm to carry out for MCMC 
iterations = 100000 # num iterations of Metropolis algo for MCMC

# define our beta distribution prior and Bernoulli likelihood model.
# 1) Firstly, we specify the theta parameter as a beta distribution, taking the prior alpha and beta values as parameters.
#       Remember that our particular values of α = 12 and β = 12 imply a prior mean μ = 0.5 and a prior s.d. σ = 0.1.
# 2) We then define the Bernoulli likelihood function, specifying the fairness parameter p=theta, the number of trials n=n and the observed heads observed=z
#       all taken from the parameters specified above.
# 3) At this stage we can find an optimal starting value for the Metropolis algorithm using the PyMC3 Maximum A Posteriori (MAP) optimisation, the details of which we will omit here.
# 4) Finally we specify the Metropolis sampler to be used and then actually sample(..) the results. These results are stored in the trace variable:

# Use PyMC3 to construct a model context
basic_model = pymc3.Model() # create a model and call it basic_model
with basic_model:
    # Define our prior belief about the fairness of the coin using a Beta distribution
    theta = pymc3.Beta("theta", alpha=alpha, beta=beta) # Define Beta distributio
    y = pymc3.Binomial("y", n=n, p=theta, observed=z) # Define the Bernoulli likelihood function

    # Carry out the MCMC analysis using the Metropolis algorithm
    # Use Maximum A Posteriori (MAP) optimisation as initial value for MCMC 
    start = pymc3.find_MAP()
    
    # Use the Metropolis algorithm (as opposed to NUTS or HMC, etc.)
    step = pymc3.Metropolis()
    # Calculate the trace (trace = list of all accepted samples)
    trace = pymc3.sample(
        iterations, step, start, random_seed=1, progressbar=True
    )



### Now that the model has been specified and sampled, we wish to plot the results.

# We create a posterior histogram from the trace of the MCMC sampling using 50 bins.
# Then, plot the analytic prior and posterior beta distributions using the SciPy stats.beta.pdf(..) method. 
# Finally, we add some labelling to the graph and display it:

# Plot the posterior histogram from MCMC analysis
bins=50
plt.hist(
    trace["theta"], bins,
    histtype="step", normed=True,
    label="Posterior (MCMC)", color="red"
)


# Plot the analytic prior and posterior beta distributions
x = np.linspace(0, 1, 100)
plt.plot( # Prior
    x, stats.beta.pdf(x, alpha, beta),
    "--", label="Prior", color="blue"
)
plt.plot( # Posterior
    x, stats.beta.pdf(x, alpha_post, beta_post),
    label='Posterior (Analytic)', color="green"
)
# Update the graph labels
plt.legend(title="Parameters", loc="best") 
plt.xlabel("$\\theta$, Fairness") 
plt.ylabel("Density")
plt.show()


# Show the trace plot
pymc3.traceplot(trace)
plt.show()














