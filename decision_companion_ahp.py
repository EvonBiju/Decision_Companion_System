import numpy as np

# Random Index values for Consistency Ratio
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}


# ---------- Utility Functions ---------- #

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


def sensitivity_analysis(criteria_weights, alt_weights_list, alternatives):
    print("\n================ SENSITIVITY ANALYSIS ================\n")

    # Original Score Calculation
    original_scores = np.zeros(len(alternatives))
    for i in range(len(criteria_weights)):
        original_scores += criteria_weights[i] * alt_weights_list[i]

    original_ranking = np.argsort(original_scores)[::-1]
    original_best = alternatives[original_ranking[0]]

    print(f"Original Best Alternative: {original_best}\n")

    # Increase each criterion weight by 10%
    for i in range(len(criteria_weights)):

        print(f"--- Testing Criterion: {i+1} ---")

        new_weights = criteria_weights.copy()
        new_weights[i] = new_weights[i] * 1.10

        # Normalize again
        new_weights = new_weights / np.sum(new_weights)

        new_scores = np.zeros(len(alternatives))

        for j in range(len(new_weights)):
            new_scores += new_weights[j] * alt_weights_list[j]

        new_ranking = np.argsort(new_scores)[::-1]
        new_best = alternatives[new_ranking[0]]

        print(f"New Best Alternative after +10% weight: {new_best}")

        if new_best == original_best:
            print("Result: Stable\n")
        else:
            print("Result: Changed (Sensitive Decision)\n")


# ---------------- MAIN PROGRAM ---------------- #

print("========== Decision Companion System (AHP CLI) ==========\n")

decision = input("What decision are you making? ")

# -------- Criteria Input -------- #

num_criteria = int(input("Number of criteria: "))

criteria = []
criteria_types = []

for i in range(num_criteria):
    name = input(f"Enter criterion {i+1}: ")

    while True:
        print("Type of criterion?")
        print("1. Benefit (Higher is better)")
        print("2. Cost (Lower is better)")
        choice = input("Enter 1 or 2: ")

        if choice == "1":
            ctype = "benefit"
            break
        elif choice == "2":
            ctype = "cost"
            break
        else:
            print("Invalid choice. Try again.")

    criteria.append(name)
    criteria_types.append(ctype)


# -------- Alternatives Input -------- #

num_alternatives = int(input("Number of alternatives: "))
alternatives = [input(f"Enter alternative {i+1}: ") for i in range(num_alternatives)]


# -------- Step 1: Criteria Matrix -------- #

criteria_matrix = np.ones((num_criteria, num_criteria))

print("\n=== Pairwise Comparison: Criteria ===")
print("Saaty Scale: 1, 3, 5, 7, 9 (Use decimals for less importance)\n")

for i in range(num_criteria):
    for j in range(i + 1, num_criteria):
        value = get_valid_number(
            f"How much is '{criteria[i]}' preferred over '{criteria[j]}'? "
        )
        criteria_matrix[i][j] = value
        criteria_matrix[j][i] = 1 / value

criteria_weights, lambda_max = calculate_weights(criteria_matrix)
criteria_cr = consistency_ratio(criteria_matrix, lambda_max)

print_matrix_info(criteria_weights, criteria_cr, criteria, "Criteria")


# -------- Step 2: Alternative Matrices -------- #

final_scores = np.zeros(num_alternatives)
alt_weights_list = []
detailed_scores = {}

for i in range(num_criteria):

    print(f"\n### Evaluating Alternatives for Criterion: {criteria[i]} ###")

    alt_matrix = np.ones((num_alternatives, num_alternatives))

    for r in range(num_alternatives):
        for c in range(r + 1, num_alternatives):

            value = get_valid_number(
                f"How much is '{alternatives[r]}' preferred over '{alternatives[c]}' "
                f"based on '{criteria[i]}'? "
            )

            # If COST criterion → invert automatically
            if criteria_types[i] == "cost":
                value = 1 / value

            alt_matrix[r][c] = value
            alt_matrix[c][r] = 1 / value

    alt_weights, alt_lambda = calculate_weights(alt_matrix)
    alt_cr = consistency_ratio(alt_matrix, alt_lambda)

    print_matrix_info(alt_weights, alt_cr, alternatives, criteria[i])

    alt_weights_list.append(alt_weights)

    contribution = criteria_weights[i] * alt_weights
    detailed_scores[criteria[i]] = contribution

    final_scores += contribution


# -------- Step 3: Final Results -------- #

print("\n================ FINAL RESULTS ================\n")

for alt, score in zip(alternatives, final_scores):
    print(f"{alt}: {score:.4f}")

ranking = np.argsort(final_scores)[::-1]

print("\nRanking (Best → Worst):")
for i in ranking:
    print(alternatives[i])

best_choice = alternatives[ranking[0]]
print(f"\nRecommended Decision: {best_choice}")


# -------- Step 4: Contribution Breakdown -------- #

print("\n--- Contribution Breakdown ---")

for i, criterion in enumerate(criteria):
    print(f"\nBased on {criterion}:")
    for alt, value in zip(alternatives, detailed_scores[criterion]):
        print(f"{alt} contributed {value:.4f}")


# -------- Step 5: Sensitivity Analysis -------- #

sensitivity_analysis(criteria_weights, alt_weights_list, alternatives)
