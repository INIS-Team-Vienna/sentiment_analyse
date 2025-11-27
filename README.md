# Social Media Sentiment Analysis Pipeline

A comprehensive Python pipeline for analyzing sentiment trends in social media posts using GPT-4, with flexible data organization and visualization capabilities.

## 📋 Overview

This project performs three main tasks:
1. **Sentiment Analysis**: Classifies social media posts using Azure OpenAI GPT models
2. **Quarterly Segmentation**: Splits data by quarters based on timestamps  
3. **Trend Visualization**: Generates line charts showing sentiment trends over time

## ✨ Key Features

- **Topic-Agnostic**: Configurable for any topic or domain
- **Flexible Data Organization**: Supports multiple file organization modes
- **Auto-Detection**: Automatically detects column names in Excel files
- **Robust Processing**: Zero data loss with comprehensive error handling
- **Customizable Visualization**: Configurable charts and styling

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Excel files with tweet data

### Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (recommended):
```bash
export AZURE_OPENAI_ENDPOINT="your_endpoint"
export AZURE_DEPLOYMENT_NAME="your_model_name" 
export AZURE_API_KEY="your_api_key"
```

### Configuration

Edit `config.py` to change the analysis topic:

```python
# Change this line to your topic
ANALYSIS_TOPIC = "nuclear power"  # e.g., "climate change", "cryptocurrency", "AI technology"

# Set your data path and years
BASE_DATA_PATH = "path/to/your/data/folder"
ANALYSIS_YEARS = [2024, 2025]  # Years to process
```

## 📊 Usage

### Option 1: Run Complete Pipeline
```bash
python run_pipeline.py
```
Choose option 4 to run all steps sequentially.

### Option 2: Run Individual Steps

#### Step 1: Sentiment Analysis
```bash
python sentiment_gpt.py
```
- **Input**: Excel files with text content (auto-detects columns like `Tweet_Content`, `Content`, `Text`, `Message`, `Post`)
- **Output**: Excel files with `text` and `sentiment` columns
- **Function**: Uses GPT to classify each post as Positive/Negative/Neutral toward your specified topic

#### Step 2: Quarterly Data Division  
```bash
python divide_by_quarter.py
```
- **Input**: Files with timestamp data (auto-detects columns like `UTC_Time`, `Created_At`, `Timestamp`, `Date`, `Time`)
- **Output**: `{year}_{quarter}.xlsx` files (e.g., `2024_Q1.xlsx`)
- **Function**: Splits data by quarters based on timestamps

#### Step 3: Trend Visualization
```bash
python line_chart_by_quarter.py
```
- **Input**: Quarterly files with sentiment data (auto-detects sentiment columns)
- **Output**: Line chart PNG file showing sentiment trends
- **Function**: Calculates percentages and generates trend visualization

## 📁 File Structure

```
sentiment_analyse/
├── sentiment_gpt.py          # Step 1: Sentiment analysis
├── divide_by_quarter.py      # Step 2: Quarterly segmentation  
├── line_chart_by_quarter.py  # Step 3: Trend visualization
├── run_pipeline.py           # Main execution script
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
└── README.md                 # This documentation
```

## 📋 Excel File Requirements

### Input Files Organization

**Yes, files must be organized by year:**

- `filtered_tweets_2024.xlsx`
- `filtered_tweets_2025.xlsx`
- etc.

### Required Excel Columns

| Step | Required Column | Description |
|------|----------------|-------------|
| **Step 1** | `Tweet_Content` | Text content for sentiment analysis |
| **Step 2** | `UTC_Time` | Timestamp for quarterly division |
| **Step 3** | `sentiment` | Sentiment labels (created by Step 1) |

### Example Excel Structure

```
| Tweet_Content                          | UTC_Time            |
|---------------------------------------|---------------------|
| "Great news about renewable energy!"  | 2024-01-15 10:30:00 |
| "Climate change is concerning..."      | 2024-01-16 14:20:00 |
| "Interesting development in tech"      | 2024-01-17 09:15:00 |
```

After Step 1, a `sentiment` column will be added.

## 📈 Output Files

1. **Sentiment Results**: `results_{year}_sentiment.xlsx` or `sentiment_results.xlsx`
   - Columns: `text`, `sentiment`
   - Contains all original text with classified sentiments
   
2. **Quarterly Files**: `{year}_{quarter}.xlsx` 
   - Example: `2024_Q1.xlsx`, `2024_Q2.xlsx`
   - Data organized by calendar quarters
   
3. **Trend Chart**: `{topic}_sentiment_trend_{start_year}_{end_year}_by_quarter.png`
   - Line chart showing sentiment percentages over time
   - Customizable styling and colors

## 🎯 Key Features

### Data Integrity
- **Zero data loss**: Every input tweet gets a sentiment classification
- **Batch validation**: Ensures input-output count matching
- **Error handling**: Failed batches use default "Neutral" sentiment

### Robust Processing  
- **Automatic retry**: API failures are handled gracefully
- **Progress tracking**: Clear console output showing processing status
- **File validation**: Checks for required columns and file existence

### Flexible Configuration
- **Environment variables**: Secure API key management
- **Customizable parameters**: Batch sizes, years, paths
- **Multiple execution modes**: Run individual steps or complete pipeline

## ⚙️ Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `BATCH_SIZE` | GPT API batch size | 30 |
| `API_DELAY` | Delay between API calls (seconds) | 1.0 |
| `ANALYSIS_YEARS` | Years to process | [2024, 2025] |
| `BASE_DATA_PATH` | Data folder path | See config.py |

## 🔍 Troubleshooting

### Common Issues:

1. **API Key Error**
   - Set `AZURE_API_KEY` environment variable
   - Or update the default value in `config.py`

2. **File Not Found**
   - Check `BASE_DATA_PATH` in `config.py`
   - Ensure input files follow naming convention

3. **Column Not Found**
   - Verify Excel files contain required columns
   - Check column names match expected values

4. **Permission Denied**
   - Ensure write permissions to output directory

## 📝 Example Workflow

1. Prepare data files by year: `filtered_tweets_2024.xlsx`, `filtered_tweets_2025.xlsx`
2. Change topic in `config.py`: `ANALYSIS_TOPIC = "climate change"`
3. Run pipeline: `python run_pipeline.py` → Choose option 4
4. View results: Check generated trend chart and quarterly data

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for research purposes. Please ensure compliance with data usage policies and API terms of service.