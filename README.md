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

## Requirements

* Python3

### 1. Get the script
```
$ curl -LO "https://github.com/wasmitnetzen/wunder2ics/raw/master/main.py"
```

### 2. Request backup from Wunderlist

You can request the backup file from 'Account Settings -> Create Backup' on Wunderlist.

[Wunderlist | Can I backup / export my data?](https://support.wunderlist.com/customer/en/portal/articles/2364564-can-i-backup-export-my-data-)

### 3. Call the tool
```
$ ./main.py --flatten-subtasks --subtasks-as-description --inherit-completed --ignore-completed /path/to/Tasks.json
```

It is recommended to call the tool with all three features regarding subtasks enabled.

`--ignore-completed`: Ignore all completed tasks (not subtasks) during conversion. based on your situation this will accelerate your import process time noticeable.

All files will be put in the output folder, which has to be created manually in advance.

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

* Flatten subtasks (`--flatten-subtasks`)

For each subtask, an additional task will be created with a title of "PARENT TITLE - SUBTASK TITLE" (This is supported by [the FLOSS android app "OpenTasks"](https://github.com/dmfs/opentasks/), [distributed by F-Droid](https://f-droid.org/packages/org.dmfs.tasks/))

* Subtasks as Description (`--subtasks-as-description`)

Each task which has subtasks will contain a list of its subtasks in its description. (this is supported by [the official Nextcloud tasks app](https://apps.nextcloud.com/apps/tasks))

* Inherit Completed (`--inherit-completed`)

This switch only makes sense in combination with "Flatten subtasks". If enabled, a completed parent task will mark all its subtasks as completed as well.

If you enable all three switches, you can then quite easily manually restore the associations of tasks and their subtasks by sorting the task list alphabetically.

## Acknowledgements

This tool is inspired by [takafumir/wunder2reminders](https://github.com/takafumir/wunder2reminders), which does a similar task in Ruby.
