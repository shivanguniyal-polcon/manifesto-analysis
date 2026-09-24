# Manifesto Analysis & Policy Taxonomy Engine

LLM-assisted classification of electoral promises from Indian Lok Sabha manifestos (BJP & INC, 2014–2024) into a 17-category policy taxonomy, built for empirical benchmarking of policy commitments across parties and election cycles.

> This repository accompanies ongoing research on manifesto content, ideological shifts, and promise evolution in Indian national elections.
> 
## What This Repo Does

1. **Ingests** electoral promises extracted from six national manifestos — BJP (2014, 2019, 2024) and INC (2014, 2019, 2024).
2. **Classifies** each promise into exactly one of 17 policy sections using a zero-temperature LLM pipeline via the Groq API (`llama-3.1-8b-instant`).
3. **Validates** classification quality through manual code-review workbooks (sampled audit of model outputs).
4. **Aggregates** per-election classified datasets into a master dataset for cross-party, cross-cycle analysis.

## Repository Structure

```
manifesto-analysis/
│
├── Classification Script using Groq.py    # Core pipeline: LLM section-tagging of promises
├── Master_Dataset_2014_2024.csv           # Combined classified dataset across six manifestos
├── Code Review - 1.xlsx                   # Manual validation workbook (audit sample 1)
├── Code Review - 2.xlsx                   # Manual validation workbook (audit sample 2)
│
└── for validation/
    ├── BJP_2014_Master_Promises_Classified.csv
    ├── BJP_2019_Master_Promises_Classified.csv
    ├── BJP_2024_Master_Promises_Classified.csv
    ├── INC_2014_Master_Promises_Classified.csv
    ├── INC_2019_Master_Promises_Classified.csv
    └── INC_2024_Master_Promises_Classified.csv
```

## The Policy Taxonomy

Every promise is assigned to exactly **one** primary section:

| | | | |
|---|---|---|---|
| Agriculture | Economy & Finance | Education | Energy & Environment |
| Foreign Policy | Governance & Anti-Corruption | Health | Infrastructure |
| Labour & Employment | Rural Development | SC/ST/OBC | Social Justice & Minorities |
| Urban Development | Women & Child Development | Youth & Sports | Defence & Security |
| Other | | | |

---

## How the Classification Works

**Pipeline (`Classification Script using Groq.py`):**

1. **System prompt** instructs the model to act as a political science research assistant and output *only* the exact section name — no punctuation, explanations, or markdown.
2. **Disambiguation rule:** if a promise spans multiple domains, the model must choose the *primary* policy domain; if none fit, it outputs `Other`.
3. **Model settings:** `llama-3.1-8b-instant` at `temperature=0` and `max_tokens=10` — deterministic, fast, and cheap at scale (chosen after testing; `gpt-oss-20b` noted as an alternative).
4. **Post-processing:** outputs are stripped of quotes/periods and checked against the valid-section list.
5. **Fallbacks:** any out-of-list or errored row is conservatively tagged `Other`; progress is logged every 100 rows.
6. **Output:** the input CSV is returned with an added `manifesto_section` column, plus a printed section distribution.

## Data Schema

| Column | Description |
|---|---|
| `promise_text` | The electoral promise / commitment text (input; required by the script) |
| `manifesto_section` | Assigned policy section (output; added by the script) |
| Party / Year | Encoded in per-election filenames (`{Party}_{Year}_Master_Promises_Classified.csv`) |

## Getting Started

**Prerequisites:** Python 3.9+, a [Groq](https://console.groq.com) API key (free tier is sufficient).

```bash
pip install pandas groq
```

1. Open `Classification Script using Groq.py`.
2. Set your credentials and paths:
   ```python
   client = Groq(api_key="YOUR_GROQ_API_KEY")
   INPUT_CSV  = "path/to/unclassified_promises.csv"   # must contain a 'promise_text' column
   OUTPUT_CSV = "path/to/output_classified.csv"
   ```
3. Run:
   ```bash
   python "Classification Script using Groq.py"
   ```

## Validation

Two Excel workbooks (`Code Review - 1.xlsx`, `Code Review - 2.xlsx`) contain manually audited samples of model classifications, used to sanity-check section assignments before acceptance into the master dataset.

## Known Limitations

- **Single-label design:** multi-domain promises are forced into one primary section by design; this trades granularity for comparability across parties and cycles.
- **`Other` is dual-purpose:** it absorbs both genuinely unclassifiable promises *and* pipeline errors/fallbacks — a caveat when interpreting `Other` counts.
- **Model-version sensitivity:** outputs can shift if the underlying Groq model version changes; re-running the full classification after any model update is recommended before publishing comparisons.
- **Manifesto text only:** promises are classified without page/section context from the source document.

## Roadmap

- [ ] Inter-coder agreement metrics (Cohen's κ) between model output and the manual review workbooks
- [ ] Cross-mapping to the [Manifesto Project (MARPOR)](https://manifesto-project.wzb.eu/) category scheme for international comparability
- [ ] Promise-evolution dashboard: section emphasis shifts across 2014 → 2019 → 2024 per party
- [ ] Multi-label extension for genuinely hybrid promises

---

## Contact

**Shivang Uniyal** — [shivang.uni@gmail.com](mailto:shivang.uni@gmail.com) · [LinkedIn](https://www.linkedin.com/in/shivang-uniyal/)

*Related work: [A Voter's Guide to Reading a Manifesto](https://vidhilegalpolicy.in/blog/a-voters-guide-to-reading-a-manifesto/) (Vidhi Centre for Legal Policy, 2024).*
