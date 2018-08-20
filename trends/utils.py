import pandas


def extract_relevant_rows(df, sense_repository, the_competitions):
    """

    :param pandas.DataFrame df: dataframe with wsd state of the art data
    :param str sense_repository: WordNet | BabelNet
    :param set the_competitions: set of allowed competitions

    :rtype: tuple
    :return: (set of systems, df with relevant info)
    """
    rows = []
    headers = df.columns


    for index, row in df.iterrows():

        if all([row['competition'] in the_competitions,
                row['sense_repository'] == sense_repository]):

            rows.append(row)

    comp_df = pandas.DataFrame(rows, columns=headers)
    systems = set(comp_df.label)

    return (systems, comp_df)


def load_relevant_data_from_rows(comp_df, competition):
    """
    extract from system with best performing setting:
    a) year
    b) name of system
    c) f1

    :param pandas.DataFrame comp_df: output 'extract_relevant_rows' function

    :rtype: pandas.DataFrame
    :return: df with relevant data
    """
    list_of_lists = []
    headers = ['Year', 'F1', 'System', 'Competition']

    for system in set(comp_df.label):
        system_df = comp_df[comp_df.label == system]

        highest_row = system_df['F1'].argmax()

        rows = system_df.loc[[highest_row]]
        assert len(rows) == 1
        for index, row in rows.iterrows():
            pass

        shortname = row['label']
        setting = row['setting']
        f1 = row['F1'] / 100
        year = row['year']

        #if type(setting) == str:
        #    label = f'{shortname} ({setting})'
        #else:
        #    label = f'{shortname}'
        label = f'{shortname}'

        one_row = [int(year), float(f1), str(label), competition]
        list_of_lists.append(one_row)


    stats_df = pandas.DataFrame(list_of_lists, columns=headers)

    return stats_df