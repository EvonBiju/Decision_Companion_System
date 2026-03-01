Weighted Sum Implementation
In this implementation, I used the weighted sum approach to combine multiple factors into a single aggregated score. The main idea behind a weighted sum is that not all inputs contribute equally to the final result — each component is assigned a weight based on its importance.
The formula used is:
 Final Score=∑( wi​ × xi​ ) 
where
    • xi​ represents each input value
    • wi​ represents the corresponding weight
The weights are carefully chosen to reflect the relative priority of each parameter. A higher weight increases the influence of that parameter on the final output. To maintain consistency and interpretability, the weights are normalized (their total equals 1), ensuring the final score remains within a predictable range.
This approach is simple, transparent, and computationally efficient. It works ,
    • The relationship between variables is linear
    • Each factor contributes independently
    • Interpret-ability is important
However, one limitation is that weighted sums do not capture complex interactions between variables. If interactions or nonlinear effects are significant, more advanced models may be required.
  
  Exploring Other Methods

1. TOPSIS

I read about TOPSIS (Technique for Order Preference by Similarity to Ideal Solution). I found it interesting because it compares options based on their distance from an ideal best and ideal worst solution. It feels more structured than a simple weighted sum.

2. AHP (Analytic Hierarchy Process)

I also looked into AHP, where weights are derived using pairwise comparisons instead of assigning them directly. I liked the idea that it provides a more systematic way of determining weights rather than choosing them manually.

3. Pareto Front

I briefly explored the concept of a Pareto Front in multi-objective optimization. The idea that some solutions are “non-dominated” and cannot be improved in one metric without worsening another was interesting.

Exploring TOPSIS, AHP, Pareto Front, and algorithm-based methods showed me that there are more rigorous ways to handle multi-criteria problems.


# BUILD PROCESS — Decision Compass (Hybrid AHP System)

> A day-by-day record of design decisions, algorithm research, and implementation evolution.

---

## Project Overview

**Decision Compass** is a hybrid Multi-Criteria Decision Making (MCDM) web system built on the Analytic Hierarchy Process (AHP). It is designed to be transparent, explainable, and usable by non-experts — not a black-box AI solution.

The system supports three evaluation modes (Objective, Subjective, Uncertain) and provides pairwise criteria weighting, consistency validation, contribution breakdown, and sensitivity analysis.

---

## 21 Feb 2026 — Initial Understanding

**Problem Statement Analysis**

The system must:
- Accept multiple alternatives and multiple criteria
- Support weighted importance across criteria
- Generate a ranked recommendation
- Clearly explain the reasoning at every step

> Core requirement: the system must be **explainable and transparent** — not a black-box.

This requirement pointed toward **Multi-Criteria Decision Making (MCDM)** as the problem domain.

---

## Research Phase — Algorithm Selection

Three candidate algorithms were studied before implementation began.

### 22 Feb 2026 — Weighted Sum Model (WSM)

Conceptually similar to a weighted bias algorithm in ML.

```
Score = Σ (weight × value)
```

**Rejected because:**
- Requires manually assigned weights with no derivation method
- No consistency validation on user inputs
- Too simplistic for decisions involving human reasoning and trade-offs

Used as a starting point to understand the fundamentals before moving on.

---

### 23 Feb 2026 — TOPSIS

TOPSIS ranks alternatives based on their geometric distance from the ideal best and ideal worst solutions.

**Strengths:**
- Mathematically rigorous
- Widely used in academic and industry settings

**Rejected because:**
- Weights must still be predefined externally — no derivation
- No validation of judgment consistency
- Less focused on modelling how humans actually reason about trade-offs

---

### 24 Feb 2026 — Final Choice: AHP

**AHP (Analytic Hierarchy Process)** was selected as the core algorithm.

**Reasons:**
- Derives criterion weights from pairwise comparisons — no manual weight assignment needed
- Models human reasoning through structured comparison
- Includes a built-in **Consistency Ratio (CR)** to validate judgment quality
- Makes the entire reasoning process visible and auditable

Unlike TOPSIS, AHP does not assume weights are known in advance — it calculates them logically from user judgments. This aligns directly with the transparency requirement.

A **hybrid extension** was also planned from the outset: combining AHP with objective data normalization and uncertainty modeling, to go beyond what a standard AHP implementation would offer.

---

## Implementation Evolution

### Version 1 — Core AHP (CLI)

**Stack:** Python + NumPy

**Features implemented:**
- CLI input for criteria, alternatives, and pairwise comparisons
- Pairwise matrix construction
- Eigenvector-based weight calculation
- Basic final score ranking

Also studied Git during this phase: `git init`, `add`, `commit`, `push`, `pull`.

---

### 25 Feb 2026 — Version 2: Improved AHP

**Enhancements:**
- Saaty scale guidance displayed to the user during input
- Input validation (positive numbers only, error handling)
- Consistency Ratio (CR) calculation and display
- Per-criterion weight breakdown
- Clear result explanation

---

### 26 Feb 2026 — Version 3: Sensitivity Analysis

**Motivation:** After implementing the improved AHP version, it became clear that real-world decisions are rarely static. Criteria importance can shift, and a small weight change can sometimes reverse the ranking.

**Implementation:**
1. Increase each criterion weight by ±10%
2. Recalculate all final scores with the adjusted weights
3. Compare new ranking against original
4. Flag if the top alternative changes

**This allows the system to:**
- Identify which criteria are dominant or decision-critical
- Detect unstable or fragile decisions
- Provide deeper insight beyond a simple ranking

**Discovery during testing (Job Selection use case):**  
While running a test case, it was found that *Package* (salary) and *Layoff Risk* had a complementary effect on scores. This led to research into **Benefit vs Cost criteria**.

**Benefit / Cost distinction added:**
- **Benefit** (higher = better): e.g. Salary, Growth, Learning opportunities
- **Cost** (lower = better): e.g. Layoff risk, Work pressure, Distance

Cost criteria values are automatically inverted before normalization, ensuring they are handled correctly without requiring users to think in reverse.

---

### 27 Feb 2026 — Version 4: Hybrid Objective + Subjective

**Motivation:** Testing the Job Selection scenario revealed a key usability problem. The pairwise matrix approach works for qualitative/subjective criteria, but is unnecessary and confusing when hard numeric data already exists.

**Example:**
- **Package (LPA)** — objective. Exact values exist (12 LPA, 10 LPA, 8 LPA). Pairwise comparison is redundant; direct normalization is more accurate and less burdensome.
- **Work Culture / Growth Opportunity** — subjective. No numeric measure exists. AHP pairwise comparison is the right tool here.

**Hybrid approach introduced:**

| Mode | When to use | How it works |
|------|------------|--------------|
| **Objective** | Real numeric data available | Enter raw values → auto-normalized |
| **Subjective** | Qualitative judgment needed | Pairwise comparison → AHP weights |

**Result:** The system became more efficient, more realistic, and less burdensome for users — while remaining mathematically sound for both types of criteria.

---

### 28 Feb 2026 — Version 5: Uncertain Mode (Mean–Variance)

**Motivation:** A further comparison revealed that classical AHP is not sufficient for all real-world scenarios.

| Job Selection | Investment Decision |
|---|---|
| Salary known | Returns uncertain |
| Layoff risk somewhat known | Risk highly dynamic |
| Culture subjective | Market sentiment unpredictable |
| Mostly stable | Highly volatile |

For scenarios involving **forecasted or estimated values with known risk**, a third evaluation mode was needed.

**Algorithm selected: Mean–Variance Model (Markowitz Portfolio Theory)**

This is the foundation of modern portfolio theory, used when comparing assets with return vs volatility trade-offs.

```
Adjusted Score = Mean − λ × Variance
```

Where **λ (lambda)** is the user's risk tolerance:
- `λ = 0` → Risk-neutral (only mean matters)
- `λ = 1` → Moderate risk-aversion (default)
- `λ > 2` → Strongly penalises high-variance options

If adjusted scores go negative, a `normalize_shift()` function shifts all values to positive before normalization.

**Other algorithms studied but not selected:** Expected Utility Theory, Monte Carlo Simulation, Fuzzy AHP.

---

### Web Application Build

**Stack:** FastAPI (Python backend) + Vanilla JS + HTML/CSS (single-file frontend)

**Key frontend UX decisions:**
- **Objective mode set as default** — most criteria have measurable values; subjective and uncertain are opt-in
- **Matrix input removed** — replaced with individual slider-based pairwise comparison cards. Each pair gets one question with a live-labeled slider (Equal → Moderate → Strong → Extreme), eliminating confusion from the raw matrix
- **Reference guide** built into the setup page with collapsible accordions explaining Benefit/Cost, all three modes, the Saaty scale, and risk tolerance

**API endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Serves frontend |
| `POST` | `/api/validate-criteria` | Validates criteria pairwise matrix, returns weights + CR |
| `POST` | `/api/calculate` | Full AHP calculation + sensitivity analysis |

**Deployment:** Vercel

---

## Project Structure

```
decision_companion/
├── Website/
│   ├── main.py              # FastAPI backend — AHP logic + API endpoints
│   ├── requirements.txt     # Python dependencies
│   └── static/
│       └── index.html       # Full frontend (single file)
└── BUILD_PROCESS.md         # This file
```

---

## Dependencies

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
numpy>=1.24.0
pydantic>=2.0.0
```

---

## Running Locally

```bash
cd Website
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
# Open http://localhost:8080
```

---

## Algorithm Summary

```
Input: Decision + Criteria (type + mode) + Alternatives

Step 1 — Criteria Weights
  → Pairwise comparison via sliders (AHP)
  → Eigenvector method → normalized weights
  → Consistency Ratio check (CR ≤ 0.10)

Step 2 — Alternative Scores per Criterion
  Objective  → normalize raw values (invert if cost)
  Subjective → pairwise comparison → AHP weights + CR check
  Uncertain  → adjusted = mean − λ × variance → normalize_shift()

Step 3 — Final Score
  Score(alt) = Σ criteria_weight[i] × alt_weight[i]

Step 4 — Sensitivity Analysis
  For each criterion: weight × 1.10 → re-rank → flag if best changes
```

---

## Key Design Principles

1. **Transparency over automation** — every weight, score, and contribution is shown
2. **Hybrid by design** — not pure AHP; combines objective normalization + subjective pairwise + uncertainty modeling
3. **User-first UX** — sliders replace matrices; objective is the default; reference guide is always accessible
4. **Consistency validation** — CR check prevents logically contradictory judgments from silently corrupting results
5. **Robustness check** — sensitivity analysis shows which criteria actually control the outcome
