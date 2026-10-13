import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Target,
  Award,
  Layers,
  Database,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Info
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import { AnalyticsData } from '../types/review';
import { api } from '../services/api';
import { MetricsCard } from './MetricsCard';
import { LoadingAnimation } from './LoadingAnimation';

export const AnalyticsDashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getAnalytics();
      setData(response);
    } catch (err: any) {
      setError(err.message || 'Unable to load model analytics from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="bg-[#29212B] border border-[#493643] rounded-lg p-12 text-center shadow-sm">
        <LoadingAnimation message="Retrieving model evaluation report from backend..." />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-[#29212B] border border-[#493643] rounded-lg p-8 text-center shadow-sm">
        <AlertCircle className="w-8 h-8 text-[#E05A68] mx-auto mb-3" />
        <h3 className="text-base font-semibold text-[#FFF7F2] mb-1">
          Model Performance Report Unavailable
        </h3>
        <p className="text-xs text-[#C5B8C1] max-w-md mx-auto mb-4">
          {error || 'The model performance metrics could not be retrieved from the server.'}
        </p>
        <button
          onClick={fetchAnalytics}
          className="inline-flex items-center space-x-1.5 text-xs font-semibold px-4 py-2 rounded-md bg-[#E8A0B8] hover:bg-[#F3C4D5] text-[#171319] transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry request</span>
        </button>
      </div>
    );
  }

  const { test_metrics, all_models_compared, dataset_info, model_name } = data;
  const baseUrl = api.getBaseUrl();

  // Recharts Model Comparison Data Preparation
  const chartData = all_models_compared.map(m => ({
    name: m.model_name.replace('Calibrated ', '').replace(' Regression', ''),
    Accuracy: +(m.test_accuracy * 100).toFixed(1),
    F1_Score: +(m.test_f1_score * 100).toFixed(1),
    Precision: +(m.test_precision * 100).toFixed(1),
    Recall: +(m.test_recall * 100).toFixed(1),
  }));

  const cm = test_metrics.confusion_matrix;

  return (
    <div className="space-y-6">
      {/* Header Info Banner */}
      <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
        <div>
          <div className="flex items-center space-x-1.5 text-xs text-[#E8A0B8] font-medium uppercase tracking-wider mb-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Held-out Test Evaluation</span>
          </div>
          <h2 className="text-2xl font-bold text-[#FFF7F2]">
            Model Performance
          </h2>
          <p className="text-xs sm:text-sm text-[#C5B8C1] mt-1 max-w-2xl leading-relaxed">
            Evaluation on the held-out test set from the deceptive opinion spam benchmark ({dataset_info.test_samples} test reviews).
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-[#201921] p-3 rounded-md border border-[#493643] shrink-0">
          <Database className="w-4 h-4 text-[#E8A0B8]" />
          <div className="text-xs">
            <span className="text-[#C5B8C1] block">Trained Model</span>
            <span className="text-[#FFF7F2] font-semibold">{model_name}</span>
          </div>
        </div>
      </div>

      {/* 5 Core Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
        <MetricsCard
          title="Accuracy"
          value={`${(test_metrics.accuracy * 100).toFixed(1)}%`}
          subtitle={`(${dataset_info.test_samples} test reviews)`}
          description="Percentage of reviews in the hold-out test set correctly classified."
          icon={Award}
        />

        <MetricsCard
          title="Precision (Fake)"
          value={`${(test_metrics.precision * 100).toFixed(1)}%`}
          description="Of all reviews predicted as deceptive, the fraction that were actually deceptive."
          icon={Target}
        />

        <MetricsCard
          title="Recall (Fake)"
          value={`${(test_metrics.recall * 100).toFixed(1)}%`}
          description="Of all truly deceptive reviews in test set, the fraction detected."
          icon={TrendingUp}
        />

        <MetricsCard
          title="F1-Score"
          value={`${(test_metrics.f1_score * 100).toFixed(1)}%`}
          description="Harmonic mean balancing precision and recall for deceptive reviews."
          icon={Layers}
        />

        <MetricsCard
          title="ROC-AUC Score"
          value={test_metrics.roc_auc != null ? test_metrics.roc_auc.toFixed(3) : 'Unavailable'}
          subtitle="Area Under ROC"
          description="Class separability score across varied decision probability thresholds."
          icon={BarChart3}
        />
      </div>

      {/* Model Comparison Recharts Section */}
      <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 shadow-sm">
        <div className="mb-4">
          <h3 className="text-base font-semibold text-[#FFF7F2] flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-[#E8A0B8]" />
            <span>Algorithm Comparison: Hold-Out Benchmark Performance</span>
          </h3>
          <p className="text-xs text-[#C5B8C1] mt-0.5">
            Empirical test set comparison across Logistic Regression, Multinomial Naive Bayes, and Calibrated LinearSVC.
          </p>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#493643" />
              <XAxis dataKey="name" stroke="#C5B8C1" fontSize={12} tickLine={false} />
              <YAxis stroke="#C5B8C1" fontSize={12} domain={[75, 100]} tickLine={false} unit="%" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#201921',
                  borderColor: '#493643',
                  borderRadius: '0.375rem',
                  fontSize: '0.75rem',
                  color: '#FFF7F2',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.4)'
                }}
              />
              <Legend wrapperStyle={{ fontSize: '0.75rem', paddingTop: '8px' }} />
              <Bar dataKey="Accuracy" fill="#E8A0B8" radius={[2, 2, 0, 0]} />
              <Bar dataKey="F1_Score" fill="#B87591" radius={[2, 2, 0, 0]} />
              <Bar dataKey="Precision" fill="#52B788" radius={[2, 2, 0, 0]} />
              <Bar dataKey="Recall" fill="#E0A96D" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Confusion Matrix & ROC Curve */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Confusion Matrix Card */}
        <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-[#FFF7F2] flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-[#52B788]" />
                <span>Confusion Matrix Breakdown</span>
              </h3>
              <span className="text-xs text-[#C5B8C1]">
                {dataset_info.test_samples} Test Reviews
              </span>
            </div>

            {/* Matrix Numerical Grid */}
            <div className="grid grid-cols-2 gap-2.5 mb-4 text-center">
              <div className="p-3 rounded-md bg-[#201921] border border-[#493643]">
                <div className="text-lg font-bold text-[#52B788]">{cm.true_negative}</div>
                <div className="text-[10px] text-[#C5B8C1] uppercase font-semibold mt-0.5">
                  True Negatives (TN)
                </div>
                <span className="text-[10px] text-[#C5B8C1]/80">Genuine correctly labeled</span>
              </div>
              <div className="p-3 rounded-md bg-[#201921] border border-[#493643]">
                <div className="text-lg font-bold text-[#E05A68]">{cm.false_positive}</div>
                <div className="text-[10px] text-[#C5B8C1] uppercase font-semibold mt-0.5">
                  False Positives (FP)
                </div>
                <span className="text-[10px] text-[#C5B8C1]/80">Genuine mistaken for fake</span>
              </div>
              <div className="p-3 rounded-md bg-[#201921] border border-[#493643]">
                <div className="text-lg font-bold text-[#E0A96D]">{cm.false_negative}</div>
                <div className="text-[10px] text-[#C5B8C1] uppercase font-semibold mt-0.5">
                  False Negatives (FN)
                </div>
                <span className="text-[10px] text-[#C5B8C1]/80">Fake mistaken for genuine</span>
              </div>
              <div className="p-3 rounded-md bg-[#201921] border border-[#493643]">
                <div className="text-lg font-bold text-[#52B788]">{cm.true_positive}</div>
                <div className="text-[10px] text-[#C5B8C1] uppercase font-semibold mt-0.5">
                  True Positives (TP)
                </div>
                <span className="text-[10px] text-[#C5B8C1]/80">Fake correctly detected</span>
              </div>
            </div>
          </div>

          {/* Generated Confusion Matrix Plot */}
          <div className="rounded-md overflow-hidden border border-[#493643] bg-[#201921] p-2 text-center">
            <img
              src={`${baseUrl}/api/visualizations/confusion-matrix`}
              alt="Model Confusion Matrix Heatmap"
              className="w-full h-auto max-h-56 object-contain mx-auto rounded"
              loading="lazy"
            />
          </div>
        </div>

        {/* ROC Curve Card */}
        <div className="bg-[#29212B] border border-[#493643] rounded-lg p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-[#FFF7F2] flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-[#E8A0B8]" />
                <span>Receiver Operating Characteristic (ROC)</span>
              </h3>
              <span className="text-xs text-[#C5B8C1]">
                AUC: {test_metrics.roc_auc != null ? test_metrics.roc_auc.toFixed(3) : 'Unavailable'}
              </span>
            </div>

            <p className="text-xs text-[#C5B8C1] leading-relaxed mb-4">
              The ROC curve evaluates trade-offs between true positive rate and false positive rate across thresholds.
              An AUC of {test_metrics.roc_auc != null ? test_metrics.roc_auc.toFixed(3) : 'high score'} demonstrates strong discrimination on the Ott et al. benchmark test set.
            </p>
          </div>

          {/* Generated ROC Curve Plot */}
          <div className="rounded-md overflow-hidden border border-[#493643] bg-[#201921] p-2 text-center">
            <img
              src={`${baseUrl}/api/visualizations/roc-curve`}
              alt="Model Receiver Operating Characteristic (ROC) Curve"
              className="w-full h-auto max-h-56 object-contain mx-auto rounded"
              loading="lazy"
            />
          </div>
        </div>
      </div>

      {/* Dataset & Benchmark Information */}
      <div className="bg-[#201921] border border-[#493643] rounded-lg p-5 text-xs text-[#C5B8C1] space-y-2">
        <div className="flex items-center space-x-1.5 text-[#FFF7F2] font-semibold">
          <Info className="w-4 h-4 text-[#E8A0B8]" />
          <span>Dataset & Methodology Transparency</span>
        </div>
        <p className="leading-relaxed">
          <strong>Source: </strong> {dataset_info.source}. Total samples: {dataset_info.total_samples.toLocaleString()} balanced reviews
          ({dataset_info.genuine_samples.toLocaleString()} genuine, {dataset_info.fake_samples.toLocaleString()} deceptive).
          Partitioned into {dataset_info.train_samples.toLocaleString()} training reviews and {dataset_info.test_samples.toLocaleString()} holdout test reviews ({dataset_info.train_test_split}).
        </p>
        <p className="leading-relaxed">
          <strong>Disclaimer: </strong> Test set evaluation confirms accuracy on the benchmark corpus. Performance across commercial platforms may vary depending on review length, domain, and modern generative AI styles.
        </p>
      </div>
    </div>
  );
};
