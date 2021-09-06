import keyboard, time, subprocess
import pandas as pd
from datetime import datetime
import pyautogui

# reading the meeting details
df = pd.read_csv('meetingschedule.csv')
df_new = pd.DataFrame()

def open_zoom():
    import sys, os
    if sys.platform.startswith('win32'):
        appdata = os.getenv('APPDATA')
        subprocess.Popen(f'{appdata}/Zoom/bin/Zoom.exe')
    else:
        subprocess.Popen('zoom')

    time.sleep(3)

def click_button_by_image(name):
    # Locate the position of the button on the screen
    position = pyautogui.locateOnScreen(name)

    if not position:
        return False

    # Move the cursor to the position of the button
    pyautogui.moveTo(position)
    # Perform click operation
    pyautogui.click()

    return True

def click_join_button_with_plus():
    result = click_button_by_image('buttons/join_button.png')

    if not result:
        # i don't know why, but on linux here is different button
        click_join_meeting_button()
        return

    time.sleep(2)

def click_join_button_with_text():
    # For tapping on the Join button
    click_button_by_image('buttons/join_button_2.png')

    time.sleep(7)

def click_join_meeting_button():
    click_button_by_image('buttons/join_meeting.png')

def click_turn_off_video():
    # For tapping the Turn off video option on Zoom app
    click_button_by_image('buttons/turn_off_vid_button.png')

    time.sleep(2)

def write_from_keyboard(text):
    # Write the meeting ID from the dataframe onto the Zoom App
    keyboard.write(text)

def main():
    # Check the current system time
    timestr = datetime.now().strftime('%H:%M')

    # Check if the current time is mentioned in the Dataframe
    if timestr not in df.Time.values:
        return

    df_new = df[df['Time'].astype(str).str.contains(timestr)]

    open_zoom()
    click_join_button_with_plus()

    # write ID
    write_from_keyboard(df_new.iloc[0,1])

    click_turn_off_video()

    click_join_button_with_text()


    # Reads the Meeting Passcode from the dataframe and enters into the zoom app
    write_from_keyboard(str(int(df_new.iloc[0,2])))
    time.sleep(3)

    click_join_meeting_button()

    # Wait for one minute before the next iteration starts
    time.sleep(60)

if __name__ == '__main__':
    while(True):
        main()
