import datetime
import re
import math

from django.utils.html import strip_tags


def count_words(html_string):
	word_string = strip_tags(html_string)
	words = re.findall(r'\w+', word_string)
	count = len(words)
	return count


def get_read_time(html_string):
	count = count_words(html_string)
	read_time = math.ceil(count/200.0)
	return int(read_time)