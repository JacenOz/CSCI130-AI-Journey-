import re
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# ==========================================
# Part 1 — Data and Setup
# ==========================================

# Balanced corpus of 120 labeled movie reviews (1 = Positive, 0 = Negative)
RAW_DATA = [
    # Positive Reviews (60)
    ("A breathtaking masterpiece with brilliant acting and a gripping plot.", 1),
    ("I loved every minute of this wonderful film, truly extraordinary.", 1),
    ("Fantastic direction and superb performances from the entire cast.", 1),
    ("An uplifting, heartwarming story that left me smiling for hours.", 1),
    ("Clever script, sharp dialogue, and stunning cinematography throughout.", 1),
    ("One of the best movies I have seen this year, highly recommend.", 1),
    ("Engaging from start to finish with a deeply satisfying ending.", 1),
    ("The lead actor delivered a phenomenal, career-defining performance.", 1),
    ("Beautifully shot and emotionally resonant, a true cinematic triumph.", 1),
    ("Brilliant pacing and an unforgettable soundtrack make this a must-watch.", 1),
    ("Fresh, original, and thoroughly entertaining cinema.", 1),
    ("A joy to watch with great chemistry between the main characters.", 1),
    ("Smart, funny, and genuinely touching in all the right places.", 1),
    ("Incredible visual effects paired with a strong, heartfelt narrative.", 1),
    ("A triumphant film that exceeds every expectation.", 1),
    ("Superb storytelling and top-notch production values.", 1),
    ("Captivating drama with nuanced, believable characters.", 1),
    ("Delightful comedy that keeps the laughs coming non-stop.", 1),
    ("A powerful and moving experience that stays with you.", 1),
    ("Masterful suspense that kept me on the edge of my seat.", 1),
    ("Exquisite art direction and a wonderful score elevate this film.", 1),
    ("A stellar cast brings this fascinating story to life.", 1),
    ("Warm, witty, and wonderfully directed from beginning to end.", 1),
    ("An absolute gem of a movie with heart and soul.", 1),
    ("Thrilling action sequences backed by genuine emotional depth.", 1),
    ("Remarkable debut from a talented director, truly impressive.", 1),
    ("Inspiring and entertaining, a perfect family film.", 1),
    ("Richly detailed world-building and fantastic character arcs.", 1),
    ("A brilliant adaptation that honors the source material.", 1),
    ("Pure cinematic magic, I was completely enchanted.", 1),
    ("Exceptionally well-written with zero dull moments.", 1),
    ("A tour de force of modern filmmaking, simply amazing.", 1),
    ("Hilarious, charming, and endlessly rewatchable.", 1),
    ("Deeply moving performances make this drama unforgettable.", 1),
    ("Gorgeous visuals and a hauntingly beautiful melody.", 1),
    ("A triumph of independent cinema, bold and visionary.", 1),
    ("Riveting plot twists that actually make sense and satisfy.", 1),
    ("Excellent pacing keeps the tension high and the audience hooked.", 1),
    ("Heartfelt and authentic, a truly wonderful viewing experience.", 1),
    ("First-rate entertainment with a brilliant ensemble cast.", 1),
    ("Radiant performances and a script full of warmth and wit.", 1),
    ("A dazzling spectacle that never loses sight of its characters.", 1),
    ("Profound, poetic, and visually arresting from frame one.", 1),
    ("An exhilarating ride that delivers on every single promise.", 1),
    ("Tender, insightful, andacted with extraordinary grace.", 1),
    ("A masterclass in tension, pacing, and atmospheric storytelling.", 1),
    ("Infectiously fun with a soundtrack you will hum for weeks.", 1),
    ("Sharp, timely, and brilliantly executed by the whole crew.", 1),
    ("A soaring achievement that reminds you why movies matter.", 1),
    ("Genuine laughs and earned tears, a wonderful balance.", 1),
    ("Impressive craftsmanship in every department, loved it.", 1),
    ("Vibrant, energetic, and packed with memorable moments.", 1),
    ("A richly rewarding drama with stellar lead work.", 1),
    ("Charming, inventive, and an absolute pleasure to watch.", 1),
    ("Compelling story told with clarity, passion, and skill.", 1),
    ("Great fun, wonderful cast, and a thoroughly satisfying finale.", 1),
    ("Bold storytelling that pays off in a spectacular way.", 1),
    ("Sublime acting and crisp editing make this a winner.", 1),
    ("A standout film that deserves all the praise it gets.", 1),
    ("Magnificent cinema, thrilling and deeply affecting.", 1),

    # Negative Reviews (60)
    ("A boring, predictable mess with terrible acting and a weak script.", 0),
    ("I hated this awful film, a complete waste of two hours.", 0),
    ("Poor direction and wooden performances from the entire cast.", 0),
    ("A dreary, lifeless story that put me to sleep.", 0),
    ("Clumsy dialogue,笨拙 pacing, and ugly cinematography throughout.", 0),
    ("One of the worst movies I have seen this year, avoid at all costs.", 0),
    ("Tedious from start to finish with a frustratingly dumb ending.", 0),
    ("The lead actor delivered a flat, uninspired performance.", 0),
    ("Sloppily edited and emotionally hollow, a total cinematic failure.", 0),
    ("Awful pacing and an annoying soundtrack make this unwatchable.", 0),
    ("Derivative, unoriginal, and thoroughly painful cinema.", 0),
    ("A chore to watch with zero chemistry between the main characters.", 0),
    ("Dull, unfunny, and cringeworthy in every single scene.", 0),
    ("Cheap visual effects paired with a messy, incoherent narrative.", 0),
    ("A disastrous film that fails every expectation.", 0),
    ("Lazy storytelling and bottom-of-the-barrel production values.", 0),
    ("Boring drama with cardboard, unbelievable characters.", 0),
    ("Painful comedy that fails to land a single joke.", 0),
    ("A shallow and forgettable experience that leaves you annoyed.", 0),
    ("Zero suspense, I was checking my watch the entire time.", 0),
    ("Tacky art direction and a grating score ruin this film.", 0),
    ("A wasted cast struggles through this incoherent story.", 0),
    ("Cold, pretentious, and poorly directed from beginning to end.", 0),
    ("An absolute disaster of a movie with no heart or soul.", 0),
    ("Confusing action sequences backed by zero emotional depth.", 0),
    ("Amateurish debut from a clueless director, truly dreadful.", 0),
    ("Bland and exhausting, a terrible excuse for entertainment.", 0),
    ("Thin world-building and nonsensical character motivations.", 0),
    ("A butchered adaptation that ruins the source material.", 0),
    ("Pure cinematic torture, I was completely miserable.", 0),
    ("Horribly written with endless dull and pointless scenes.", 0),
    ("A trainwreck of modern filmmaking, simply atrocious.", 0),
    ("Obnoxious, charmless, and painfully repetitive.", 0),
    ("Wooden performances make this drama a complete slog.", 0),
    ("Murky visuals and a repetitive, headache-inducing noise.", 0),
    ("A failure of independent cinema, indulgent and messy.", 0),
    ("Ridiculous plot holes that insult the audience's intelligence.", 0),
    ("Sluggish pacing drains all tension and bores the viewer.", 0),
    ("Fake and manipulative, a truly awful viewing experience.", 0),
    ("Third-rate entertainment with a sleepwalking ensemble cast.", 0),
    ("Lifeless performances and a script full of clichés and groans.", 0),
    ("A bloated spectacle that forgets to tell a coherent story.", 0),
    ("Shallow, pretentious, and visually ugly from frame one.", 0),
    ("An exhausting slog that breaks every single promise.", 0),
    ("Clunky, tone-deaf, and acted with shocking incompetence.", 0),
    ("A masterclass in boredom, bad editing, and incoherent plotting.", 0),
    ("Gratingly loud with a soundtrack that gives you a migraine.", 0),
    ("Dull, dated, and incompetently executed by the whole crew.", 0),
    ("A dismal failure that makes you regret buying a ticket.", 0),
    ("Forced jokes and unearned melodrama, a terrible combination.", 0),
    ("Shoddy craftsmanship in every department, hated it.", 0),
    ("Flat, lethargic, and packed with尷尬 awkward moments.", 0),
    ("A punishingly dull drama with abysmal lead work.", 0),
    ("Charmless, derivative, and an absolute chore to sit through.", 0),
    ("Incoherent story told with confusion, laziness, and ineptitude.", 0),
    ("Zero fun, miscast actors, and a thoroughly insulting finale.", 0),
    ("Cowardly storytelling that collapses in a spectacular way.", 0),
    ("Abysmal acting and choppy editing make this a loser.", 0),
    ("A forgettable flop that deserves all the criticism it gets.", 0),
    ("Dreadful cinema, boring and deeply frustrating.", 0),
]


def preprocess_text(text: str) -> str:
    """Lowercases text and removes punctuation while keeping words intact."""
    text = text.lower()
    # Expand common contractions so negation tokens like 'not' are explicit
    text = re.sub(r"n't\b", " not", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_and_train_model():
    """Splits data, vectorizes with unigram TF-IDF, and trains Logistic Regression."""
    texts = [preprocess_text(item[0]) for item in RAW_DATA]
    labels = [item[1] for item in RAW_DATA]

    # Split 80% training, 20% test, stratified to preserve class balance
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )

    # Unigram TF-IDF Vectorizer (no stop_words removal so 'not' stays in vocabulary)
    vectorizer = TfidfVectorizer(ngram_range=(1, 1))
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)

    classifier = LogisticRegression(random_state=42)
    classifier.fit(X_train, y_train)

    return vectorizer, classifier, X_train_raw, X_test_raw, y_train, y_test


def predict_sentiment(vectorizer, classifier, raw_reviews):
    """Returns predicted labels (0 or 1) and positive class probabilities."""
    cleaned = [preprocess_text(r) for r in raw_reviews]
    features = vectorizer.transform(cleaned)
    preds = classifier.predict(features)
    probs = classifier.predict_proba(features)[:, 1]
    return preds, probs


if __name__ == "__main__":
    vectorizer, classifier, X_train_raw, X_test_raw, y_train, y_test = build_and_train_model()

    total_counts = Counter([label for _, label in RAW_DATA])
    train_counts = Counter(y_train)
    test_counts = Counter(y_test)

    print("=== PART 1: DATA AND CLASS DISTRIBUTION ===")
    print(f"Total dataset size: {len(RAW_DATA)} reviews")
    print(f"  - Positive (1): {total_counts[1]} ({total_counts[1]/len(RAW_DATA)*100:.1f}%)")
    print(f"  - Negative (0): {total_counts[0]} ({total_counts[0]/len(RAW_DATA)*100:.1f}%)")
    print(f"Training set: {len(y_train)} reviews (Positive: {train_counts[1]}, Negative: {train_counts[0]})")
    print(f"Test set:     {len(y_test)} reviews (Positive: {test_counts[1]}, Negative: {test_counts[0]})")
    print(
        "Class balance note: The dataset is strictly balanced (50.0% Positive / 50.0% Negative), "
        "preventing majority-class guessing from inflating accuracy.\n"
    )

    # Evaluate on held-out test set
    X_test_vec = vectorizer.transform(X_test_raw)
    y_pred = classifier.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("=== PART 2: HELD-OUT TEST SET EVALUATION ===")
    print(f"Test Set Accuracy: {acc * 100:.2f}% ({int(acc * len(y_test))}/{len(y_test)} correct)\n")
    print("Confusion Matrix (Rows = Actual, Columns = Predicted):")
    print("                 Pred Neg (0)   Pred Pos (1)")
    print(f"Actual Neg (0)       {cm[0][0]:>4}           {cm[0][1]:>4}")
    print(f"Actual Pos (1)       {cm[1][0]:>4}           {cm[1][1]:>4}\n")

    print("=== WHAT THE MODEL ACTUALLY SEES ===")
    print(
        "With a unigram TF-IDF representation, the model sees only an unordered bag of isolated word "
        "frequencies weighted by rarity—discarding all word order, syntax, and grammatical attachments."
    )