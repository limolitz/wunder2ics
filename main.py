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


def handle_list(todo_list: Dict, flatten_subtasks: bool, subtasks_as_description: bool, inherit_completed: bool) -> List[str]:
	list_created_at = todo_list["createdAt"]
	str_list = []
	for task in todo_list["tasks"]:
		description = ""
		# parse notes
		if len(task["notes"]) > 0:
			description += "Notes:\n"
			description += "".join([note["content"] for note in task["notes"]])
			description += "\n"

		# add subtasks to desc if needed
		if subtasks_as_description and len(task["subtasks"]) > 0:
			description += "Subtasks:\n"
			for subtask in task["subtasks"]:
				if subtask["completed"]:
					status = "[x]"
				else:
					status = "[ ]"
				description += f"{status} {subtask['title']}\n"
		# replace newlines in desc with literal '\n'
		desc_literal = description.replace('\n', '\\n')

		parsed_str = f"""
BEGIN:VTODO
DTSTAMP:{parse_timestamp(task["createdAt"])}
SEQUENCE:0
SUMMARY:{task["title"]}
CREATED:{parse_timestamp(task["createdAt"])}
UID:{task["id"]}
DESCRIPTION:{desc_literal}
"""

		# add completed info
		if task["completed"]:
			parsed_str += f"""STATUS:COMPLETED
COMPLETED:{parse_timestamp(task["completedAt"])}
PERCENT-COMPLETE:100
LAST-MODIFIED:{parse_timestamp(task["completedAt"])}
"""

		# due date
		if task["dueDate"]:
			parsed_str += f"DUE:{parse_timestamp(task['dueDate'])}\n"

		parsed_str += "END:VTODO"

		if flatten_subtasks and len(task["subtasks"]) > 0:
			# add all subtasks as their own tasks
			for idx, subtask in enumerate(task["subtasks"]):
				subtask_id = f"{task['id']}-{idx}"
				subtask_title = f"{task['title']} - {subtask['title']}"
				parsed_str += f"""
BEGIN:VTODO
DTSTAMP:{parse_timestamp(subtask["createdAt"])}
SEQUENCE:0
SUMMARY:{subtask_title}
CREATED:{parse_timestamp(subtask["createdAt"])}
UID:{subtask_id}
"""
				if subtask["completed"]:
					parsed_str += f"""STATUS:COMPLETED
COMPLETED:{parse_timestamp(subtask["completedAt"])}
PERCENT-COMPLETE:100
LAST-MODIFIED:{parse_timestamp(subtask["completedAt"])}
"""
				else:
					if task["completed"] and inherit_completed:
						parsed_str += f"""STATUS:COMPLETED
COMPLETED:{parse_timestamp(task["completedAt"])}
PERCENT-COMPLETE:100
LAST-MODIFIED:{parse_timestamp(task["completedAt"])}
"""
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

def main(file, flatten_subtasks, subtasks_as_description, inherit_completed) -> None:
	with codecs.open(file, 'r', 'utf-8-sig') as json_file:
		data = json.load(json_file)
		for todo_list in data:
			parsed = handle_list(todo_list, flatten_subtasks, subtasks_as_description, inherit_completed)
			write_ics(todo_list["title"], parsed)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Parse Wunderlist export.')
	parser.add_argument("--subtasks-as-description", help="Put subtasks into description of parent task", action="store_true")
	parser.add_argument("--flatten-subtasks", help="Put subtasks into their own task, with textual reference of parent task", action="store_true")
	parser.add_argument("--inherit-completed", help="If a parent if a subtask is done, it will be considered as done as well", action="store_true")
	parser.add_argument('file', metavar='f', help='The Tasks.json from the Wunderlist export')


	args = parser.parse_args()
	if args.inherit_completed and not args.flatten_subtasks:
		print("Warning: --inherit-completed is ignored without enabling --flatten-subtasks.", file=sys.stderr)
	sys.exit(main(args.file, args.flatten_subtasks, args.subtasks_as_description, args.inherit_completed))
