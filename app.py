import sys
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
import numpy as np
from flask import Flask, render_template, request, jsonify
import transformers

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

new_model = AutoModelForSequenceClassification.from_pretrained('./model/bert_model/').to(device)


tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased',model_max_length=128)

label_info = {
'LABEL_1':'digestive system diseases',
'LABEL_2':'cardiovascular diseases' ,
'LABEL_3':'neoplasms',
'LABEL_4':'nervous system diseases',
'LABEL_5':'general pathological conditions'
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    
    # try:

    input_text = request.get_json(force=True)['input']
    print(input_text,file=sys.stderr)

    pipeline = transformers.pipeline(
        "sentiment-analysis",
        model = new_model.to(device),
        tokenizer = tokenizer,
        max_length = 128,
        device=device,
        function_to_apply='softmax'
    )
    
    
    y_pred = pipeline(input_text)
    predictions = y_pred[0]['label']
    
    return jsonify({'prediction': (label_info[predictions])})
    
    # except Exception as e:
    #     return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=7860)