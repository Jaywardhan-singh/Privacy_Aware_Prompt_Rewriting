import pandas as pd
import random
import requests
import re
from datetime import datetime, timedelta
import cohere

# Cohere API Client
co = cohere.Client('Cohere API key')  # Replace with your Cohere API key

# Function to communicate with local LLM to decide masking strategies
def determine_masking_strategy(df):
    GROQCLOUD_API_KEY = "API key"  # Replace with your API key
    GROQCLOUD_API_URL = "API URL"
    
    headers = {"Authorization": f"Bearer {GROQCLOUD_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Analyze the following columns and suggest appropriate masking strategies for each in JSON format. 
The strategies include:
- Rounding: For floating-point columns where precision isn’t critical.
- Synthetic: For columns where statistical similarity is important but data must be anonymized.
- Shuffling: For columns where data points can be randomized without affecting the analysis.
- Multiplicative: For columns with proportional relationships (e.g., salary or sales).

Example response format:
{{
    "Column1": "rounding",
    "Column2": "shuffling",
    "Column3": "multiplicative",
    "Column4": "synthetic"
}}

Dataset Columns: {list(df.columns)}
"""
    
    payload = {
        "model": "llama3-70b-8192",  # Replace with the specific model if required
        "messages": [{"role": "user", "content": prompt}],
    }
    
    try:
        response = requests.post(GROQCLOUD_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            # Extract the relevant response from the API
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            raise Exception(f"Local LLM Error: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"Error in API Call: {str(e)}")

# Function to apply relevant masking techniques and store original values
def apply_masking(df, columns_to_mask):
    original_data = df.copy()  # Store original data before applying any masking
    for col, mask_type in columns_to_mask.items():
        if mask_type == "rounding":
            df[col] = df[col].apply(lambda x: round(float(x), 1) if isinstance(x, (int, float)) else x)
        elif mask_type == "synthetic":
            if pd.api.types.is_numeric_dtype(df[col]):
                mean, std = df[col].mean(), df[col].std()
                df[col] = [round(random.gauss(mean, std), 1) for _ in range(len(df))]
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                min_date, max_date = df[col].min(), df[col].max()
                df[col] = [min_date + timedelta(seconds=random.randint(0, int((max_date - min_date).total_seconds()))) for _ in range(len(df))]
        elif mask_type == "shuffling":
            df[col] = random.sample(df[col].tolist(), len(df[col]))
        elif mask_type == "multiplicative":
            df[col] = df[col].apply(lambda x: round(float(x) * random.uniform(0.8, 1.2), -2) if isinstance(x, (int, float)) else x)
    
    return df, original_data  # Return both masked data and the original data

# Function to unmask data by replacing masked values with original ones
def unmask_data(masked_df, original_df, columns_to_mask):
    for col in columns_to_mask.keys():
        masked_df[col] = original_df[col]  # Replace the masked column with the original data
    return masked_df

# Function to parse the LLM response
def parse_masking_strategy(strategy_text):
    columns_to_mask = {}
    pattern = re.compile(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([a-zA-Z]+)['\"]")
    matches = pattern.findall(strategy_text)
    for col, strategy in matches:
        columns_to_mask[col] = strategy.lower()
    return columns_to_mask

# Function to analyze masked data using Cohere
def analyze_data_with_cohere(masked_data):
    try:
        # Prepare a smaller preview of the dataset to avoid overwhelming the API
        masked_data_preview = masked_data.head(25).to_json(orient="split")  # Use 'split' or 'records' to structure the preview
        
        response = co.generate(
            model='command-xlarge-nightly',  # Specify the Cohere model
            prompt=f"""You are a data analyst assigned to analyze a dataset where the numerical 
columns have been masked. Focus on numerical insights, trends, correlations, and statistical summaries, 
with as much precision as possible. Identify and list key numerical metrics such as:
- Mean, median, and standard deviation for key numerical columns
- Correlations between numerical variables (showing correlation coefficients)
- Any numerical outliers (using Z-scores or other statistical methods)
- Significant trends in numerical data (e.g., increases or decreases in mean values over time)
- Cluster centers and distribution (if applicable)

Please present your findings in the following format:
{{
    "Mean": {{}},
    "Median": {{}},
    "Standard Deviation": {{}},
    "Correlations": {{}},
    "Outliers": {{}},
    "Trends": {{}}
}}

Dataset Preview:
Provide numerical insights based on the dataset preview below:
{masked_data_preview}""",
            max_tokens=500  # Adjust the token limit if needed
        )

        return response.generations[0].text
    except Exception as e:
        raise Exception(f"Error in Cohere analysis: {str(e)}")

# Function to clean up redundant or repetitive parts of the result
def clean_response(response_text):
    # Remove duplicate keys or redundant entries by using regular expressions or manual cleanup
    cleaned_text = re.sub(r'(\s+){2,}', r'\1', response_text)  # Remove excessive whitespace
    cleaned_text = re.sub(r'(,)\1+', r'\1', cleaned_text)  # Remove repeated commas
    
    # Optional: Additional steps for cleaning specific formats
    cleaned_text = cleaned_text.replace('},\n', '}\n')  # Remove any unnecessary line breaks
    return cleaned_text


# Main function
def main():
    print("Privacy-Aware Numerical Data Analysis System")

    # Step 1: Load the dataset
    file_path = "Sales.csv"  # Replace with your dataset file path
    try:
        df = pd.read_csv(file_path)
        # Parse datetime columns if any
        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Step 2: Select 20-30 rows (Randomly sample if needed)
    sampled_df = df.head(n=30)  # Adjust sample size as required

    # Step 3: Use Local LLM to determine masking strategy
    print("Determining masking strategies using Local LLM...")
    try:
        masking_strategy = determine_masking_strategy(sampled_df)
        print("Masking Strategy Determined:", masking_strategy)
        
        # Parse the masking strategy from the LLM response
        columns_to_mask = parse_masking_strategy(masking_strategy)

    except Exception as e:
        print("Error in determining masking strategies:", e)
        return

    # Step 4: Apply relevant masking and store original data
    masked_df, original_df = apply_masking(sampled_df.copy(), columns_to_mask)

    # Step 5: Display masked dataset
    print("\nMasked Dataset:\n", masked_df.head())

    # Step 6: Analyze masked data using Cohere
    print("Analyzing masked data using Cohere...")
    try:
        analysis_result = analyze_data_with_cohere(masked_df)
        print("\nCohere Analysis Result:\n", analysis_result)
    except Exception as e:
        print("Error in Cohere analysis:", e)

    # Step 7: Unmask the data (Restoring original content)
    unmasked_df = unmask_data(masked_df.copy(), original_df, columns_to_mask)
    print("\nUnmasked Dataset:\n", unmasked_df.head())


if __name__ == "__main__":
    main()
