from flask import Flask, request, jsonify, render_template, send_file
import json

app = Flask(__name__)

# Sample dataset (replace this with your actual data or database)
# dataset = pd.read_csv("dataset.csv")

app.static_folder = 'static'  # Set the name of the static folder
app.static_url_path = '/static'  # Set the URL path for static files

file = open('dataset_10k.json')
dataset = json.load(file)

@app.route('/')
def main_page():
    return render_template('main_page2.html')

@app.route('/Resource')
def resource():
    return render_template('Resource.html')

@app.route('/CaseStudy1')
def case1():
    return render_template('CaseStudy1.html')

@app.route('/CaseStudy2')
def case2():
    return render_template('CaseStudy2.html')


@app.route('/download/dataset_10k_100723.csv')
def download_file():
    return send_file('dataset_10k_100723.csv', as_attachment=True)


# Define a route to retrieve the dataset
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    
    min_age_filter = request.args.get('min_age')
    max_age_filter = request.args.get('max_age')
    min_date_filter = request.args.get('min_date')
    max_date_filter = request.args.get('max_date')
    gender_filter = request.args.get('gender')
    race_filter = request.args.get('race')
    
    hospital_filter = request.args.get('hospital_id')

    filtered_data = dataset

    if min_age_filter:
        filtered_data = [item for item in filtered_data if item['age'] >= int(min_age_filter)]

    if max_age_filter:
        filtered_data = [item for item in filtered_data if item['age'] <= int(max_age_filter)]

    if min_date_filter and max_date_filter:
        filtered_data = [
            item for item in filtered_data
            if datetime.strptime(item['datetime'], '%Y-%m-%d') >= datetime.strptime(min_date_filter, '%Y-%m-%d')
            and datetime.strptime(item['datetime'], '%Y-%m-%d') <= datetime.strptime(max_date_filter, '%Y-%m-%d')
        ]
    if gender_filter:
        filtered_data = [item for item in filtered_data if item['gender'] == gender_filter]

    if race_filter:
        filtered_data = [item for item in filtered_data if item['race'] == race_filter]

    if hospital_filter:
        filtered_data = [item for item in filtered_data if item['hospital_id'] == hospital_filter]
    
    return jsonify(filtered_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)