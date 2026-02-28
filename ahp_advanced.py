import numpy as np

# Random Index values
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

# ---------------- Utility Functions ---------------- #

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
    return CI / RI[n]


def normalize_objective(values, criterion_type):
    values = np.array(values)

    if criterion_type == "benefit":
        normalized = values / np.sum(values)
    else:
        inverted = 1 / values
        normalized = inverted / np.sum(inverted)

    return normalized


def normalize_shift(values):
    """
    Used for uncertain criteria in case adjusted values become negative.
    Shifts them to positive before normalization.
    """
    values = np.array(values)
    min_val = np.min(values)

    if min_val <= 0:
        values = values - min_val + 0.0001

    return values / np.sum(values)


def sensitivity_analysis(criteria_weights, alt_weights_list, alternatives):
    print("\n=========== Sensitivity Analysis ===========\n")

    original_scores = np.zeros(len(alternatives))
    for i in range(len(criteria_weights)):
        original_scores += criteria_weights[i] * alt_weights_list[i]

    original_best = alternatives[np.argmax(original_scores)]
    print("Original Best:", original_best, "\n")

    for i in range(len(criteria_weights)):

        new_weights = criteria_weights.copy()
        new_weights[i] *= 1.10
        new_weights = new_weights / np.sum(new_weights)

        new_scores = np.zeros(len(alternatives))
        for j in range(len(new_weights)):
            new_scores += new_weights[j] * alt_weights_list[j]

        new_best = alternatives[np.argmax(new_scores)]

        print(f"If Criterion {i+1} weight increases by 10% → Best = {new_best}")

        if new_best == original_best:
            print("Stable\n")
        else:
            print("Changed (Sensitive)\n")


# ---------------- MAIN PROGRAM ---------------- #

print("========== Hybrid AHP Decision System ==========\n")

decision = input("What decision are you making? ")

# -------- Criteria -------- #

num_criteria = int(input("Number of criteria: "))

criteria = []
criteria_types = []
criteria_modes = []

for i in range(num_criteria):

    name = input(f"\nEnter criterion {i+1}: ")

    # Benefit / Cost
    while True:
        print("Type?")
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
            print("Invalid input.")

    # Mode
    while True:
        print("Mode?")
        print("1. Objective")
        print("2. Subjective (Pairwise)")
        print("3. Uncertain (Mean–Variance)")
        mode_choice = input("Enter 1, 2 or 3: ")
        if mode_choice == "1":
            mode = "objective"
            break
        elif mode_choice == "2":
            mode = "subjective"
            break
        elif mode_choice == "3":
            mode = "uncertain"
            break
        else:
            print("Invalid input.")

    criteria.append(name)
    criteria_types.append(ctype)
    criteria_modes.append(mode)

# -------- Alternatives -------- #

num_alternatives = int(input("\nNumber of alternatives: "))
alternatives = [input(f"Enter alternative {i+1}: ") for i in range(num_alternatives)]

# -------- Criteria Weights (AHP) -------- #

criteria_matrix = np.ones((num_criteria, num_criteria))

print("\n=== Pairwise Comparison: Criteria Importance ===")

for i in range(num_criteria):
    for j in range(i + 1, num_criteria):
        value = get_valid_number(
            f"How much is '{criteria[i]}' preferred over '{criteria[j]}'? "
        )
        criteria_matrix[i][j] = value
        criteria_matrix[j][i] = 1 / value

criteria_weights, lambda_max = calculate_weights(criteria_matrix)
cr = consistency_ratio(criteria_matrix, lambda_max)

print("\nCriteria Weights:")
for c, w in zip(criteria, criteria_weights):
    print(c, ":", round(w, 4))
print("Consistency Ratio:", round(cr, 4))

# -------- Alternative Evaluation -------- #

alt_weights_list = []
final_scores = np.zeros(num_alternatives)

for i in range(num_criteria):

    print(f"\n### Evaluating Alternatives for: {criteria[i]} ###")

    # ---------- OBJECTIVE ----------
    if criteria_modes[i] == "objective":

        values = []
        for alt in alternatives:
            v = get_valid_number(
                f"Enter value of '{alt}' for '{criteria[i]}': "
            )
            values.append(v)

        alt_weights = normalize_objective(values, criteria_types[i])

    # ---------- SUBJECTIVE ----------
    elif criteria_modes[i] == "subjective":

        alt_matrix = np.ones((num_alternatives, num_alternatives))

        for r in range(num_alternatives):
            for c in range(r + 1, num_alternatives):

                value = get_valid_number(
                    f"How much is '{alternatives[r]}' preferred over '{alternatives[c]}' "
                    f"based on '{criteria[i]}'? "
                )

                if criteria_types[i] == "cost":
                    value = 1 / value

                alt_matrix[r][c] = value
                alt_matrix[c][r] = 1 / value

        alt_weights, alt_lambda = calculate_weights(alt_matrix)
        alt_cr = consistency_ratio(alt_matrix, alt_lambda)

        print("Consistency Ratio:", round(alt_cr, 4))

    # ---------- UNCERTAIN ----------
    else:

        means = []
        variances = []

        print("\nEnter Expected Value and Variance for each alternative:\n")

        for alt in alternatives:
            mean = get_valid_number(f"Expected value for '{alt}': ")
            var = get_valid_number(f"Variance (risk) for '{alt}': ")
            means.append(mean)
            variances.append(var)

        risk_factor = get_valid_number("\nEnter your risk tolerance (λ): ")

        adjusted_scores = []
        print("\nRisk Adjusted Calculations:")

        for alt, m, v in zip(alternatives, means, variances):
            adjusted = m - (risk_factor * v)
            adjusted_scores.append(adjusted)
            print(f"{alt}: {m} - ({risk_factor} × {v}) = {round(adjusted,4)}")

        alt_weights = normalize_shift(adjusted_scores)

    alt_weights_list.append(alt_weights)
    final_scores += criteria_weights[i] * alt_weights

# -------- Final Results -------- #

print("\n=========== FINAL RESULTS ===========\n")

for alt, score in zip(alternatives, final_scores):
    print(alt, ":", round(score, 4))

ranking = np.argsort(final_scores)[::-1]

print("\nRanking (Best → Worst):")
for i in ranking:
    print(alternatives[i])

print("\nRecommended Decision:", alternatives[ranking[0]])

# -------- Sensitivity -------- #

sensitivity_analysis(criteria_weights, alt_weights_list, alternatives)
