from astropy.io import fits
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd

# Load the SAO catalog from a FITS file
fits_file = 'I_131A.fits'  # this is probably going to cause errors later
hdul = fits.open(fits_file)
data = hdul[1].data

# Extract the necessary columns (RA, DE, distance, Vmag)
ra = data['RA']            # Right Ascension in degrees
dec = data['DE']           # Declination in degrees
distances = data['distance']  # Distance of stars in parsecs (if available)
vmag = data['Vmag']        # Visual magnitude

# Define the position of the exoplanet in the same coordinate system
# Example: Kepler-22b coordinates
exo_ra = 285.679  # Right Ascension of the exoplanet in degrees
exo_dec = 6.459   # Declination of the exoplanet in degrees
exo_distance = 600  # Distance from Earth to the exoplanet in light-years

# Convert the star coordinates (RA, Dec, distance) to 3D Cartesian coordinates
def to_cartesian(ra, dec, distance):
    # Convert RA/Dec from degrees to radians
    ra_rad = np.deg2rad(ra)
    dec_rad = np.deg2rad(dec)
    
    # Convert spherical to Cartesian coordinates
    x = distance * np.cos(ra_rad) * np.cos(dec_rad)
    y = distance * np.sin(ra_rad) * np.cos(dec_rad)
    z = distance * np.sin(dec_rad)
    
    return x, y, z

# Cartesian coordinates of stars from Earth's perspective
x_stars, y_stars, z_stars = to_cartesian(ra, dec, distances)

# Convert the exoplanet's position to Cartesian coordinates
x_exo, y_exo, z_exo = to_cartesian(exo_ra, exo_dec, exo_distance)

# Shift the stars' positions relative to the exoplanet
x_rel = x_stars - x_exo
y_rel = y_stars - y_exo
z_rel = z_stars - z_exo

# Calculate the new distances from the exoplanet to each star
distances_from_exoplanet = np.sqrt(x_rel**2 + y_rel**2 + z_rel**2)

# Recalculate the apparent brightness using the inverse square law
# The apparent brightness (magnitude) from the exoplanet's point of view:
# m_exo = m_earth - 5 * log10(d_exo / d_earth) - shoutout to my astrophysics stars and galaxies from last semester
vmag_exo = vmag + 5 * np.log10(distances_from_exoplanet / distances)

# Create a DataFrame to store the recalculated data
df = pd.DataFrame({
    'RA': ra,
    'DE': dec,
    'Vmag_exo': vmag_exo,
    'distance_from_exoplanet': distances_from_exoplanet
})

# Sort by the new apparent magnitude from the exoplanet's perspective
df_sorted = df.sort_values(by='Vmag_exo')

# Select the top 200 brightest stars
top_200_brightest = df_sorted.head(200)

# Save the top 200 brightest stars to a CSV file
top_200_brightest.to_csv('top_200_brightest_exoplanet.csv', index=False)

# Print the top 200 stars
print(top_200_brightest)

# Close the FITS file to free resources
hdul.close()
