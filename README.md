# ReviewGuard AI — Smart Fake Review Detection System

> **Tagline:** *"Trust Reviews. Detect Deception."*  
> An end-to-end Machine Learning web application that identifies potentially fake, deceptive, or opinion-spam product reviews using Natural Language Processing (NLP) and supervised classification algorithms.

---

## 1. Project Overview

Online consumer decisions are heavily influenced by customer ratings and reviews. However, e-commerce platforms and hospitality portals frequently suffer from **opinion spam**—deceptive positive reviews purchased to artificially boost a product, or malicious negative reviews designed to harm competitors.

**ReviewGuard AI** provides a transparent, scientifically grounded machine learning solution to detect deceptive patterns in review text. The application includes a trained NLP pipeline, a high-performance **FastAPI** backend, and a modern **React 18 + TypeScript + Tailwind CSS** frontend dashboard that provides responsible confidence scoring, stylistic signals, and feature attribution.

> [!IMPORTANT]
> **Mandatory Disclaimer:** ReviewGuard AI provides automated predictions based on learned patterns in empirical review data. Results are indicative and should not be treated as definitive proof of review fraud.

---

## 2. Problem Statement & Objectives

### Problem Statement
Human readers struggle to differentiate between genuine and deceptive reviews, often achieving detection accuracy no better than chance (~57%). Automated NLP classifiers can uncover subtle stylistic, structural, and lexical cues—such as exaggerated superlatives, lack of spatial detail, elevated pronoun frequency, and skewed sentiment intensity.

### Core Objectives
1. **Empirical NLP & Supervised ML:** Train and compare multiple classification models on a verified academic benchmark dataset.
2. **Explainable AI (XAI):** Go beyond binary outputs by surfacing qualitative stylistic indicators and influential TF-IDF token contributions.
3. **Calibrated Confidence:** Present model certainty responsibly, avoiding deceptive claims of absolute certainty.
4. **Single & Batch Screening:** Support real-time single-review analysis as well as bulk CSV uploads (up to 2,000 records).
5. **Academic Viva Readiness:** Provide verifiable hold-out evaluation metrics, confusion matrices, and ROC curves for college microproject demonstrations.

---

## 3. System Architecture

```mermaid
flowchart TD
    A[Raw Benchmark Dataset\nOtt et al. Deceptive Opinion Spam] --> B[Data Cleaning & Validation\nml/data_loader.py]
    B --> C[Cleaned Dataset\n1,596 Balanced Samples]
    C --> D[Stratified 80/20 Train/Test Split\nSeed: 42]
    
    subgraph Training Pipeline [Training Partition (80%)]
        D --> E[NLP Normalization & TF-IDF Vectorizer\n1-2 N-grams, Sublinear TF]
        E --> F1[Multinomial Naive Bayes]
        E --> F2[Calibrated LinearSVC]
        E --> F3[Logistic Regression\n(Selected Best Model)]
        F1 & F2 & F3 --> G[5-Fold Stratified Cross-Validation]
    end
    
    subgraph Evaluation [Untouched Hold-Out Test Partition (20%)]
        F3 --> H[Final Metric Computation\nAcc: 90.31%, F1: 0.9028, AUC: 0.9486]
        H --> I[Confusion Matrix & ROC Plots]
        H --> J[Persisted Joblib Artifact\nmodels/fake_review_model.joblib]
    end
    
    subgraph REST API & UI [Serving Layer]
        J --> K[FastAPI Backend\nmain.py + api/routes.py]
        K --> L[Single Review Inference\nPOST /api/predict]
        K --> M[Batch CSV Analysis\nPOST /api/predict/batch]
        K --> N[Model Telemetry & Analytics\nGET /api/analytics]
        
        L & M & N --> O[React 18 + TypeScript Dashboard\nTailwind CSS + Recharts]
    end
```

---

## 4. Technology Stack

### Backend & Machine Learning
- **Python 3.11+ / 3.13**
- **scikit-learn:** NLP vectorization, model pipelines, cross-validation, and metrics.
- **pandas & NumPy:** Data preprocessing, manipulation, and array computation.
- **FastAPI:** High-throughput asynchronous REST API framework.
- **Uvicorn:** Production-grade ASGI web server.
- **Joblib:** Model artifact persistence and serialization.
- **Matplotlib (Agg):** Non-interactive generation of confusion matrices and ROC curves.
- **pytest & HTTPX:** Comprehensive automated unit and integration testing.

### Frontend
- **React 18 & TypeScript:** Strongly typed component architecture.
- **Vite:** Next-generation frontend tooling and bundler.
- **Tailwind CSS:** Responsive dark theme design (`#0B1020`, violet, and cyan accents).
- **Lucide React:** Modern UI iconography.
- **Recharts:** Interactive algorithm comparison and analytics charts.

---

## 5. Repository Structure

```
smart-fake-review-system/
│
├── README.md                          # Comprehensive project documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Backend environment template
├── main.py                            # FastAPI application entry point
│
├── data/
│   ├── raw/
│   │   └── reviews.csv                # Raw benchmark dataset
│   └── processed/
│       └── cleaned_reviews.csv        # Cleaned, validated, deduplicated dataset
│
├── ml/
│   ├── __init__.py                    # ML package marker
│   ├── data_loader.py                 # Ingestion, schema validation, and label mapping
│   ├── preprocess.py                  # Text normalization & stylistic indicators
│   ├── train_model.py                 # Multi-model training, 5-fold CV & artifact export
│   ├── predict.py                     # Single and batch inference engine
│   ├── evaluate_model.py              # Metric calculation and figure plotting
│   └── explain_prediction.py          # TF-IDF token attribution & explainability
│
├── models/
│   ├── fake_review_model.joblib       # Persisted scikit-learn best model pipeline
│   ├── model_metadata.json            # Model parameters and dataset metadata
│   ├── model_metrics.json             # Test set evaluation results
│   ├── model_comparison.csv           # Multi-model comparison benchmark table
│   ├── confusion_matrix.png           # Confusion matrix heatmap visualization
│   └── roc_curve.png                  # Receiver Operating Characteristic plot
│
├── api/
│   ├── __init__.py                    # API package marker
│   ├── routes.py                      # REST endpoints (/predict, /batch, /analytics)
│   ├── schemas.py                     # Pydantic request and response schemas
│   └── exceptions.py                  # Custom exceptions and security error handlers
│
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py          # Normalization & indicator unit tests
│   ├── test_data_loader.py            # Data loading & validation tests
│   ├── test_model_training.py         # Pipeline & metric tests
│   ├── test_predictions.py            # Model inference tests
│   ├── test_api.py                    # REST API endpoint integration tests
│   └── test_batch_analysis.py         # CSV batch screening tests
│
├── scripts/
│   ├── download_dataset.py            # Dataset downloader utility
│   └── prepare_dataset.py             # Data preparation & validation script
│
└── frontend/                          # React + TypeScript Vite frontend
    ├── package.json
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── index.css
        ├── types/review.ts
        ├── services/api.ts
        ├── hooks/useReviewAnalysis.ts
        ├── utils/validation.ts
        └── components/
            ├── Navbar.tsx
            ├── HeroSection.tsx
            ├── ReviewAnalyzer.tsx
            ├── PredictionResult.tsx
            ├── ConfidenceMeter.tsx
            ├── SuspiciousSignals.tsx
            ├── BatchUpload.tsx
            ├── AnalyticsDashboard.tsx
            ├── MetricsCard.tsx
            ├── ReviewHistory.tsx
            ├── HowItWorks.tsx
            ├── LoadingAnimation.tsx
            └── Footer.tsx
```

---

## 6. Dataset Details & Label Mapping

### Source & Provenance
The model is trained on the **Ott et al. Deceptive Opinion Spam Corpus** (Cornell NLP / ACL 2011: *"Finding Deceptive Opinion Spam by Any Stretch of the Imagination"*).
- Contains 1,600 verified reviews across 20 prestigious Chicago hotels.
- Truthful reviews were gathered from genuine TripAdvisor guest postings.
- Deceptive reviews were authored by unique crowd workers under explicit deception guidelines.

### Standardized Schema
| Column Name | Description | Example |
|---|---|---|
| `review_id` | Unique identifier | `rev_00001` |
| `review_text` | Natural language review text | `"The hotel room was very clean..."` |
| `label` | Binary target class | `0` or `1` |
| `product_category` | Hotel / Product domain | `Hilton`, `Marriott` |
| `source` | Benchmark source name | `Ott et al. Benchmark` |

### Label Mapping
- `0` = **Genuine Review** (`truthful`, `genuine`, `real`)
- `1` = **Potentially Fake Review** (`deceptive`, `fake`, `spam`)

---

## 7. NLP Preprocessing & Feature Engineering

1. **Text Normalization:**
   - HTML entity unescaping (e.g., `&amp;` $\to$ `&`).
   - Removal of HTML tags (`<p>`, `<div>`).
   - Unicode NFKD normalization.
   - Repeated character capping (e.g., `amazzzzing` $\to$ `amazing`).
   - Multiple whitespace reduction.
   - Preserves negation tokens (`not`, `never`, `didn't`) which are critical for sentiment context.

2. **TF-IDF Feature Representation:**
   - Vectorizer fitted **strictly** on training partitions (preventing test set leakage).
   - N-gram range: Unigrams and Bigrams `(1, 2)`.
   - Max Features: `15,000` most informative features.
   - Sublinear term-frequency scaling enabled: $\text{tf} = 1 + \log(\text{tf})$.
   - Minimum document frequency (`min_df=2`) to prune typos.

3. **Interpretable Heuristic Signals:**
   - **Brevity Flag:** Reviews with $< 10$ words lacking descriptive substance.
   - **Capitalization Intensity:** $> 30\%$ uppercase ratio indicating spam emphasis.
   - **Punctuation Intensity:** Multiple exclamation sequences (`!!`, `???`).
   - **Promotional Lexicon:** Detection of aggressive sales triggers (*"must buy"*, *"100% recommend"*, *"best ever"*).
   - **Lexical Diversity:** Low unique-to-total word ratio revealing repetitive phrasing.
   - **Pronoun Density:** High concentration of first-person pronouns (*"I"*, *"we"*).

---

## 8. Machine Learning Model Comparison & Results

Three candidate architectures were trained and evaluated using stratified 5-fold cross-validation on the training split ($N=1,276$) and evaluated on the untouched hold-out test set ($N=320$):

| Model Candidate | CV Accuracy | CV F1 | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
|---|---|---|---|---|---|---|---|
| **Logistic Regression** *(Selected)* | **88.87%** | **88.86%** | **90.31%** | **90.57%** | **90.00%** | **90.28%** | **0.9486** |
| **Multinomial Naive Bayes** | 88.95% | 89.35% | 88.44% | 84.75% | 93.75% | 89.02% | 0.9504 |
| **Calibrated LinearSVC** | 89.18% | 89.15% | 88.75% | 87.80% | 90.00% | 88.89% | 0.9497 |

### Why Logistic Regression was Selected
1. **Superior Test F1-Score (0.9028):** Delivers the highest balanced detection performance on unseen test data.
2. **Balanced Precision & Recall (90.57% / 90.00%):** Minimizes both false accusations against honest reviews and misses of deceptive spam.
3. **Calibrated Probabilities:** Naturally produces true class probabilities via the sigmoid function ($\sigma(z)$) for responsible confidence scoring.
4. **Mathematical Interpretability:** Enables direct token attribution ($w_i \cdot x_i$) for explainable AI.

---

## 9. Installation & Setup Instructions

Follow these step-by-step instructions in **Windows PowerShell**:

### Prerequisites
- Python 3.11, 3.12, or 3.13 installed (`python --version`)
- Node.js v18+ and npm installed (`node --version`)

---

### Step 1: Open Project Directory
```powershell
cd c:\Users\admin\Desktop\smart-fake-review-system
```

### Step 2: (Optional) Set up a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Backend Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Prepare & Validate the Dataset
```powershell
python scripts/prepare_dataset.py
```
*Output will confirm 1,596 validated samples saved to `data/processed/cleaned_reviews.csv`.*

### Step 5: Train and Evaluate the ML Model
```powershell
python -m ml.train_model
```
*Trains all 3 models, generates `models/model_comparison.csv`, `models/confusion_matrix.png`, `models/roc_curve.png`, and saves `models/fake_review_model.joblib`.*

### Step 6: Run Automated Tests
```powershell
python -m pytest tests -v
```
*Executes all 36 unit and integration tests across preprocessing, data loading, training, prediction, and API endpoints.*

### Step 7: Start the FastAPI Backend
```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
*API interactive documentation is available at `http://127.0.0.1:8000/docs`.*

---

### Step 8: Install Frontend Dependencies & Start UI
Open a **second** terminal window:
```powershell
cd c:\Users\admin\Desktop\smart-fake-review-system\frontend
npm install
npm run dev
```
*Open your browser and navigate to `http://localhost:5173`.*

---

## 10. API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Application info, version, and operational status |
| `GET` | `/health` | Health check endpoint returning model loading status |
| `GET` | `/api/model-info` | Metadata including classes, hyperparameters, and dataset info |
| `POST` | `/api/predict` | Classify a single review with explainability |
| `POST` | `/api/predict/batch` | Upload CSV for batch review screening |
| `GET` | `/api/analytics` | Retrieve actual evaluation metrics and comparison records |
| `GET` | `/api/visualizations/confusion-matrix` | Serves the generated confusion matrix PNG |
| `GET` | `/api/visualizations/roc-curve` | Serves the generated ROC curve PNG |

### Example Request (`POST /api/predict`):
```json
{
  "review_text": "We stayed at this hotel last weekend. The room was spacious and clean, though breakfast was a bit crowded."
}
```

### Example Response:
```json
{
  "prediction": "genuine",
  "label": 0,
  "label_name": "Likely Genuine Review",
  "confidence": 74.2,
  "confidence_level": "medium",
  "confidence_text": "Moderate confidence (74.2%)",
  "probabilities": {
    "genuine": 74.2,
    "potentially_fake": 25.8
  },
  "model_name": "Logistic Regression",
  "review_length": 105,
  "word_count": 18,
  "signals": [
    {
      "type": "natural",
      "severity": "info",
      "title": "Balanced Stylistic Profile",
      "description": "No abnormal punctuation, capitalization, or heavy promotional phrasing patterns detected."
    }
  ],
  "influential_terms": {
    "fake_influential": [],
    "genuine_influential": [
      {
        "term": "room",
        "contribution": -0.42,
        "impact": "pushes toward Genuine"
      }
    ]
  },
  "explanation_summary": "The linguistic characteristics align with typical truthful consumer reviews found in empirical benchmark corpora.",
  "disclaimer": "ReviewGuard AI provides automated predictions based on learned patterns in review data. Results are indicative and should not be treated as definitive proof of review fraud."
}
```

---

## 11. Limitations & Ethical Considerations

1. **Contextual Limitations:** The model evaluates linguistic and lexical patterns; it cannot verify whether the author physically visited a location or purchased an item.
2. **Domain Specificity:** The model is trained on hospitality and consumer product benchmarks. Performance may vary on non-English texts or specialized technical documentation.
3. **Short / Ambiguous Inputs:** Reviews consisting of only 2–3 words (e.g., *"Good product"*) provide minimal statistical signal, leading to lower model certainty.
4. **Ethical AI:** To prevent false accusations, the system uses responsible phrasing (*"Potentially Fake Review"*, *"Likely Genuine Review"*) rather than asserting guilt.

---

## 12. Future Scope

1. **Multilingual NLP:** Extend classification to non-English reviews using multilingual embeddings.
2. **Reviewer Metadata Fusion:** Integrate temporal review velocity, reviewer account age, and verified-purchase flags into a hybrid multi-modal architecture.
3. **Browser Extension:** Package ReviewGuard AI as a Chrome/Firefox extension for real-time Amazon, Flipkart, and Google Maps review auditing.
4. **Active Learning:** Implement human-in-the-loop review auditing for continuous model refinement.

---

## 13. License & Academic Attribution
- **Dataset:** Ott et al. Deceptive Opinion Spam Corpus, Cornell University.
- **Project License:** MIT License for academic and educational demonstration purposes.
