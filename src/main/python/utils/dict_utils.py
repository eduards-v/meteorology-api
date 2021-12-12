def nest_flat_dict(original, sub_dict_name, *args):
    """ Utility function to create the nested dict from the flat dict
    Functional will create and return a copy of the original dict to avoid unwanted data mutations.
    :param original: flat dictionary as a base
    :param sub_dict_name: key name for the sub dict
    :param args: key names from the flat dict to be added to the sub dict
    :return: dict
    """
    assert isinstance(original, dict), "original parameter must be an instance of dict"
    assert set(args).issubset(original.keys()), "original dict keys must contain args key names"

    mutated_dict = original.copy()
    sub_dict = {}
    for arg in args:
        sub_dict[arg] = mutated_dict.pop(arg)
    mutated_dict[sub_dict_name] = sub_dict
    return mutated_dict


if __name__ == '__main__':
    org = {'sens_id': 1, 'city_name': 'Galway', 'country_name': 'Ireland'}
    mdict = nest_flat_dict(org, "metadata", "country_name", "city_name")
    print(org)
    print(mdict)
