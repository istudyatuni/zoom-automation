import argparse
import os, time
import csv
from datetime import datetime

# https://superuser.com/a/1563359
# https://superuser.com/a/1624394
join_url = '--url="zoommtg://zoom.us/join?confno={meeting_id}&pwd={pwd}"'


silent_log = False

def simple_log(*args):
    if not silent_log:
        print(*args)

def parse_args():
    parser = argparse.ArgumentParser(description='Zoom start automation')

    parser.add_argument('-c', '--cron', action='store_true', help='Script is running with crontab. Also can be used for running script once')
    parser.add_argument('-s', '--schedule', type=str, help='File with schedule', default='meetingschedule.csv')
    parser.add_argument('-q', '--quite', action='store_true', help='Be more quite')

    return parser.parse_args()

def get_zoom_exec():
    import sys
    if sys.platform.startswith('win32'):
        # %HOME%/Appdata/Roaming
        appdata = os.getenv('APPDATA')
        zoom_exe = f'{appdata}/Zoom/bin/Zoom.exe'

        if os.path.exists(zoom_exe):
            return zoom_exe
    else:
        # linux, unix, etc (I hope)
        if os.system('which zoom') == 0:
            return 'zoom'

    quit('zoom is not installed or not found')

def open_zoom(meeting_id, hashed_pass):
    join_param = join_url.format(
        meeting_id=meeting_id.replace(' ', ''),
        pwd=hashed_pass,
    )

    run_url = f'{get_zoom_exec()} {join_param}'

    simple_log('run:', run_url)
    os.system(run_url)

def check_zoom_running():
    import psutil
    return 'zoom' in (p.name() for p in psutil.process_iter())

def main(schedule_file):
    # reading the meeting details
    with open(schedule_file) as csv_file:
        meetings = list(csv.DictReader(
            csv_file,
            # rename columns
            fieldnames=('time', 'meeting_id', 'pwd'),
        ))

    # Check the current system time
    timestr = datetime.now().strftime('%H:%M')

    # get first meeting with current time
    current = next(a for a in meetings if a['time'] == timestr, {})

    if not current:
        simple_log('no meeting at', timestr)
        return

    simple_log('meeting at', timestr)
    open_zoom(current['meeting_id'], current['pwd'])

if __name__ == '__main__':
    if check_zoom_running():
        quit('Another instance of zoom is running. Quitting')

    args = parse_args()
    silent_log = args.quite

    if args.cron:
        main(args.schedule)
        quit()

    while(True):
        main(args.schedule)

        # Wait for one minute before the next iteration starts
        time.sleep(60)
