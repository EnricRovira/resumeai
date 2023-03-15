"""
python3 resumeai/app.py
"""

from flask import Flask, render_template, request
import openai
import requests
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
DEBUG = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resumen', methods=['POST'])
def resumir():
    resumen_generado = False
    url = request.form['url']
    if not url.startswith("https://"):
        error = "Por favor, ingrese una URL que comience con 'https://'"
        return render_template('index.html', error=error)

    response = requests.get(url)
    texto_html = response.text
    
    if DEBUG:
        resumen = 'Estas en modo Debug, esto es un resumen de ejemplo.'
    else:
        resumen = openai.Completion.create(
            engine="davinci",
            prompt=texto_html,
            max_tokens=100, 
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].text
    resumen_generado = True
    return render_template('index.html', resumen=resumen, resumen_generado=resumen_generado)


if __name__ == '__main__':
    app.run(debug=True)