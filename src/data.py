import glob
import pandas as pd


def load_or_create_data():
    """Load data from gap.csv or create it from raw data files"""
    try:
        grouped = pd.read_csv('data/gap.csv')
        print("Loaded data from gap.csv")
        return grouped
    except Exception:
        print("Creating data from raw files...")
        return create_data_from_raw_files()


def create_data_from_raw_files():
    """Create processed data from raw order and region files"""
    # Get a list of all order files
    order_files = glob.glob('data/A03_data/training_data/order_data/order_data_*')

    # Read each file and append it to a list
    dfs = [pd.read_csv(file, sep='\t', header=None) for file in order_files]

    # Concatenate all dataframes into one
    orders = pd.concat(dfs, ignore_index=True)

    # Assign column names for the orders data
    orders.columns = ['order_id', 'driver_id', 'passenger_id', 'start_region_hash',
                      'dest_region_hash', 'price', 'Time']

    # Read the regions data
    regions = pd.read_csv('data/A03_data/training_data/cluster_map/cluster_map', sep='\t', header=None)

    # Assign column names for the regions data
    regions.columns = ['region_hash', 'region_id']

    # Merge the orders and regions data on the region hash
    data = pd.merge(orders, regions, left_on='start_region_hash', right_on='region_hash')

    # Get time slot from the 'Time' column
    data['Time'] = pd.to_datetime(data['Time'])
    data['time_slot'] = data['Time'].dt.hour * 6 + data['Time'].dt.minute // 10

    # Group the data by region, and time slot to calculate the demand and supply
    grouped = data.groupby(['region_id', 'time_slot']).agg({
        'driver_id': lambda x: x.notna().sum(),  # supply
        'order_id': 'count',  # demand,
        'Time': 'first'  # time
    }).reset_index()

    # Calculate the gap between demand and supply
    grouped['gap'] = grouped['order_id'] - grouped['driver_id']

    # Select only the necessary columns
    grouped = grouped[['region_id', 'time_slot', 'Time', 'gap']]

    # Save the grouped data to a CSV file
    grouped.to_csv(r'data/gap.csv', index=False)

    return grouped


def preprocess_data(grouped):
    """Process and clean the data for modeling"""
    # Calculate the upper and lower bound
    lower = grouped['gap'].quantile(0.1)
    upper = grouped['gap'].quantile(0.9)

    # Remove outliers
    grouped = grouped[(grouped['gap'] >= lower) & (grouped['gap'] <= upper)]

    # Split the data into features (X) and target (y)
    X = grouped[['region_id', 'time_slot']]
    y = grouped['gap']

    # Keep original data for output
    output = grouped[['region_id', 'time_slot', 'Time']].copy()

    # Convert the 'Time' column to datetime
    output['Time'] = pd.to_datetime(output['Time'])

    return X, y, output


def tokenize_input(input_str):
    """Tokenize the input string into a format suitable for prediction"""
    try:
        region_id, time_str = input_str.split(', ')
        time = pd.to_datetime(time_str) + pd.DateOffset(minutes=30)
        time_slot = time.hour * 6 + time.minute // 10
        data = {
            'region_id': [int(region_id)],
            'time_slot': [time_slot],
        }
        return pd.DataFrame(data), time
    except ValueError:
        print("Invalid input format. Expected format: 'region_id, Date Time'")
        return None, None
