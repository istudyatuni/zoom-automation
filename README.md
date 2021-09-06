# Zoom Automation
A python script that automatically joins a zoom meeting based on your timetable.

## What does it do?
It performs the following processes:
1. Checks the "meetingschedule.csv" file to look for meetings that are going to start.
2. As soon as the current time matches any meeting time it opens the Zoom Desktop application.
3. Navigates the cursor automatically to various steps to join the meeting.
4. The meeting ID and hashed passcode are extracted from "meetingschedule.csv" and entered into the Zoom app automatically.

*Note*. Hashed passcode you should pick from share url, for example, for url `https://us04web.zoom.us/j/12345678910?pwd=AB3CD6fghijkL8MalsdfjaDHSFSDiuN9` passcode is `AB3CD6fghijkL8MalsdfjaDHSFSDiuN9`. You can also pick from this url meeting id: `12345678910`.

## Prerequisites
1. Zoom app must be installed in your system.
2. You must be logged in to your Zoom account.
3. Meeting time for the day along with Meeting ID and hashed passcode must be entered manually into the "meetingschedule.csv"

## How to use?
1. The best way to use my script is to firstly clone the git repo where you want to.
2. On Windows expected that Zoom.exe is installed in `APPDATA` folder (default installation), so path will be `%APPDATA%/Zoom/bin/Zoom.exe`
2. Open "meetingschedule.csv" and fill in the Meeting Time, Meeting ID and Hashed passcode of each meeting you want to join automatically.
3. Run `python zoom.py` from project folder.

NOTE: Meeting Time must be in Hours and Minutes format only!

## What happens behind the scene?
1. An infinite loop keeps checking the current time of the system using `datetime.now()` funtion.
2. The zoom app is opened using `os.system()` funtion as soon as current time matches the time mentioned in "meetingschedule.csv".
3. Meeting ID and Hashed passcode are passed to zoom application via CLI argument as `--url="zoommtg://zoom.us/join?confno={meeting id}&pwd={hashed passcode}"`
