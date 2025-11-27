"""
Step 1: Sentiment Analysis Module
Functionality: Analyze sentiment of social media posts using GPT
Input: Excel file with text content column
Output: Excel file with text and sentiment columns
"""
import os
import pandas as pd
import time
import json
from openai import AzureOpenAI
from typing import List, Dict, Optional
from config import Config


class SentimentAnalyzer:
    """Social media sentiment analyzer using GPT models"""
    
    def __init__(self):
        """Initialize sentiment analyzer with configuration"""
        self.azure_endpoint = Config.AZURE_OPENAI_ENDPOINT
        self.deployment_name = Config.AZURE_DEPLOYMENT_NAME
        self.api_version = Config.AZURE_API_VERSION
        self.api_key = Config.AZURE_API_KEY
        
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
        )
        
        self.batch_size = Config.BATCH_SIZE
        self.api_delay = Config.API_DELAY
    
    def extract_text_from_excel(self, file_path: str) -> List[str]:
        """Extract text content from Excel file (expects Tweet_Content column)"""
        print(f"Reading file: {file_path}")
        df = pd.read_excel(file_path, usecols=["Tweet_Content"], dtype=str)
        documents = df["Tweet_Content"].dropna().tolist()
        print(f"Successfully extracted {len(documents)} text entries")
        return documents
    
    def classify_sentiment_batch(self, texts: List[str]) -> List[str]:
        """Perform batch sentiment classification using GPT"""
        try:
            formatted_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])
            len_text = len(texts)

            # Use configurable prompt
            system_prompt = Config.get_sentiment_prompt()

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Classify the sentiment of these social media posts (Positive, Negative, or Neutral):\n{formatted_texts}\n\n"
                            f"Return ONLY the JSON object without any extra text, and make sure the number of labels corresponds exactly to {len_text}!!!"
                        )
                    }
                ],
                response_format={"type": "json_object"}
            )

            result = response.choices[0].message.content.strip()
            
            if not result:
                raise ValueError("Empty response from API")

            sentiments = json.loads(result).get("sentiments", [])
            
            # Ensure count matching
            if len(sentiments) != len_text:
                print(f"⚠️ Count mismatch: expected {len_text}, got {len(sentiments)}")
                if len(sentiments) < len_text:
                    sentiments.extend(["Neutral"] * (len_text - len(sentiments)))
                else:
                    sentiments = sentiments[:len_text]
            
            return sentiments

        except Exception as e:
            print(f"Error processing batch: {e}")
            return ["Neutral"] * len(texts)
    
    def analyze_file(self, input_file: str, output_file: str):
        """Analyze sentiment of a single file"""
        print(f"=== Starting to process file: {input_file} ===")
        
        # Extract text content
        documents = self.extract_text_from_excel(input_file)
        
        if not documents:
            print("No valid text data found")
            return
        
        # Batch processing
        results = []
        total_docs = len(documents)
        
        for i in range(0, total_docs, self.batch_size):
            batch = documents[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (total_docs + self.batch_size - 1) // self.batch_size
            
            print(f"Processing batch {batch_num}/{total_batches}, size: {len(batch)}")
            
            try:
                sentiments = self.classify_sentiment_batch(batch)
                
                # Strict one-to-one correspondence
                for j, (text, sentiment) in enumerate(zip(batch, sentiments)):
                    results.append({
                        "text": text,
                        "sentiment": sentiment
                    })
                
                # Fill missing data if count mismatch
                if len(sentiments) < len(batch):
                    for j in range(len(sentiments), len(batch)):
                        results.append({
                            "text": batch[j],
                            "sentiment": "Neutral"
                        })
                        
            except Exception as e:
                print(f"❌ Batch processing failed: {e}")
                # Use default values for entire batch on failure
                for text in batch:
                    results.append({
                        "text": text,
                        "sentiment": "Neutral"
                    })
            
            time.sleep(self.api_delay)  # API rate limiting
        
        # Final validation
        if len(results) != total_docs:
            print(f"⚠️ Final check failed: input {total_docs}, output {len(results)}")
            while len(results) < total_docs:
                missing_idx = len(results)
                results.append({
                    "text": documents[missing_idx] if missing_idx < len(documents) else "Missing",
                    "sentiment": "Neutral"
                })
        
        # Save results
        df_results = pd.DataFrame(results)
        df_results.to_excel(output_file, index=False)
        print(f"✅ Processing complete, results saved to: {output_file}")
        print(f"Total processed: {len(results)} entries\n")


def main():
    """Main function for sentiment analysis"""
    analyzer = SentimentAnalyzer()
    
    # Process files by year
    for year in Config.ANALYSIS_YEARS:
        input_file = Config.get_input_file_path(year)
        output_file = Config.get_output_file_path(year)
        
        if not os.path.exists(input_file):
            print(f"❌ Input file does not exist: {input_file}")
            continue
            
        analyzer.analyze_file(input_file, output_file)


if __name__ == "__main__":
    main()
