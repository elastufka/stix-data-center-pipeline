#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @title        : stix_xml_to_bin.py
# @description  : read hex string from clipboard and write it to a binary file
# @date         : March. 28, 2019
import sys
import binascii
import Tkinter as tk
import re
from tools import parser
LOGGER = stix_logger.LOGGER
def parser_clipboard_data():
    root = tk.Tk()
    root.withdraw()
    raw_hex=root.clipboard_get()
    data_hex= re.sub(r"\s+", "", raw_hex)
    print('header:%s'%data_hex[:10])
    data_binary = binascii.unhexlify(data_hex)
    in_file=StringIO(data_binary)
    status, header, parameters, param_type, num_bytes_read = parser.parse_one_packet(
        in_file, LOGGER)
    LOGGER.pprint(header,parameters)
if __name__ == '__main__':
    parser_clipboard_data()
