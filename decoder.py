#! /usr/bin/python
import sys
import base64

coded_string = sys.argv[1]
decoded_string = base64.urlsafe_b64decode(coded_string)
print decoded_string