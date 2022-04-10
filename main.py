from src.preprocessing import Preprocessing


def main():

    # ----------------------- General Rules Preprocessing ----------------------------
    # Preprocess data:
    #   1. merging close brush sessions,
    #   2. discard very small sessions,
    #   3. discard double sessions in morning or evening
    p = Preprocessing()
    #raw_data_path = "./input_data/1_rawdata.csv"
    #group_data_path = "./input_data/2_groups.csv"
    #output_data_path = "./output_data/output.csv"
    raw_data_path = "../input_data/1_rawdata.csv"
    group_data_path = "../input_data/2_groups.csv"
    output_data_path = "../output_data/user_data_results.csv"
    output_data_dir = "../output_data/"

    user_sessions_data = p.preprocess_raw_data(raw_data_path)

    # ----------------------- Task 1. ----------------------------
    user_summarized_data = p.create_output_task_1(user_sessions_data, group_data_path, output_data_path)

    # ----------------------- Task 2. ----------------------------
    group_summarized_data = p.create_output_task_2(user_summarized_data, output_data_dir)



if __name__ == "__main__":
    main()