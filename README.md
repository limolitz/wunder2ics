# wunder2ics

This python tool transforms the export from Wunderlist into ics files. It creates one file per list, so you can create one calendar per list.

It is mainly tested with Nextcloud, but follows the Icalendar standard, so it should support any software which supports this.

One main downside is the handling of subtasks due to limitations of the Icalendar standard, see below for details.

## Features
* Converts all tasks in all lists
* Conserves created and completed time
* Conserves completion status
* Conserves notes
* Three different options regarding subtasks

## Usage
### 1. Clone this repo
```
$ git clone git@github.com:wasmitnetzen/wunder2ics.git
```

### 2. Request backup from Wunderlist

You can request the backup file from 'Account Settings -> Create Backup' on Wunderlist.

[Wunderlist | Can I backup / export my data?](https://support.wunderlist.com/customer/en/portal/articles/2364564-can-i-backup-export-my-data-)

Then, move the backup file to the wunder2ics directory, especially the Tasks.json file.

### 3. Call the tool
```
$ ./main.py --flatten-subtasks --subtasks-as-description --inherit-completed Tasks.json
```

It is recommended to call the tool with all three features regarding subtasks enabled.

All files will be put in the output folder.

### 4. Import to Nextcloud

You need both the Calendar app as well as the Tasks app in Nextcloud.
1. Go to the Calendar
2. Create a calendar for each list you want to import
3. In the Calendar app, click on "Settings & import" in the bottom left, and then on "Import calendar"
4. Select the file and choose the appropriate calendar in the downdown
5. Wait for the import to finish, then you can go to the Tasks app to see all your tasks
6. (Optional) Fix the subtask relations
7. Profit!

## Subtaks
The Icalendar standard does not support subtasks, but both Wunderlist and Nextcloud do. There are three switches regarding subtasks in this tool:

* Flatten subtasks

For each subtask, an additional task will be created with a title of "PARENT TITLE - SUBTASK TITLE"

* Subtasks as Description

Each task which has subtasks will contain a list of its subtasks in its description.

* Inherit Completed

This switch only makes sense in combination with "Flatten subtasks". If enabled, a completed parent task will mark all its subtasks as completed as well.

If you enable all three switches, you can then quite easily manually restore the associations of tasks and their subtasks by sorting the task list alphabetically.

## Dependencies

* Python3

## Acknowledgements

This tool is inspired by [takafumir/wunder2reminders](https://github.com/takafumir/wunder2reminders), which does a similar task in Ruby.
