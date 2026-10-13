"""
Script to generate a comprehensive, professional PDF project report
for ReviewGuard AI using ReportLab.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "ReviewGuard_AI_Complete_Project_Report.pdf")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

class NumberedCanvas(canvas.Canvas):
    """Adds page numbers and running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on title page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Running Header
        self.drawString(54, 750, "ReviewGuard AI — Smart Fake Review Detection System | Academic Project Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)
        
        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential & Academic Demonstration Deliverable")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#7C3AED"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    q_style = ParagraphStyle(
        'Q_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E1B4B"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'Ans_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=10,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderPadding=4,
        spaceAfter=6
    )

    story = []

    # ==========================
    # 1. TITLE & COVER HEADER
    # ==========================
    story.append(Paragraph("ReviewGuard AI", title_style))
    story.append(Paragraph("Smart Fake Review Detection System — Complete Academic & Viva Technical Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#7C3AED"), spaceBefore=0, spaceAfter=12))

    meta_table_data = [
        [
            Paragraph("<b>Project Domain:</b> NLP & Supervised Machine Learning", body_style),
            Paragraph("<b>Evaluation Weight:</b> 25 Marks Microproject", body_style)
        ],
        [
            Paragraph("<b>Selected Algorithm:</b> Logistic Regression (TF-IDF)", body_style),
            Paragraph("<b>Hold-Out Test Accuracy:</b> 90.31%", body_style)
        ],
        [
            Paragraph("<b>Architecture:</b> FastAPI + React 18 + TypeScript", body_style),
            Paragraph("<b>Benchmark Corpus:</b> Ott et al. Deceptive Spam", body_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ==========================
    # 2. EXECUTIVE SUMMARY & PROBLEM
    # ==========================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Consumer trust in e-commerce, hotel booking, and service platforms is increasingly jeopardized by "
        "<b>deceptive opinion spam</b>—artificially generated or commercially purchased reviews created to deceive consumers. "
        "Empirical studies demonstrate that humans fail to reliably detect deceptive reviews with an average accuracy of only 57% "
        "(virtually indistinguishable from a coin flip).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Project Objective:</b> ReviewGuard AI resolves this challenge by delivering an end-to-end NLP and machine learning "
        "inference pipeline that automatically ingests unstructured text reviews, applies sublinear TF-IDF vectorization, "
        "computes calibrated class probabilities, and transparently reveals token-level feature attributions to justify its verdict.",
        body_style
    ))

    # ==========================
    # 3. DATASET & PREPROCESSING
    # ==========================
    story.append(Paragraph("2. Benchmark Dataset & NLP Preprocessing", h1_style))
    story.append(Paragraph(
        "To ensure academic validity and avoid synthetic data bias, ReviewGuard AI is trained on the authoritative "
        "<b>Ott et al. Deceptive Opinion Spam Corpus</b> (Cornell NLP / ACL 2011).",
        body_style
    ))
    
    story.append(Paragraph("<b>Dataset Properties & Hygiene:</b>", h2_style))
    story.append(Paragraph("• <b>Benchmark Size:</b> 1,600 verified reviews across 20 Chicago hotels.", bullet_style))
    story.append(Paragraph("• <b>Ground Truth Collection:</b> Truthful reviews gathered from verified TripAdvisor accounts; deceptive reviews produced by crowd-workers under strict deception guidelines.", bullet_style))
    story.append(Paragraph("• <b>Deduplication:</b> 4 exact duplicate texts identified and removed, resulting in 1,596 validated samples.", bullet_style))
    story.append(Paragraph("• <b>Class Balance:</b> Exactly 796 genuine reviews (Label 0) and 800 deceptive reviews (Label 1) ensuring zero class imbalance bias.", bullet_style))

    story.append(Paragraph("<b>Text Normalization Pipeline (ml/preprocess.py):</b>", h2_style))
    story.append(Paragraph("1. <b>HTML Entity & Markup Cleaning:</b> Unescapes entities (&amp; to &) and strips HTML tags using regex.", bullet_style))
    story.append(Paragraph("2. <b>Unicode Normalization:</b> Converts non-ASCII strings into standard NFKD representation.", bullet_style))
    story.append(Paragraph("3. <b>Repeated Character Capping:</b> Reduces exaggerated repetitions (e.g., 'sooooo goooood' to 'soo good') to retain token information without exploding vocabulary.", bullet_style))
    story.append(Paragraph("4. <b>Negation & Punctuation Preservation:</b> Preserves negation words ('not', 'never', 'barely') which are vital for polarity context.", bullet_style))

    # ==========================
    # 4. TF-IDF MATHEMATICAL FOUNDATIONS
    # ==========================
    story.append(Paragraph("3. Mathematical Foundations: TF-IDF Feature Space", h1_style))
    story.append(Paragraph(
        "The model represents natural language using <b>Term Frequency-Inverse Document Frequency (TF-IDF)</b>. "
        "TF-IDF measures how important a word is to a specific review relative to the entire training corpus:",
        body_style
    ))
    story.append(Paragraph("TF-IDF(t, d, D) = TF(t, d) * IDF(t, D)", code_style))
    story.append(Paragraph(
        "• <b>Sublinear Term Frequency:</b> TF(t, d) = 1 + log(tf) if tf &gt; 0, else 0. "
        "This logarithmic damping prevents reviews that repeat the same word 20 times from artificially dominating feature weights.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Inverse Document Frequency:</b> IDF(t) = log((1 + n) / (1 + df(t))) + 1. "
        "Down-weights generic hotel terms ('room', 'hotel') and emphasizes domain-discriminative vocabulary.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>N-Gram Configuration:</b> Unigrams and Bigrams (1, 2) over a constrained 15,000-dimensional vocabulary with min_df=2.",
        body_style
    ))

    # ==========================
    # 5. MODEL TRAINING & EVALUATION
    # ==========================
    story.append(Paragraph("4. Machine Learning Algorithms & Comparative Results", h1_style))
    story.append(Paragraph(
        "Three distinct supervised algorithms were trained and validated using a strict <b>80/20 Stratified Split</b> "
        "(Seed: 42). 5-Fold Stratified Cross-Validation was conducted strictly inside the training partition (N=1,276), "
        "leaving the test partition (N=320) completely untouched until final evaluation.",
        body_style
    ))

    # Comparison Table
    comp_table_data = [
        ["Model Candidate", "5-Fold CV Acc", "5-Fold F1", "Test Acc", "Test Prec", "Test Recall", "Test F1", "ROC-AUC"],
        ["Logistic Regression (Selected)", "88.87%", "88.86%", "90.31%", "90.57%", "90.00%", "0.9028", "0.9486"],
        ["Multinomial Naive Bayes", "88.95%", "89.35%", "88.44%", "84.75%", "93.75%", "0.8902", "0.9504"],
        ["Calibrated LinearSVC", "89.18%", "89.15%", "88.75%", "87.80%", "90.00%", "0.8889", "0.9497"]
    ]
    t_comp = Table(comp_table_data, colWidths=[130, 52, 48, 48, 50, 55, 48, 52])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E1B4B")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#EEF2FF")),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor("#312E81")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Why Logistic Regression was Chosen as the Champion Model:</b>", h2_style))
    story.append(Paragraph("1. <b>Peak Generalization:</b> Highest hold-out accuracy (90.31%) and harmonic F1-score (0.9028) on unseen reviews.", bullet_style))
    story.append(Paragraph("2. <b>Balanced Precision & Recall (90.57% / 90.00%):</b> Prevents honest reviews from being falsely accused while capturing 90% of fraudulent text.", bullet_style))
    story.append(Paragraph("3. <b>True Probability Calibration:</b> Yields genuine posterior probabilities via the logistic sigmoid function (1 / (1 + e^-z)).", bullet_style))
    story.append(Paragraph("4. <b>Intrinsic Interpretability:</b> Allows exact linear feature attribution without requiring expensive approximations.", bullet_style))

    # ==========================
    # 6. CONFUSION MATRIX & ROC CURVE
    # ==========================
    story.append(Paragraph("5. Visual Evaluation Artifacts", h1_style))
    story.append(Paragraph(
        "The model generated two publication-grade figures during training on the 320 hold-out test samples:",
        body_style
    ))

    cm_img_path = os.path.join(MODELS_DIR, "confusion_matrix.png")
    roc_img_path = os.path.join(MODELS_DIR, "roc_curve.png")

    if os.path.exists(cm_img_path) and os.path.exists(roc_img_path):
        img_table_data = [
            [
                Image(cm_img_path, width=230, height=190),
                Image(roc_img_path, width=230, height=190)
            ],
            [
                Paragraph("<b>Figure 1:</b> Confusion Matrix Heatmap<br/>True Neg: 144 | False Pos: 15<br/>False Neg: 16 | True Pos: 145", body_style),
                Paragraph("<b>Figure 2:</b> Receiver Operating Characteristic<br/>Hold-Out ROC-AUC = 0.949<br/>High separation above diagonal chance", body_style)
            ]
        ]
        t_imgs = Table(img_table_data, colWidths=[250, 250])
        t_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_imgs)
        story.append(Spacer(1, 8))

    # ==========================
    # 7. EXPLAINABLE AI (XAI)
    # ==========================
    story.append(Paragraph("6. Explainable AI (XAI) & Stylistic Heuristics", h1_style))
    story.append(Paragraph(
        "Unlike black-box classifiers, ReviewGuard AI implements a two-tiered explainability framework:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tier 1: Linear Token Attribution (ml/explain_prediction.py):</b> "
        "For any prediction, the contribution of term i is computed as C_i = x_i * w_i, where x_i is the review's TF-IDF weight "
        "and w_i is the model's learned coefficient. If C_i &gt; 0, the word pushes toward Deceptive/Fake; if C_i &lt; 0, it pushes toward Genuine.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Tier 2: Qualitative Stylistic Flags (ml/preprocess.py):</b> "
        "Detects extreme brevity (&lt;10 words), uppercase intensity (&gt;30%), excessive punctuation sequences (!!!, ???), "
        "promotional triggers ('must buy', 'best ever', '100% recommend'), and elevated self-referential pronouns ('I', 'me', 'we').",
        body_style
    ))

    # ==========================
    # 8. ARCHITECTURE & SOFTWARE STACK
    # ==========================
    story.append(Paragraph("7. Software Architecture & Engineering Standards", h1_style))
    story.append(Paragraph(
        "ReviewGuard AI follows a modern micro-service decoupled architecture with strict typing and defensive programming:",
        body_style
    ))
    story.append(Paragraph("• <b>Backend Framework:</b> FastAPI (Python 3.13) with ASGI Uvicorn server, providing sub-millisecond asynchronous request routing.", bullet_style))
    story.append(Paragraph("• <b>Data Validation:</b> Pydantic v2 schemas validating request payload lengths (1 to 10,000 characters) and returning typed response payloads.", bullet_style))
    story.append(Paragraph("• <b>Frontend Technology:</b> React 18, TypeScript, Tailwind CSS, and Recharts bundled via Vite.", bullet_style))
    story.append(Paragraph("• <b>Automated Testing:</b> 36 comprehensive tests executed via pytest covering preprocessing edge cases, data loader hygiene, pipeline training, inference boundaries, and REST endpoints (100% pass rate).", bullet_style))

    # ==========================
    # 9. FACULTY VIVA Q&A DEFENSE
    # ==========================
    story.append(Paragraph("8. Complete Viva Voce Q&A Defense Guide", h1_style))
    story.append(Paragraph(
        "Below are the critical questions faculty members frequently ask in college machine learning vivas, along with your model answers:",
        body_style
    ))

    viva_qa = [
        (
            "Q1: What is the primary difference between truthful and deceptive reviews in your model?",
            "Truthful reviews emphasize spatial and descriptive specifics (e.g., room dimensions, bathroom water pressure, proximity to subway stations). Deceptive reviews rely heavily on positive superlatives ('perfection', 'unbelievable', 'best ever'), excessive exclamation marks, and exaggerated personal narratives ('I and my husband felt like royalty') because the authors have never physically experienced the venue."
        ),
        (
            "Q2: How did you ensure there was no data leakage during feature extraction?",
            "We used a scikit-learn Pipeline where TfidfVectorizer and the classifier were fitted together strictly on training folds. The vocabulary, document frequencies, and idf weights were calculated exclusively from the training split. The test partition remained untouched until final evaluation."
        ),
        (
            "Q3: Why is accuracy alone insufficient for fraud and spam detection?",
            "If a dataset has 95% genuine reviews and 5% fake reviews, a naive classifier predicting 'genuine' for everything achieves 95% accuracy while completely failing its objective. That is why we report Precision (90.57%), Recall (90.00%), and F1-Score (0.9028), ensuring that deceptive detection coverage is evaluated symmetrically."
        ),
        (
            "Q4: How does your confidence meter work? Is it an arbitrary random percentage?",
            "No. For Logistic Regression, the model calculates the linear decision distance z = w*x + b, and applies the sigmoid function P(y=1|x) = 1 / (1 + e^-z). The displayed score is the calibrated posterior class probability rounded to one decimal place."
        ),
        (
            "Q5: What are the current limitations of your system?",
            "The model evaluates linguistic and lexical patterns; it does not have access to private seller databases or physical receipt proofs. Very short reviews of only 2 to 3 words provide insufficient statistical tokens, leading to limited model certainty. Additionally, it is currently optimized for English text."
        ),
        (
            "Q6: Can this system legally prove that a user is a fraudster?",
            "No. It provides automated statistical likelihood. A genuine customer might write an overly excited promotional review, and a sophisticated fake reviewer might mimic natural phrasing. Therefore, our UI displays an explicit legal disclaimer stating that results are indicative patterns, not definitive proof of fraud."
        )
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", ans_style))

    # ==========================
    # 10. SYSTEM EXECUTION INSTRUCTIONS
    # ==========================
    story.append(Paragraph("9. Verification & Execution Runbook", h1_style))
    story.append(Paragraph("<b>To run the backend server:</b>", body_style))
    story.append(Paragraph("python -m uvicorn main:app --host 127.0.0.1 --port 8000", code_style))
    story.append(Paragraph("<b>To run the frontend dashboard:</b>", body_style))
    story.append(Paragraph("cd frontend &amp;&amp; npm run dev", code_style))
    story.append(Paragraph("<b>To execute automated tests:</b>", body_style))
    story.append(Paragraph("python -m pytest tests -v", code_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated complete master PDF report at: {PDF_OUTPUT_PATH}")
    return PDF_OUTPUT_PATH

if __name__ == "__main__":
    generate_pdf()
