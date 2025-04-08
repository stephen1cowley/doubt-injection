import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def prob_beta1_greater_beta2(alpha1, beta1, alpha2, beta2, num_samples=1000000):
    """
    Calculate the probability that a random sample from Beta(alpha1, beta1)
    is greater than a random sample from Beta(alpha2, beta2).
    
    Parameters:
    -----------
    alpha1, beta1: Parameters of the first Beta distribution
    alpha2, beta2: Parameters of the second Beta distribution
    num_samples: Number of Monte Carlo samples to use
    
    Returns:
    --------
    float: Probability that Beta1 > Beta2
    """
    # Generate random samples from both distributions
    samples1 = np.random.beta(alpha1, beta1, num_samples)
    samples2 = np.random.beta(alpha2, beta2, num_samples)
    
    # Calculate the proportion of times samples1 > samples2
    prob = np.mean(samples1 > samples2)
    
    return prob


def plot_beta_distributions(alpha1, beta1, alpha2, beta2):
    """
    Plot two Beta distributions for visual comparison.
    """
    x = np.linspace(0, 1, 1000)
    y1 = stats.beta.pdf(x, alpha1, beta1)
    y2 = stats.beta.pdf(x, alpha2, beta2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, 'b-', lw=2, label=f'Beta({alpha1}, {beta1})')
    plt.plot(x, y2, 'r-', lw=2, label=f'Beta({alpha2}, {beta2})')
    plt.fill_between(x, y1, color='blue', alpha=0.2)
    plt.fill_between(x, y2, color='red', alpha=0.2)
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Comparison of Beta Distributions')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


# Example usage
if __name__ == "__main__":
    # Example parameters for two Beta distributions
    # These could represent accuracy distributions for two LLM settings
    alpha1, beta1 = 2, 4  # First setting: 80 correct answers, 20 incorrect
    alpha2, beta2 = 4, 2  # Second setting: 75 correct answers, 25 incorrect
    
    # Calculate probability that the first setting is better
    prob = prob_beta1_greater_beta2(alpha1, beta1, alpha2, beta2)
    print(f"Probability that Beta({alpha1}, {beta1}) > Beta({alpha2}, {beta2}): {prob:.4f}")
    
    # Visualize the distributions
    plot_beta_distributions(alpha1, beta1, alpha2, beta2)
    
    # You can also calculate the expected values for reference
    expected1 = alpha1 / (alpha1 + beta1)
    expected2 = alpha2 / (alpha2 + beta2)
    print(f"Expected value of Beta({alpha1}, {beta1}): {expected1:.4f}")
    print(f"Expected value of Beta({alpha2}, {beta2}): {expected2:.4f}")
