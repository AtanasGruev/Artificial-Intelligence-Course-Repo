import numpy as np
import pandas as pd
import pprint

def data_preprocessing(df):
    """ Remove or predict missing values in the data set. """

    # Remove 1 instance from the data set with missing attribute #9.
    df = df.drop(df.loc[df["breast-quad"] == '?'].index)

    # Guess values for 9 instances with missing attribute #6
    prob_yes = (df["node-caps"] == "yes").sum(axis=0) / df.shape[0]
    prob_no = 1 - prob_yes

    list_node_caps = df["node-caps"].tolist()
    replace_missing = np.random.choice(["yes", "no"],
                                       size=df.loc[df["node-caps"] == '?'].shape[0],
                                       p=[prob_yes, prob_no])

    j = 0
    for i in range(len(list_node_caps)):
        if list_node_caps[i] == '?':
            list_node_caps[i] = replace_missing[j]
            j += 1

    df["node-caps"] = list_node_caps
    return df


def numeric_entropy(list_values):
    """ Compute entropy given two probabilities """
    num_entropy = 0
    for value in list_values:
        if value == 0:
            return 0
        num_entropy -= value * np.log2(value)
    return num_entropy


def entropy(feature_df, feature):
    """ Compute entropy of attribute with respect to a given category.
        Suitable for more than two classes, too. """

    total_size = feature_df.shape[0]
    entropy = 0

    # IDEA
    # 1) Select unique values for classes and features
    # 2) Traverse features for values and build dictionaries for each of the classes
    # 3) These dictionaries are stored in a list
    # 4) The list is iterated and all useful information is extracted to compute entropy

    list_values = feature_df[feature].unique()
    list_categories = []

    for category in feature_df["class"].unique():
        category_dict = {}
        for value in list_values:
            category_dict[value] = 0
        for value in feature_df.loc[feature_df["class"] == category][feature]:
            category_dict[value] += 1
        list_categories.append(category_dict)

    for value in list_values:
        value_prob = 0
        list_entropy = []
        for cnt in range(len(list_categories)):
            value_prob += list_categories[cnt][value]
            list_entropy.append(list_categories[cnt][value] / (feature_df[feature] == value).sum(axis=0))
        value_prob = value_prob / total_size
        entropy += value_prob * numeric_entropy(list_entropy)

    return entropy


def build_decision_tree(df_current, df_original, limit=4, parent_node_class=None):
    """ ID3 algorithm for decision tree. """

    # Stop conditions - recursion base
    # 1) All instances have the same class --
    #    -- return that class
    if len(df_current["class"].unique()) == 1:
        return df_current["class"].values[0]

    # 2) The dataset passed has less than K instances --
    #    -- return most common class in original dataset
    if df_current.shape[0] < limit:
        if limit == 1:
            return df_original["class"].value_counts.idxmax()
        return parent_node_class

    # 3) All features have been expended --
    #    -- return to previous node and return most common class
    column_names = df_current.columns.tolist()[1:]
    if len(column_names) == 0:
        return parent_node_class

    total_size = df_current.shape[0]
    no_recurrence_df = df_current.loc[df_current["class"] == "no-recurrence-events"]
    recurrence_df = df_current.loc[df_current["class"] == "recurrence-events"]

    # Calculate entropy of target
    target_entropy = numeric_entropy([no_recurrence_df.shape[0] / total_size,
                                      recurrence_df.shape[0] / total_size])

    # For different attributes, calculate respective entropies
    feature_gain_dict = {}

    for feature in column_names:
        feature_gain_dict[feature] = target_entropy - \
            entropy(df_current[["class", feature]], feature)

    best_feature = max(feature_gain_dict.items(), key=lambda x: x[1])[0]

    # Get parent node class = best class according to the previous level of the tree
    parent_node_class = df_current["class"].value_counts().idxmax()

    tree = {best_feature: {}}
    for value in df_current[best_feature].unique():
        df_rec = df_current.loc[df_current[best_feature] == value]
        df_rec = df_rec.drop(best_feature, axis=1)
        subtree = build_decision_tree(df_rec, df_original, limit, parent_node_class)
        tree[best_feature][value] = subtree

    return tree


def test_query(query, tree, default="no-recurrence-events"):
    """ Once the decision tree has been built, it's time to test it. """
    for key in list(query.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]]
            except:
                return default

            result = tree[key][query[key]]
            if isinstance(result, dict):
                return test_query(query, result)
            return result


def main():
    """ Decision Tree Implementation (ID3) """
    list_names = ["class", "age", "menopause", "tumor-size", "inv-nodes",
                  "node-caps", "deg-malig", "breast", "breast-quad", "irradiat"]

    df = pd.read_csv("breast-cancer.data", names=list_names)
    limit = int(input("Please enter constant K: minimum number of instances required per tree level: ").strip())

    # NOTE - Data preprocessing required by breast-cancer.names
    df = data_preprocessing(df)

    accuracy = 0
    list_df = []
    df_remainder = df

    while len(list_df) < 10:
        if len(list_df) < 5:
            df_chunk = df_remainder.sample(n=28)
        else:
            df_chunk = df_remainder.sample(n=29)
        df_remainder = df_remainder.drop(df_chunk.index)
        list_df.append(df_chunk)

    for index, test in enumerate(list_df):
        test_dict = test.to_dict(orient="records")
        train_df = pd.concat(list_df[:index] + list_df[index+1:])
        tree = build_decision_tree(train_df, train_df, limit)
        # pprint.pprint(tree)

        train_dict = train_df.to_dict(orient="records")
        train_accuracy = 0
        for instance in train_dict:
            guess_class = instance["class"]
            if guess_class == test_query(instance, tree):
                train_accuracy += 1 

        test_accuracy = 0
        for instance in test_dict:
            guess_class = instance["class"]        
            if guess_class == test_query(instance, tree):
                test_accuracy += 1

        print('Accuracy on turn', index, "-->", test_accuracy / len(test_dict))
        accuracy += test_accuracy / len(test_dict)
    print("Total accuracy is: ", accuracy / 10)


if __name__ == "__main__":
    main()
