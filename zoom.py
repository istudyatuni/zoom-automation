import os
import pandas as pd
from datetime import datetime

# reading the meeting details
df = pd.read_csv('meetingschedule.csv')
df_new = pd.DataFrame()

# https://superuser.com/a/1563359
# https://superuser.com/a/1624394
join_url = '--url="zoommtg://zoom.us/join?confno={meeting_id}&pwd={hashed_pass}"'

def open_zoom(meeting_id, hashed_pass):
    join_param = join_url.format(
        meeting_id=meeting_id.replace(' ', ''),
        hashed_pass=hashed_pass,
    )

    import sys
    if sys.platform.startswith('win32'):
        appdata = os.getenv('APPDATA')
        os.system(f'{appdata}/Zoom/bin/Zoom.exe {join_param}')
    else:
        # linux, unix, etc (I hope)
        os.system(f'zoom {join_param}')

def main():
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
    import time

    while(True):
        main()

        # Wait for one minute before the next iteration starts
        time.sleep(60)
