# RAG Application - ChatWorkSafeBC - README

## Overview

This RAG (Retrieval Augmented Generation) application leverages the latest advancements in language models and text embeddings to provide accurate, context-aware responses based on a set of provided documents. It consists of two main components: a Chatbot for Conversational AI and a Question and Answering System. The application aims to deliver relevant information with references and confidence scores, enhancing user experience through efficient information retrieval and response generation.

## Features

### Chatbot for Conversational AI

- **Chat History**: Maintains conversation context to provide coherent follow-up responses.
- **Sources/Citations**: Enhances credibility by providing sources for the information given.
- **Custom Retrievals**: Tailors information retrieval to the specific needs of the conversation.
- **Confidence Scores**: Assigns scores to responses to indicate the reliability of the information.

### Question and Answering System

- **Default Q&A Approach**: Offers direct answers to queries based on document retrieval.
- **Sources/Citations and Default Retrievals**: Provides sources for answers and employs a standard method for information retrieval.
- **Confidence Scores**: Includes scores to reflect the certainty of the provided answers.

## Implementation Details

### Models and Technologies Used

- **Text Embedding Models**: Started with `text-embedding-3-large` for deep semantic understanding. To improve latency, we switched to `text-embedding-3-small`, which offers a balanced trade-off between performance and semantic richness.
- **Generative Models**: Initially utilized the latest GPT-4 model for its advanced generative capabilities. Transitioned to `gpt-3.5-turbo-16k` to enhance response times while maintaining quality.
- **Semantic Chunking**: Employed for its effectiveness in maintaining the integrity and contextuality of the text.

### Parameters and Configuration

- **Reduced Embedding Dimensions**: Addressed latency issues by adjusting the embedding vector dimensions without losing conceptual accuracy.
- **Model Selection**: Chose models based on their balance between latency, semantic understanding, and generative quality.

## Testing and Evaluation

- **Langchain LLM**: Generated Q&A pairs for automated testing.
- **Manual Evaluation**: Ensured the ground truth accuracy of the test datasets.
- **RAGAS Framework**: Employed for comprehensive evaluation, including component-wise and end-to-end assessments.

Creating a concise `README.md` file for a GitHub repository involves summarizing the project, its features, how to set it up, and how to use it. Below is a template based on the information you've provided about your Flask application, which integrates both a chatbot (`RagChatApplication`) and a question-answering system (`QuestionAnsweringSystem`).


## Setup

To run this application on your local machine, follow these steps:

1. **Clone the Repository**

```bash
git clone <repository-url>
cd <repository-name>
```

2. **Install Dependencies**

Ensure you have Python 3.x installed, then run:

```bash
pip install -r requirements.txt
```

3. **Environment Variables**

Create a `.env` file in the root directory and add your OpenAI and Pinecone API keys:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

4. **Run the Application**

```bash
flask run
```

## Usage

Once the application is running, navigate to `http://127.0.0.1:5000/` in your web browser. You will be greeted with a home page linking to both the Chatbot.
Also, navigate to `http://127.0.0.1:5000/qna` for Question Answering interfaces.

- **Chatbot**: Click on the Chatbot link to start interacting with the AI chatbot. Type your message and press enter to see the AI's response.
- **Question Answering**: Click on the Question Answering link to ask a specific question. Enter your question and press submit to receive an answer.
