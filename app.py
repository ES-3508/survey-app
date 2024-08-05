# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from services.geoid_point import calculate_UN_for_point
from services.geoid_file import calculate_UN_for_dataframe

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'geoid_point' in request.form:
            return redirect(url_for('geoid_point_form'))
        elif 'geoid_file' in request.form:
            return redirect(url_for('geoid_file_form'))
        elif 'hybrid' in request.form:
            return redirect(url_for('hybrid_form'))
        elif 'hybrid_file' in request.form:
            return redirect(url_for('hybrid_file_form'))
    return render_template('home.html')

@app.route('/geoid_point', methods=['GET', 'POST'])
def geoid_point_form():
    orthometric_height = None
    north = east = undulation = 0.0
    order = 5  # Default value

    if request.method == 'POST':
        try:
            north = float(request.form.get('north', 0))
            east = float(request.form.get('east', 0))
            undulation = float(request.form.get('undulation', 0))
            order = int(request.form.get('order', 5))  # Default value is 5
            csv_path = 'services/Model.csv'
            UN_new, UN_diff = calculate_UN_for_point(east, north, undulation, order, csv_path)
            print(UN_new)

            # Print the input values
            print(f"North: {north}, East: {east}, Undulation: {undulation}, Order: {order}")

            # Perform calculations or processing here
            orthometric_height = UN_new  # Example calculation

        except ValueError:
            print("Invalid input for one of the fields.")

    return render_template('geoid_point_form.html', 
                           orthometric_height=orthometric_height, 
                           north=north, 
                           east=east, 
                           undulation=undulation,
                           order=order)

@app.route('/geoid_file', methods=['GET', 'POST'])
def geoid_file_form():
    table_data = None
    order = 5  # Default value

    if request.method == 'POST':
        file = request.files['file']
        if file:
            df_i = pd.read_csv(file)
            csv_path = 'services/Model.csv'
            order = int(request.form.get('order', 5))  # Default value is 5
            df = calculate_UN_for_dataframe(df_i, csv_path, order)
            if set(['East', 'North', 'UN1', 'UN_new']).issubset(df.columns):
                df = df[['East', 'North', 'UN1', 'UN_new']]
                table_data = {
                    "columns": df.columns.tolist(),
                    "data": df.values.tolist()
                }
                print("File uploaded and processed.")
            else:
                print("Required columns not found in the uploaded file.")

    return render_template('geoid_file_form.html', table_data=table_data)

@app.route('/hybrid', methods=['GET', 'POST'])
def hybrid_form():
    orthometric_height = None
    north = east = undulation = elipse = 0.0
    order = 5  # Default value

    if request.method == 'POST':
        north = float(request.form.get('north', 0))
        east = float(request.form.get('east', 0))
        elipse = float(request.form.get('elipse', 0))
        undulation = float(request.form.get('undulation', 0))
        order = int(request.form.get('order', 5))  # Default value is 5

        csv_path = 'services/Model.csv'
        UN_new, UN_diff = calculate_UN_for_point(east, north, undulation, order, csv_path)

        # Print the input values
        print(f"North: {north}, East: {east}, Elipse: {elipse}, Undulation: {undulation}, Order: {order}")

        # Perform calculations or processing here
        orthometric_height = UN_new+elipse # Example calculation

    return render_template('hybrid_form.html', 
                           orthometric_height=orthometric_height, 
                           north=north, 
                           east=east, 
                           elipse=elipse,
                           undulation=undulation,
                           order=order)


@app.route('/hybrid_file', methods=['GET', 'POST'])
def hybrid_file_form():
    table_data = None

    if request.method == 'POST':
        file = request.files['file']
        order = int(request.form.get('order', 5))  # Default value is 5
        if file:
            df_input = pd.read_csv(file)
            df_results = calculate_UN_for_dataframe(df_input, 'services/Model.csv', order)
            table_data = {
                "columns": df_results.columns.tolist(),
                "data": df_results.values.tolist()
            }
            print("File uploaded and processed.")

    return render_template('hybrid_file_form.html', table_data=table_data)


if __name__ == '__main__':
    app.run(debug=True)
