import pygetwindow as gw
from pypresence import Presence
import psutil
import time
import pypresence
from dotenv import load_dotenv
import os
import shutil
from itertools import cycle
import datetime
from datetime import datetime, timedelta

load_dotenv()

buttons = [{'label': 'My Site', 'url': 'https://rionnag.net/'},
           {'label': 'PC Perfomance', 'url': 'https://www.userbenchmark.com/UserRun/63476314'}]


def truncate_text(text, max_length=128):
    if len(text) > max_length:
        truncated_text = text[:max_length - 3] + "..."
    else:
        truncated_text = text
    return truncated_text


def get_space():
    disks = ['C', 'D', 'G']
    storageUsed = 0
    totalStorage = 0
    for disk in disks:
        d = shutil.disk_usage(f'{disk}:/')
        storageUsed += d.used
        totalStorage += d.total
    storageUsed = round(storageUsed / (1024 * 1024 * 1024 * 1024), 4)
    totalStorage = round(totalStorage / (1024 * 1024 * 1024 * 1024), 4)
    return f'{storageUsed}TB / {totalStorage}TB'


def get_time():
    current_time = datetime.now()

    formatted_time = current_time.strftime("%I:%M %p")

    return formatted_time


def get_amount_of_processes():
    return len([i for i in psutil.process_iter()])


def get_cpu_usage():
    return f'{round(psutil.cpu_percent(), 3)}%'


def convTime(input_time_str: str):
    year = int(input_time_str[0:4])
    month = int(input_time_str[4:6])
    day = int(input_time_str[6:8])
    hour = int(input_time_str[8:10])
    minute = int(input_time_str[10:12])
    second = int(input_time_str[12:14])
    microseconds = int(float(input_time_str[14:20]))

    offset_str = input_time_str[20:]

    offset_sign = 1 if offset_str[0] == '-' else -1
    offset_seconds = int(offset_str[1:])

    total_offset_seconds = offset_sign * offset_seconds

    input_datetime = datetime(year, month, day, hour,
                              minute, second, microseconds)

    offset = timedelta(seconds=total_offset_seconds)

    adjusted_datetime = input_datetime - offset

    return adjusted_datetime.timestamp()


def get_computerDur():
    data = os.popen(
        'wmic path Win32_OperatingSystem get LastBootUpTime').read()
    time = data.splitlines()[2].replace(' ', '')
    return convTime(time)


def get_commands_used():
    with open(r'C:\Users\giris\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt', 'r', encoding='utf-8') as f:
        return len(f.read().splitlines())


def get_last_command():
    with open(r'C:\Users\giris\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt', 'r', encoding='utf-8') as f:
        return f.read().splitlines()[-1]


types = cycle([
    {'fun': get_space, 'name': 'Storage', 'state': '{}'},
    {'fun': get_time, 'name': 'Time here', 'state': '{}'},
    {'fun': get_amount_of_processes, 'name': 'Processes open', 'state': '{} tasks'},
    {'fun': get_cpu_usage, 'name': 'CPU usage', 'state': '{} being used'},
    {'fun': get_commands_used, 'name': 'Commands used', 'state': '{} commands'},
    {'fun': get_last_command, 'name': 'Last command', 'state': '{}'}
])


def main():
    try:
        client_id = os.getenv("CLIENTID")
        RPC = Presence(client_id)
        RPC.connect()
        print('Started')
        while True:
            boottime = get_computerDur()
            todo = next(types)
            for i in range(5):
                fundata = todo['fun']()
                string = todo['state'].format(fundata)

                RPC.update(large_text='insane computer',
                           large_image='logo', details=todo['name'], state=truncate_text(string), start=boottime, buttons=buttons)
                time.sleep(1)
    except Exception as e:
        print(f'Error: {e}')
        return


while True:
    main()
    time.sleep(5)
