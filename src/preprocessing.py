

import pandas as pd
import matplotlib.pyplot as plt

class Preprocessing:
    """ Includes functions to clean/preprocess data """

    @staticmethod
    def preprocess_raw_data(raw_data_path):
        """ Preprocess/clean input data  """

        # Load data from csv to dataframes
        df_raw_data = pd.read_csv(raw_data_path)

        # Drop null data from raw-data (last column that has NaN, and rows with PlaybrushID NaN)
        df_raw_data = Preprocessing.drop_null_data(df_raw_data)

        # Transform data types of input dataframes into correct types
        df_raw_data = Preprocessing.transform_data_types(df_raw_data)

        # Append total brushing time length to the data
        df_raw_data = Preprocessing.append_total_length(df_raw_data)

        # Merge brush sessions less than 2 min apart
        df_grouped_data = Preprocessing.create_merged_data(df_raw_data)

        # Append is morning time to the data
        df_grouped_data = Preprocessing.append_is_morning(df_grouped_data)

        # Discard tiny brush sessions (less than 20 seconds)
        df_grouped_data = Preprocessing.discard_tiny_sessions(df_grouped_data)

        # Get only the longest sessions for morning and evening per user
        df_grouped_data = Preprocessing.get_longest_morning_evening_sessions(df_grouped_data)

        return df_grouped_data

    @staticmethod
    def create_output_task_1(sessions_data, group_data_path, output_data_path):
        """ Create output of task 1: users sessions summarized data  """

        # Set day name in brush sessions
        sessions_data["Day"] = sessions_data["TimestampUTC"].apply(Preprocessing.get_day_name)

        # Rename PlaybrushID as PBID
        sessions_data = sessions_data.rename(columns={"PlaybrushID": "PBID"})

        # Count valid sessions none = 0, morning or evening = 1, morning and evening = 2
        sessions_data_groupby_day = sessions_data.groupby(['PBID', 'Day']).size().reset_index(name='Counts')

        # Read user group data
        output = pd.read_csv(group_data_path)

        # Set how many times the user brushed in the morning, and in the evening for each day of the week. 0 for no
        # brush, 1 for morning or evening brush, and 2 for morning and evening brush.
        output = Preprocessing.merge_day_sessions_count('mon', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('tue', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('wed', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('thu', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('fri', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('sat', sessions_data_groupby_day, output)
        output = Preprocessing.merge_day_sessions_count('sun', sessions_data_groupby_day, output)

        # Set total-brushes
        output['total-brushes'] = output["mon"]+output["tue"]+output["wed"]+output["thu"]+output["fri"]+output["sat"]+output["sun"]

        # Set twice brushes
        output['twice-brushes'] = (output[['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']] == 2).sum(axis=1)

        # Get user average brushing times
        users_avg_sessions_time = sessions_data.groupby(['PBID'])['TotalLength'].mean().reset_index()
        users_avg_sessions_time = users_avg_sessions_time.rename(columns={'TotalLength': 'avg-brush-time'})
        output = output.merge(users_avg_sessions_time, how='left', on='PBID')
        output['avg-brush-time'] = output['avg-brush-time'].fillna(0)

        # Save task1 output to csv
        output.to_csv(output_data_path)

        return output

    @staticmethod
    def create_output_task_2(user_summarized_data, output_data_dir):
        """ Create output of task 2: user groups summarized data  """

        # Compute:
        #   1) how many valid brush sessions were observed in total for each group "users-total-brushes"
        #   2) how many valid brush sessions were observed by a user on average for each group "users-avg-brushes"
        #   3) what is the average brush time of a user in each group "users-avg-brush-time"

        user_summarized_data["total-brushes-copy"] = user_summarized_data["total-brushes"]

        group_summarized_data = user_summarized_data.groupby(['group'], as_index=False)[['total-brushes', 'total-brushes-copy', 'avg-brush-time']]\
            .agg({"total-brushes": "sum", "total-brushes-copy": "mean", "avg-brush-time": "mean"})
        group_summarized_data = group_summarized_data.rename(columns={"total-brushes": "users-total-brushes",
                                                                      "total-brushes-copy": "users-avg-brushes",
                                                                      "avg-brush-time": "users-avg-brush-time"})

        group_summarized_data = group_summarized_data.sort_values(by=["users-total-brushes"], ascending=False)

        # Save group data output to csv
        group_summarized_data.to_csv(output_data_dir+'groups_data_results.csv')

        # Print group data
        print(group_summarized_data)

        # Plot group data
        lines = group_summarized_data.plot.bar()
        lines.set_xticklabels(group_summarized_data.group, rotation=0)
        lines.set_xlabel("Groups")
        lines.set_ylabel("Performance")
        plt.title("User Groups Performance")

        # Save group data plot
        plt.savefig(output_data_dir+'groups_performance.png')
        plt.show()

        return group_summarized_data

    @staticmethod
    def merge_day_sessions_count(day_name, df_grouped_data, output):
        """ Merge to the output user data the brushing sessions count for the particular day name found in df_grouped_data """

        filter_monday_counts = df_grouped_data.Day == day_name
        monday_counts = df_grouped_data.loc[filter_monday_counts, ['PBID', 'Counts']]

        output = output.merge(monday_counts, how='left', on='PBID')
        output = output.rename(columns={"Counts": day_name})
        output[day_name] = output[day_name].fillna(0)

        return output


    @staticmethod
    def get_day_name(date_time):
        """ Returns day name from date time """

        return date_time.strftime("%a").lower()

    @staticmethod
    def drop_null_data(df_raw_data):
        """ Drops null data from raw-data (last column that has NaN, and rows with PlaybrushID NaN) """

        # Drop last column of raw-data that has NaN
        df_raw_data = df_raw_data.iloc[:, :-1]

        # Drop rows of raw-data with PlaybrushID null
        rows_filter_null_playbrush_id = df_raw_data["PlaybrushID"].notnull()
        df_raw_data = df_raw_data[rows_filter_null_playbrush_id]

        return df_raw_data

    @staticmethod
    def transform_data_types(df_raw_data):
        """ Transforms data types of input dataframes into correct types """

        df_raw_data.TimestampUTC = pd.to_datetime(df_raw_data.TimestampUTC, format="%a %b %d %Y %H:%M:%S GMT%z (BST)")

        return df_raw_data

    @staticmethod
    def is_morning_time(date_time):
        """ Returns if the date time provided is in the morning (before 2:00 pm) """

        return date_time.hour < 14

    @staticmethod
    def append_total_length(df_raw_data):
        """ Appends total length to the data as sum of up, down, left, right and none times """

        df_raw_data["TotalLength"] = df_raw_data["UpTime"] + df_raw_data["DownTime"] + df_raw_data["LeftTime"] + \
                                     df_raw_data["RightTime"] + df_raw_data["NoneTime"]

        return df_raw_data

    @staticmethod
    def append_is_morning(df_raw_data):
        """ Appends if it is morning time """

        df_raw_data["IsMorning"] = df_raw_data.TimestampUTC.apply(Preprocessing.is_morning_time)

        return df_raw_data

    @staticmethod
    def create_merged_data(df_raw_data):
        """ Merge brush sessions less than 2 min apart """

        df_grouped_data = df_raw_data.groupby(['PlaybrushID', pd.Grouper(key='TimestampUTC', axis=0, freq='2 min')]).sum().reset_index()
        return df_grouped_data


    @staticmethod
    def discard_tiny_sessions(df_grouped_data):
        """ Discard tiny brush sessions (less than 20 seconds) """

        rows_filter = df_grouped_data["TotalLength"] > 20
        df_grouped_data = df_grouped_data[rows_filter]

        return df_grouped_data


    @staticmethod
    def get_longest_morning_evening_sessions(df_grouped_data):
        """ Get only the longest sessions for morning and evening per user """

        df_grouped_data["Date"] = df_grouped_data["TimestampUTC"].dt.date
        filter = df_grouped_data.groupby(['PlaybrushID', 'Date', 'IsMorning'])['TotalLength'].idxmax()
        df_grouped_data = df_grouped_data.loc[filter]
        df_grouped_data.drop('Date', axis=1, inplace=True)

        return df_grouped_data


