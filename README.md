# Elysia: An Agentic RAG App

![1758556308083](image/elysia.png)
Elysia is an agentic Retrieval-Augmented Generation (RAG) application designed to enhance the capabilities of AI models by integrating them with external knowledge bases. This application leverages the power of Weaviate, a vector search engine, to provide contextually relevant information to AI models, thereby improving their performance in tasks requiring external knowledge.

## Features

- **Weaviate Integration**: Seamlessly connect to a Weaviate instance to store and retrieve vectorized data.
- **Batch Processing**: Efficiently process large datasets with batch operations, ensuring smooth and fast data handling.
- **Error Handling**: Robust error management during data import to prevent disruptions.
- **Environment Configuration**: Securely manage credentials and configurations using environment variables.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.12
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/edcalderin/elysia-agentic-rag-app.git
   cd elysia-agentic-rag-app
   ```

2. Create and activate a conda environment:
   ```bash
   conda create --name elysia-env python=3.12
   conda activate elysia-env
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env` file in the root directory and add your Weaviate credentials (ie. `.env.example`):
   ```
   WEAVIATE_URL=your_weaviate_url
   WEAVIATE_API_KEY=your_weaviate_api_key
   COLLECTION_NAME=name_for_your_collection
   ```

### Usage
1. If your dataset is too large, use the existing notebook in the `notebooks/` directory to reduce its size by subsampling. Ensure both the original and the subsampled data are saved in the `data/` directory. 

2. Use the subsampled data for loading into Weaviate. If you do not subsampled the data, ensure to rename the variable in `load_data.py` located in root directory:

   ```python
   FILE_NAME=custom_dataset_name
   ```
    Then, run:

   ```bash
   python load_data.py
   ```

   **Note:** Verify the connection and data import through the console output.

3. Run the Elysia application:
   ```bash
   elysia start
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Acknowledgments

- Thanks to the developers of Weaviate for providing a powerful vector search engine.