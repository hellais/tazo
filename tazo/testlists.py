import os
import csv

def _iterate_csv(file_path, skip_header=False):
     with open(file_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next() # Skip the header line
        for row in reader:
            yield row

def load_category_codes(test_lists_path):
    category_codes = {}
    cat_codes_file = os.path.join(test_lists_path, 'lists',
                                  '00-proposed-category_codes.csv')
    for row in _iterate_csv(cat_codes_file, skip_header=True):
        short_description = row[0]
        new_code = row[1]
        _ = row[2] # Ignore old_code
        long_description = row[3]
        category_codes[new_code] = (unicode(short_description),
                                    unicode(long_description))
    return category_codes

def load_country_codes(test_lists_path):
    country_codes = {}
    country_codes_file = os.path.join(test_lists_path, 'lists',
                                      '00-LEGEND-country_codes.csv')
    for row in _iterate_csv(country_codes_file, skip_header=True):
        code, name = row
        country_codes[code] = unicode(name, encoding='utf-8')
    return country_codes

def csv_to_dict(file_name, filter_by={}):
    """
    :param file_name: the path to a csv file
    :param filter_by: a dictionary of keys to be filtering by

    :return:
    a list of JSON documents containing the test list items.
    """
    output = []
    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = reader.next()
        for row in reader:
            item = {}
            include = True
            for idx, key in enumerate(header):
                item[key] = unicode(row[idx], 'utf-8')
            for key, value in filter_by.items():
                if (value is not None and
                        item.get(key, None) != value):
                    include = False
                    break
            if include or not filter_by:
                output.append(item)
    return output
