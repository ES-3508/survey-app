import pandas as pd
import numpy as np
def print_dataframe_info(df):
    print("DataFrame Head:")
    print(df.head())
    print("\nDataFrame Info:")
    print(df.info())
    print("\nDataFrame Describe:")
    print(df.describe())

# Example usage in calculate_UN_for_point function
def calculate_UN_for_point(E_point, N_point, UN_point, order, csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Print DataFrame information
    # print_dataframe_info(df)

    # Ensure the data types are consistent
    df['UN'] = df['UN'].astype(np.float64)
    df['E'] = df['E'].astype(np.float64)
    df['N'] = df['N'].astype(np.float64)

    UN = df['UN'].values
    E = df['E'].values
    N = df['N'].values

    # Degree of the polynomial
    n = order

    # Initialize the list for storing columns of the design matrix
    columns = [np.ones(len(E), dtype=np.float64)]  # Start with the intercept term

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

    # Print intermediate results
    print("\nDesign Matrix (X):")
    print(X)
    print("\nATX:")
    print(ATX)
    print("\nATXI:")
    print(ATXI)
    print("\nY:")
    print(Y)
    print("\nCoefficients (Z):")
    print(Z)

    # Preparing the input point for prediction
    point_columns = [1.0]  # Start with the intercept term
    for i in range(1, n + 1):  # Powers of E
        point_columns.append(E_point**i)
    for i in range(1, n + 1):  # Powers of N
        point_columns.append(N_point**i)
    for i in range(1, n):  # Mixed terms
        for j in range(1, n - i + 1):
            point_columns.append((E_point**i) * (N_point**j))

    point_array = np.array(point_columns, dtype=np.float64)

    # Print point array
    print("\nPoint Array:")
    print(point_array)

    # Predict UN value for the given point
    UN_new = point_array.dot(Z)
    UN_diff = UN_new - UN_point

    return UN_new, UN_diff



csv_path = 'Model.csv'
E_point = 397402.05
N_point = 554803.0
UN_point = -98.27
order = 6

UN_new, UN_diff = calculate_UN_for_point(E_point, N_point, UN_point, order, csv_path)
print("Predicted UN value for the given point:", UN_new)
print("Difference between predicted and given UN:", UN_diff)

