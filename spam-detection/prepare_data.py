import pandas as pd
import numpy as np
import os
import re

# Part 1: Feature Engineering
# Two new features: 'link_count' and 'urgent_words'
def extract_features(text):
    text_lower = text.lower()
    
    word_count = len(text.split())
    exclamations = text.count('!')
    money_words = sum(text_lower.count(w) for w in ['$', 'dollars', 'cash', 'money', 'crypto'])
    all_caps = sum(1 for w in text.split() if w.isupper() and len(w) > 1)
    
    # New Feature 1: Links
    link_count = text.count('http') + text.count('www.')
    
    # New Feature 2: Urgency
    urgent_words = sum(text_lower.count(w) for w in ['urgent', 'immediate', 'act now', 'limited time', 'hurry'])
    
    return [word_count, exclamations, money_words, all_caps, link_count, urgent_words]

# 16 Base Emails (8 Legitimate, 8 Spam)
base_emails = [
    # Legitimate (0)
    ("Hey team, the project deadline is next week. Please review the attached document.", 0),
    ("Mom, I'll be home for dinner around 7 PM. See you then.", 0),
    ("Your doctor's appointment is confirmed for Tuesday at 9 AM.", 0),
    ("Can we reschedule our 1-on-1 meeting to Thursday?", 0),
    ("Thanks for the feedback on the pull request, I'll update the code.", 0),
    ("Are we still on for lunch today at the cafe?", 0),
    ("Please find the Q3 financial report attached for your review.", 0),
    ("Don't forget to submit your timesheets by Friday afternoon.", 0),
    
    # Spam (1)
    ("URGENT: Claim your $1000 cash prize immediately! Click http://spam.com", 1), ("Hot new crypto investment! Double your money in days! Act now!!!", 1), ("You have been selected for a limited time offer. $$$ Save big!", 1),
    ("Immediate action required: Your account will be locked. http://fake-bank.com", 1),
    ("Buy cheap watches and luxury items. Huge discount! Hurry!", 1),
    ("Congratulations! You won the lottery. Send dollars to claim.", 1),
    ("Make money fast working from home! No experience needed!!!", 1),
    ("URGENT UPDATE: Pay your invoice immediately or face legal action. http://virus.com", 1)
]

def generate_dataset():
    data