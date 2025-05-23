# GenAI : Privacy-Aware Prompt Rewriting 🚀

## 🔍 Abstract
This project implements a **privacy-aware system** to mask sensitive data in prompts sent to LLMs and unmask the processed output. The system ensures data confidentiality through techniques like **rounding**, **synthetic data generation**, **shuffling**, and **multiplicative masking** while maintaining analytical utility.

---

![Workflow diagram](https://github.com/Jaywardhan-singh/Privacy_Aware_Prompt_Rewriting/blob/df8af58ef529e3f91608df33c91834bb641aa0ad/assets/Workflow%20diagram.png)

*A modular system to secure sensitive data for safe interaction with Large Language Models (LLMs)*

---


## 🌟 Key Features
- **Modular Workflow:** Separate components for masking, analysis, and unmasking.
- **Flexible Strategies:** Adaptable masking techniques based on data types.
- **Enterprise Ready:** High compatibility with global LLMs for diverse analytics.

---

## 🏗️ System Architecture
### High-Level Workflow
1. **Input Prompt** → Sensitive data in tabular format.
2. **Local LLM** → Applies context-specific masking strategies.
3. **Global LLM** → Analyzes masked data to generate insights.
4. **Unmasking** → Restores original data for actionable outputs.

![Flowchart](https://github.com/Jaywardhan-singh/Privacy_Aware_Prompt_Rewriting/blob/df8af58ef529e3f91608df33c91834bb641aa0ad/assets/Flowchart.png)

*Overall Flowchart of the Proposed Idea*

---

## 💡 Masking Strategies
| **Technique**           | **Description**                        | **Example**                   |
|--------------------------|----------------------------------------|-------------------------------|
| **Rounding**             | Reduces numerical precision.           | Input: 45.768 → 45.8         |
| **Synthetic Data**       | Generates statistically similar values.| Input: Age: 35 → Age: 33      |
| **Shuffling**            | Randomizes data order.                 | Input: [NY, LA] → [LA, NY]    |
| **Multiplicative Masking**| Scales data while preserving ratios.  | Input: $50k → $60k (scaled)   |

---

## 📊 Results
### Performance Metrics (KS Test)
| **Column**              | **p-value**          | **Inference**         |
|--------------------------|----------------------|-----------------------|
| Unit Price              | 0.78                 | ✅ Good Masking        |
| Quantity                | 0.68                 | ✅ Good Masking        |
| Tax                     | 3.95e-42             | ❌ Poor Masking        |
| Gross Margin Percentage | 3.95e-42             | ❌ Poor Masking        |
| Gross Income            | 3.95e-42             | ❌ Poor Masking        |
| Rating                  | 0.97                 | ✅ Good Masking        |


> **Note:** A p-value > 0.5 indicates good masking.

---

## 📦 Tools and Technologies
- **Programming Language:** Python  
- **Local LLMs:** Llama, GroqCloud's Model
- **Global LLMs:** GPT-4, Cohere's Model
- **Libraries:** Pandas, NumPy, Requests, Regular Expressions  

---

## Comparison with Alternatives

| Aspect               | Privacy-Aware Masking | Direct Obfuscation | Encryption          |
|----------------------|----------------------|--------------------|---------------------|
| Confidentiality      | High                 | Medium             | Very High           |
| Usability in LLMs    | Compatible           | Partially Compatible| Incompatible        |
| Ease of Implementation| Medium               | Easy               | Complex             |

---

## 📜 Conclusion
The Privacy-Aware Prompt Rewriting system effectively balances data confidentiality with analytical power by integrating local and global LLMs and applying flexible masking techniques. This modular approach makes it highly suitable for enterprise adoption.

---

## 🛠️ How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Jaywardhan-singh/Privacy_Aware_Prompt_Rewriting.git
   cd Privacy_Aware_Prompt_Rewriting
