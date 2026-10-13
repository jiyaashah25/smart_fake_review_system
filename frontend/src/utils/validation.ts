export interface ValidationResult {
  isValid: boolean;
  error?: string;
  wordCount: number;
  charCount: number;
}

export const validateReviewText = (text: string, maxLength: number = 10000): ValidationResult => {
  const trimmed = text.trim();
  const charCount = trimmed.length;
  const words = trimmed.length > 0 ? trimmed.split(/\s+/).filter(Boolean) : [];
  const wordCount = words.length;

  if (charCount === 0) {
    return {
      isValid: false,
      error: 'Review text cannot be empty. Please enter a review to analyze.',
      wordCount: 0,
      charCount: 0,
    };
  }

  if (charCount > maxLength) {
    return {
      isValid: false,
      error: `Review text exceeds the maximum limit of ${maxLength.toLocaleString()} characters.`,
      wordCount,
      charCount,
    };
  }

  return {
    isValid: true,
    wordCount,
    charCount,
  };
};
