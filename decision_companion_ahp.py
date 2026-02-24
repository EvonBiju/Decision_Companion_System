import numpy as np

# Random Index values
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

# Function to build pairwise comparison matrix
def build_matrix(items, title):
    n = len(items)
    matrix = np.ones((n, n))

    print("\nPairwise comparison for", title)
    print("Use scale 1-9 (if less important, use decimal like 0.33)\n")

    for i in range(n):
        for j in range(i + 1, n):
            value = float(input(f"How much is '{items[i]}' preferred over '{items[j]}'? "))
            matrix[i][j] = value
            matrix[j][i] = 1 / value

    return matrix


# Function to calculate weights using eigenvector method
def calculate_weights(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_index = np.argmax(eigenvalues.real)
    max_eigenvalue = eigenvalues.real[max_index]
    weights = eigenvectors[:, max_index].real
    weights = weights / sum(weights)
    return weights, max_eigenvalue


# Function to calculate consistency ratio
def consistency_ratio(matrix, lambda_max):
    n = matrix.shape[0]
    if n < 3:
        return 0

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]
    return CR


#MAIN PROGRAM#

print("=== Decision Companion System (AHP - CLI) ===\n")

decision = input("What decision are you making? ")

num_criteria = int(input("Number of criteria: "))
criteria = []

for i in range(num_criteria):
    criteria.append(input(f"Enter criterion {i+1}: "))

num_alternatives = int(input("Number of alternatives: "))
alternatives = []

for i in range(num_alternatives):
    alternatives.append(input(f"Enter alternative {i+1}: "))

# Build criteria matrix
criteria_matrix = build_matrix(criteria, "Criteria")

criteria_weights, lambda_max = calculate_weights(criteria_matrix)
cr = consistency_ratio(criteria_matrix, lambda_max)

if cr > 0.1:
    print("\nWarning: Criteria matrix may be inconsistent (CR =", round(cr, 3), ")")

# Build alternative matrices
final_scores = np.zeros(num_alternatives)

for i in range(num_criteria):
    print(f"\n--- Evaluating alternatives based on '{criteria[i]}' ---")
    alt_matrix = build_matrix(alternatives, criteria[i])

    alt_weights, alt_lambda = calculate_weights(alt_matrix)
    alt_cr = consistency_ratio(alt_matrix, alt_lambda)

    if alt_cr > 0.1:
        print("Warning: Inconsistency detected (CR =", round(alt_cr, 3), ")")

    final_scores += criteria_weights[i] * alt_weights

# Print Results
print("\n====== RESULTS ======\n")

print("Criteria Weights:")
for i in range(num_criteria):
    print(criteria[i], ":", round(criteria_weights[i], 4))

print("\nFinal Scores:")
for i in range(num_alternatives):
    print(alternatives[i], ":", round(final_scores[i], 4))

# Ranking
ranking = np.argsort(final_scores)[::-1]

print("\nRanking (Best to Worst):")
for i in ranking:
    print(alternatives[i])

print("\nBest Choice:", alternatives[ranking[0]])
