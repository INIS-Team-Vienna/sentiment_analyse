"""
Social Media Sentiment Analysis Pipeline Configuration
Centralized configuration management for all parameters
"""
import os
from typing import Dict, Any, List, Optional


class Config:
    """Project configuration class for sentiment analysis pipeline"""
    
    # ===== API Configuration =====
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://pdf2json.openai.azure.com/")
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "o4-mini")
    AZURE_API_VERSION = "2025-01-01-preview"
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "your_api_key_here")
    
    # ===== Data Path Configuration =====
    BASE_DATA_PATH = "C:\\Users\\wangze\\OneDrive - IAEA\\Desktop\\Nuclear power excel\\clean data"
    
    # ===== Processing Parameters =====
    BATCH_SIZE = 30  # GPT batch processing size
    API_DELAY = 1.0  # API call delay in seconds
    
    # ===== Analysis Topic Configuration =====
    # TODO: Change this to your analysis topic (e.g., "climate change", "cryptocurrency", "AI technology")
    ANALYSIS_TOPIC = "nuclear power"
    
    # ===== Data Configuration =====
    ANALYSIS_YEARS = [2024, 2025]  # Years to process
    
    # ===== Visualization Configuration =====
    CHART_CONFIG = {
        'figsize': (14, 8),
        'dpi': 300,
        'colors': {
            'positive': '#2E8B57',
            'negative': '#DC143C',
            'neutral': '#4682B4'
        },
        'markers': {
            'positive': 'o',
            'negative': 's', 
            'neutral': '^'
        },
        'title_template': "{topic} Sentiment Trends Analysis"
    }
    
    @classmethod
    def get_input_file_path(cls, year: int) -> str:
        """Get input file path"""
        return f"{cls.BASE_DATA_PATH}\\filtered_tweets_{year}.xlsx"
    
    @classmethod
    def get_output_file_path(cls, year: int) -> str:
        """Get output file path"""
        return f"{cls.BASE_DATA_PATH}\\results_{year}_sentiment.xlsx"
    
    @classmethod
    def get_quarterly_file_path(cls, year: int, quarter: str) -> str:
        """Get quarterly file path"""
        return f"{cls.BASE_DATA_PATH}\\{year}_{quarter}.xlsx"
    
    @classmethod
    def get_chart_output_path(cls, year_range: tuple) -> str:
        """Get chart output path"""
        topic_clean = cls.ANALYSIS_TOPIC.lower().replace(" ", "_")
        return f"{cls.BASE_DATA_PATH}\\{topic_clean}_sentiment_trend_{year_range[0]}_{year_range[1]}_by_quarter.png"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.AZURE_API_KEY or cls.AZURE_API_KEY == "your_api_key_here":
            print("❌ Please set a valid AZURE_API_KEY in environment variables or config.py")
            return False
        
        if not os.path.exists(cls.BASE_DATA_PATH):
            print(f"❌ Data path does not exist: {cls.BASE_DATA_PATH}")
            return False
        
        return True
    
    @classmethod
    def get_sentiment_prompt(cls) -> str:
        """Get customized sentiment analysis prompt"""
        return (
            f"You are a helpful assistant that classifies social media posts into Positive, Negative, or Neutral sentiment toward {cls.ANALYSIS_TOPIC}. "
            "You must output ONLY a valid JSON object in the following format:\n"
            '{"sentiments": ["Positive", "Negative", "Neutral", ...]}\n'
            "Ensure the number of sentiments matches the number of posts. "
            "Each sentiment corresponds exactly to one post in the order they are presented."
        )