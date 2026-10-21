# Author: Jacen Nolan Osborn
# Date: October 21, 2026
# CSCI 130 - Week 1 Project: Simple Reflex Agent

import datetime
import random

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def get_ai_fact():
    facts = [
        "The term 'Artificial Intelligence' was coined in 1956 at Dartmouth College.",
        "ELIZA, one of the first chatbots, was created in the 1960s to simulate a psychotherapist.",
        "The concept of neural networks is inspired by the human brain's architecture.",
        "Machine learning is a subset of AI that focuses on data-driven learning without explicit programming.",
        "A simple reflex agent acts only on the basis of current percepts, ignoring the rest of the percept history.",
        "Python is widely used in AI due to its readability and massive ecosystem of data science libraries."
    ]
    return random.choice(facts)

def main():
    print(f"{get_greeting()} I am a simple reflex agent.")
    print("I can observe your environment and respond based on my programming.\n")
    
    mood = input("How are you feeling about learning AI today? ").lower()
    
    # Mood keyword checks
    if "excited" in mood or "good" in mood or "great" in mood:
        print("I am glad to hear you are enthusiastic! AI is a fascinating field.")
    elif "nervous" in mood or "overwhelmed" in mood or "scared" in mood:
        print("It's completely normal to feel that way. We'll take it one step at a time.")
    elif "curious" in mood or "wondering" in mood:
        print("Curiosity is the best trait for a computer scientist. Let's learn together!")
    elif "bored" in mood or "tired" in mood or "sleepy" in mood:
        print("Hopefully, the magic of building intelligent systems will wake you up!")
    else:
        print("I see. Let's dive into some interesting concepts regardless.")

    print("\nHere is a random AI fact for you:")
    print(get_ai_fact())

if __name__ == "__main__":
    main()