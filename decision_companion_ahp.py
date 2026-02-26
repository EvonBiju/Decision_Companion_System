import numpy as np
def sensitivity_analysis(criteria_weights, detailed_scores, alternatives):
    print("\n================ SENSITIVITY ANALYSIS ================\n")

    original_scores = np.zeros(len(alternatives))

    # Calculate original scores again
    for criterion in detailed_scores:
        original_scores += detailed_scores[criterion]

    original_ranking = np.argsort(original_scores)[::-1]
    original_best = alternatives[original_ranking[0]]

    print(f"Original Best Alternative: {original_best}\n")

    for i in range(len(criteria_weights)):

        print(f"--- Testing Sensitivity for Criterion {i+1} ---")

        # Copy weights
        new_weights = criteria_weights.copy()

        # Increase weight by 10%
        new_weights[i] = new_weights[i] * 1.10

        # Normalize weights again
        new_weights = new_weights / np.sum(new_weights)

        # Recalculate final scores
        new_scores = np.zeros(len(alternatives))

        for j, criterion in enumerate(detailed_scores):
            # Recalculate contribution using adjusted weight
            alt_weights = detailed_scores[criterion] / criteria_weights[j]
            contribution = new_weights[j] * alt_weights
            new_scores += contribution

        new_ranking = np.argsort(new_scores)[::-1]
        new_best = alternatives[new_ranking[0]]

        print(f"New Best Alternative after +10% change: {new_best}")

        if new_best == original_best:
            print("Result: Stable (No change in top alternative)\n")
        else:
            print("Result: Changed (Decision is sensitive!)\n")
            
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}


def get_valid_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Value must be positive.")
                continue
            return value
        except:
            print("Invalid input. Enter a numeric value.")


def build_matrix(items, title):
    n = len(items)
    matrix = np.ones((n, n))

    print(f"\n=== Pairwise Comparison: {title} ===")
    print("Saaty Scale Guide:")
    print("1 = Equal importance")
    print("3 = Moderate importance")
    print("5 = Strong importance")
    print("7 = Very strong importance")
    print("9 = Extreme importance")
    print("Use decimals (e.g., 0.33) for less importance.\n")

    for i in range(n):
        for j in range(i + 1, n):
            value = get_valid_number(
                f"How much is '{items[i]}' preferred over '{items[j]}'? "
            )
            matrix[i][j] = value
            matrix[j][i] = 1 / value

    return matrix


def calculate_weights(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_index = np.argmax(eigenvalues.real)
    lambda_max = eigenvalues.real[max_index]
    weights = eigenvectors[:, max_index].real
    weights = weights / np.sum(weights)
    return weights, lambda_max


def consistency_ratio(matrix, lambda_max):
    n = matrix.shape[0]
    if n < 3:
        return 0

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]
    return CR


def print_matrix_info(weights, cr, items, title):
    print(f"\n--- {title} Weights ---")
    for item, weight in zip(items, weights):
        print(f"{item}: {weight:.4f}")

    print(f"Consistency Ratio (CR): {cr:.4f}")
    if cr <= 0.1:
        print("Consistency Status: Acceptable")
    else:
        print("Consistency Status: WARNING (Judgments may be inconsistent)")


# ---------------- MAIN PROGRAM ---------------- #

print("========== Decision Companion System (AHP CLI) ==========\n")

decision = input("What decision are you making? ")

num_criteria = int(input("Number of criteria: "))
criteria = [input(f"Enter criterion {i+1}: ") for i in range(num_criteria)]

num_alternatives = int(input("Number of alternatives: "))
alternatives = [input(f"Enter alternative {i+1}: ") for i in range(num_alternatives)]

# Step 1: Criteria Matrix
criteria_matrix = build_matrix(criteria, "Criteria")
criteria_weights, lambda_max = calculate_weights(criteria_matrix)
criteria_cr = consistency_ratio(criteria_matrix, lambda_max)

print_matrix_info(criteria_weights, criteria_cr, criteria, "Criteria")

# Step 2: Alternative Matrices
final_scores = np.zeros(num_alternatives)
detailed_scores = {}

for i in range(num_criteria):
    print(f"\n### Evaluating Alternatives for Criterion: {criteria[i]} ###")

    alt_matrix = build_matrix(alternatives, criteria[i])
    alt_weights, alt_lambda = calculate_weights(alt_matrix)
    alt_cr = consistency_ratio(alt_matrix, alt_lambda)

    print_matrix_info(alt_weights, alt_cr, alternatives, criteria[i])

    contribution = criteria_weights[i] * alt_weights
    detailed_scores[criteria[i]] = contribution

    final_scores += contribution

# Step 3: Final Results
print("\n================ FINAL RESULTS ================\n")

print("Final Scores (Global Priorities):")
for alt, score in zip(alternatives, final_scores):
    print(f"{alt}: {score:.4f}")

ranking = np.argsort(final_scores)[::-1]

print("\nRanking (Best → Worst):")
for i in ranking:
    print(alternatives[i])

best_choice = alternatives[ranking[0]]
print(f"\nRecommended Decision: {best_choice}")

# Step 4: Explanation Breakdown
print("\n--- Contribution Breakdown ---")
for criterion in criteria:
    print(f"\nBased on {criterion}:")
    for alt, value in zip(alternatives, detailed_scores[criterion]):
        print(f"{alt} contributed {value:.4f}")
        
# Step 5: Sensitivity Analysis
sensitivity_analysis(criteria_weights, detailed_scores, alternatives)



