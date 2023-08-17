import pygetwindow as gw
from pypresence import Presence
import psutil
import time
import pypresence
from dotenv import load_dotenv
import os

load_dotenv()

appsTimes = {}


def truncate_text(text, max_length=128):
    if len(text) > max_length:
        truncated_text = text[:max_length - 3] + "..."
    else:
        truncated_text = text
    return truncated_text


def focused_window():
    global appsTimes
    active_window = gw.getActiveWindow()
    if active_window is not None:
        if active_window.title not in appsTimes:
            appsTimes[active_window.title] = time.time()
        return active_window.title
    else:
        appsTimes['Nothing'] = time.time()
        return 'Nothing'


client_id = os.getenv("CLIENTID")
RPC = Presence(client_id)
RPC.connect()
print('Started')

buttons = [{'label': 'My socials', 'url': 'https://e-z.bio/rionnag'},
           {'label': 'PC Perfomance', 'url': 'https://www.userbenchmark.com/UserRun/63476314'}]

while True:
    try:
        window = focused_window()
        if window == '':
            text = 'Nothing open'
        else:
            text = truncate_text(f'Window: {window}', 125)
        cpu_per = round(psutil.cpu_percent(), 1)
        RPC.update(large_text='insane computer',
                   large_image='logo', details=text, state="CPU: "+str(cpu_per)+"%", start=appsTimes[window], buttons=buttons)
        time.sleep(1)
    except pypresence.exceptions.PipeClosed:
        print('Piped closed. Restarting...')
        RPC = Presence(client_id)
        RPC.connect()
