# Privacy Aware Prompt Rewriting

This project is a **Privacy Aware Prompt Re-writing for Numerical Data Analysis** designed to handle sensitive datasets by applying masking strategies to ensure confidentiality. It integrates advanced LLMs and APIs to provide privacy-compliant insights while safeguarding sensitive data.

## Features

- **Masking Strategies**: Automatically applies strategies like rounding, synthetic generation, shuffling, and multiplicative masking to numerical columns.
- **Unmasking**: Restores original data for analysis or verification.
- **Local LLM Integration**: Uses a local LLM to decide appropriate masking strategies & genrating masked output based on dataset characteristics.
- **Global LLM Integration**: Analyzes masked data using Cohere AI's plateform, generating statistical insights and trends.
- **Customizable Masking**: Flexible to handle different types of columns based on user requirements.

## Prerequisites

- Python 3.7+
- Required Python packages:
  - `pandas`
  - `random`
  - `requests`
  - `re`
  - `datetime`
  - `cohere`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Privacy_Aware_Prompt_Rewriting.git
   cd Privacy_Aware_Prompt_Rewriting
   ```

2. Install the dependencies:
   ```bash
   pip install pandas requests
   ```

3. Add your API keys:
   - Replace the placeholders in the script with your respective API keys for Cohere and GroqCloud.

## Usage

1. **Prepare Your Dataset**:
   - Save your dataset as a CSV file (e.g., `data.csv`).
   - Ensure the dataset contains numerical or datetime columns.

2. **Run the Script**:
   ```bash
   python main.py
   ```

3. **Process Overview**:
   - **Step 1**: Load the dataset.
   - **Step 2**: Select a subset of rows for processing.
   - **Step 3**: Determine masking strategies using Local LLM.
   - **Step 4**: Apply masking techniques.
   - **Step 5**: Analyze masked data using Cohere AI.

## Example Output

### Masked Dataset
| Column A | Column B | Order Date   |
|----------|----------|--------------|
| 123.4    | 89.6     | 2022-01-15   |
| 456.7    | 76.8     | 2022-02-10   |

### Unmasked Dataset
| Column A | Column B | Order Date   |
|----------|----------|--------------|
| 123.456  | 89.654   | 2022-01-15   |
| 456.789  | 76.854   | 2022-02-10   |

### Cohere Analysis Output
```json
{
    "Mean": {"Column A": 123.5, "Column B": 89.6},
    "Standard Deviation": {"Column A": 12.3, "Column B": 8.9},
    "Trends": {"Column A": "Increasing over time"}
}
```

## Customization

- **Masking Strategies**: Modify the `determine_masking_strategy` and `apply_masking` functions to include additional strategies or rules.
- **LLM Integration**: Replace the GroqCloud API or Cohere model with your preferred LLM APIs - Better to use ChatGPT's API.

## Limitations

- Requires valid API keys for LLM integration.
- Sensitive data might need additional masking strategies based on regulatory requirements
