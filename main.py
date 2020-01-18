#! /usr/bin/env python3

import json
import argparse
import sys
import codecs
from datetime import datetime
from typing import Dict, List


def parse_timestamp(timestamp: str) -> str:
	# format as 19810329T020000
	# incoming as 2017-03-22T15:06:28.338Z
	# first throw away .XXXZ
	parsed = datetime.strptime(timestamp[:timestamp.rfind('.')], '%Y-%m-%dT%H:%M:%S')
	return parsed.strftime("%Y%m%dT%H%M%SZ")


def handle_list(todo_list: Dict) -> List[str]:
	list_created_at = todo_list["createdAt"]
	str_list = []
	for task in todo_list["tasks"]:
		parsed_str = f"""
BEGIN:VTODO
DTSTAMP:{parse_timestamp(task["createdAt"])}
SEQUENCE:0
SUMMARY:{task["title"]}
CREATED:{parse_timestamp(task["createdAt"])}
UID:{task["id"]}"""
		if task["completed"]:
			parsed_str += f"""
STATUS:COMPLETED
COMPLETED:{parse_timestamp(task["completedAt"])}
PERCENT-COMPLETE:100
LAST-MODIFIED:{parse_timestamp(task["completedAt"])}
"""
		else:
			parsed_str += "\n"
		parsed_str += "END:VTODO"
		str_list.append(parsed_str)
	return str_list

def write_ics(name: str, str_list: List[str]) -> None:
	ics_str = """BEGIN:VCALENDAR
PRODID:wasmitnetzen/wunder2ics
VERSION:2.0"""
	ics_str += ''.join(str_list)
	ics_str += "\nEND:VCALENDAR"
	with open(f"output/{name}.ics", "w") as f:
		# RFC 5545 3.1. Content Lines requires CLRF line endings
		f.write(ics_str.replace('\n', '\r\n'))

def main(file) -> None:
	with codecs.open(file, 'r', 'utf-8-sig') as json_file:
		data = json.load(json_file)
		for todo_list in data:
			parsed = handle_list(todo_list)
			write_ics(todo_list["title"], parsed)
			return

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Parse Wunderlist export.')
	parser.add_argument('file', metavar='f', help='The Tasks.json from the Wunderlist export')

	args = parser.parse_args()
	sys.exit(main(args.file))
