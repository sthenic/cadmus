# Description:
#   This module implements formatting functions for reStructuredText elements

# RST table header divider
def table_hdivider(col_sizes):
    retstr = ''
    for size in col_sizes:
        retstr += '+' + '='*size
    retstr += '+\n'
    return retstr

# RST table divider
def table_divider(col_sizes):
    retstr = ''
    for size in col_sizes:
        retstr += '+' + '-'*size
    retstr += '+\n'
    return retstr

# RST table row
def table_row(row, col_sizes):
    retstr = ''
    for i in range(len(row)):
        retstr += '| ' + row[i] + ' '*(col_sizes[i] - len(row[i]) - 1)
    retstr += '|\n'
    return retstr

# Returns a formatted RST table given a valid table dict
def format_table(table_dict):
    if 'header' in table_dict:
        header = table_dict['header']
    else:
        raise ValueError('Missing header field in table dictionary.')

    if 'body' in table_dict:
        body = table_dict['body']
    else:
        raise ValueError('Missing body field in table dictionary.')

    # TODO: Validate structure

    # Determine column sizes
    col_sizes = []
    for h in header:
        col_sizes.append(len(h))
    for row in body:
        for i in range(len(row)):
            col_sizes[i] = max(col_sizes[i], len(row[i]))

    # Add two surrounding spaces
    col_sizes = [s + 2 for s in col_sizes]

    # Format table
    table_str = table_divider(col_sizes)
    # Insert headers
    table_str += table_row(header, col_sizes)
    table_str += table_hdivider(col_sizes)
    # Insert body
    for row in body:
        table_str += table_row(row, col_sizes)
        table_str += table_divider(col_sizes)

    return table_str
