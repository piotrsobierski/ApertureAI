# ApertureAI

Welcome to ApertureAI! This is a nifty Streamlit application that uses artificial intelligence to understand images and answer questions. It can look at a picture you upload, tell you what's in it using OpenAI's Vision capabilities, and pick out relevant tags with Amazon Rekognition. Plus, it has a helpful FAQ section powered by a local FAISS vector search and OpenAI embeddings.

## What You'll Need

Before you start, make sure you have a few things ready:

- Python (version 3.8 or newer is best).
- An AWS account with an IAM user. This user will need permission for Amazon Rekognition (specifically `rekognition:DetectLabels`).
- An API key from OpenAI.

## Getting Started

Let's get ApertureAI set up on your computer.

1.  **Grab the Code:**
    Clone the repo

2.  **Set Up Your Workspace:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

    Install all the necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Your Keys:**

    Application settings like default prompts are defined in `config.py`.
    For sensitive credentials like API keys, create a file named `.env` in` project directory. Inside this file, you'll list your keys and any specific configurations. Here's a general idea of what it will contain:

    ```env
    # AWS Credentials
    AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY"
    AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_KEY"
    AWS_DEFAULT_REGION="your-aws-region"

    # OpenAI API Key
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

    # Application Settings (like paths and model names)
    FAQ_SOURCE_JSON_FILE="data/dummy_faq.json"
    FAISS_OUTPUT_DIR_NAME="faiss_index"
    # ... other model names as needed
    ```

    Make sure this `.env` file is listed in your `.gitignore` so you don't accidentally share your secrets!

4.  **Prepare the FAQ Search:**
    To make the FAQ section work, you need to build a local search index. Run the following script:
    ```bash
    python index_faq.py
    ```
    You typically only need to do this once. If you update your FAQ data later (the `dummy_faq.json` file by default), just run this script again.

## Running ApertureAI

Once everything is set up:

1.  Ensure your virtual environment is active.
2.  Navigate to the main project directory (`ApertureAI/`).
3.  Start the application:
    ```bash
    streamlit run app.py
    ```
