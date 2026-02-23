from typing import List


class Criterion:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def normalize(self, total_weight: float):
        if total_weight == 0:
            raise ValueError("Total weight cannot be zero.")
        self.weight = self.weight / total_weight


class Option:
    def __init__(self, name: str):
        self.name = name
        self.scores = {}  # {criterion_name: score}

    def add_score(self, criterion_name: str, score: float):
        self.scores[criterion_name] = score


class DecisionEngine:
    def __init__(self, criteria: List[Criterion], options: List[Option]):
        self.criteria = criteria
        self.options = options

    def normalize_weights(self):
        total_weight = sum(c.weight for c in self.criteria)
        for criterion in self.criteria:
            criterion.normalize(total_weight)

    def evaluate(self):
        self.normalize_weights()
        results = []

        for option in self.options:
            total_score = 0
            breakdown = {}

            for criterion in self.criteria:
                score = option.scores.get(criterion.name, 0)
                weighted_score = score * criterion.weight
                breakdown[criterion.name] = weighted_score
                total_score += weighted_score

            results.append({
                "option": option,
                "total_score": total_score,
                "breakdown": breakdown
            })

        results.sort(key=lambda x: x["total_score"], reverse=True)
        return results

    def explain(self, results):
        winner = results[0]
        print("\n🏆 Recommended Option:", winner["option"].name)
        print("Total Score:", round(winner["total_score"], 3))

        print("\nContribution Breakdown:")
        for criterion, value in winner["breakdown"].items():
            print(f"  {criterion}: {round(value, 3)}")

        strongest = max(winner["breakdown"], key=winner["breakdown"].get)
        print(f"\nReason: '{strongest}' contributed the most to this decision.")


class CLI:
    def run(self):
        print("=== Decision Companion System (OOP Version) ===\n")

        criteria = self._input_criteria()
        options = self._input_options(criteria)

        engine = DecisionEngine(criteria, options)
        results = engine.evaluate()

        self._display_ranking(results)
        engine.explain(results)

    def _input_criteria(self) -> List[Criterion]:
        num = int(input("How many criteria? "))
        criteria = []

        for _ in range(num):
            name = input("Criterion name: ")
            weight = float(input("Weight (importance value): "))
            criteria.append(Criterion(name, weight))

        return criteria

    def _input_options(self, criteria: List[Criterion]) -> List[Option]:
        num = int(input("\nHow many options? "))
        options = []

        for _ in range(num):
            name = input("\nOption name: ")
            option = Option(name)

            for criterion in criteria:
                score = float(input(f"Score for {criterion.name} (0-10): "))
                option.add_score(criterion.name, score)

            options.append(option)

        return options

    def _display_ranking(self, results):
        print("\n=== Ranking ===")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['option'].name} — Score: {round(result['total_score'], 3)}")


if __name__ == "__main__":
    CLI().run()
