import argparse
import os, time
import pandas as pd
from datetime import datetime

# https://superuser.com/a/1563359
# https://superuser.com/a/1624394
join_url = '--url="zoommtg://zoom.us/join?confno={meeting_id}&pwd={hashed_pass}"'


def parse_args():
    parser = argparse.ArgumentParser(description='Zoom start automation')

    parser.add_argument('-c', '--cron', action='store_true', help='Script is running with crontab. Also can be used for running script once')
    parser.add_argument('-s', '--schedule', type=str, help='File with schedule', default='meetingschedule.csv')

    return parser.parse_args()

def zoom_exec():
    import sys
    if sys.platform.startswith('win32'):
        # %HOME%/Appdata/Roaming
        appdata = os.getenv('APPDATA')
        zoom_exe = f'{appdata}/Zoom/bin/Zoom.exe'

        if not os.path.exists(zoom_exe):
            zoom_exe = ''
    else:
        # linux, unix, etc (I hope)
        zoom_exe = 'zoom'

        if os.system('which zoom') == 256:
            zoom_exe = ''

    if zoom_exe:
        return zoom_exe

    quit('zoom not installed or not found')

def open_zoom(meeting_id, hashed_pass):
    join_param = join_url.format(
        meeting_id=meeting_id.replace(' ', ''),
        hashed_pass=hashed_pass,
    )

    run_url = f'{zoom_exec()} {join_param}'

    print('run:', run_url)
    os.system(run_url)

def check_zoom_running():
    import psutil
    return 'zoom' in (p.name() for p in psutil.process_iter())

def main(schedule_file):
    # reading the meeting details
    df = pd.read_csv(schedule_file)
    df_new = pd.DataFrame()

    # Check the current system time
    timestr = datetime.now().strftime('%H:%M')

    # Check if the current time is mentioned in the Dataframe
    if timestr not in df.Time.values:
        return

    df_new = df[df['Time'].astype(str).str.contains(timestr)]

    meeting_id = df_new.iloc[0,1]
    hashed_pass = df_new.iloc[0,2]

    open_zoom(meeting_id, hashed_pass)

if __name__ == '__main__':
    if check_zoom_running():
        quit('Another instance of zoom is running. Quitting')

    args = parse_args()

    if args.cron:
        main(args.schedule)
        quit()

    while(True):
        main(args.schedule)

        # Wait for one minute before the next iteration starts
        time.sleep(60)
