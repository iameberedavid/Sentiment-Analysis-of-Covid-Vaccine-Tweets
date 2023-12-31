import gradio as gr
import numpy as np
import os
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
from scipy.special import softmax


# Load the model components from huggingface
model_path = 'iameberedavid/results'
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def sentiment_analysis(text):
    text = preprocess(text)

    # PyTorch-based models
    input = tokenizer(text, return_tensors='pt')
    output = model(**input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)

    # Format output results
    labels = {0: 'NEGATIVE', 1: 'NEUTRAL', 2: 'POSITIVE'}
    scores = {labels[i]: float(s) for i, s in enumerate(scores_)}
    return scores

# App setup
demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(placeholder='What do you think about COVID vaccines?'),
    outputs='label',
    interpretation='default',
    examples=[
    ['The vaccines are cool'],
    ["I don't know about the vaccines"],
    ['Covid vaccines are not effective'],
    ['Covid vaccines are effective'],
    ["I don't trust those vaccines"]
    ],
    title='SENTIMENT ANALYSIS FOR COVID VACCINATION',
    description="This app predicts the public sentiment on COVID vaccines, telling if users have 'NEGATIVE', 'NEUTRAL', or 'POSITIVE' sentiments.",
    theme='default', 
    live=True 
)
demo.launch(inbrowser=True, show_error=True, share=True)