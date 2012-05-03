import csv
import sys
    
from collections import defaultdict

def main(args):

    import argparse
    parser = argparse.ArgumentParser(description='repeat the task of filling out known campaign tags from last month')
    parser.add_argument('primer', type=argparse.FileType('rb'),
        help="csv file containing last month's data to train the repeater")
    parser.add_argument('input', type=argparse.FileType('rb'),
        help="guess values for this file")
    parser.add_argument('--output', type=argparse.FileType('wb'),
        help="output the results to this file")
    opts = parser.parse_args(args)

    # TODO: open a file to write to
    if not opts.output:
        output = sys.stdout

    # TODO: Convert the csv file names into tables

    primer = csv.reader(opts.primer)
    table = csv.reader(opts.input)
    # Campaign type depends on campaign tag
    repeat(primer, table, { 0 : 1 })

def repeat(primer, table, dependencies, ignore_header=True):
    """
    Build a knowledge map from the previous table and use that to fill in any
    empty values in the given table.

    Preconditions:
        - Both tables have the same schema
        - There are no duplicate values for a given column to map

    """
    import pdb
    pdb.set_trace()
    knowledge_map = learn(primer, dependencies)
    # TODO: Go through the tables and map the known values from the knowledge map
    # Sorry I made dependencies a level more abstract than you wanted.
    # Just use knowledge_map['campaign type'][campaigntype] to get the learned value
    # for that campaign type... beitch
        

def learn(primer, dependencies):
    """Constructs a knowledge map from a given table.

    The keys of the map are the column names (or indexes) and
    the values of the map are dicts that map a value of the column
    to the learned value of independent value column.

    """
    knowledge_map = defaultdict(dict)
    for row in primer:
        for dv, iv in dependencies.items():
            # knowledge of the dependent value is mapped to the value
            # of the independent value col
            #
            # notice:
            # - if the knowledge_map has no entry for the dv col,
            #   a dict is constructed automatically
            # - the value of the iv col is used
            # - overwrites the previous known relationship
            knowledge_map[dv][row[iv]] = row[dv]
    return knowledge_map

if __name__ == '__main__':    
    main(sys.argv[1:])
