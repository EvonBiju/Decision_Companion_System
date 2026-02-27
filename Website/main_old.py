from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = FastAPI(title="AHP Decision Companion")

# RI Table
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}


# ---------- AHP Core Logic ----------

def calculate_weights(matrix: np.ndarray):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_index = int(np.argmax(eigenvalues.real))
    lambda_max = float(eigenvalues.real[max_index])
    weights = eigenvectors[:, max_index].real
    weights = weights / np.sum(weights)
    return weights.tolist(), lambda_max


def consistency_ratio(n: int, lambda_max: float) -> float:
    if n < 3:
        return 0.0
    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]
    return float(CR)


def build_matrix(n: int, comparisons: List[float]) -> np.ndarray:
    """Build pairwise matrix from upper triangle values."""
    matrix = np.ones((n, n))
    idx = 0
    for i in range(n):
        for j in range(i + 1, n):
            v = comparisons[idx]
            matrix[i][j] = v
            matrix[j][i] = 1.0 / v
            idx += 1
    return matrix


# ---------- Request / Response Models ----------

class Criterion(BaseModel):
    name: str
    type: str  # "benefit" or "cost"


class AHPRequest(BaseModel):
    decision: str
    criteria: List[Criterion]
    alternatives: List[str]
    criteria_comparisons: List[float]           # upper triangle, len = n*(n-1)/2
    alt_comparisons: List[List[float]]          # one list per criterion


class SensitivityRequest(BaseModel):
    criteria_weights: List[float]
    alt_weights_list: List[List[float]]
    alternatives: List[str]


# ---------- Endpoints ----------

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(BASE_DIR / "static" / "index.html") as f:
        return f.read()


@app.post("/api/validate-criteria")
async def validate_criteria(payload: dict):
    """Validate criteria pairwise matrix only."""
    n = payload["n"]
    comparisons = payload["comparisons"]
    matrix = build_matrix(n, comparisons)
    weights, lmax = calculate_weights(matrix)
    cr = consistency_ratio(n, lmax)
    return {
        "weights": weights,
        "lambda_max": lmax,
        "consistency_ratio": cr,
        "consistent": cr <= 0.1
    }


@app.post("/api/validate-alternatives")
async def validate_alternatives(payload: dict):
    """Validate single alternative pairwise matrix."""
    n = payload["n"]
    comparisons = payload["comparisons"]
    criterion_type = payload.get("criterion_type", "benefit")
    
    matrix = build_matrix(n, comparisons)
    
    # Invert if cost criterion
    if criterion_type == "cost":
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j] = 1.0 / matrix[i][j]
                matrix[j][i] = 1.0 / matrix[j][i]
        # Rebuild properly
        raw = build_matrix(n, comparisons)
        for i in range(n):
            for j in range(i + 1, n):
                raw[i][j] = 1.0 / raw[i][j]
                raw[j][i] = raw[i][j]
        matrix = raw
    
    weights, lmax = calculate_weights(matrix)
    cr = consistency_ratio(n, lmax)
    return {
        "weights": weights,
        "lambda_max": lmax,
        "consistency_ratio": cr,
        "consistent": cr <= 0.1
    }


@app.post("/api/calculate")
async def calculate(req: AHPRequest):
    n_criteria = len(req.criteria)
    n_alt = len(req.alternatives)

    # Criteria matrix
    crit_matrix = build_matrix(n_criteria, req.criteria_comparisons)
    crit_weights, crit_lmax = calculate_weights(crit_matrix)
    crit_cr = consistency_ratio(n_criteria, crit_lmax)

    # Alternative matrices
    final_scores = np.zeros(n_alt)
    alt_weights_list = []
    detailed_scores = {}
    alt_crs = []

    for i, criterion in enumerate(req.criteria):
        raw_matrix = build_matrix(n_alt, req.alt_comparisons[i])

        # Invert for cost criteria
        if criterion.type == "cost":
            for r in range(n_alt):
                for c in range(r + 1, n_alt):
                    raw_matrix[r][c] = 1.0 / raw_matrix[r][c]
                    raw_matrix[c][r] = raw_matrix[r][c]

        alt_weights, alt_lmax = calculate_weights(raw_matrix)
        alt_cr = consistency_ratio(n_alt, alt_lmax)
        alt_crs.append(alt_cr)
        alt_weights_list.append(alt_weights)

        contribution = [crit_weights[i] * w for w in alt_weights]
        detailed_scores[criterion.name] = contribution
        final_scores += np.array(contribution)

    ranking = np.argsort(final_scores)[::-1].tolist()
    final_scores_list = final_scores.tolist()

    # Sensitivity analysis
    sensitivity = []
    cw = np.array(crit_weights)
    awl = [np.array(w) for w in alt_weights_list]
    original_scores = sum(cw[i] * awl[i] for i in range(n_criteria))
    original_best = req.alternatives[int(np.argmax(original_scores))]

    for i in range(n_criteria):
        new_weights = cw.copy()
        new_weights[i] *= 1.10
        new_weights /= np.sum(new_weights)
        new_scores = sum(new_weights[j] * awl[j] for j in range(n_criteria))
        new_best = req.alternatives[int(np.argmax(new_scores))]
        sensitivity.append({
            "criterion": req.criteria[i].name,
            "original_best": original_best,
            "new_best": new_best,
            "stable": new_best == original_best,
            "new_scores": new_scores.tolist()
        })

    return {
        "decision": req.decision,
        "criteria_weights": crit_weights,
        "criteria_cr": crit_cr,
        "criteria_consistent": crit_cr <= 0.1,
        "alt_weights_list": alt_weights_list,
        "alt_crs": alt_crs,
        "final_scores": final_scores_list,
        "ranking": ranking,
        "best": req.alternatives[ranking[0]],
        "detailed_scores": detailed_scores,
        "sensitivity": sensitivity
    }


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
