# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'geoid' in request.form:
            return redirect(url_for('geoid_form'))
        elif 'hybrid' in request.form:
            return redirect(url_for('hybrid_form'))
    return render_template('home.html')

@app.route('/geoid', methods=['GET', 'POST'])
def geoid_form():
    orthometric_height = None
    north = east = elipse = 0.0

    if request.method == 'POST' and 'submit_point' in request.form:
        north = float(request.form.get('north', 0))
        east = float(request.form.get('east', 0))
        elipse = float(request.form.get('elipse', 0))
        # Perform calculations or processing here
        orthometric_height = 5  # Example value

    return render_template('geoid_form.html', 
                           orthometric_height=orthometric_height, 
                           north=north, 
                           east=east, 
                           elipse=elipse)

@app.route('/hybrid', methods=['GET', 'POST'])
def hybrid_form():
    orthometric_height = None
    north = east = elipse = 0.0

    if request.method == 'POST':
        north = float(request.form.get('north', 0))
        east = float(request.form.get('east', 0))
        elipse = float(request.form.get('elipse', 0))
        # Perform calculations or processing here
        orthometric_height = 5  # Example value

    return render_template('hybrid_form.html', 
                           orthometric_height=orthometric_height, 
                           north=north, 
                           east=east, 
                           elipse=elipse)

if __name__ == '__main__':
    app.run(debug=True)
