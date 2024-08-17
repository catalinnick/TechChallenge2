# TechChallenge2
I decided to use Python for this problem. The py file can be executed and will ask for the number of input files to process.
It will output each processed csv files as "output_**STOCKID**.csv". Attach the set of folders with the csv files and modify
the **directory_path**(by default is **stock_price_data_files**) variable with the absolute/relative path of the input folder.
Each file is run through the two functions, the first function (using the **filename** variable as a parameter) picks a random 
index(between 1 and the size of dataframe minus 10, in order to assure the 10 consecutive data points) and extract 10 rows 
starting from the randomn index, then it's transformed in a csv file. Using the global **output_filename** the second function
picks on and predicts the 3 next data points; for the sake of simplicty, I used the prediction logic present in the challenge 
file. The predicted dataframe is a converted dictionary of 3 list: the variable **stock_name** repeated 3 times, a list of datetime
for 4 consecutive days starting from the last day (the first elemenent is skipped) in the sampled file(**output_filename**), and the 
list of the calculated values. This dataframe is appended to the original dataframe and converted in a csv file. The input and the 
randomn sample is sanitized. Also error handling is installed through try and except blocks and exceptions For more details check 
the comments and docstring in the py file.
