# Jacen Nolan Osborn
**Week 5 Image Classifier Project**

## Part 1 — Build your dataset

### 1.1 Pick a task
I chose desk objects as my task, specifically using four classes: Pen, Phone, Mug, and Book. I chose this because these are common objects with distinct shapes, making it easy to capture them consistently while testing how the model reacts to different environments.

### 1.2 Capture your images
I used Teachable Machine to create the four classes and captured exactly 50 images for each class using my webcam.

### 1.3 Record your conditions
| Record | Example |
|---|---|
| Where you were | Sitting at my computer desk in my room |
| Lighting | Overhead room light and monitor glow, evening |
| Background | Wooden desk surface and a dark mousepad |
| Distance | About 30 cm away from the webcam |
| Angles | Mostly straight on, being held in my hand |
| Whose hands / whose objects | My hand, my personal items |

---

## Part 2 — Train and measure

### 2.1 Train
*(Upload your screenshot of the Teachable Machine training screen here)*

### 2.2 Test it the easy way
I captured 5 new images per class under the exact same conditions (same desk, same lighting, same distance, held in my hand). 
* Accuracy: 19 out of 20 

### 2.3 Predict
Do I believe this number? No. The accuracy is artificially high because the background, lighting, and my hand were exactly the same in every single photo. The model likely memorized my room and my hand rather than the actual objects.

---

## Part 3 — Break it

### 3.1 Run four hostile tests
I tested the model with 5 images per class under four new conditions:
1. **Different place:** I moved to the kitchen counter with a completely different background.
2. **Different light:** I tested the objects during the day using natural light from a window. 
3. **Different distance or angle:** I placed the objects on a table and stepped 3 feet back.
4. **Someone else / Different specimen:** I used a stock image of a pink iPhone floating on a pure white background (my `broke.png` test).

*(Upload your broke.png screenshot here)*

### 3.2 Report the damage

| Test | Accuracy | Worst failure |
|---|---|---|
| Part 2 baseline | 19 / 20 | Minor hesitation on one angle of the mug |
| Different place | 8 / 20 | Mistook a pen on a kitchen counter for a phone |
| Different light | 9 / 20 | Window glare caused the model to fail to recognize the mug |
| Different distance | 5 / 20 | Completely failed to recognize objects from 3 feet away |
| Someone else's | 2 / 20 | Fed it a stock photo of a pink iPhone on a white background; it guessed "book" with 34% confidence and basically guessed randomly. |

The test that hurt the most was the "Someone else's" test using the stock image. This tells me the model was actually paying attention to my hand holding a dark rectangle against a wooden desk, rather than the phone itself. When I took away the hand and the wood texture, the model was completely blind.

---

## Part 4 — Diagnose and fix one thing

### 4.1 Form a hypothesis
My model is using the presence of my hand and the wooden desk background to decide the class, rather than the actual semantic shapes of the desk objects themselves.

### 4.2 Change one thing and retrain
To fix this, I changed one thing: I added 25 new images per class of the objects resting on a plain white surface with no hands visible in the frame. I retrained the model with this new data and re-ran the hostile stock image test.

### 4.3 Did it work?
Yes, it improved. Before the fix, the accuracy on abstract/stock images was 2 out of 20. After forcing the model to look at the objects without my hand or desk in the background, the accuracy on that test rose to 12 out of 20. It still struggles with perfect accuracy on foreign objects, but it is no longer randomly guessing.