import pandas as pd
from datetime import datetime
from multiprocessing import Pool
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path

# ================================
# MARKING SCHEME NOTES
# ===============================
# 1. In the accompanying assignment Python file, students are supposed to fill in the required code
# in all places where it says "YOUR CODE HERE"
# 2. To find points for that particular line, please refer to the
# corresponding line here, where it has comment POINTS at the end of the line

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
    df_first_100k = pd.read_csv(large_csv, nrows=100000)    # POINTS: 1
    print(df_first_100k)
    # Identify the time column in the dataset
    str_time_col = 'ACTIVITY_TIME'  # POINTS: 1

    # ============================================================
    # FIND THE FIRST [EARLIEST] AND LAST DATE IN THE WHOLE DATASET
    # BY USING CHUNKING
    # =============================================================
    # set chunk size
    chunksize = 1000000 # POINTS: 1
    # declare a list to hold the dates
    dates = []      # POINTS: 1
    with pd.read_csv(large_csv, chunksize=chunksize) as reader: # POINTS: 1
        for chunk in reader:
            # convert the string to Python datetime object
            # add a new column to hold this datetime object
            time_col = 'activ_time' # POINTS: 1
            chunk[time_col] = chunk[str_time_col].apply(lambda x: pd.to_datetime(x[:9]))
            chunk.sort_values(by=time_col, inplace=True)
            top_date = chunk.iloc[0][time_col]
            dates.append(top_date)  # POINTS: 1
            chunk.sort_values(by=time_col, ascending=False, inplace=True)
            bottom_date = chunk.iloc[0][time_col]
            dates.append(bottom_date)   # POINTS: 1


    # Find the earliest and last date by sorting the dates list
    sorted_dates = sorted(dates, reverse=False)     # POINTS: 1
    first = sorted_dates[0] # POINTS: 2
    last = sorted_dates[-1] # POINTS: 2
    print("First date is {} and the last date is {}".format(first, last))

    return first, last


def quadratic_func(x, a):
    """
    Define the quadratic function: y = 2x^2 + y-1
    :param x:
    :return:
    """
    y = 2*(x**2) + a-1      # POINTS: 3
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
    processors = Pool(num_processors)      # POINTS: 2
    params = [i for i in zip(list_x, list_y)]
    results = processors.starmap(quadratic_func, params)    # POINTS: 3
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
        x = [i for i in range(list_len)]        # POINTS: 2
        y = [i for i in range(list_len)]        # POINTS: 2

        start_time = datetime.now()
        run_the_quad_func_without_multiprocessing(x, y)     # POINTS: 2
        end_time = datetime.now()
        time_taken_seq = (end_time - start_time).total_seconds()
        data.append({'ListLen': list_length, 'Type' : 'Parallel', 'TimeTaken': time_taken_seq})

        start_time = datetime.now()
        run_the_quad_func_with_multiprocessing(x, y, 4)     # POINTS: 2
        end_time = datetime.now()
        time_taken_mult = (end_time - start_time).total_seconds()
        data.append({'ListLen': list_length, 'Type' : 'Sequential', 'TimeTaken': time_taken_mult})

    df = pd.DataFrame(data)     # POINTS: 1
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x='ListLen', y='TimeTaken', hue='Type')
    plt.savefig(out_plot)       # POINTS: 1
    df.to_csv(out_csv, index=False)     # POINTS: 1


def get_num_uniq_users(csv_file, userid_col):
    """
    A Helper function to help get the number of unique users
    :param csv_file: path to CSV file
    :param userid_col: Column for user ID
    :return:
    """
    df = pd.read_csv(csv_file)      # POINTS: 1
    num = df[userid_col].nunique()      # POINTS: 2

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
    # Create processors
    processors = Pool(num_processors)       # POINTS: 1

    # Prepare parameters for the get_num_uniq_users() function
    user_id_col = ['user_id']*len(list_csv)     # List containing parameters for the user_id column
    params = [i for i in zip(list_csv, user_id_col)]  # combine the two lists
    # Run the function in parallel
    results = processors.starmap(get_num_uniq_users, params)    # POINTS: 2
    processors.close()

    # combine results
    tot_users = sum(results)        # POINTS: 3
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
        df = pd.read_csv(csv)       # POINTS: 1
        uniq = df[userid_col].nunique() # POINTS: 1
        tot_users += uniq       # POINTS: 2

    end = datetime.now()
    time_taken = round((end - start).total_seconds(), 2)
    print('Total unique users: {:,} in {} seconds'.format(tot_users, time_taken))

    return tot_users


if __name__ == '__main__':
    # Question-1: Pandas chunks
    file = "/Volumes/GoogleDrive/My Drive/TEACHING/aims-cameroon-2020/DAY-4-data/data/activity_log_raw.csv"
    # get_date_range_by_chunking(file)

    # Question-2: CPU bound parallelization
    # multiprocessing_vs_sequential_quadratic(9, 'tmp.png', 'tmp.csv')

    # Question-3: CPU bound parallelization with pandas
    fpath = "/Volumes/GoogleDrive/My Drive/TEACHING/AIMS-22/data/fragmented_CSV"
    get_tot_uniq_users_parallel(fpath, 12)
    # get_tot_uniq_users_seq(fpath, 'user_id')
