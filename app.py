from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


# This route is for all URLs submitted by the user for job descriptions
@app.route('/add_job', methods=['POST'])
def add_job():
    url = request.form.get('url')
    
    if url is None:
        return {"error": "No url provided"}, 400

    # Here we will use job_processor to process the URL
    # job_details = process_url(url)

    # For now, we'll just return a placeholder response
    return {"message": "Job added successfully", "url": url}


if __name__ == '__main__':
    app.run(debug=True)
