# Knowledge Graph and Argument Generator

## Prerequisites

To visualize the graph, ensure you have [Graphviz](https://graphviz.org/) installed. You can install it using Homebrew:

```sh
brew install graphviz
```

## Setup

1. **Create a Virtual Environment**

   Set up a virtual environment. For example:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**

   Install the required dependencies by running:

   ```sh
   pip install -r requirements.txt -U
   ```

## Usage

1. **Generate Knowledge Graph**

   Run the following script to generate a knowledge graph for the course:

   ```sh
   python generate_graph.py
   ```

2. **Generate Logical Arguments**

   To generate logical arguments about the nature of the concepts based on the knowledge graph, run:

   ```sh
   python generate_argument.py
   ```

## Customization

If you want to fork and customize the generation of relationships for your own course, create a `.env` file in the project directory with your OpenAI API key:

```
OPENAI_API_KEY = "your-api-key-here"
```

Feel free to explore and modify the scripts to fit your needs!