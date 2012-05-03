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
    # In case output is not given, use stdout
    output = sys.stdout if not "output" in vars(opts) else opts.output
    repeat_files(opts.primer, opts.input, output)


def repeat_files(primer, input, out):
    # TODO: Make this match the csv output from OpenOffice
    primer_reader = csv.reader(primer)
    input_reader = csv.reader(input)
    # Campaign type (column #0) depends on campaign tag (column #1)
    completed = repeat_tables(primer_reader, input_reader, { 0 : 1 })
    output_writer = csv.writer(out, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    for row in completed:
        output_writer.writerow(row)


def repeat_tables(primer, table, dependencies, ignore_header=True):
    """
    Build a knowledge map from the previous table and use that to fill in any
    empty values in the given table.

    Preconditions:
        - Both tables have the same schema
        - There are no duplicate values for a given column to map

    """
    knowledge_map = learn(primer, dependencies)
    completed = []
    for row in table:
        # copy everything over
        completed_row = row
        for dvcol, ivcol in dependencies.items():
            iv = row[ivcol]
            # if the value is empty and we know what to put
            if row[dvcol] == "" and iv in knowledge_map[dvcol]:
                # fill in what we learned
                completed_row[dvcol] = knowledge_map[dvcol][iv]
        completed.append(completed_row)
    return completed

def learn(primer, dependencies):
    """Constructs a knowledge map from a given table.

    The keys of the map are the column names (or indexes) and
    the values of the map are dicts that map a value of the column
    to the learned value of independent value column.

    """
    knowledge_map = defaultdict(dict)
    for row in primer:
        for dvcol, ivcol in dependencies.items():
            # knowledge of the dependent value is mapped to the value
            # of the independent value col
            #
            # notice:
            # - if the knowledge_map has no entry for the dv col,
            #   a dict is constructed automatically
            # - the value of the iv col is used
            # - overwrites the previous known relationship
            knowledge_map[dvcol][row[ivcol]] = row[dvcol]
    return knowledge_map

if __name__ == '__main__':    
    main(sys.argv[1:])
