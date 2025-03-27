import pandas as pd
from datetime import datetime
from multiprocessing import Pool
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path

"""
INCORRECT CODES LINES 29,43,48,147,150,163,187,226
"""

# ==================================
# INSTRUCTIONS
# ==================================
# 1. Replace all places where there is 'YOUR CODE HERE" with your own code
# 2. You can test and check the code in Jupyter Notebook but the submission should be a Python file
# 3. Please name your Python script like this: FirstName_MiddleName_LastName

def get_date_range_by_chunking(large_csv):
    """
    In this function, the idea is to use pandas chunk feature.
    :param large_csv: Full path to activity_log_raw.csv
    :return:
    """
    # ======================================
    # EXPLORE THE DATA
    # ======================================
    # Read the first 100,000 rows in the dataset
    df_first_100k = pd.read_csv("activity_log_raw.csv",nrows=100.000)
    print(df_first_100k.head())
    # Identify the time column in the dataset
    str_time_col = 'ACTIVITY_TIME'

    # ============================================================
    # FIND THE FIRST [EARLIEST] AND LAST DATE IN THE WHOLE DATASET
    # BY USING CHUNKING
    # =============================================================
    # set chunk size to some number. You can play around with the chunk size to see its effect
    chunksize = 500000

    # declare a list to hold the dates
    dates =  []
    with pd.read_csv("activity_log_raw.csv", nrows=100 ,chunksize=chunksize) as reader:
        for chunk in reader:
            # convert the string to Python datetime object
            # add a new column to hold this datetime object. For instance,
            # you can call it "activ_time"
            #time_col = data['ACTIVITY_TIME']
            chunk['str_time_col']=chunk['ACTIVITY_TIME']
            chunk['time_col'] = chunk['str_time_col'].apply(lambda x: pd.to_datetime(x[:9]))
            chunk.sort_values(by='time_col', inplace=True)
            top_date = chunk.iloc[0]['time_col']
            # Add the top_date to the list
            dates.append(top_date)
            chunk.sort_values(by='time_col', ascending=False, inplace=True)
            bottom_date = chunk.iloc[0]['time_col']
            # Add the bottom_date to the list
            dates.append(bottom_date)


    # Find the earliest and last date by sorting the dates list we created above
    sorted_dates = sorted(dates)
    first =  sorted_dates[0]
    last = sorted_dates[-1]
    print("First date is {} and the last date is {}".format(first, last))

    return first, last


def quadratic_func(x, a):
    """
    Define the quadratic function like this: y = 2x^2 + a -1
    (read as y is equal to 2 x squared plus a minus 1)
    :param x:
    :return:
    """
    y =  2*x**2+a-1
    return y


def run_the_quad_func_without_multiprocessing(list_x, list_y):
    """
    Run the quadratic function on a huge list of X and Ys without using parallelism
    :param list_x: List of xs
    :param list_y: List of ys
    :return:
    """
    results = [quadratic_func(x, y) for x, y in zip(list_x, list_y)]
    return results


def run_the_quad_func_with_multiprocessing(list_x, list_y, num_processors):
    """
    Run the quadratic function with multiprocessing
    :param list_x: List of xs
    :param list_y: List of xs
    :param num_processors: Number of processors to use
    :return:
    """
    # Use the Pool method to initiate processors with number
    # of processors set to num_processors
    processors =  Pool(4)
    params = [i for i in zip(list_x, list_y)]

    # Use the starmap method for Pool to run the processes
    # Like this: Pool.starmap(func_name, params)
    results = processors.starmap(quadratic_func, params)
    processors.close()
    return results


def multiprocessing_vs_sequential_quadratic(list_len, out_plot, out_csv):
    """
    Compare how
    :param list_len:
    :return:
    """

    data = []
    for i in range(1, list_len):
        list_length = 10 ** i

        # Create lists using the range() function
        # and provided list length param
        x = [i for i in range(list_length)]
        y = [i for i in range(list_length)]

        start_time = datetime.now()
        run_the_quad_func_without_multiprocessing(x, y)
        end_time = datetime.now()
        time_taken_seq = (end_time - start_time).total_seconds()
        data.append({'ListLen': list_length, 'Type' : 'Parallel', 'TimeTaken': time_taken_seq})

        start_time = datetime.now()
        # Call the function run_the_quad_func_with_multiprocessing below
        run_the_quad_func_with_multiprocessing(x, y, 4)
        end_time = datetime.now()
        time_taken_mult = (end_time - start_time).total_seconds()
        data.append({'ListLen': list_length, 'Type' : 'Sequential', 'TimeTaken': time_taken_mult})

    # Create a data frame using the data variable defined above
    df = pd.DataFrame(data)
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='ListLen', y='TimeTaken', hue='Type')

    # Use plt.savefig() to save the plot
    plt.savefig('Multi')

    # Also save the pandas dataframe defined above
    df.to_csv("dataframe")

def get_num_uniq_users(csv_file, userid_col):
    """
    A Helper function to help get the number of unique users
    :param csv_file: path to CSV file
    :param userid_col: Column for user ID
    :return:
    """
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)

    # Use the nunique() method to get number of unique users
    num = len(np.unique(df[userid_col]))

    return num


def get_tot_uniq_users_parallel(path_to_csv, num_processors):
    """

    :param path_to_csv:
    :return:
    """
    # ==================================================
    # GET LIST OF ALL CSV FILES AND PUT IN A LIST
    # ===================================================
    # convert the string URL for path to a Path object for easier interaction
    start = datetime.now()
    path_to_csv = Path(path_to_csv)
    list_csv = [f for f in path_to_csv.iterdir() if f.suffix == '.csv']


    # ======================================================
    # USE MULTIPROCESSING TO GET UNIQUE USERS FROM ALL CSV'S
    # ======================================================
    # Create processors using Pool and num_processors
    processors = Pool(4)

    # Prepare parameters for the get_num_uniq_users() function
    user_id_col = ['user_id']*len(list_csv)     # List containing parameters for the user_id column
    params = [i for i in zip(list_csv, user_id_col)]  # combine the two lists
    # Run the function in parallel
    results = processors.starmap(get_num_uniq_users, params)
    processors.close()

    # combine results to get the total
    tot_users = sum(results)
    end = datetime.now()
    time_taken = round((end - start).total_seconds(), 2)
    print('Total unique users: {:,} in {} seconds'.format(tot_users, time_taken))

    return tot_users

def get_tot_uniq_users_seq(path_to_csv, userid_col):
    """

    :param path_to_csv:
    :return:
    """
    # ==================================================
    # GET LIST OF ALL CSV FILES AND PUT IN A LIST
    # ===================================================
    # convert the string URL for path to a Path object for easier interaction
    start = datetime.now()
    path_to_csv = Path(path_to_csv)
    list_csv = [f for f in path_to_csv.iterdir() if f.suffix == '.csv']

    tot_users = 0
    for csv in list_csv:
        # Read CSV into pandas dataframe
        df = pd.read_csv(csv)
        # Get unique number of users using nunique() and the column for user_id
        uniq = np.unique(df['userid_col'])

        # Increment the total number of users
        tot_users += len(uniq)

    end = datetime.now()
    time_taken = round((end - start).total_seconds(), 2)
    print('Total unique users: {:,} in {} seconds'.format(tot_users, time_taken))

    return tot_users



if __name__ == '__main__':
    # Question-1: Pandas chunks
    file = "home/mozart/Desktop/big data analytic/activity_log_raw.csv"#->"activity_log_raw.csv"
    get_date_range_by_chunking(file)

    # Question-2: CPU bound parallelization
    out_plot = "/home/mozart/Desktop/big data analytic"
    out_csv = "/home/mozart/Desktop/big data analytic"
    multiprocessing_vs_sequential_quadratic(9, out_plot, out_csv)

    # =====================================================
    # QUESTION-3: CPU BOUND PARALLELIZATION WITH PANDAS
    # =====================================================
    fpath = "/home/mozart/Desktop/big data analytic"
    get_tot_uniq_users_parallel(fpath, 12)
    get_tot_uniq_users_seq(fpath, 'user_id')