import pandas as pd
import random
import numpy as np
import datetime
import glob
import os

def random_get(filename):
    """Select 10 consecutive random data points and outputs them in a
    csv file.
    Args:
        filename (str): the name of the csv file that is going to be processed

    Raises:
        Exception: "The file {} is empty." 
        Exception: "There isn't enough data in the {}." - less than 10 data points
        Exception: "The file {} doesn't have a proper format." - there should be only 3 types of values

    Returns:
        boolean,str: If the sampled dataframe doesn't respect the format, the program is terminated
    """    
    # to be accesible by the second function
    global output_filename
    if os.path.getsize(filename) == 0:
        raise Exception("The file {} is empty.".format(filename))
    df=pd.read_csv(filename,header=None)
    # checks if it's possible to extract 10 data points
    if len(df) < 9:
        raise Exception("There isn't enough data in the {}.".format(filename))
    if len(df.columns) != 3:
        raise Exception("The file {} doesn't have a proper format.".format(filename))
    stock_id=df.iat[0,0]
    # in order to prevent an "out-of-bound" index and extract 10 data points
    random_index=random.randint(1,len(df)-10)
    random_df=df.iloc[random_index:random_index + 10]
    # in order to corelate the output with the input
    output_filename='output_'+stock_id + '.csv'
    # for a better optimization, data sanitization is done only for the randomn sample

    # it tries to convert the second column to type datetime, if it fails an error will be returned
    try:
        pd.to_datetime(random_df.iloc[:,1],dayfirst=True)
    except ValueError:
        return False,"The file {} doesn't have a proper format, check the timestamp column.".format(filename)
    if not pd.api.types.is_numeric_dtype(random_df.iloc[:,2]):
        return False,"The file {} doesn't have a proper format, check the stock value column.".format(filename)
    random_df.to_csv(output_filename,header=None,index=False)
    return True,"All is good."

def prediction():
    """Predicites the next 3 stock values for each file,
    for the sake of simplictiy it uses the prediction logic 
    presented in the challenge
    """    
    df=pd.read_csv(output_filename,header=None)
    # extract the first value, the stock id doesn't change throught the file
    stock_name=df.iat[0,0]
    # extract the last date and format to datetime type
    timestamp=df.iat[len(df)-1,1]
    timestamp=datetime.datetime.strptime(timestamp, "%d-%m-%Y")
    # extract the last column as a list
    stock_value=df[2].tolist()
    # using a second list in order to not alter the original list
    sorted_stock_value=[]
    sorted_stock_value=sorted(stock_value)
    # extracting the second highest value
    stock_value_predict1=sorted_stock_value[-2]
    # for a better prediction, the difference will be always positive
    stock_value_predict2=round(stock_value[-1] + abs(stock_value[-1] - stock_value_predict1)/2,2)
    stock_value_predict3=round(stock_value[-1] + abs(stock_value_predict2 - stock_value_predict1)/4,2)
    # creating a list from the variable stock name by repeating it 3 times
    stock_name_list=np.repeat(stock_name,3)
    # creating a list of 4 consecutive days starting with the timestamp value
    timestamp_list=pd.date_range(timestamp,periods=4)
    stock_value_list=[stock_value_predict1,stock_value_predict2,stock_value_predict3]
    # the first element from the timestamp list is ignored, because is already present in the file
    prediction_df=pd.DataFrame({0:stock_name_list,1:timestamp_list[1:].strftime("%d-%m-%Y"),2:stock_value_list})
    final_df= pd.concat([df, prediction_df], ignore_index=True)
    final_df.to_csv(output_filename,header=None,index=False)

# the program will process whatever csv files are present in the directory path
directory_path = 'stock_price_data_files'
num_csv_files = len(glob.glob(os.path.join(directory_path, '**', '*.csv'), recursive=True))
if num_csv_files == 0:
    raise Exception("There is no file(s) to process.")
while True:
    try:
        input_num=int(input('How many files are going to be sampled: '))
        if input_num <= 0 or input_num > 100:
            raise Exception("Invalid input, try a number between 1 and 100.")
        # an exception is raised, because it doesn't know which of the file to process,
        # if presented with a lower input number than files, altough a higher input number won't matter
        if input_num<num_csv_files:
            raise Exception("The number of csv files in this path exceeds the input. The number of csv files is {}.".format(num_csv_files))
        break
    except ValueError:
        print("Invalid input, try a number between 1 and 100.")
# for each file the two function will be executed, if the first function returns an error
# the program will terminated and an exception will be raised
for filename in glob.glob(os.path.join(directory_path, '**', '*.csv'), recursive=True):
    proper_format,error_message=random_get(filename)
    if not proper_format:
        raise Exception(error_message)
    prediction()
    print("The file {} is processed!".format(filename))