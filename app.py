from flask import Flask, render_template, jsonify
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd

app = Flask(__name__)

# Function to load the star catalog from CSV file
def load_star_catalog():
    df = pd.read_csv('star_catalog.csv')  # Replace with your actual file
    stars = []
    for index, row in df.iterrows():
        star_coord = SkyCoord(ra=row['ra'], dec=row['dec'], distance=row['distance'], unit='deg')
        stars.append({
            'ra': star_coord.ra.deg,
            'dec': star_coord.dec.deg,
            'distance': row['distance']
        })
    return stars

stars = load_star_catalog()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planet/<name>')
def show_planet(name):
    return render_template('exoplanet1.html', planet=name)

@app.route('/api/stars')
def get_stars():
    planet_ra = 280.0  # Example RA for the exoplanet
    planet_dec = -23.5 # Example Dec for the exoplanet
    exo_coords = SkyCoord(ra=planet_ra, dec=planet_dec, unit='deg')

    star_positions = []
    for star in stars:
        star_coord = SkyCoord(ra=star['ra'], dec=star['dec'], distance=star['distance'], unit='deg')
        relative_position = exo_coords.separation(star_coord)
        star_positions.append({
            'x': np.cos(relative_position.ra.deg), 
            'y': np.sin(relative_position.ra.deg), 
            'z': np.cos(relative_position.dec.deg), 
            'brightness': 1 / star['distance']
        })

    return jsonify(star_positions)

if __name__ == '__main__':
    app.run(debug=True)
