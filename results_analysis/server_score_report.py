import datetime
import glob
from time import strftime
import pandas as pd
import csv
import os

base_dir = "/home/nsedex/score_report/"
input_dir = "raw/"
output_dir = "/home/data/result_analysis/Transformed/"
exception_column_list = [
    "file_name",
    "row_number",
    "testdate",
    "testtime",
    "examid",
    "candidatename",
    "registrationnumber",
    "eed_id",
    "testcenter",
    "language",
    "module",
    "status",
    "qtp_eed_id",
    "totalquestion",
    "attemptedquestions",
    "nonattemptedquestions",
    "deletedquestions",
    "correctanswers",
    "wronganswers",
    "totalnewscore",
    "error"

]
master_column_list = ["filename"]


def process_file(file_name):
    read_files = []
    exception_rows = []
    output_rows = []
    extension = file_name.split("/")[-1].split(".")[-1]
    client_id = file_name.split("/")[-1].split("_")[0].lower()
    if not os.path.isfile(output_dir + client_id + "_score_report.csv"):
        if extension == "xlsx":
            dataframe = pd.read_excel(file_name)
        elif extension == "csv":
            if "Master" not in file_name and "Exception" not in file_name:
                dataframe = pd.read_csv(file_name,low_memory=False).reset_index(drop=True)
            else:
                return
        else:
            print("invalid file")
            return
        input_csv_data = [dataframe.columns.tolist()]
        values = dataframe.values.tolist()
        input_csv_data.extend(values)
        for index, item in enumerate(input_csv_data):
        
            if "nan" in str(item):
                file_name_list = [file_name, index + 1]
                file_name_list.extend(item)
                file_name_list.append("NaN value found")
                exception_rows.append(file_name_list)
                
            else:
                if index == 0:
                    # item[12] = "crr_qst_no"
                    item.insert(0, "clientid")
                    output_rows.append(item)
                    continue
                output_row = [client_id]
                output_row.extend(item)
                output_rows.append(output_row)
                

            
        read_files.append([file_name])
        with open(output_dir + client_id + "_score_report.csv", "w", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerows(output_rows)
        if os.path.isfile(base_dir + input_dir + "Master.csv"):
            with open(base_dir + input_dir + "Master.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(read_files)
        else:
            with open(base_dir + input_dir + "Master.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(master_column_list)
                writer.writerows(read_files)
        if os.path.isfile(base_dir + input_dir + "Exception.csv"):
            with open(base_dir + input_dir + "Exception.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(exception_rows)
        else:
            with open(base_dir + input_dir + "Exception.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(exception_column_list)
                writer.writerows(exception_rows)


def main():
    list_of_files = glob.glob(base_dir + input_dir + "*")
    for file in list_of_files:
        process_file(file)


start_time = datetime.datetime.now()
main()
print("time taken: " + str(datetime.datetime.now() - start_time))
