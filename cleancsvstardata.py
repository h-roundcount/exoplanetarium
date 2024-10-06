import pandas as pd

def parse_and_clean_csv(input_file, output_file):
    # Read the CSV file, assuming it might be comma-separated
    df = pd.read_csv(input_file, header=None)

    # Split the first row to get column names
    column_names = df.iloc[0, 0].split(',')
    df.columns = column_names

    # Remove the first row from the dataframe
    df = df[1:]

    # List of columns to keep
    columns_to_keep = ['ra', 'dec', 'sy_dist', 'sy_vmag']  # Adjust this to your needs

    # Check for missing columns
    missing_columns = [col for col in columns_to_keep if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following columns are missing: {missing_columns}")

    # Filter the dataframe to keep only the desired columns
    df = df[columns_to_keep]

    # Write the cleaned dataframe to a new CSV file
    df.to_csv(output_file, index=False)



cleaned_data = parse_and_clean_csv(r'C:\Users\23rou\Downloads\exoplanetarium\No_Header STELLARHOSTS_2024.10.06_08.14.11 - STELLARHOSTS_2024.10.06_08.14.11.csv', 'cleaned_file.csv')

