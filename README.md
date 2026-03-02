
# Hybrid AHP Decision Companion System  
An Explainable Multi-Criteria Decision Support Framework

---

## 🌐 Live Application

🔗 **Live App:**  
[https://ahp-app-gamma.vercel.app/](https://ahp-app-gamma.vercel.app/)

📂 **GitHub Repository:**  
[https://github.com/EvonBiju/Decision_Companion_System](https://github.com/EvonBiju/Decision_Companion_System)

---

## 1. Introduction

Decision-making in real-world scenarios often involves multiple criteria, uncertainty, and subjective judgment. Traditional weighted scoring methods fail to address:

- Inconsistency in human judgment
- Risk and uncertainty
- Benefit vs cost factors
- Sensitivity to weight changes

This project implements a **Hybrid Analytical Hierarchy Process (AHP) Decision System** that integrates:

- Objective numeric evaluation  
- Subjective pairwise comparison  
- Risk-adjusted scoring (Mean–Variance model)  
- Sensitivity analysis  
- CLI + Web Interface  

The system is fully explainable and mathematically grounded.

---

## 2. Problem Statement

Complex decisions such as:

- Job selection  
- Startup evaluation  
- Investment analysis  
- Project prioritization  
- Supplier selection  

involve:

- Multiple criteria
- Benefit and cost factors
- Subjective importance judgments
- Uncertain outcomes
- Risk tolerance differences

Basic weighted sum models:
- Ignore consistency validation
- Do not handle uncertainty
- Cannot personalize risk preference

This project builds a **Unified Hybrid Decision Framework** that:

1. Handles objective and subjective criteria.
2. Supports benefit and cost normalization.
3. Incorporates uncertainty using Mean–Variance risk adjustment.
4. Performs sensitivity analysis for robustness.
5. Provides full explainability of each calculation.

---

## 3. Algorithms Used

### 3.1 Analytical Hierarchy Process (AHP)

Used for:
- Criteria weight determination
- Subjective alternative comparison
- Consistency validation

Mathematical basis:
A w = λmax w

Consistency Index:
CI = (λmax − n) / (n − 1)

Consistency Ratio:
CR = CI / RI

Acceptable if CR < 0.1

---

### 3.2 Weighted Sum Model (WSM)

Final aggregation:

Score_j = Σ (w_i × v_ij)

Where:
- w_i = criterion weight
- v_ij = alternative score

---

### 3.3 Benefit / Cost Normalization

Benefit:
Value / Sum(Value)

Cost:
(1 / Value) / Sum(1 / Value)

---

### 3.4 Mean–Variance Risk Model

Used for uncertain criteria.

Adjusted Score:

Adjusted = Mean − (λ × Variance)

Where:
- Mean = Expected value
- Variance = Risk
- λ = User-defined risk tolerance

Allows:
- Risk-averse behavior
- Risk-neutral behavior
- Personalized decisions

---

### 3.5 Sensitivity Analysis

Each criterion weight is increased by 10%.

If ranking remains same → Stable  
If ranking changes → Sensitive  

Ensures robustness of decision.

---

## 4. Methodology

Step 1 – Define Decision  
Step 2 – Define Criteria (Benefit/Cost + Mode)  
Step 3 – Compute Criteria Weights using AHP  
Step 4 – Evaluate Alternatives:

- Objective → Direct normalization  
- Subjective → Pairwise comparison  
- Uncertain → Risk-adjusted Mean–Variance  

Step 5 – Aggregate final scores  
Step 6 – Perform Sensitivity Analysis  

---

## 🏗 Repository Structure

```

Decision_Companion_System/
│
├── ahp_advanced.py              # CLI version (Hybrid AHP + Risk)
├── decision_companion.py
├── decision_companion_ahp.py
│
├── Website/                     # FastAPI Web Application
│   ├── main.py                  # FastAPI backend
│   ├── requirements.txt
│   └── static/
│       └── index.html
│
├── BUILD_PROCESS.md
├── RESEARCH_LOG.md
├── README.md
└── Sample_Documentation.pdf

````

---

## 📥 How to Clone the Repository

Open Terminal (Ubuntu/macOS)  
or Git Bash / PowerShell (Windows):

```bash
git clone https://github.com/EvonBiju/Decision_Companion_System.git
cd Decision_Companion_System
````

---

## 🖥 Running the CLI Version

Main CLI file:

```
ahp_advanced.py
```

### 🐧 Ubuntu

```bash
python3 ahp_advanced.py
```

### 🍎 macOS

```bash
python3 ahp_advanced.py
```

### 🪟 Windows

```bash
python ahp_advanced.py
```

---

## 🌐 Running the Web Version (FastAPI)

Backend file:

```
Website/main.py
```

### Step 1 — Navigate to Website Folder

```bash
cd Website
```

### Step 2 — Create Virtual Environment (Recommended)

#### Ubuntu / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run FastAPI Server

```bash
uvicorn main:app --reload
```

### Step 5 — Open in Browser

```
http://127.0.0.1:8000
```

---

## ☁ Deployment

The project is deployed using **Vercel**.
### 🌍 Live URL

[https://ahp-app-gamma.vercel.app/](https://ahp-app-gamma.vercel.app/)

---

## 5. Key Features

* Hybrid AHP framework
* Objective + Subjective + Uncertain criteria
* Benefit and cost handling
* Risk-adjusted scoring
* Sensitivity analysis
* CLI + Web version
* Fully explainable white-box model
* Extendable architecture

---

## 6. Applications

* Job offer comparison
* Startup vs corporate selection
* Investment evaluation
* Academic program selection
* Project prioritization
* Risk-based business decisions

---

## 7. Future Scope

* Monte Carlo simulation
* Portfolio covariance modeling
* JSON input/output mode
* Excel export
* Dashboard visualization
* AI-assisted preference estimation

---

## 8. Conclusion

The Hybrid AHP Decision Companion System combines:

* Multi-Criteria Decision Making (MCDM)
* Risk-adjusted evaluation
* Mathematical consistency validation
* Sensitivity robustness testing

It provides a powerful, explainable, and practical decision support system suitable for real-world complex decision scenarios.
