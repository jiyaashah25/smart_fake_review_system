export interface TextSignal {
  type: string;
  severity: 'low' | 'medium' | 'high' | 'info';
  title: string;
  description: string;
}

export interface InfluentialTerm {
  term: string;
  contribution: number;
  impact: string;
}

export interface InfluentialTerms {
  fake_influential: InfluentialTerm[];
  genuine_influential: InfluentialTerm[];
}

export interface Probabilities {
  genuine: number;
  potentially_fake: number;
}

export interface PredictionResultData {
  prediction: 'genuine' | 'potentially_fake';
  label: 0 | 1;
  label_name: string;
  confidence: number;
  confidence_level: 'high' | 'medium' | 'low';
  confidence_text: string;
  probabilities?: Probabilities;
  model_name: string;
  review_length: number;
  word_count: number;
  signals: TextSignal[];
  influential_terms: InfluentialTerms;
  explanation_summary: string;
  disclaimer: string;
}


export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number | null;
  confusion_matrix: {
    true_negative: number;
    false_positive: number;
    false_negative: number;
    true_positive: number;
    raw_matrix: number[][];
  };
  support: {
    total_samples: number;
    genuine_count: number;
    fake_count: number;
  };
}

export interface ModelComparisonRecord {
  model_name: string;
  train_duration_sec: number;
  cv_accuracy_mean: number;
  cv_accuracy_std: number;
  cv_f1_mean: number;
  test_accuracy: number;
  test_precision: number;
  test_recall: number;
  test_f1_score: number;
  test_roc_auc: number | null;
}

export interface AnalyticsData {
  model_name: string;
  test_metrics: ModelMetrics;
  all_models_compared: ModelComparisonRecord[];
  dataset_info: {
    total_samples: number;
    train_samples: number;
    test_samples: number;
    genuine_samples: number;
    fake_samples: number;
    train_test_split: string;
    source: string;
  };
  confusion_matrix_url: string;
  roc_curve_url: string;
}

export interface HistoryItem {
  id: string;
  text: string;
  result: PredictionResultData;
  timestamp: string;
}
