import numpy as np
import pandas as pd

# Function to calculate UN for a given point and polynomial order
def calculate_UN_for_point(E_point, N_point, UN_point, order, csv_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Extract the UN, E, and N columns
    point = df['Field1']
    df['UN'] = df['UN'].astype(float)
    UN = df['UN'].values
    df['E'] = df['E'].astype(float)
    E = df['E'].values
    df['N'] = df['N'].astype(float)
    N = df['N'].values

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

# Example usage
# 397402.0	554803.0	-98.27
csv_path = 'Model.csv'
E_point = 397402.0
N_point = 554803.0
UN_point = -98.27
order = 6

UN_new, UN_diff = calculate_UN_for_point(E_point, N_point, UN_point, order, csv_path)
print("Predicted UN value for the given point:", UN_new)
print("Difference between predicted and given UN:", UN_diff)

