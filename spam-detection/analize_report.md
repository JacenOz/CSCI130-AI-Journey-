# Spam Classifier Analysis Report

## Part 1: Data and Features
In addition to `word_count`, `exclamations`, `money_words`, and `all_caps`, I engineered two custom features:
1. **`link_count`**: The number of URLs ("http" or "www"). *Justification:* Spam and phishing emails rely heavily on directing victims to external malicious pages, creating a stark contrast with standard conversational ham.
2. **`urgent_words`**: Counts of words like "urgent", "immediate", "act now". *Justification:* Scammers manufacture artificial urgency to force users into making poor, unthinking decisions, a tactic rarely used with the same density in normal workplace or personal emails.

## Part 2: Model Training and Split Rationale
The dataset was divided into an 75% training set and a 25% test set. This split exists strictly to prevent the model from memorizing the data. Evaluating a model on the exact data it trained on tests its *recall*, resulting in artificially perfect scores. By holding out a test set, we force the model to prove it can *generalize* the rules of spam to emails it has never seen before. 

Our Random Forest classifier achieved a baseline test accuracy of **100%** (a suspicious figure that is unpacked in Part 3.6).

## Part 3: Evaluation and Interrogation

### Confusion Matrix, Precision, and Recall
* **True Negatives (Legit passed):** 21
* **False Positives (Legit flagged spam):** 0
* **False Negatives (Spam missed):** 0
* **True Positives (Spam caught):** 19

* **Precision (1.00)** means that when the model flags an email as spam, it is 100% correct. There are no false alarms.
* **Recall (1.00)** means that out of all actual spam in the dataset, the model successfully caught 100% of it.

### The Cost of Errors
A **False Positive** (a legitimate email wrongly marked as spam) is far worse than a **False Negative** (a spam email letting through). If a spam email hits the inbox, the user spends one second deleting it. If a job offer, a doctor's result, or an urgent client message hits the spam folder, the missed opportunity could be catastrophic. To shift the filter's balance to prefer False Negatives, I would increase the classification threshold (e.g., requiring a 90% confidence score to classify as spam rather than a simple >50% majority).

### Feature Importances
The model prioritized the features in this order:
1. `urgent_words` (Highest influence)
2. `money_words` 
3. `link_count`
4. `all_caps`
5. `exclamations`
6. `word_count` (Lowest influence)

This matches my intuition from Part 1. Generic metrics like `word_count` are noisy, while highly specific semantic markers like `urgent_words` and `money_words` carry the strongest, most direct signal of malicious intent.

### Adversarial Attacks
I wrote three emails to break the classifier:
1. **Spam masking as ham:** *"Hey Alice, please review the document here: http://docs.com"* -> Classified as **LEGIT** (Successfully fooled the model by using low spam signals despite the link).
2. **Ham masking as spam:** *"URGENT: I need the MONEY for the event immediately!!! BOB"* -> Classified as **SPAM** (Successfully fooled the model; flagged a panicked coworker as a scammer due to high caps and urgent words).
3. **Standard spam:** *"Click here for a limited time offer to save cash!"* -> Classified as **SPAM** (Caught correctly).

### Data Leakage
The 100% accuracy score is an illusion. Generating the dataset via variations meant I took 16 base emails and made 9 near-copies of each. The random Train/Test split scattered copies of the *exact same underlying emails* into both datasets. The leakage check proved that 16 out of 16 base emails in the test set had variations present in the training set. The model did not learn to identify spam; it effectively saw the exam paper in advance and memorized the 16 specific data profiles. I cannot trust this accuracy number for real-world application.

## Bonus: Keras Neural Network
I trained a small Sequential Keras neural network (Dense layers: 8 -> 4 -> 1) on the same features. The neural network achieved identical accuracy to the Random Forest model. On a dataset this small and tabular, the extra capacity of a deep learning model buys nothing. The simpler tree-based model trained faster, required no hyperparameter scaling, natively provided feature importances, and performed just as well—a common finding in structured data tasks.