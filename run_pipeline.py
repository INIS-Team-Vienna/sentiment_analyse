"""
Social Media Sentiment Analysis Pipeline - Main Execution Script
Execute three steps in sequence: Sentiment Analysis -> Quarterly Segmentation -> Trend Visualization
"""
import sys
from config import Config
from sentiment_gpt import SentimentAnalyzer
from divide_by_quarter import QuarterlyDataProcessor
from line_chart_by_quarter import SentimentVisualizer


def run_sentiment_analysis():
    """Step 1: Run sentiment analysis"""
    print("🚀 Step 1: Starting sentiment analysis...")
    
    analyzer = SentimentAnalyzer()
    
    for year in Config.ANALYSIS_YEARS:
        input_file = Config.get_input_file_path(year)
        output_file = Config.get_output_file_path(year)
        
        try:
            analyzer.analyze_file(input_file, output_file)
        except Exception as e:
            print(f"❌ Sentiment analysis failed for year {year}: {e}")
            return False
    
    print("✅ Step 1 completed: Sentiment Analysis\n")
    return True


def run_quarterly_division():
    """Step 2: Run quarterly data segmentation"""
    print("🚀 Step 2: Starting quarterly data segmentation...")
    
    processor = QuarterlyDataProcessor()
    
    try:
        processor.process_all_files()
    except Exception as e:
        print(f"❌ Quarterly segmentation failed: {e}")
        return False
    
    print("✅ Step 2 completed: Quarterly Data Segmentation\n")
    return True


def run_visualization():
    """Step 3: Run trend visualization"""
    print("🚀 Step 3: Starting trend visualization...")
    
    visualizer = SentimentVisualizer()
    
    try:
        # Set year range
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
        
    except Exception as e:
        print(f"❌ Trend visualization failed: {e}")
        return False
    
    print("✅ Step 3 completed: Trend Visualization\n")
    return True


def main():
    """Main function: Run complete sentiment analysis pipeline"""
    print("="*60)
    print(f"🎯 Social Media Sentiment Analysis Pipeline")
    print(f"📊 Topic: {Config.ANALYSIS_TOPIC.title()}")
    print("="*60)
    
    # Validate configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed, exiting program")
        sys.exit(1)
    
    # Ask user which steps to run
    print("\nPlease select steps to execute:")
    print("1. Sentiment Analysis Only")
    print("2. Quarterly Segmentation Only") 
    print("3. Trend Visualization Only")
    print("4. Run Complete Pipeline (1->2->3)")
    print("5. Skip Sentiment Analysis (2->3)")
    
    try:
        choice = input("\nPlease enter your choice (1-5): ").strip()
    except KeyboardInterrupt:
        print("\nUser cancelled operation")
        sys.exit(0)
    
    success = True
    
    if choice == "1":
        success = run_sentiment_analysis()
    elif choice == "2":
        success = run_quarterly_division()
    elif choice == "3":
        success = run_visualization()
    elif choice == "4":
        # Complete pipeline
        success = (run_sentiment_analysis() and 
                  run_quarterly_division() and 
                  run_visualization())
    elif choice == "5":
        # Skip sentiment analysis
        success = (run_quarterly_division() and 
                  run_visualization())
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    # Output final result
    if success:
        print("🎉 All selected steps executed successfully!")
    else:
        print("❌ Errors occurred during execution")
        sys.exit(1)


if __name__ == "__main__":
    main()