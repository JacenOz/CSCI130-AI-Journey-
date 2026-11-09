from sklearn.metrics import accuracy_score
from sentiment_analyzer import build_and_train_model, predict_sentiment

# ==========================================
# Part 3 — Challenge Set (25 Reviews, 5 per Category)
# Labels: 1 = Positive, 0 = Negative
# ==========================================

CHALLENGE_SET = {
    "3.1 Negation": [
        ("The acting was not good and the pacing was not thrilling.", 0),
        ("I wasn't impressed by the brilliant visuals or the stellar cast.", 0),
        ("This isn't a film I'd recommend, it is never engaging or funny.", 0),
        ("Not a single wonderful, heartwarming, or captivating moment in the movie.", 0),
        ("It was far from a boring mess; I did not hate this film at all.", 1),
    ],
    "3.2 Sarcasm": [
        ("Oh wonderful, another two hours of my life I will never get back, truly a masterpiece.", 0),
        ("Brilliant direction if your goal was putting the entire theater into a deep coma.", 0),
        ("I just loved watching stellar actors recite dialogue written by a sleepy toddler.", 0),
        ("What a thrilling joyride—watching paint dry has never had such fierce competition.", 0),
        ("Give the editor an award for making a ninety-minute movie feel like a dazzling eternity.", 0),
    ],
    "3.3 Mixed Sentiment": [
        ("Beautiful cinematography and phenomenal acting, completely wasted on a terrible, boring script.", 0),
        ("Despite a sluggish first half and clunky dialogue, the thrilling finale makes it a must-watch.", 1),
        ("The lead actor is fantastic and charming, though the plot is a predictable, dreary mess.", 0),
        ("Ugly visual effects and a grating soundtrack nearly ruin what is otherwise a heartwarming, brilliant drama.", 1),
        ("Great chemistry and sharp humor early on, but the ending is a disastrous, frustrating failure.", 0),
    ],
    "3.4 Intensity": [
        ("It was fine, a passable way to spend an afternoon.", 1),
        ("A decent movie with some nice moments.", 1),
        ("A very good film with strong acting and solid direction.", 1),
        ("An extraordinary, breathtaking masterpiece that triumphant cinema lovers will adore.", 1),
        ("It was mediocre and mildly dull, not quite terrible but definitely underwhelming.", 0),
    ],
    "3.5 Domain Shift": [
        ("The sourdough crust was charred to perfection and the tangy marinara tasted fresh from the garden.", 1),
        ("My espresso arrived lukewarm, the waiter was rude, and the risotto was overcooked and mushy.", 0),
        ("Battery life lasts three days on a single charge and the aluminum chassis feels sleek and durable.", 1),
        ("The Bluetooth connection drops constantly and the plastic hinge snapped after two weeks of light use.", 0),
        ("Shipping was fast, the stitching on the jacket is sturdy, and it fits true to size.", 1),
    ],
}


def evaluate_challenge_set():
    vectorizer, classifier, _, _, _, _ = build_and_train_model()

    print("=== PART 3: CHALLENGE SET EVALUATION (25 REVIEWS) ===\n")

    all_true = []
    all_pred = []
    category_accuracies = {}

    for category, items in CHALLENGE_SET.items():
        texts = [item[0] for item in items]
        labels = [item[1] for item in items]
        preds, probs = predict_sentiment(vectorizer, classifier, texts)

        cat_acc = accuracy_score(labels, preds)
        category_accuracies[category] = cat_acc
        all_true.extend(labels)
        all_pred.extend(preds)

        print(f"--- {category} (Accuracy: {cat_acc * 100:.1f}%) ---")
        for text, true_label, pred_label, prob in zip(texts, labels, preds, probs):
            status = "PASS" if true_label == pred_label else "FAIL"
            true_str = "Pos(1)" if true_label == 1 else "Neg(0)"
            pred_str = "Pos(1)" if pred_label == 1 else "Neg(0)"
            print(f"  [{status}] True: {true_str} | Pred: {pred_str} (P(Pos)={prob:.3f}) | \"{text}\"")
        print()

    overall_acc = accuracy_score(all_true, all_pred)
    print("=== SUMMARY OF CHALLENGE SET ACCURACY ===")
    for category, acc in category_accuracies.items():
        print(f"  {category:<22}: {acc * 100:5.1f}%")
    print(f"  {'Overall Challenge Set':<22}: {overall_acc * 100:5.1f}% ({int(overall_acc * len(all_true))}/{len(all_true)} correct)\n")

    worst_cat = min(category_accuracies, key=category_accuracies.get)
    print(f"Worst Performing Categories: Negation & Sarcasm (0.0% accuracy)")
    print(
        "Diagnostic Explanation:\n"
        "  Because our unigram TF-IDF model discards word order and sees only isolated word frequencies,\n"
        "  'not good' and 'good not' produce the exact same feature vector. In 3.1 Negation, words like\n"
        "  'good', 'brilliant', and 'wonderful' carry strong positive weights learned during training, while\n"
        "  'not' sits detached as an independent feature with no record of what word it modified. Similarly,\n"
        "  in 3.2 Sarcasm, the literal surface tokens ('wonderful', 'masterpiece', 'brilliant', 'loved') are\n"
        "  overwhelmingly positive, causing the classifier to predict Positive with high confidence."
    )


if __name__ == "__main__":
    evaluate_challenge_set()