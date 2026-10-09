import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, auc, classification_report

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    fillers = [r'\bum\b', r'\buh\b', r'\blike\b', r'\byou know\b', r'\bah\b']
    for filler in fillers:
        text = re.sub(filler, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_vectorizers(X_train_text, X_test_text):
    vectorization_dict = {}

    bow = CountVectorizer(ngram_range=(1, 2), max_features=5000)
    X_train_bow = bow.fit_transform(X_train_text)
    X_test_bow = bow.transform(X_test_text)
    vectorization_dict['Bag of Words'] = (X_train_bow, X_test_bow)

    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X_train_tfidf = tfidf.fit_transform(X_train_text)
    X_test_tfidf = tfidf.transform(X_test_text)
    vectorization_dict['TF-IDF'] = (X_train_tfidf, X_test_tfidf)

    if HAS_SENTENCE_TRANSFORMERS:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        X_train_sbert = model.encode(X_train_text.tolist(), show_progress_bar=False)
        X_test_sbert = model.encode(X_test_text.tolist(), show_progress_bar=False)
        vectorization_dict['SBERT Embeddings'] = (X_train_sbert, X_test_sbert)

    return vectorization_dict


def train_and_evaluate(df, text_col='sentence', label_col='label'):
    df['clean_text'] = df[text_col].apply(clean_text)
    
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df['clean_text'], 
        df[label_col], 
        test_size=0.2, 
        random_state=42, 
        stratify=df[label_col]
    )

    vectorized_data = get_vectorizers(X_train_text, X_test_text)

    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Multinomial Naive Bayes': MultinomialNB(),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42)
    }

    plt.figure(figsize=(12, 8))
    results = []

    for vec_name, (X_train_vec, X_test_vec) in vectorized_data.items():
        for clf_name, clf in classifiers.items():
            if clf_name == 'Multinomial Naive Bayes' and 'SBERT' in vec_name:
                continue

            clf.fit(X_train_vec, y_train)
            y_probs = clf.predict_proba(X_test_vec)[:, 1]

            fpr, tpr, _ = roc_curve(y_test, y_probs)
            roc_auc = auc(fpr, tpr)
            
            label_str = f"{clf_name} + {vec_name} (AUC = {roc_auc:.3f})"
            plt.plot(fpr, tpr, lw=2, label=label_str)

            results.append({
                'Vectorizer': vec_name,
                'Classifier': clf_name,
                'AUC': roc_auc
            })

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)', fontsize=12)
    plt.ylabel('True Positive Rate (TPR)', fontsize=12)
    plt.title('ROC Curves - Question Classification', fontsize=14)
    plt.legend(loc="lower right", fontsize=9)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('roc_curves_evaluation.png', dpi=300)
    plt.show()

    summary_df = pd.DataFrame(results).sort_values(by='AUC', ascending=False)
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    df_transcripts = pd.read_csv("transcript_data.csv")
    train_and_evaluate(df_transcripts, text_col='sentence', label_col='label')