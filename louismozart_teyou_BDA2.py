"""
GENERAL INSTRUCTIONS
1. WHICH PART TO CHANGE?: Uncomment every line with  [YOUR CODE HERE] and replace it with your code.
Please don't change anything else other than these lines. In other parts, the code isnt commented,
so just replace the parts with YOUR CODE or YOUR CODE HEREE

2. USE OF JUPYTER NOTEBOOK: For those who would like to use Jupyter Notebook. You can copy and paste
each function in the notebook environment, test your code their. However,
remember to paste back your code in a .py file and ensure that its running
okay.

3. INDENTATION: Please make sure that you check your indentation

4. Returning things from function: Please dont forget to use the return statement
to return a value when applicable

5. HINTS: please read my comments for hints and instructions where applicable

6. DEFINING YOUR OWN FUNCTIONS: where I ask you to define your own function
please make sure that you name the function exactly as I said.

7. Please work on the following functions in the order provided:
    - add_date_and_filter
    - get_events_before_jul13
    - preprocess_cdrs_using_spark
    - explore_data_with_spark
    - generate_user_attributes_with_pandas
8. Dataset for this work: all the questions are based on the simulated_cdrs dataset,
please download it and have it on your machine
"""
from itertools import groupby
import random
import seaborn as sns
import numpy as np
from collections import namedtuple
from datetime import datetime
from pathlib import Path
import random
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import matplotlib.pyplot as plt

def add_date_and_filter(csv_file, date_format, ref_date):
    """
    Create a dataframe, add date and filter out events based on ref date
    :return:
    """
    df = pd.read_csv(csv_file)
    str_time_col = 'cdr datetime'

    # convert date string to Python datetime
    # please extract only the Year, month and day from the date string using
    # indexing, please use solutions from first assignment to achieve this
    #f = lambda x: pd.to_datetime(x[:10], format=date_format)
    df['cdr_date'] = df[str_time_col].apply(lambda x: pd.to_datetime(str(x)[:9],format=date_format))     ########YOUR CODE

    # please retrieve all events older than or equal to the reference date
    # please use the query function for pandas DataFrame like below
    df.query('cdr_date <= @ref_date', inplace=True)

    if df.shape[0]:
        return df
    else:
        return 'NA'


def get_events_before_jul13(csv_folder, ref_date, date_format, num_csv_files):
    """
    In this function, we will use the map function to run the
    add_date_and_filter above on a list of CSV_files
    :param csv_folder:
    :return:
    """
    list_csv = [f for f in csv_folder.iterdir() if f.suffix == '.csv']
    # use the function random.choices() to select only a sample of the CSVs  for fast processing
    # set k to num_csv_files in the function
    list_csv =  random.choices(list_csv,k= num_csv_files)
    time_format = "%Y%m%d"

    # Use  the datetime.strptime() to convert the string ref_date to Python datetime object
    # This function requires two args, the other one is date format
    ref_date = datetime.strptime(ref_date,  date_format)

    # Run map with multiple iterables(r.g., two lists)
    # Note that input-1 is the list of CSV we generated above
    # Prepare input-2 and input-3 as below. Please use the  multiplication
    # operator on a single list item to repeat the same element multiple
    # times in a list as we did in the first assignment
    list_date_format = [date_format]*len(list_csv)
    list_date_ref_date = [ref_date]*len(list_csv)

    # now run the map function with the three input lists we have defined
    results = map(add_date_and_filter,list_csv,list_date_format,list_date_ref_date)

    # write code to identify elements in the list which arent s 'NA'
    # You can use a list comprehension with if condition. To identify elements
    # which are 'NA', you can use isinstance() function to detect data type
    no_na_results = []
    print('I found {} non NA results'.format(len(no_na_results)))

    return no_na_results


def rename_sdf(df, mapper=None):
    ''' Rename column names of a dataframe
        mapper: a dict mapping from the old column names to new names
        Usage:
            df.rename({'old_col_name': 'new_col_name', 'old_col_name2': 'new_col_name2'})
            df.rename(old_col_name=new_col_name)
    '''
    for before, after in mapper.items():
        df = df.withColumnRenamed(before, after)

    return df

def preprocess_cdrs_using_spark(file_or_folder=None, number_of_users_to_sample=None,
                                output_csv=None, date_format='%Y%m%d%H%M%S',
                                debug_mode=True, loc_file=None, save_to_csv=False,
                                userid_col="user_id"):
    """
    In this function, we perfom some basic preprocessing such as below:
    1. rename columns
    2. change some data types
    3. Add location details
    Eventually, we will sample the data to use for our analysis
    :param data_folder:
    :param output_csv_for_sample_users:
    :return:
    """

    # ==============================
    # LOAD DATA
    # ==============================
    # create SparkSession
    spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Assignement Of Louis") \
    .getOrCreate() 
    # read data with spark and ensure you set header to True
    df = spark.read.csv(file_or_folder ,header=True)
    # repartition to speed up
    df = df.repartition(10)

    # if just testing/debugging, pick only a small subset of the dataset
    # for instance, 0.01 percent of the data
    # by using the sample function of spark
    if debug_mode:
        dfs = df.sample(fraction = 0.1) 
        df = dfs

    # ==================================================
    # RENAME, DROP COLUMNS, ADD DATETIME AND DROP NULLS
    # ===================================================
    # rename columns to remove space the names
    # replace space with underscore
    cols_to_rename = {}
    for c in df.columns:
        if " " in c:
            cols_to_rename[c] = c.replace(" ", "_")

    #  now call the rename_sdf function
    # using df and the dictionary above
    df = rename_sdf(df, mapper=cols_to_rename)

    # this approach is also okay but you are hardcoding the column names
    # so, lets avoid hardcoding at all times
    #     df = (df.withColumnRenamed("cdr datetime", "cdrDatetime")
    #         .withColumnRenamed("last calling cellid", "cellId")
    #         .withColumnRenamed("call duration", "cellDuration"))

    # change the column "last_calling_cellid" to just cell_id
    df = df.withColumnRenamed("last_calling_cellid","cell_id") 
    # drop the cdr_type and call_duration because we dont really need them
    df = df.drop("cdr type","call_duration") 
    # lets make sure we don't have any values in the user_id
    # and cdr_datetime columns
    # use spark filter() function and isNotNull() in a nested
    # fashion to achieve this
    df = df.filter(df['user_id'].isNotNull()) 
    df = df.filter(df.cdr_datetime.isNotNull())

    # Use Spark UDF to add date and datetime
    add_datetime = udf(lambda x: datetime.strptime(x, date_format), TimestampType())
    add_date = udf(lambda x: datetime.strptime(x, date_format), DateType())


    # create timestamp and date column
    df = df.withColumn('datetime', add_datetime(col('cdr_datetime')))
    df = df.withColumn('date', add_date(col('cdr_datetime'))) 

    # ==================================================
    # ADD LOCATION THROUGH JOIN
    # ===================================================
    # Lets merge with location details using cellId from CDRs and also
    # cellID on the other
    # read pandas dataframe of location details
    dfLoc = pd.read_csv(loc_file)
    # remove duplicates from the cell_id column to make sure we only
    # unique cell_ids.Use the drop_duplicates() in pandas
    dfLoc = dfLoc.drop_duplicates(subset='cell_id')
    # create spark dataframe from the pandas dataframe
    # using the function createDataFrame from the SparkSession object
    # and the pandas DataFrame created above
    sdfLoc = spark.createDataFrame(dfLoc)

    # join the cdrs dataframe with the location dataframe
    # When using the join function, make sure you choose the option which allows
    # to keep all records on the cdrs side which match with records on the right.
    # please use "inner"
    # best option here. Check the docs for details:
    # https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrame
    df = df.join(sdfLoc,on='cell_id',how = "inner")

    # Drop all records which didn't find a match in the location file because we cant do this analysis
    # without location. There are several ways to do this. For instance, you can drop all rows where
    # use spark filter and condition set to cell_id isNotNull()
    df = df.filter(df.cell_id.isNotNull()) 
    # ==================================================
    # SAMPLE USERS
    # ===================================================
    # first, create a list of unique user user_ids
    # using the distinct() function on the userid_col
    all_users =  df.select(userid_col).distinct().collect() 

    # randomly select the required number of users
    # using the random.choices() function
    random_userid_list = [i[userid_col] for i in random.choices(all_users, k=number_of_users_to_sample)]

    # Now, for each of the selected users, leets get their data
    # select only our random user data using spark filter
    # use df.filter(). Inside it, use the isin() function on the
    # userid column
    dfu = df.filter(df['user_id'].isin(random_userid_list))

    # save to CSV if necessary
    if save_to_csv:
        dfu.coalesce(1).write.csv(path=output_csv, header=True)
    else:
        return dfu



def explore_data_with_spark(df=None, output_plot_file=None, output_heatmap=None):
    """
    Lets do a quick exploration of the data by generating the following:
    1. Number of days in the data
    2. User call count stats
    3. Weekday and hour calling patterns
    """
    # =====================================
    # CALCULATE THE NUMBER OF DAYS IN DATA
    # =====================================

    # use relevant spark function to generate
    # a list of unique dates, recall that the date
    # column is 'date
    dates_rows = df.select('date').distinct().collect() 
    # sort the dates using sorted() function
    sorted_dates = sorted(dates_rows)  
    # use list indexing to get the first element and last
    # element from the sorted list, substract them to get
    # time difference
    diff = sorted_dates[-1]['date']-sorted_dates[0]['date']
    # use days function to get the number of days
    num_days = diff.days
    # =====================================
    # GENERATE WEEKDAY AND HOUR CALL COUNT
    # =====================================

    # define UDF to calculate hour and weekday
    # for weekday use weekday() function while
    # for hour, use hour()
    add_hr = udf(lambda x :x.hour)              # Define Spark udf to get hour from the datetime column
    add_wkday = udf(lambda x: x.weekday())         # Define Spark udf to get hour from the datetime column
    # create a dictionary with keys as the weekday integers while the values
    # are the weekday name
    day_dict = {'1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday','7':'Sunday'}

    # add hour column, lets call it 'hr
    # also add weekday column, we call it 'wkday'
    df = df.withColumn('hr',add_hr(col('datetime')))

    df = df.withColumn('wkday',add_wkday(col('date')))

    # create pandas DataFrame from Spark DataFrame above using toPandas()
    pdf =  df.groupBy('wkday','hr').count().toPandas()
    # use the Pandas.Series.map() function on the "wkday" column to convert
    # wkday as numbers to week day names and create  new column for weekday name
    # Lets call that column 'weekDay'
    pdf['weekDay']=pdf['wkday'].map(lambda x: day_dict[x])
    # drop the "wkday" column now
    pdf = pdf.drop("wkday", axis = 1)
    pdf = pdf.pivot(index='weekDay', columns='hr', values='count')

    # create and save heatmap
    # use plt.figure() to create figure with your chosen size
    plt.figure(figsize = (7,7))
    # use sns.heatmap() function to create heatmap using the Pandas DataFrame, pdf
    sns.heatmap(pdf)
    # save the figure to file
    plt.savefig(output_heatmap)

    # =====================================
    # NUMBER OF CALLS FOR EACH USER
    # =====================================
    # Use Spark groupBy function to group user and count number of events
    # convert resulting spark dataframe to pandas in the samee line of code
    df_grp_user =  df.groupby('user_id').count().toPandas()

    # create a distribution plot of user call count using
    # seaborn distplot() function and save the figure
    # first, use plt.figure() to create new figure environment
    # Next, create the plot and then finally save it
    plt.figure(figsize= (5,5))
    sns.distplot(df_grp_user)                                                        # A refaire
    plt.savefig(output_plot_file)

    # report average number calls per day for each user
    # first use spark groupBy on user_id and day, then
    # convert that object to pandas dataframe using toPandas()
    # function
    df_grp_day = df.groupby('user_id','date').count().toPandas()

    # get mean and median
    mean =  df_grp_day['count'].mean()
    median = df_grp_day['count'].median()

    # return results like this mean, median, number of days
    return mean, median, df_grp_day['date'].nunique()

if __name__ == '__main__':
    # ============================================
    # QUESTION 1: USING MAP FUNCTION
    # ============================================
    time_format = "%Y%m%d"
    reference_date = '20180713'
    num_csv_files = 20
    #  add full path to the CSV folder and the function Path() to convert to
    # a path object
    path_to_csv = Path('/home/user/Desktop/big data analytic/simulated_cdr')
    get_events_before_jul13(path_to_csv , reference_date, time_format,num_csv_files)

    # ============================================
    # QUESTION 2: PREPROCESS SIMULATED CDRS
    # ============================================
    cdrs_dir ='/home/user/Desktop/big data analytic/simulated_cdr'                              #ADD PATH TO FOLDER WITH MULTIPLE CSV FILE
    # please start  with a few number of users, e.g., 1000
    number_of_users_to_sample =  1000
    # Full path to CSV to write outputs
    output_csv = "/home/user/Desktop/output_csv"
    # Download the file called simulated_locs.csv
    # and add its full path below
    loc_file = "/home/user/Desktop/big data analytic/simulated_locs.csv"
    # finall call the function preprocess_cdrs_using_spark and with other options left
    # as default
    dfu =  preprocess_cdrs_using_spark(file_or_folder=cdrs_dir, number_of_users_to_sample=number_of_users_to_sample,
                                output_csv=output_csv, date_format='%Y%m%d%H%M%S',
                                debug_mode=True, loc_file=loc_file, save_to_csv=False,
                                userid_col="user_id")

    # ============================================
    # QUESTION 3: EXPLORE USER ACTIVITY PATTERNS
    # ============================================
    # 1. use the df you save from above as input here
    # 2. create a full path to save a plot with "png" extension
    # 3. create a full path to save the heatmap plot
    # Run the function explore_data_with_spark below
    results = explore_data_with_spark(df=dfu, output_plot_file='/home/user/Desktop/big_data_analytic.png', output_heatmap='/home/user/Desktop/big.png')
