from flask import Flask, render_template, request
from job_processor import process_url


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    job_data = None
    if request.method == 'POST':
        url = request.form.get('url')
        job_data = process_url(url)
    return render_template('index.html', job_data=job_data)


if __name__ == '__main__':
    app.run(debug=True)
