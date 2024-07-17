# Knowledge Graph and Argument Generator for Abstract Algebra

## Introduction
(Can be skipped)

When I started studying math at university, I always felt a disconnect between how math was taught and how I most easily learned math. This project is an attempt to approach the abstract concepts taught in math courses in a structured way and to reduce the complexity of what the concepts mean. A key idea in this project is that the essence of a conept can be described through its relationship with other concepts. A mathematical concept has to interact with other concepts, if it is completely isolated from other concepts is will be unusable. 

What I've tried to (with help and feedback from a lot of friends) is, to an as high degree as possible, "factor" out the part of a concept that can be explained through its relationship with other concepts. The "factors" have considered the transferrability of properties between concepts and what context the concept operates in. I call these relationships the "generalization" and "context" relationship. 

The generalization relationship asks the question of whether concept 'a' has all of the properties concept 'b' has, if it does then 'a' specializes b'. One example of this is inheritance in computer science. But this relationship is more general, it could also encompass the object-instance relationship. In fact, the best way of describing the relationship between the inheritance relationship and the generalization relationship is through the generalization relaitonship itself. Every inheritance relationship is a generalization relationship but not the other way around. This type of nestling of the meaning relationship is what is being used to generate arguments based on the graph.

The context relationship simply asks the question of whether the concept of 'a' has to be defined for concept 'b' to make sense. In essence, do we need to include 'a' in our context for concept 'b'.

The graph is generated using LLM's (a mix of GPT-4-turbo and and GPT4o) through function calling and a variety of algorithms based on category theory (and some other stuff) to improve how relationships are predicted. There has also been some manual curation to correct predictions when incorrect predictions are identified.

Finally, arguments are generated using the two relationships above and what I like to call the analogy relationship, if you are interested in how this works, feel free to reach out and I can explain how it works. Might update this here later too. 

For the interested, try to determine whether the generated arguments are True or False. I know that there are False ones, which can stem from incorrect relationship classifications or flaws in the theory used, but most of them actually appear to make sense given enough thought.

Some examples:

 - A submonoid is to a monoid what a subset is to a set (A submonoid is a subset to a monoid)
 - A Ring Endomorphism is to a Ring Automorphism what a Ring Homomorphism is to a Ring Isomorphism (A Ring Endomorphism that is also ismorphic is a Ring Automorphism)
 - An A-module is to a Free A-module what a Group is to an A-module (An A-module is a generalization of a Free A-module)

## Prerequisites

There is a pdf containing the graph, but to recompile the graph, ensure you have grahpviz installed. You can install it using Homebrew:

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

   Run the following script to regenerate the knowledge graph for the course:

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

Feel free to explore and fork to fit your needs!
