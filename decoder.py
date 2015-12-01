#! /usr/bin/python
import sys
import base64
__author__ = 'Shane Rogers'


def decode_string(phrase):
	return base64.urlsafe_b64decode(phrase)
