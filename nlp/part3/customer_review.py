import os
import re
import warnings
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import spacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel, Word2Vec
from gensim.models.coherencemodel import CoherenceModel
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

warnings.filterwarnings("ignore", category=UserWarning)

RANDOM_STATE = 42
INPUT_FILE = "beauty_reviews.csv"
OUTPUT_DIR = "nlp_outputs"


def create_output_directory(output_dir=OUTPUT_DIR):
    """Create a folder for charts, tables, and other generated outputs."""
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_dataset(file_path):
    """Load and validate the CSV dataset."""
    df = pd.read_csv(file_path)

    required_columns = {"review_text", "sentiment"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    df = df[["review_text", "sentiment"]].copy()
    df["review_text"] = df["review_text"].fillna("").astype(str)
    df["sentiment"] = pd.to_numeric(df["sentiment"], errors="coerce")
    df = df.dropna(subset=["sentiment"])
    df = df[df["sentiment"].isin([0, 1])]
    df["sentiment"] = df["sentiment"].astype(int)
    df = df[df["review_text"].str.strip().ne("")].reset_index(drop=True)

    if len(df) < 10:
        raise ValueError("The dataset has too few valid reviews to run this pipeline.")

    print(f"Loaded {len(df):,} reviews.")
    print("Sentiment distribution:")
    print(df["sentiment"].value_counts().sort_index().rename(
        index={0: "Negative", 1: "Positive"}
    ))
    return df


def load_spacy_model():
    """Load the requested large English spaCy model."""
    try:
        return spacy.load("en_core_web_lg")
    except OSError as exc:
        raise OSError(
            "spaCy model en_core_web_lg is not installed. Run:\n"
            "python -m spacy download en_core_web_lg"
        ) from exc


def preprocess_texts(df, nlp, batch_size=64):
    """
    Create two token streams:
      1. pos_tokens: NOUN + ADJ only, lemmatised; for TF-IDF and LDA.
      2. w2v_tokens: all non-stopword alphabetic tokens, lemmatised, without POS filtering.
    NER later uses the original full review text, not either cleaned stream.
    """
    pos_stream = []
    w2v_stream = []

    texts = df["review_text"].tolist()
    for doc in nlp.pipe(texts, batch_size=batch_size):
        pos_tokens = []
        w2v_tokens = []

        for token in doc:
            lemma = token.lemma_.lower().strip()
            if (
                token.is_alpha
                and not token.is_stop
                and not token.is_punct
                and not token.is_space
                and len(lemma) > 1
            ):
                w2v_tokens.append(lemma)

                if token.pos_ in {"NOUN", "ADJ"}:
                    pos_tokens.append(lemma)

        pos_stream.append(pos_tokens)
        w2v_stream.append(w2v_tokens)

    df = df.copy()
    df["pos_tokens"] = pos_stream
    df["w2v_tokens"] = w2v_stream
    df["pos_text"] = df["pos_tokens"].apply(lambda tokens: " ".join(tokens))
    print("Text preprocessing complete: created both token streams.")
    return df


def extract_named_entities(df, nlp, output_dir=OUTPUT_DIR):
    """
    Run NER on the original, unfiltered review text.
    Keep entity labels useful for brands, products, and locations.
    Note: generic spaCy NER is not a dedicated beauty-brand/product detector,
    so some brand and product names may not be recognised.
    """
    accepted_labels = {"ORG", "PRODUCT", "GPE", "LOC", "FAC"}
    entity_counts = Counter()
    entity_sentiments = defaultdict(list)
    entity_types = defaultdict(Counter)

    for text, sentiment, doc in zip(
        df["review_text"],
        df["sentiment"],
        nlp.pipe(df["review_text"].tolist(), batch_size=64),
    ):
        seen_in_review = set()
        for ent in doc.ents:
            if ent.label_ not in accepted_labels:
                continue
            name = re.sub(r"\s+", " ", ent.text).strip(" .,:;!?")
            if len(name) < 2:
                continue
            key = name.casefold()
            entity_types[key][ent.label_] += 1
            if key not in seen_in_review:
                entity_counts[key] += 1
                entity_sentiments[key].append(int(sentiment))
                seen_in_review.add(key)

    if not entity_counts:
        print("No accepted named entities were detected by spaCy.")
        return pd.DataFrame(columns=["entity", "mentions", "mean_sentiment", "majority_type"])

    top_entities = entity_counts.most_common(20)
    rows = []
    for entity, count in top_entities:
        mean_sentiment = float(np.mean(entity_sentiments[entity]))
        majority_type = entity_types[entity].most_common(1)[0][0]
        rows.append({
            "entity": entity,
            "mentions": count,
            "mean_sentiment": mean_sentiment,
            "majority_type": majority_type,
        })

    entity_df = pd.DataFrame(rows)
    entity_df.to_csv(os.path.join(output_dir, "top_20_entities_sentiment.csv"), index=False)

    plot_df = entity_df.sort_values("mentions")
    plt.figure(figsize=(11, 8))
    plt.barh(plot_df["entity"], plot_df["mentions"])
    plt.xlabel("Number of reviews mentioning entity")
    plt.ylabel("Entity")
    plt.title("Top 20 Named Entities in Amazon Beauty Reviews")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_20_entities.png"), dpi=300)
    plt.close()

    plt.figure(figsize=(11, 8))
    sentiment_plot = entity_df.sort_values("mean_sentiment")
    plt.barh(sentiment_plot["entity"], sentiment_plot["mean_sentiment"])
    plt.axvline(0.5, linestyle="--", linewidth=1)
    plt.xlim(0, 1)
    plt.xlabel("Mean sentiment (0 = negative, 1 = positive)")
    plt.ylabel("Entity")
    plt.title("Mean Review Sentiment for Top 20 Entities")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_20_entities_mean_sentiment.png"), dpi=300)
    plt.close()

    print("\nTop 20 entities and mean sentiment:")
    print(entity_df.to_string(index=False))
    return entity_df


def build_tfidf_features(df, output_dir=OUTPUT_DIR):
    """Split the data and fit TF-IDF on training reviews only."""
    indices = np.arange(len(df))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=df["sentiment"],
    )

    vectorizer = TfidfVectorizer(
        lowercase=False,  # spaCy already lowercased and lemmatised the tokens
        max_features=20000,
        min_df=2,
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    train_texts = df.iloc[train_idx]["pos_text"]
    test_texts = df.iloc[test_idx]["pos_text"]

    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)
    y_train = df.iloc[train_idx]["sentiment"].to_numpy()
    y_test = df.iloc[test_idx]["sentiment"].to_numpy()

    split_df = pd.DataFrame({
        "row_index": np.concatenate([train_idx, test_idx]),
        "split": ["train"] * len(train_idx) + ["test"] * len(test_idx),
    })
    split_df.to_csv(os.path.join(output_dir, "train_test_split_indices.csv"), index=False)

    print(f"\nTF-IDF shape: train={X_train.shape}, test={X_test.shape}")
    print(f"Train reviews: {len(train_idx)}; held-out test reviews: {len(test_idx)}")
    return vectorizer, X_train, X_test, y_train, y_test, train_idx, test_idx


def plot_cosine_similarity_heatmap(df, vectorizer, output_dir=OUTPUT_DIR, sample_size=50):
    """Plot pairwise TF-IDF cosine similarities with sentiment labels on both axes."""
    n = min(sample_size, len(df))
    sample = df.sample(n=n, random_state=RANDOM_STATE)
    matrix = vectorizer.transform(sample["pos_text"])
    similarities = cosine_similarity(matrix)
    labels = sample["sentiment"].map({0: "Negative", 1: "Positive"}).tolist()
    tick_labels = [f"{i + 1}: {label}" for i, label in enumerate(labels)]

    plt.figure(figsize=(14, 12))
    sns.heatmap(
        similarities,
        cmap="viridis",
        vmin=0,
        vmax=1,
        xticklabels=tick_labels,
        yticklabels=tick_labels,
        cbar_kws={"label": "Cosine similarity"},
    )
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(rotation=0, fontsize=6)
    plt.title("TF-IDF Pairwise Cosine Similarity (review index and sentiment)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "tfidf_cosine_similarity_heatmap.png"), dpi=300)
    plt.close()

    # Quantitative check: compare within-label pairs against cross-label pairs.
    upper_i, upper_j = np.triu_indices(n, k=1)
    pair_sims = similarities[upper_i, upper_j]
    y = sample["sentiment"].to_numpy()
    same = y[upper_i] == y[upper_j]
    same_mean = float(pair_sims[same].mean()) if same.any() else float("nan")
    cross_mean = float(pair_sims[~same].mean()) if (~same).any() else float("nan")

    comparison = pd.DataFrame({
        "pair_type": ["Same sentiment", "Different sentiment"],
        "mean_cosine_similarity": [same_mean, cross_mean],
    })
    comparison.to_csv(os.path.join(output_dir, "cosine_similarity_label_check.csv"), index=False)
    print("\nCosine similarity validation:")
    print(comparison.to_string(index=False))
    if np.isfinite(same_mean) and np.isfinite(cross_mean):
        if same_mean > cross_mean:
            print("In this sample, same-sentiment pairs have higher mean similarity.")
        else:
            print("In this sample, same-sentiment pairs do NOT have higher mean similarity.")
            print("This is a diagnostic result, not a requirement that must always hold.")
    return comparison


def train_word2vec_and_embed(df, train_idx, vector_size=100):
    """Train Word2Vec on training reviews and average token vectors per document."""
    train_sentences = [
        tokens for tokens in df.iloc[train_idx]["w2v_tokens"].tolist() if tokens
    ]
    model = Word2Vec(
        sentences=train_sentences,
        vector_size=vector_size,
        window=5,
        min_count=2,
        workers=4,
        sg=1,
        seed=RANDOM_STATE,
        epochs=10,
    )

    embeddings = np.zeros((len(df), vector_size), dtype=np.float32)
    for row_idx, tokens in enumerate(df["w2v_tokens"]):
        vectors = [model.wv[word] for word in tokens if word in model.wv]
        if vectors:
            embeddings[row_idx] = np.mean(vectors, axis=0)

    return model, embeddings


def plot_pca_comparison(df, vectorizer, word2vec_embeddings, output_dir=OUTPUT_DIR):
    """Create 2-D PCA-style plots for TF-IDF (via TruncatedSVD) and Word2Vec."""
    labels = df["sentiment"].to_numpy()
    label_names = np.where(labels == 1, "Positive", "Negative")

    tfidf_matrix = vectorizer.transform(df["pos_text"])
    n_components = min(50, tfidf_matrix.shape[0] - 1, tfidf_matrix.shape[1] - 1)
    if n_components < 2:
        print("Not enough TF-IDF features for the requested SVD/PCA visualisation.")
        return

    svd = TruncatedSVD(n_components=n_components, random_state=RANDOM_STATE)
    tfidf_reduced = svd.fit_transform(tfidf_matrix)
    tfidf_2d = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(tfidf_reduced)
    w2v_2d = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(word2vec_embeddings)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for sentiment, color, label in [(0, "tab:blue", "Negative"), (1, "tab:orange", "Positive")]:
        mask = labels == sentiment
        axes[0].scatter(tfidf_2d[mask, 0], tfidf_2d[mask, 1], s=16, alpha=0.55,
                        c=color, label=label)
        axes[1].scatter(w2v_2d[mask, 0], w2v_2d[mask, 1], s=16, alpha=0.55,
                        c=color, label=label)
    axes[0].set_title("TF-IDF: TruncatedSVD to 50 dimensions, then PCA to 2-D")
    axes[1].set_title("Word2Vec: mean document vectors, then PCA to 2-D")
    for ax in axes:
        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "tfidf_vs_word2vec_pca.png"), dpi=300)
    plt.close()


def run_lda_topic_modeling(df, output_dir=OUTPUT_DIR):
    """Train LDA models for k=5, 7, 10 using a BoW corpus and select by c_v coherence."""
    token_lists = df["pos_tokens"].tolist()
    dictionary = Dictionary(token_lists)
    dictionary.filter_extremes(no_below=2, no_above=0.90, keep_n=30000)
    corpus = [dictionary.doc2bow(tokens) for tokens in token_lists]

    if len(dictionary) == 0 or not any(corpus):
        print("LDA skipped: the POS-filtered corpus has no usable vocabulary.")
        return None, None, None

    models = {}
    coherence_rows = []
    for k in (5, 7, 10):
        model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=k,
            random_state=RANDOM_STATE,
            passes=8,
            iterations=100,
            alpha="auto",
            eta="auto",
            eval_every=None,
        )
        coherence = CoherenceModel(
            model=model,
            texts=token_lists,
            dictionary=dictionary,
            coherence="c_v",
        ).get_coherence()
        models[k] = model
        coherence_rows.append({"num_topics": k, "coherence_cv": coherence})
        print(f"LDA k={k}: c_v coherence={coherence:.4f}")

    coherence_df = pd.DataFrame(coherence_rows).sort_values("coherence_cv", ascending=False)
    coherence_df.to_csv(os.path.join(output_dir, "lda_coherence_scores.csv"), index=False)
    best_k = int(coherence_df.iloc[0]["num_topics"])
    best_model = models[best_k]
    print(f"Selected LDA model: k={best_k} (highest c_v coherence)")

    # Save top words and create a word-cloud panel for every topic in the selected model.
    topic_terms = {}
    topic_rows = []
    for topic_id in range(best_k):
        terms = best_model.show_topic(topic_id, topn=15)
        topic_terms[topic_id] = dict(terms)
        words = [word for word, _ in terms]
        # Human-readable provisional label based on the leading terms; inspect and rename
        # these labels in the report after viewing the word clouds and example reviews.
        label = " / ".join(words[:3])
        topic_rows.append({
            "topic_id": topic_id,
            "human_readable_label": label,
            "top_words": ", ".join(words),
        })

    topics_df = pd.DataFrame(topic_rows)
    topics_df.to_csv(os.path.join(output_dir, "lda_topic_labels_and_words.csv"), index=False)

    cols = 3
    rows = int(np.ceil(best_k / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4.5 * rows))
    axes = np.array(axes).reshape(-1)
    for topic_id in range(best_k):
        wc = WordCloud(width=800, height=450, background_color="white")
        wc.generate_from_frequencies(topic_terms[topic_id])
        axes[topic_id].imshow(wc, interpolation="bilinear")
        axes[topic_id].axis("off")
        axes[topic_id].set_title(f"Topic {topic_id}: {' / '.join(list(topic_terms[topic_id])[:3])}")
    for unused in range(best_k, len(axes)):
        axes[unused].axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "lda_topic_wordclouds.png"), dpi=300)
    plt.close()

    # Dominant topic = topic with the highest posterior probability for each review.
    dominant_topics = []
    for bow in corpus:
        distribution = best_model.get_document_topics(bow, minimum_probability=0.0)
        dominant_topics.append(max(distribution, key=lambda item: item[1])[0])

    df = df.copy()
    df["dominant_topic"] = dominant_topics
    df[["review_text", "sentiment", "dominant_topic"]].to_csv(
        os.path.join(output_dir, "reviews_with_dominant_topic.csv"), index=False
    )

    # Proportion within each topic: positive and negative percentages sum to 100%.
    topic_sentiment = pd.crosstab(
        df["dominant_topic"], df["sentiment"], normalize="index"
    ).reindex(columns=[0, 1], fill_value=0)
    topic_sentiment = topic_sentiment.rename(
        columns={0: "negative_proportion", 1: "positive_proportion"}
    ).reset_index()
    topic_sentiment = topic_sentiment.merge(topics_df[["topic_id", "human_readable_label"]],
                                            left_on="dominant_topic", right_on="topic_id",
                                            how="left")
    topic_sentiment["negative_percent"] = 100 * topic_sentiment["negative_proportion"]
    topic_sentiment["positive_percent"] = 100 * topic_sentiment["positive_proportion"]
    topic_sentiment.to_csv(os.path.join(output_dir, "topic_sentiment_proportions.csv"), index=False)

    print("\nLDA topic labels:")
    print(topics_df.to_string(index=False))
    print("\nSentiment proportions by dominant topic:")
    print(topic_sentiment[["dominant_topic", "human_readable_label",
                           "negative_percent", "positive_percent"]].to_string(index=False))
    return best_model, dictionary, topic_sentiment


def train_and_evaluate_classifiers(X_train, X_test, y_train, y_test, output_dir=OUTPUT_DIR):
    """Train three required classifiers and compare metrics and ROC curves."""
    classifiers = {
        "MultinomialNB": MultinomialNB(),
        "BernoulliNB": BernoulliNB(),
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=RANDOM_STATE, class_weight=None
        ),
    }

    rows = []
    plt.figure(figsize=(9, 7))
    for name, model in classifiers.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        if hasattr(model, "predict_proba"):
            scores = model.predict_proba(X_test)[:, 1]
        else:
            scores = model.decision_function(X_test)

        rows.append({
            "classifier": name,
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1_score": f1_score(y_test, predictions, zero_division=0),
            "roc_auc": roc_auc_score(y_test, scores),
        })

        fpr, tpr, _ = roc_curve(y_test, scores)
        plt.plot(fpr, tpr, label=f"{name} (AUC={roc_auc_score(y_test, scores):.3f})")

        report = classification_report(y_test, predictions, zero_division=0)
        with open(os.path.join(output_dir, f"{name.lower().replace(' ', '_')}_report.txt"),
                  "w", encoding="utf-8") as file:
            file.write(f"Classifier: {name}\n\n{report}\n")
            file.write("Confusion matrix:\n")
            file.write(str(confusion_matrix(y_test, predictions)))

    plt.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves: TF-IDF Sentiment Classifiers")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classifier_roc_curves.png"), dpi=300)
    plt.close()

    results_df = pd.DataFrame(rows).sort_values("f1_score", ascending=False)
    results_df.to_csv(os.path.join(output_dir, "classifier_comparison.csv"), index=False)
    print("\nClassifier comparison:")
    print(results_df.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    return results_df


def save_summary_notes(results_df, coherence_df=None, output_dir=OUTPUT_DIR):
    """Save a short report template with interpretation prompts, not fabricated findings."""
    best_classifier = results_df.iloc[0]["classifier"] if not results_df.empty else "N/A"
    lines = [
        "AMAZON BEAUTY REVIEWS NLP PIPELINE — INTERPRETATION NOTES",
        "",
        f"Highest-F1 classifier in this run: {best_classifier}.",
        "",
        "Use the generated charts and CSV tables to write findings specific to this dataset.",
        "Do not claim same-sentiment TF-IDF pairs are more similar unless the measured result supports it.",
        "Review the LDA top words and representative reviews before finalising topic names.",
        "spaCy's general-purpose en_core_web_lg NER may miss beauty brands and product names.",
        "The mean sentiment for an entity is the average of binary labels among reviews mentioning it;",
        "values closer to 1 indicate more positive reviews and values closer to 0 indicate more negative reviews.",
        "",
        "Representation comparison:",
        "- TF-IDF represents word/ngram importance and often highlights specific review vocabulary.",
        "- Mean Word2Vec embeddings represent semantic similarity, but averaging loses word order and nuance.",
        "",
        "Limitations:",
        "- NER coverage depends on the general-purpose spaCy model and can be weak for product/brand names.",
        "- Topic labels are provisional labels based on leading terms and should be manually reviewed.",
        "- The test split is held out from supervised TF-IDF fitting and classifier training.",
    ]
    if coherence_df is not None and not coherence_df.empty:
        best = coherence_df.sort_values("coherence_cv", ascending=False).iloc[0]
        lines.insert(2, f"Highest LDA c_v coherence: k={int(best['num_topics'])}, "
                        f"score={best['coherence_cv']:.4f}.")
    with open(os.path.join(output_dir, "report_interpretation_notes.txt"), "w",
              encoding="utf-8") as file:
        file.write("\n".join(lines))


def main():
    """Run the full NLP pipeline in the requested analytical order."""
    create_output_directory()
    df = load_dataset(INPUT_FILE)
    nlp = load_spacy_model()

    # Stage 1: create the two required token streams.
    df = preprocess_texts(df, nlp)

    # Stage 2: NER uses the original full, unfiltered review text.
    extract_named_entities(df, nlp)

    # Stage 3: split first, then fit TF-IDF on training data only.
    vectorizer, X_train, X_test, y_train, y_test, train_idx, test_idx = build_tfidf_features(df)

    # Stage 4: similarity heatmap and label-pair diagnostic.
    plot_cosine_similarity_heatmap(df, vectorizer)

    # Stage 5: Word2Vec embeddings and 2-D representation comparison.
    w2v_model, w2v_embeddings = train_word2vec_and_embed(df, train_idx)
    w2v_model.save(os.path.join(OUTPUT_DIR, "beauty_reviews_word2vec.model"))
    np.save(os.path.join(OUTPUT_DIR, "word2vec_document_embeddings.npy"), w2v_embeddings)
    plot_pca_comparison(df, vectorizer, w2v_embeddings)

    # Stage 6: LDA on gensim BoW corpus, comparing k=5, 7, and 10 with c_v coherence.
    lda_model, dictionary, topic_sentiment = run_lda_topic_modeling(df)
    coherence_path = os.path.join(OUTPUT_DIR, "lda_coherence_scores.csv")
    coherence_df = pd.read_csv(coherence_path) if os.path.exists(coherence_path) else None

    # Stage 7: required supervised sentiment classifiers and evaluation.
    results_df = train_and_evaluate_classifiers(X_train, X_test, y_train, y_test)
    save_summary_notes(results_df, coherence_df)

    print(f"\nPipeline complete. Check the '{OUTPUT_DIR}' folder for charts, CSV tables, and reports.")


if __name__ == "__main__":
    main()
