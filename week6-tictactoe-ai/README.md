# Week 6 — Tic-Tac-Toe Q-Learning AI
**Name:** Jacen Osborn

---

## Part 1 — The Game Engine

1. **Why does `play()` build a new string instead of changing the old one?**
   Python strings are immutable, and the Q-table uses board strings as dictionary keys. Building a new string keeps the previous board state intact so `update()` can still look up `Q[board][action]` without corrupting the key or overwriting the old state.
2. **What do the four return values of `winner()` mean to the agent?**
   * `'X'` — The agent won; the episode ends and it gets `REWARD_WIN`.
   * `'O'` — The agent lost; the episode ends and it gets `REWARD_LOSS`.
   * `'draw'` — The board is full with no winner; the episode ends and it gets `REWARD_DRAW`.
   * `None` — The game is still going; the agent gets `0.0` immediate reward and keeps playing.
3. **How many squares does `moves()` return on an empty board, and how many after four turns?**
   **9** squares on an empty board, and **5** squares after four turns (four marks placed, five empty spaces left).

---

## Part 2.2 — Reward Choices

* `REWARD_WIN = 1.0` — Gives the agent a clear positive goal to chase.
* `REWARD_LOSS = -1.0` — Penalizes losing so the agent learns to block threats instead of treating a loss the same as an unfinished move.
* `REWARD_DRAW = 0.2` — Treats a draw as slightly better than losing (so the agent will still defend if it can't win), but much worse than winning so it still plays aggressively.

---

## Part 3 — Training & Measurement

### 3.1 Baseline Before Training
* **Baseline (0 games):** *[Paste your Win / Draw / Loss % from Cell 3]*
* **Why does a random player win more than half the time?**
  Because **X goes first**. Going first gives X up to 5 moves compared to O's 4, meaning X always gets the first chance to complete a three-in-a-row before O can.

### 3.2 Training Results
*[Paste the Markdown table printed by Cell 3 here]*

### 3.3 Reading the Curve
Almost all of the improvement happens in the **first 5,000 games** (jumping from ~58% to ~95%+). After 10,000 games, the curve flattens out completely. The last 40,000 games only squeeze out an extra 1–2% because the agent has already seen almost every common position a random opponent can create and is just fine-tuning rare edge cases.

---

## Part 4 — Beat It

### 4.1 Playing Against the Agent
* **My 5-game record as O:** *[e.g., Agent (X): 1 | Me (O): 3 | Draws: 1]*
* *[Add one honest sentence about how the games went—e.g., once I blocked its usual opening or set up a fork, it made weird moves and let me win.]*

### 4.2 How Many Positions Does It Know?
* **Positions in my Q-table:** *[Paste your `len(Q)` number from Cell 3]* out of 5,478 legal Tic-Tac-Toe positions.
* **Where did the other positions go?**
  First, the agent only stores boards where it is **X's turn** (it never stores O's turn or terminal boards). Second, because it only trained against a **random** opponent, it rarely—or never—saw board states that only happen when O plays smartly (like blocking two-in-a-rows, setting up forks, or forcing tight defensive lines).

### 4.3 Explaining the Gap
Winning 98% against a random opponent and losing to a human are both true because **the agent only learned how to beat a random player, not how to play Tic-Tac-Toe**. Against a random opponent, O rarely blocks or sets up traps, so X learns aggressive moves that work against careless play. When a human blocks those lines and sets up a fork, the agent lands on board positions it has barely seen (or never seen at all) and has no idea how to defend.

This is the exact same failure we saw earlier in the term with supervised models—like a classifier that works great on your own desk and fails everywhere else, or a model that confuses shirts with coats. **A model only learns the distribution it was trained on.** When the real world (a smart human opponent) looks different from the training data (a random opponent), performance collapses.