import numpy as np
import pandas as pd

# Function to calculate UN for a given point and polynomial order
def calculate_UN_for_point(E_point, N_point, UN_point, order, df_model):
    # Extract the UN, E, and N columns from the model DataFrame
    df_model['UN'] = df_model['UN'].astype(float)
    UN = df_model['UN'].values
    df_model['E'] = df_model['E'].astype(float)
    E = df_model['E'].values
    df_model['N'] = df_model['N'].astype(float)
    N = df_model['N'].values

    # Degree of the polynomial
    n = order

    # Initialize the list for storing columns of the design matrix
    columns = [np.ones(len(E))]  # Start with the intercept term

    # Generate terms for the design matrix
    for i in range(1, n + 1):  # Powers of E
        columns.append(E**i)
    for i in range(1, n + 1):  # Powers of N
        columns.append(N**i)
    for i in range(1, n):  # Mixed terms
        for j in range(1, n - i + 1):
            columns.append((E**i)*(N**j))

    X = np.column_stack(columns)

    AT = np.transpose(X)
    ATX = np.dot(AT, X)
    ATXI = np.linalg.inv(ATX)
    Y = np.dot(ATXI, AT)
    Z = np.dot(Y, UN)

    # Preparing the input point for prediction
    point_columns = [1]  # Start with the intercept term
    for i in range(1, n + 1):  # Powers of E
        point_columns.append(E_point**i)
    for i in range(1, n + 1):  # Powers of N
        point_columns.append(N_point**i)
    for i in range(1, n):  # Mixed terms
        for j in range(1, n - i + 1):
            point_columns.append((E_point**i) * (N_point**j))

    point_array = np.array(point_columns)

    # Predict UN value for the given point
    UN_new = point_array.dot(Z)
    UN_diff = UN_new - UN_point

    return UN_new, UN_diff

# Function to process a DataFrame of points and calculate UN for each
def calculate_UN_for_dataframe(df_input, model_csv_path, order):
    # Load the model CSV file into a DataFrame
    df_model = pd.read_csv(model_csv_path)

    # Ensure input DataFrame has the required columns
    required_columns = ['UN1', 'East', 'North']
    if not all(col in df_input.columns for col in required_columns):
        raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

    # Calculate UN_new and UN_diff for each row
    results = []
    for _, row in df_input.iterrows():
        E_point = row['East']
        N_point = row['North']
        UN_point = row['UN1']

        UN_new, UN_diff = calculate_UN_for_point(E_point, N_point, UN_point, order, df_model)
        results.append([E_point, N_point, UN_point, UN_new, UN_diff])

    # Create a DataFrame with the results
    df_results = pd.DataFrame(results, columns=['East', 'North', 'UN1', 'UN_new', 'UN_diff'])

    return df_results

# Example usage
if __name__ == '__main__':
    # Model data
    model_csv_path = 'Model.csv'

    # Input points
    data = {
        'UN1': [-98.27, -98.30],
        'East': [554803.0, 554804.0],
        'North': [397402.0, 397403.0]
    }
    df_input = pd.DataFrame(data)

    order = 3

    # Calculate UN for each point in the DataFrame
    df_results = calculate_UN_for_dataframe(df_input, model_csv_path, order)
    print(df_results)
