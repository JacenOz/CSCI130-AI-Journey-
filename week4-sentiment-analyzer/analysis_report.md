# Sentiment Analyzer Evaluation & Linguistic Failure Analysis

## 1. Held-Out Test Set vs. Challenge Set Accuracy

On the standard held-out test set (24 reviews stratified 50/50 from the same distribution as the 96 training reviews), the unigram TF-IDF + Logistic Regression model achieved **100.0% accuracy (24/24)** with zero false positives and zero false negatives:

| Metric / DatasetSubset | Sample Size | Accuracy | Key Observation |
| :--- | :---: | :---: | :--- |
| **Held-Out Test Set** | 24 | **100.0%** | High lexical overlap with training data; straightforward polarity. |
| **3.1 Negation** | 5 | **0.0%** | Inverted polarity words ("not good", "not hate") completely fool the model. |
| **3.2 Sarcasm** | 5 | **0.0%** | Literal positive tokens ("wonderful", "masterpiece") override negative intent. |
| **3.3 Mixed Sentiment** | 5 | **40.0%** | Whichever clause has more known training words wins, ignoring discourse structure. |
| **3.4 Intensity** | 5 | **60.0%** | Strong words ("extraordinary") score `P(Pos)=0.761`, while mild out-of-vocabulary words ("fine", "mediocre") hover near `P(Pos)=0.500`. |
| **3.5 Domain Shift** | 5 | **40.0%** | Food and hardware terms ("sourdough", "risotto", "Bluetooth") are out-of-vocabulary (OOV), collapsing predictions toward random chance. |
| **Overall Challenge Set** | **25** | **28.0%** | **72.0 percentage-point drop** from the in-distribution test set. |

This gap illustrates why held-out test accuracy is an optimistic illusion when train and test splits come from the same clean pool: the model memorizes single-word correlations rather than understanding compositional English.

---

## 2. Which Linguistic Phenomenon Hurt Most and Why

**Negation (0.0%)** and **Sarcasm (0.0%)** broke the classifier hardest, flipping every single prediction to the opposite class.

The root cause traces directly back to what the model actually sees: **a unigram TF-IDF vectorizer converts a review into an unordered bag of isolated word counts, discarding all syntax and word order before the classifier ever sees the input.** 

* **Why Negation Fails:** To a bag-of-words model, `"not good"` and `"good not"` are mathematically identical vectors. The token `not` is recorded as present in the document, but nothing binds it to `good`, `thrilling`, or `recommend`. Because words like `brilliant`, `stellar`, and `wonderful` carry large positive coefficients from the training set (and `hate` or `boring` carry large negative coefficients in `"did not hate"`), the model sums the isolated weights of those adjectives and predicts the exact opposite of the sentence's meaning. The model is not malfunctioning; the feature representation stripped away the structural link between the negator and its target.
* **Why Sarcasm Fails:** Sarcasm relies on a mismatch between literal lexical polarity and pragmatic intent. In `"Oh wonderful, another two hours of my life I will never get back, truly a masterpiece"`, the model only sees known positive unigrams (`wonderful`, `truly`, `masterpiece`) while the pragmatic punchline (`two hours... never get back`) consists of neutral or out-of-vocabulary tokens.
* **Intensity & Domain Shift Observations:** Even when the model gets positive reviews right in **3.4 Intensity**, its predicted probabilities show how brittle unigram matching is: `"extraordinary, breathtaking masterpiece"` achieves `P(Pos) = 0.761`, whereas `"It was fine, a passable way to spend an afternoon"` drops to `P(Pos) = 0.500` because mild qualifiers (`fine`, `passable`, `mediocre`) did not appear in the training vocabulary. The exact same out-of-vocabulary failure hits **3.5 Domain Shift**, where restaurant and electronics reviews (`sourdough`, `risotto`, `Bluetooth`, `hinge`) produce nearly empty feature vectors.

---

## 3. Fixing Negation: Architectural Trade-Offs

To fix negation, the feature representation must preserve local word order so the model knows *which* word is being negated. There are two primary approaches:

1. **Adding Bigrams/Trigrams (`ngram_range=(1, 2)` or `(1, 3)`):** This creates composite features like `"not good"`, `"not thrilling"`, and `"not hate"` as distinct vocabulary entries separate from `"good"` and `"not"`.
2. **Sequence Models (e.g., BiLSTM or Transformer/BERT):** These read tokens sequentially using recurrence or self-attention, allowing a negation token to modulate the representation of downstream words even across long clauses (e.g., `"not a single wonderful, heartwarming, or captivating moment"`).

**What I Would Try First and What It Costs:**
I would first switch the TF-IDF vectorizer to **unigrams + bigrams (`ngram_range=(1, 2)`) paired with sublinear term scaling (`sublinear_tf=True`)**. It requires a one-line code change, keeps inference latency under a millisecond, and immediately separates `"not good"` from `"good"`. 

**The Cost:**
* **Feature Space Explosion & Sparsity:** Moving from unigrams ($|V|$ features) to bigrams expands the vocabulary toward $|V|^2$ potential pairs, dramatically increasing memory usage and vector sparsity.
* **Data Hunger & Overfitting:** The model now must see `"not good"`, `"not great"`, and `"not entertaining"` explicitly in the training data to learn negative weights for each pair; unseen negated adjectives still fail.
* **Long-Range Blindness:** Bigrams still fail when words intervene between the negator and the adjective (e.g., `"not a single wonderful, heartwarming, or captivating moment"`, where `"not a"` is the bigram and `"heartwarming"` remains detached). Fixing long-range negation requires a pretrained Transformer, which costs orders of magnitude more compute, memory, and inference latency.

---

## 4. Deployment Verdict: Routing Angry Customers

**I would not deploy this model in production to route customer support tickets.** If a company used this analyzer to flag negative messages and route angry customers to a human agent, **sarcastic and negated complaints would be misclassified as glowing praise and silently ignored.** A furious customer writing, *"Oh wonderful, my package is lost for the third time—truly brilliant service!"* or *"I am not happy with how my billing issue was handled"* would be scored as Positive by the model and sent to an automated "Thank you for your feedback!" queue instead of a human representative. Leaving the angriest, most exasperated customers trapped in an automated loop—or worse, thanking them for their "positive" review—turns a recoverable service failure into permanent customer churn. Before deployment, the system would require at least a pretrained sequence classifier (such as a fine-tuned RoBERTa model) capable of handling negation and pragmatic context, combined with a confidence-threshold fallback that routes ambiguous or mixed-polarity messages directly to human triage.