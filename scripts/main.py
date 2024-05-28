import subprocess
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_path):
    try:
        logging.info(f"Running {script_path}...")
        subprocess.run(['python', script_path], check=True)
        logging.info(f"Finished running {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running {script_path}: {e}")

def main():
    # Define the directory where the scripts are located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List of scripts to run
    scripts_to_run = [
        'data_cleaning.py',
        'data_cleaning_reviews.py',
        'data_prepration.py',
        'eda_imdb_top_1000.py',
        'eda_rotten_tomatoes.py',
        'descriptive_analysis.py',
        'comparative_analysis.py',
        'contentRating_Profitability.py',
        'revenue_analysis.py',
        'sentiment_analysis.py'
    ]

    for script in scripts_to_run:
        script_path = os.path.join(script_dir, script)
        run_script(script_path)

if __name__ == "__main__":
    main()
