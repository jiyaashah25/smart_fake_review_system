# Technical Audit & Diagnostic Report: ML Model Prediction Behavior

**Project:** ReviewGuard AI — Smart Fake Review Detection System  
**Audit Status:** Completed (Strict Read-Only Audit — Zero Code or Model Artifact Modifications)  
**Evaluated Model Artifact:** `models/fake_review_model.joblib`  
**Execution Environment:** Python 3.13.7 | scikit-learn 1.9.1 | Windows x64  
**Date:** October 2026  

---

## Executive Summary

An exhaustive technical audit of ReviewGuard AI's machine learning model and inference architecture was performed to investigate reported prediction inconsistencies (genuine reviews classified as fake, and deceptive reviews classified as genuine).

### Key Conclusions:
1. **The Model Is Not Globally Inverted:** On the untouched 20% stratified test split (320 samples) of the Ott et al. benchmark dataset, the model achieves **90.31% test accuracy** (145/160 genuine reviews classified correctly as Genuine; 144/160 fake reviews classified correctly as Potentially Fake).
2. **The Apparent "Inversion" Stems From Four Identifiable Root Causes:**
   - **Case-Sensitivity Flaw in Feature Extraction:** `TfidfVectorizer(preprocessor=clean_text)` in `ml/train_model.py` uses a custom preprocessor function that did not convert text to lowercase. In scikit-learn, providing a custom `preprocessor` replaces the default preprocessor and bypasses `lowercase=True`. Consequently, the TF-IDF vocabulary is strictly case-sensitive. All-caps promotional text (such as UI Preset 2: *"BEST HOTEL EXPERIENCE EVER IN MY ENTIRE LIFE!!!! Words cannot describe the unbelievable perfection of this place. You MUST BOOK NOW! 100% recommended, guaranteed satisfaction!"*) misses crucial vocabulary tokens (e.g. `"EXPERIENCE"` and `"PLACE"` have 0 weight, and `"MY"` has only +0.05 instead of +2.97), causing the model to predict **Likely Genuine (51.23%)**. When typed in normal casing or lowercase, the exact same text predicts **Potentially Fake (62.88%)**.
   - **Domain Specificity of Training Corpus:** The model was trained on the Ott et al. corpus (20 Chicago hotels). In this corpus, real guests focused on physical hotel logistics (`"floor"`, `"bathroom"`, `"water"`, `"rate"`, `"small"`), whereas deceptive writers focused on luxury claims and hotel names (`"Chicago"`, `"Hilton"`, `"luxury"`, `"vacation"`, `"experience"`). Reviews lacking physical hotel descriptions or praising general amenities can trigger unexpected classifications.
   - **Disconnect Between Heuristic Signals and ML Verdict:** The qualitative indicator engine (`ml/preprocess.py`) correctly flags *"Excessive Capitalization"*, *"Heightened Punctuation"*, and *"Strong Promotional Phrasing"*. However, because the linear TF-IDF classifier operates independently, the frontend renders alert badges right below a *"Likely Genuine Review"* verdict, creating the distinct perception that the verdict is backwards.
   - **Permissive Unit Tests:** Existing test suites in `tests/test_predictions.py` only asserted `assert result["label"] in [0, 1]`, allowing silent classification failures to pass CI unnoticed.

---

## Technical Audit Findings

### 1. Active Loaded Model Artifact
- **File Location:** `models/fake_review_model.joblib`
- **Metadata Record:** `models/model_metadata.json`
- **Pipeline Architecture:**
  ```python
  Pipeline(steps=[
      ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=15000, sublinear_tf=True, min_df=2)),
      ('clf', LogisticRegression(C=2.5, max_iter=1000, random_state=42, class_weight='balanced', solver='liblinear'))
  ])
  ```
- **Internal Classes:** `[0, 1]`
- **Class Label Dictionary:** `{0: "Genuine Review", 1: "Potentially Fake Review"}`
- **Model Intercept:** `[-0.24649836]`
- **Training Timestamp:** `2026-10-13T14:15:45.624756+00:00`
- **Runtime Loading:** Loaded in `ml/predict.py` via `get_model()` using in-memory singleton caching (`_MODEL_CACHE`).

### 2. Dataset and Target Column
- **Raw Benchmark Dataset:** `data/raw/reviews.csv` (1,600 rows).
  - Source: Ott et al. Deceptive Opinion Spam Benchmark (ACL 2011 / Cornell NLP).
  - Schema: `['deceptive', 'hotel', 'polarity', 'source', 'text']`
  - Raw Label Column: `'deceptive'` (`'truthful'` vs. `'deceptive'`).
  - Raw Text Column: `'text'`
- **Processed Cleaned Dataset:** `data/processed/cleaned_reviews.csv` (1,596 rows after removing 4 exact duplicate texts: 796 genuine, 800 deceptive).
  - Schema: `['review_id', 'review_text', 'label', 'product_category', 'source']`
  - Target Label Column: `'label'` (integers `0` and `1`).

### 3. Label Encoding During Training
In `ml/data_loader.py` and `ml/train_model.py`:
- `truthful` $\to$ `0` (Genuine / Negative Class)
- `deceptive` $\to$ `1` (Potentially Fake / Positive Class)

#### Learned Feature Weights:
- **Top Deceptive Signals ($w_i > 0$, Pushing Toward Class 1 / Fake):**
  - `"Chicago"`: `+4.0019`
  - `"my"`: `+2.9749`
  - `"Hotel"`: `+2.7379`
  - `"luxury"`: `+2.4581`
  - `"my room"`: `+1.7704`
  - `"Hilton"`: `+1.6055`
  - `"luxurious"`: `+1.5316`
  - `"vacation"`: `+1.4234`
  - `"experience"`: `+1.4044`
- **Top Genuine Signals ($w_i < 0$, Pushing Toward Class 0 / Genuine):**
  - `"location"`: `-2.4936`
  - `"floor"`: `-2.3405`
  - `"We"`: `-2.1318`
  - `"small"`: `-1.7957`
  - `"rate"`: `-1.7121`
  - `"bathroom"`: `-1.2282`
  - `"coffee"`: `-1.3068`
  - `"walk"`: `-1.3392`

### 4. End-to-End Prediction Translation
Tracing prediction flow from inference to frontend:
1. **Inference (`ml/predict.py`):**
   `pred_label = int(pipeline.predict([cleaned_input])[0])`  
   `prediction_slug = "potentially_fake" if pred_label == 1 else "genuine"`  
   `label_name = "Potentially Fake Review" if pred_label == 1 else "Likely Genuine Review"`
2. **REST API (`api/routes.py` & `api/schemas.py`):**
   Exposes `/api/predict` returning JSON payload with `prediction`, `label` (0 or 1), `label_name`, and `confidence`.
3. **Frontend (`frontend/src/components/PredictionResult.tsx`):**
   `const isFake = data.label === 1;`  
   Renders red banner (`#E05A68`) and `"Potentially Fake"` when `isFake === true`.  
   Renders green banner (`#52B788`) and `"Likely Genuine"` when `isFake === false`.
4. **History & Confidence Meter:**
   Both `ReviewHistory.tsx` and `ConfidenceMeter.tsx` strictly follow `label === 1` for fake status.  
   **No frontend inversion or label flipping exists.**

### 5. Preprocessing & Feature Extraction Analysis
- **Custom Preprocessor Override:** In `ml/preprocess.py`, `clean_text()` strips HTML, normalizes Unicode (NFKD), and collapses whitespaces, but **does not lowercase text**.
- Because `TfidfVectorizer(preprocessor=clean_text)` receives a custom function, scikit-learn bypasses its default `lowercase=True`.
- This causes case sensitivity:
  - `"my"` has coefficient `+2.9749` (strong deceptive indicator).
  - `"MY"` has coefficient `+0.0525` (almost neutral).
  - `"EXPERIENCE"` and `"PLACE"` are omitted from vocabulary entirely.

### 6. Probability & Confidence Calculation
- `ml/predict.py` calculates confidence as the probability of the *winning class*:
  `pred_prob = float(probs[pred_label])`  
  `confidence = round(pred_prob * 100.0, 2)`
- Therefore, confidence is always in the range $[50.0\%, 100.0\%]$.
- The API also returns explicit class probabilities: `probabilities: {"genuine": ..., "potentially_fake": ...}`.
- If a user reads "Confidence: 85%" on a Genuine prediction and assumes it means "85% probability of being fake", this creates cognitive confusion. The frontend `ConfidenceMeter.tsx` explicitly clarifies this with tailored descriptions for genuine vs. fake.

---

## Empirical Verification Results

Tests were performed against the saved model artifact without altering any files:

### 1. Test Split Performance (80/20 Stratified Split, 320 Samples)
- **Accuracy:** `90.31%`
- **Precision (Fake):** `90.57%`
- **Recall (Fake):** `90.00%`
- **F1-Score (Fake):** `90.28%`
- **ROC-AUC:** `0.9486`
- **Confusion Matrix:** True Negative: 145, False Positive: 15, False Negative: 16, True Positive: 144.

### 2. Ott et al. Benchmark Samples

| Sample ID | True Label | Review Text Excerpt | Model Prediction | Winning Confidence |
| :--- | :--- | :--- | :--- | :--- |
| `rev_00001` | Truthful (0) | *"We stayed for a one night getaway with family on a thursday. Triple AAA rate of..."* | **Genuine (0)** | 88.52% |
| `rev_00002` | Truthful (0) | *"Triple A rate with upgrade to view room was less than $200 which also included..."* | **Genuine (0)** | 89.10% |
| `rev_00003` | Truthful (0) | *"This comes a little late as I'm finally catching up on my reviews from the past..."* | **Genuine (0)** | 79.73% |
| `rev_00401` | Deceptive (1) | *"My husband and I visited the Fairmont Chicago Millennium Park for our honeymoon..."* | **Potentially Fake (1)** | 75.17% |
| `rev_00402` | Deceptive (1) | *"My wife and I booked a Deluxe Accessible Room at this beautiful hotel for three..."* | **Potentially Fake (1)** | 71.91% |
| `rev_00403` | Deceptive (1) | *"Quite simply the Hyatt Regency Chicago is the business traveler's best friend..."* | **Potentially Fake (1)** | 78.36% |

### 3. UI Preset Samples (Diagnosis of False Classification)

| Preset Name | Review Input | Detected Stylistic Signals | Model Prediction | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Preset 1** (*Descriptive & Specific*) | *"We stayed at this hotel for three nights on our family trip to Chicago. The front desk was friendly and check-in took five minutes. The bathroom was spotless..."* | Balanced Stylistic Profile | **Genuine (0)** (80.42%) | Correct genuine prediction. |
| **Preset 2** (*Promotional Language*) | *"BEST HOTEL EXPERIENCE EVER IN MY ENTIRE LIFE!!!! Words cannot describe the unbelievable perfection of this place. You MUST BOOK NOW! 100% recommended, guaranteed satisfaction!"* | Excessive Capitalization, Punctuation Intensity, Strong Promotional Phrasing | **Genuine (0)** (51.23%) | **Flawed prediction:** Due to ALL CAPS, key fake tokens missed the vocabulary. When lowercased, correctly predicts **Fake (1)** (62.88%). |
| **Preset 3** (*Short Generic Feedback*) | *"Great product and good value for money. Highly recommend to everyone."* | Strong Promotional Phrasing | **Genuine (0)** (74.45%) | Tokens `"Great"`, `"good"`, `"value"` in hotel benchmark dataset strongly associate with real guests discussing room rates. |

---

## Action Plan & Proposed Files For Modification

*(Awaiting user authorization before applying any code changes.)*

| File | Proposed Change | Purpose |
| :--- | :--- | :--- |
| `ml/preprocess.py` | Add `.lower()` inside `clean_text()` | Ensure case-insensitivity across both training and inference. |
| `ml/train_model.py` | Ensure lowercase normalization in vectorizer pipeline; retrain artifact | Enable uppercase promotional text to properly match learned deceptive vocabulary. |
| `frontend/src/components/ReviewAnalyzer.tsx` | Refine preset test examples | Provide benchmark examples representative of the hotel domain vocabulary. |
| `tests/test_predictions.py` | Add deterministic ground-truth assertions | Prevent regression and verify that deceptive/genuine samples produce expected labels. |
