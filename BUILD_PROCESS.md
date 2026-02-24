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
