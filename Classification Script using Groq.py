import pandas as pd
from groq import Groq
import time
import os

# 1. SETUP
# Paste your Groq API key here
client = Groq(api_key="")

# Point this to the unclassified CSV you want to process
INPUT_CSV = "" 
OUTPUT_CSV = ""

VALID_SECTIONS = [
    "Agriculture", "Economy & Finance", "Education", "Energy & Environment", 
    "Foreign Policy", "Governance & Anti-Corruption", "Health", "Infrastructure", 
    "Labour & Employment", "Rural Development", "SC/ST/OBC", "Social Justice & Minorities", 
    "Urban Development", "Women & Child Development", "Youth & Sports", "Defence & Security", "Other"
]

SYSTEM_PROMPT = f"""You are a political science research assistant. Classify the given electoral promise into exactly ONE of the following manifesto sections:
{', '.join(VALID_SECTIONS)}

RULES:
1. Output ONLY the exact name of the section. No punctuation, no explanations, no markdown.
2. If the promise fits multiple, choose the primary policy domain.
3. If it truly doesn't fit, output 'Other'."""

# 2. LOAD DATA
df = pd.read_csv(INPUT_CSV)
print(f"Starting section tagging for {len(df)} promises using Groq...")

tagged_sections = []

# 3. TAGGING LOOP
for index, row in df.iterrows():
    text = row['promise_text']
    
    try:
        # Groq API call
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Promise: {text}"}
            ],
            model="llama-3.1-8b-instant", # Extremely fast and accurate for classification
            temperature=0,
            max_tokens=10
        )
        
        section = chat_completion.choices[0].message.content.strip().replace('"', '').replace('.', '')
        
        # Safety check
        if section not in VALID_SECTIONS:
            section = "Other" 
            
        tagged_sections.append(section)
        
    except Exception as e:
        print(f"Error on row {index}: {e}")
        tagged_sections.append("Other")
        
    # Groq is so fast you barely need a delay, but let's be polite
    if index % 100 == 0:
        print(f"Tagged {index} rows...")

# 4. SAVE FINAL DATASET
df['manifesto_section'] = tagged_sections
df.to_csv(OUTPUT_CSV, index=False)

print(f"\n🎉 SUCCESS! Final dataset saved to {OUTPUT_CSV}")
print("Section Distribution:")
print(df['manifesto_section'].value_counts())