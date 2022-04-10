# Playbrush Data Analysis

## User and Group Data Analytics
This project analyzes offline brushing data of all participants in a toothbrushing study that are categorized into groups. 
The analysis provides data for each user and group. The input data are provided in the 1_raw_data.csv file and the user groups are provided in the 2_groups.csv file that 
are located in the input_data folder. Specifically the following data are analyzed.


<b>User Data:</b>
1. How many times the user brushed in the morning, and in the evening for each day of the week. 0 for no
   brush, 1 for morning or evening brush, and 2 for morning and evening brush. Multiple brushes in the
   same morning should only be counted once.
2. How many days in the week a user brushed twice a day. Again, twice a day represents morning and
   evening, and not just multiple brushes.
3. The total number of valid morning and evening brush sessions in the week.
4. The average time spent brushing per valid session in the week.

<b>Group Data:</b>
1. How many valid brush sessions were observed in total?
2. What is the average number of brushing sessions per user in that group?
3. What is the average brushing duration per user in that group?
4. Which group performed the best? Rank the groups in terms of performance.

## Setup

Create and activate a virtual environment for python.
From the virtual environment ".../playbrush-test/venv" run:

```
$ pip install -r ../requirements.txt
$ python ../main.py
```
This command with create an user_data_results.csv with the user data analytics results in the project folder and 
will also save the group data analytics results in the group_data_results.csv. The group data results of the second file
will also be plotted using bar plots and the image will be saved in the folder.

