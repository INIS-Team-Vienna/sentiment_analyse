"""
Step 3: Sentiment Trend Visualization Module
Functionality: Read quarterly data, calculate sentiment percentages and generate trend charts
Input: Quarterly Excel files with sentiment columns
Output: Sentiment trend line chart PNG file
"""
import pandas as pd 
import matplotlib.pyplot as plt
import os
from typing import Dict, List, Tuple, Optional
from config import Config


class SentimentVisualizer:
    """Visualizer for sentiment trends analysis"""
    
    def __init__(self, data_folder: str = None):
        """Initialize visualizer with data folder"""
        self.data_folder = data_folder or Config.BASE_DATA_PATH
        self.sentiment_data = {"quarter": [], "positive": [], "negative": [], "neutral": []}
        
        # Set up matplotlib font support for better compatibility
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def find_sentiment_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find sentiment column (expects 'sentiment' column)"""
        if 'sentiment' in df.columns:
            return 'sentiment'
        return None
    
    def process_quarterly_file(self, file_path: str, quarter_name: str) -> bool:
        """Process a single quarterly file"""
        try:
            print(f"Processing file: {quarter_name}")
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Auto-detect sentiment column
            sentiment_col = self.find_sentiment_column(df)
            if sentiment_col is None:
                print(f"⚠️ Skipping {quarter_name}: No sentiment column found")
                return False
            
            # Calculate percentage for each sentiment category
            sentiment_counts = df[sentiment_col].value_counts(normalize=True) * 100
            print(f"  Sentiment distribution: {dict(sentiment_counts)}")
            
            # Ensure all sentiment categories have values, fill with 0 if missing
            positive = (sentiment_counts.get("Positive", 0) + 
                       sentiment_counts.get("positive", 0))
            negative = (sentiment_counts.get("Negative", 0) + 
                       sentiment_counts.get("negative", 0))
            neutral = (sentiment_counts.get("Neutral", 0) + 
                      sentiment_counts.get("neutral", 0))
            
            # Add to dataset
            self.sentiment_data["quarter"].append(quarter_name)
            self.sentiment_data["positive"].append(positive)
            self.sentiment_data["negative"].append(negative)
            self.sentiment_data["neutral"].append(neutral)
            
            print(f"  ✅ Successfully processed: P={positive:.1f}%, N={negative:.1f}%, Neu={neutral:.1f}%")
            return True
            
        except Exception as e:
            print(f"❌ Failed to process {quarter_name}: {e}")
            return False
    
    def collect_data(self, year_range: Tuple[int, int]) -> None:
        """Collect quarterly data for specified year range"""
        print(f"=== Starting to collect quarterly data for {year_range[0]}-{year_range[1]} ===")
        
        processed_count = 0
        for year in range(year_range[0], year_range[1] + 1):
            for quarter in ["Q1", "Q2", "Q3", "Q4"]:
                file_path = Config.get_quarterly_file_path(year, quarter)
                quarter_name = f"{year}_{quarter}"
                
                if os.path.exists(file_path):
                    if self.process_quarterly_file(file_path, quarter_name):
                        processed_count += 1
                else:
                    print(f"⚠️ File does not exist: {quarter_name}")
        
        print(f"\n✅ Successfully processed {processed_count} quarterly files")
    
    def generate_chart(self, output_path: str, title: str = None) -> None:
        """Generate sentiment trend line chart"""
        if not self.sentiment_data["quarter"]:
            print("❌ No data available for plotting")
            return
        
        print("=== Starting to generate trend chart ===")
        
        # Convert to DataFrame
        result_df = pd.DataFrame(self.sentiment_data)
        print(f"Data overview:\n{result_df}")
        
        # Create chart
        chart_config = Config.CHART_CONFIG
        plt.figure(figsize=chart_config['figsize'])
        
        # Draw three trend lines using configuration
        colors = chart_config['colors']
        markers = chart_config['markers']
        
        plt.plot(result_df['quarter'], result_df['positive'], 
                marker=markers['positive'], label='Positive', color=colors['positive'], 
                linewidth=2, markersize=6)
        plt.plot(result_df['quarter'], result_df['negative'], 
                marker=markers['negative'], label='Negative', color=colors['negative'], 
                linewidth=2, markersize=6)
        plt.plot(result_df['quarter'], result_df['neutral'], 
                marker=markers['neutral'], label='Neutral', color=colors['neutral'], 
                linewidth=2, markersize=6)
        
        # Set chart style
        plt.xlabel("Time Quarter", fontsize=12)
        plt.ylabel("Percentage (%)", fontsize=12)
        
        # Set title
        if title is None:
            title = chart_config['title_template'].format(topic=Config.ANALYSIS_TOPIC.title())
        plt.title(title, fontsize=14, fontweight='bold')
        
        # Legend and grid
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save chart
        plt.savefig(output_path, dpi=chart_config['dpi'], bbox_inches='tight')
        print(f"✅ Trend chart saved to: {output_path}")
        
        # Display chart
        plt.show()
    
    def print_summary(self) -> None:
        """Print data summary"""
        if not self.sentiment_data["quarter"]:
            return
        
        result_df = pd.DataFrame(self.sentiment_data)
        
        print("\n=== Data Summary ===")
        print(f"Total quarters: {len(result_df)}")
        print(f"Average positive sentiment: {result_df['positive'].mean():.1f}%")
        print(f"Average negative sentiment: {result_df['negative'].mean():.1f}%")
        print(f"Average neutral sentiment: {result_df['neutral'].mean():.1f}%")


def main():
    """Main function for sentiment visualization"""
    # Create visualizer
    visualizer = SentimentVisualizer()
    
    # Set year range based on configuration
    if Config.ANALYSIS_YEARS:
        year_range = (min(Config.ANALYSIS_YEARS), max(Config.ANALYSIS_YEARS))
    else:
        year_range = (2024, 2025)  # Default fallback
    
    # Collect data
    visualizer.collect_data(year_range)
    
    # Generate chart
    output_path = Config.get_chart_output_path(year_range)
    chart_title = f"{Config.ANALYSIS_TOPIC.title()} Sentiment Trends ({year_range[0]}-{year_range[1]})"
    visualizer.generate_chart(output_path, chart_title)
    
    # Print summary
    visualizer.print_summary()


if __name__ == "__main__":
    main()

