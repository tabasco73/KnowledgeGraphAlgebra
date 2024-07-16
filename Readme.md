To see graph:
Run:
```
brew install graphviz
```
to install graphviz and then create a virtual environment with for example
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -U
```
to create, activate and install dependencies

Then you can run it with it
```
generate_graph.py
```
to see a knowledge graph for the course and
```
generate_argument.py
```
to generate logical arguments about the nature of the concepts based on the knowledge graph.

If you want to fork my generation of relationships and try it on your course, you need to create a .env file with OPENAI_API_KEY = "whatever-your-key-is"
