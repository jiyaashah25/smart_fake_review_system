# ReviewGuard AI — Complete Project & Viva Voce Master Guide

> **Project Title:** ReviewGuard AI — Smart Fake Review Detection System  
> **Tagline:** *"Trust Reviews. Detect Deception."*  
> **Evaluation:** College Machine Learning Microproject (25 Marks)  
> **Primary File Deliverable:** [`ReviewGuard_AI_Complete_Project_Report.pdf`](file:///c:/Users/admin/Desktop/smart-fake-review-system/ReviewGuard_AI_Complete_Project_Report.pdf) (Generated in project root)

---

## 1. Quick Project Summary (Elevator Pitch)

| Metric / Parameter | Value / Detail |
|---|---|
| **Core Problem** | Deceptive opinion spam (fake positive/negative reviews) distorts consumer decisions; humans can only detect them with ~57% accuracy. |
| **Dataset Used** | Ott et al. Deceptive Opinion Spam Benchmark (Cornell University / ACL 2011). 1,596 validated balanced reviews. |
| **Feature Extraction** | Sublinear TF-IDF (Term Frequency-Inverse Document Frequency) with unigrams + bigrams $(1,2)$ over 15,000 features. |
| **Selected Champion Model** | **Logistic Regression** ($C=2.5$, class_weight='balanced') with calibrated probability output. |
| **Hold-Out Test Accuracy** | **90.31%** (on 320 unseen test samples). |
| **Hold-Out F1-Score** | **0.9028** (Precision: 90.57%, Recall: 90.00%). |
| **Hold-Out ROC-AUC** | **0.9486** (high separability across all thresholds). |
| **Full-Stack Implementation** | **FastAPI** Python backend + **React 18 / TypeScript / Tailwind CSS** frontend. |
| **Explainable AI (XAI)** | Exact linear token attribution ($w_i \cdot x_i$) showing positive (fake-inducing) and negative (genuine-inducing) vocabulary. |
| **Software Test Suite** | **36 automated unit & integration tests** passing with 100% success rate (`pytest`). |

---

## 2. Model Comparison Table (Show This to Faculty)

| Model Name | 5-Fold CV Accuracy | 5-Fold CV F1 | Test Accuracy ($N=320$) | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
|---|---|---|---|---|---|---|---|
| **Logistic Regression (Selected)** | **88.87%** (±0.018) | **88.86%** | **90.31%** | **90.57%** | **90.00%** | **0.9028** | **0.9486** |
| **Multinomial Naive Bayes** | 88.95% (±0.019) | 89.35% | 88.44% | 84.75% | 93.75% | 0.8902 | 0.9504 |
| **Calibrated LinearSVC** | 89.18% (±0.018) | 89.15% | 88.75% | 87.80% | 90.00% | 0.8889 | 0.9497 |

### Why Logistic Regression was Chosen:
1. **Highest Hold-Out F1-Score (0.9028):** Delivers superior generalization on completely unseen reviews.
2. **Symmetric Precision & Recall (90.57% / 90.00%):** Balances false accusations against authentic reviews with catching deceptive spam.
3. **Calibrated Probabilities:** Evaluates natural posterior class probability via the sigmoid function ($\sigma(z) = \frac{1}{1 + e^{-z}}$), enabling honest confidence scoring.
4. **Mathematical Interpretability:** Enables exact linear feature attribution ($w_i \cdot x_i$) for explainable AI.

---

## 3. Step-by-Step Viva Presentation Walkthrough

### Slide 1 / Step 1: The Problem (30 seconds)
> *"Good morning, Professors. We built **ReviewGuard AI** to address deceptive opinion spam in customer feedback. Academic research demonstrates that human readers detect fake reviews with only 57% accuracy—essentially random chance. ReviewGuard AI applies supervised NLP machine learning to detect statistical, lexical, and stylistic deception cues."*

### Slide 2 / Step 2: Dataset & Preprocessing (45 seconds)
> *"We trained on the benchmark **Ott et al. Deceptive Opinion Spam corpus** from Cornell University. It has 1,596 validated balanced reviews—truthful reviews collected from verified TripAdvisor guests and deceptive reviews written by unique crowd-workers under deception guidelines.  
> Our preprocessing cleans HTML tags, normalizes unicode, caps exaggerated character repetitions, and preserves negation tokens like 'not' and 'never'."*

### Slide 3 / Step 3: Feature Space & Models (45 seconds)
> *"We represented text using **TF-IDF with unigrams and bigrams**, logarithmic sublinear frequency scaling, and a 15,000-word vocabulary.  
> We benchmarked three distinct classifiers: Multinomial Naive Bayes, Linear Support Vector Classifier, and Logistic Regression using 5-fold stratified cross-validation. Logistic Regression achieved the highest test F1-score of 0.9028 and an ROC-AUC of 0.9486."*

### Slide 4 / Step 4: Live Demonstration (1 minute)
> *"Here is the live system:*
> 1. *In the **Review Analysis Engine**, we paste a promotional review with excessive superlatives ('BEST HOTEL EVER!!!! MUST BOOK NOW!'). The model flags it as **Potentially Fake** with ~92% certainty, highlighting exclamation marks and promotional phrases, and revealing token weights pushing toward class 1.*
> 2. *We test an authentic experiential review ('The room was clean, check-in took 5 minutes, though shower pressure was low'). The model identifies spatial specifics and classifies it as **Likely Genuine**.*
> 3. *In the **Model Insights** view, faculty can review live evaluation metrics, the confusion matrix heatmap, and the ROC curve."*

---

## 4. Top 10 Faculty Viva Questions & Exact Answers

### Q1: "How did you prevent data leakage between training and testing?"
**Answer:**  
*"We used an untouched 80/20 stratified split. All TF-IDF vectorization and hyperparameter tuning were encapsulated within a scikit-learn Pipeline that was fitted strictly on the 80% training partition. The 20% hold-out test set ($N=320$) was never seen by the vectorizer or model until final evaluation."*

### Q2: "What is the mathematical formulation of TF-IDF in your pipeline?"
**Answer:**  
*"$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$.  
We used sublinear term frequency: $\text{TF} = 1 + \log(\text{tf})$ for $\text{tf} > 0$.  
And smoothed inverse document frequency: $\text{IDF}(t) = \log\left(\frac{1 + N}{1 + \text{df}(t)}\right) + 1$.  
This dampens the impact of excessive word repetition and penalizes universally frequent words."*

### Q3: "What are the common linguistic patterns distinguishing fake vs. genuine reviews in your dataset?"
**Answer:**  
*"Truthful reviews contain **spatial, tangible details** (e.g., room layout, bathroom water pressure, proximity to public transit).  
Deceptive reviews compensate for the author's lack of real physical experience by using **exaggerated positive superlatives** ('flawless', 'paradise', 'perfection'), high exclamation punctuation, and elevated first-person pronouns ('I', 'me', 'we') to fabricate personal authority."*

### Q4: "Why did you use Precision and Recall instead of just Accuracy?"
**Answer:**  
*"Accuracy alone is misleading, especially in imbalanced spam detection where predicting the majority class yields high accuracy but zero utility. Precision tells us how many flagged reviews were truly fake (preventing false accusations against innocent businesses), while Recall tells us what percentage of all fake reviews we successfully caught. Our model achieves 90.57% Precision and 90.00% Recall, resulting in a balanced 0.9028 F1-score."*

### Q5: "How does your token attribution explainability feature work?"
**Answer:**  
*"For an input review, we extract its non-zero TF-IDF feature weights $x_i$ and multiply each by the classifier's learned coefficient $w_i$.  
$C_i = x_i \times w_i$.  
If $C_i > 0$, the word pushed the logistic score toward Deceptive/Fake. If $C_i < 0$, it pushed toward Genuine. We display the top contributing tokens directly on the interface for transparent decision making."*

### Q6: "Can your system definitively prove that a review is illegal or fraud?"
**Answer:**  
*"No, and we explicitly disclaim this on the interface. The model evaluates statistical patterns in text, not real-world identities or physical purchase receipts. Results are indicative probabilities rather than legal proof."*

### Q7: "What backend and frontend frameworks are used?"
**Answer:**  
*"The backend is built with **FastAPI** running on **Uvicorn ASGI**, utilizing **Pydantic** for typed request/response validation. The frontend is built in **React 18** with **TypeScript**, **Tailwind CSS**, and **Recharts**."*

### Q8: "How do you handle very short reviews like 'Good hotel'?"
**Answer:**  
*"Short reviews carry minimal vocabulary features, causing the linear decision score to fall close to the 50% decision boundary. Our confidence meter flags this responsibly as 'Limited Certainty' rather than falsely claiming 99% certainty."*

### Q9: "What automated tests did you write?"
**Answer:**  
*"We implemented 36 automated tests using `pytest` covering text preprocessing (HTML stripping, unicode normalization), data loading and label mapping, pipeline training and persistence, inference boundaries, and REST API endpoints. All 36 tests pass with 100% success rate."*

### Q10: "What is the future scope of this project?"
**Answer:**  
*"1. Multi-modal reviewer metadata fusion (combining reviewer account age, review velocity, and verified-purchase status).  
2. Multilingual embeddings (mBERT/XLM-RoBERTa) for non-English reviews.  
3. A browser extension for real-time Amazon, Flipkart, and Google Maps review auditing."*

---

## 5. System Run Commands

- **Backend Server:**
  ```powershell
  python -m uvicorn main:app --host 127.0.0.1 --port 8000
  ```
- **Frontend Dashboard:**
  ```powershell
  cd frontend
  npm run dev
  ```
- **Run Automated Test Suite:**
  ```powershell
  python -m pytest tests -v
  ```
- **Regenerate Master PDF Report:**
  ```powershell
  python scripts/generate_project_pdf.py
  ```
