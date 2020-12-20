import numpy as np
import pandas as pd


def calculate_probabilities(df, size):
    """ Conditional probabilities are stored in dictionaries """
    df_dict = {}
    for col_name in df.columns[1:]:
        df_dict[col_name] = {'y': 0, 'n': 0, '?': 0}
        for item in df[col_name]:
            df_dict[col_name][item] += 1

    for col_name in df.columns[1:]:
        for item in df_dict[col_name]:
            df_dict[col_name][item] = (df_dict[col_name][item] + 1) / (size + 3)

    return df_dict


def train_naive_bayes(train_df):
    """ Training of Naive Bayes Classifier """
    size = train_df["party"].shape[0]

    prior_republican = (train_df["party"] == "republican").sum(axis=0) / size
    prior_democrat = (train_df["party"] == "democrat").sum(axis=0) / size
    prior = [prior_republican, prior_democrat]

    republican_df = train_df.loc[train_df["party"] == "republican"]
    democrat_df = train_df.loc[train_df["party"] == "democrat"]

    republican_size = republican_df.shape[0]
    democrat_size = democrat_df.shape[0]

    republican_dict = calculate_probabilities(republican_df, republican_size)
    democrat_dict = calculate_probabilities(democrat_df, democrat_size)

    vote_list = [republican_dict, democrat_dict]

    return prior, vote_list


def test_naive_bayes(test_data, prior, vote_list):
    """ Testing of Naive Bayes Classifier """
    max_score = 0
    answer = 0

    for index in range(len(prior)):
        score = np.log(prior[index])
        for i, col_name in enumerate(vote_list[index].keys()):
            score += np.log(vote_list[index][col_name][test_data[i]])
        if index == 0:
            max_score = score
        elif score > max_score:
            max_score = score
            answer = index
    return "republican" if answer == 0 else "democrat"

def main():
    names_columns = ["party", "handicapped-infants", "water-project-cost-sharing",
                     "adoption-of-the-budget-resolution", "physician-fee-freeze",
                     "el-salvador-aid", "religious-groups-in-schools", "anti-satellite-test-ban",
                     "aid-to-nicaraguan-contras", "mx-missile", "immigration",
                     "synfuels-corporation-cutback", "education-spending", "superfund-right-to-sue",
                     "crime", "duty-free-exports", "export-administration-act-south-africa"]

    df = pd.read_csv("house-votes-84.data", names=names_columns)

    accuracy = 0
    list_df = []
    df_remainder = df
    
    while len(list_df) < 10:
        if len(list_df) < 5:
            df_chunk = df_remainder.sample(n=44)
        else:
            df_chunk = df_remainder.sample(n=43)
        df_remainder = df_remainder.drop(df_chunk.index)
        list_df.append(df_chunk)

    for index, test in enumerate(list_df):
        test_df = test
        train_df = pd.concat(list_df[:index] + list_df[index+1:])
        prior, vote_list = train_naive_bayes(train_df)

        turn_accuracy = 0
        for row in range(test_df.shape[0]):
            if test_df.iloc[row]["party"] == test_naive_bayes(test_df.iloc[row].drop("party"), prior, vote_list):
                turn_accuracy += 1

        print('Accuracy on turn', index, "-->", turn_accuracy / test_df.shape[0])
        accuracy += turn_accuracy / test_df.shape[0]
    print("Total accuracy is: ", accuracy / 10)


if __name__ == "__main__":
    main()
