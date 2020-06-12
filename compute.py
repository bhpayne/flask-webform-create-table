#!/usr/bin/env python3

import random
import logging

logger = logging.getLogger(__name__)


def create_output(table_dict: dict, num_rows: str, num_cols: str, list_of_opts: list, filename: str) -> None:
    """
    given a table, write sequence to file
    """
    trace_id = str(random.randint(1000000, 9999999))
    logger.info("[trace page start " + trace_id + "]")
    # eliminate nop values
    cleaned_table_dict = {}
    for k, v in table_dict.items():
        if v!='nop':
            cleaned_table_dict[k]=v

    logger.debug('after cleaning, table dict =' + str(cleaned_table_dict))

    # convert table as dict to columns
    list_of_keys = list(cleaned_table_dict.keys())

    str_to_write = ""
    for col_indx in range(int(num_cols)):
        list_of_col_ops = []
        for this_key in list_of_keys:
            if 'col'+str(col_indx) in this_key:
                list_of_col_ops.append((this_key, cleaned_table_dict[this_key]))
                str_to_write += this_key + ": " + cleaned_table_dict[this_key] + "\n"
#        logger.debug(str(col_indx) + ":" + str(list_of_col_ops))

    with open(filename,'w') as fil:
        fil.write('# my file\n')
        fil.write(str_to_write)

    logger.info("[trace page end " + trace_id + "]")
    return
