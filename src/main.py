import pytz
import os
import requests
from dotenv import load_dotenv
from calendar import c
from datetime import datetime, timedelta
from typing import Set

#from calendar import c
from ics.alarm import none
from ics import Calendar
from ics import Event as IcsEvent

from caldav import DAVClient
from icalendar import Calendar as iCalendar
from icalendar import Event as CalEvent
from icalendar import Alarm

import segno
from PIL import Image, ImageDraw, ImageFont


load_dotenv()

icloud_username = os.getenv("icloud_username")
icloud_password = os.getenv("icloud_password")


# Public iCloud Calender URLs:
KA_Kepi_6c_url  = os.getenv("KA_Kepi_6c_url")
KA_Kepi_8c_url  = os.getenv("KA_Kepi_8c_url")


user1   = os.getenv("user1")
passwd1 = os.getenv("passwd1")    

user2   = os.getenv("user2")
passwd2 = os.getenv("passwd2")    




# Kepler-URLs

base_url="https://orga.kepi.de"
auth_frag="gfs/ajax/dologin.php"
ical_frag="/gfs/icsexport.php?thisyear=1"

local_tz = pytz.timezone("Europe/Berlin")


def remove_duplicate_dtstamp(lines: str) -> str:
    cleaned_lines = []
    for line in str(lines).split("\n"):
        line=line.strip()
        if line == "":
            continue
        
        if not (line.startswith("DTSTAMP:") and "Z" in line):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def get_ical_events_from_kepler(user: str, passwd: str) -> Set[IcsEvent]:
    data = {
        "username": user,
        "password": passwd
    }

    response = requests.post(f"{base_url}/{auth_frag}", data=data)

    if response.status_code != 200:
        print("Failed:", response.status_code, response.text)
        exit(-1)

    cookies = response.cookies

    response = requests.get(f"{base_url}/{ical_frag}", cookies=cookies)

    if "BEGIN:VCALENDAR" not in response.text:
        print("Failed, can't find calendar entries (bad login?)")
        exit(-1)
        
    cleaned_content = remove_duplicate_dtstamp(response.text)

    calendar = Calendar(cleaned_content)
    
    # Check for duplicate events ids:    
    ids = set()
    for event in calendar.events:
        if event.uid in ids:
            print(f"Warning: Duplicate calender IDs: {event.uid}, one entry is lost!")
        ids.add(event.uid)

    return calendar.events
   
   
def add_to_ical(calender_name: str, events: Set[IcsEvent]) -> Set[IcsEvent]:
    
    client = DAVClient(
        url="https://caldav.icloud.com/",
        username=icloud_username,
        password=icloud_password
    )

    principal = client.principal()
    calendars = principal.calendars()

    calendar = None

    for i_calender in calendars:
        if i_calender.name == calender_name:
            calendar = i_calender
            break

    if calendar is None:
        print(f"Error: Calender '{calender_name}' not found!")
        exit(-1)
        
    ical = iCalendar()

    for event in events:
        print(f"Event: {event.uid}  --> {event.name}")

        calEvent = CalEvent()
    
        dtstart = event.begin.datetime.replace(tzinfo=local_tz)
        dtend   = event.end.datetime.replace(tzinfo=local_tz)

        title = event.name.replace("Klassenarbeit", "KA")
        
        calEvent.add("summary", title)
        calEvent.add("dtstart", dtstart.date())
        calEvent.add("dtend", dtend.date())
        #calEvent.add("description", "This is a test...")
        #calEvent.add("location", "Online")
        calEvent.add("uid", event.uid)

        alarm_hour = 7
        
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')  # Alarm-Typ: DISPLAY zeigt eine Erinnerung an
        alarm.add('description', f'Erinnerung morgen: {title}!')

        alarm_time = dtstart - timedelta(days=1, hours=24-alarm_hour)  # diff to alarm time
        alarm.add('trigger', alarm_time)
        calEvent.add_component(alarm)

        alarm2 = Alarm()
        alarm2.add('action', 'DISPLAY')  # Alarm-Typ: DISPLAY zeigt eine Erinnerung an
        alarm2.add('description', f'Erinnerung in einer Woche: {title}!')

        alarm2_time = dtstart - timedelta(days=7, hours=24-alarm_hour)  # diff to alarm time
        alarm2.add('trigger', alarm2_time)
        calEvent.add_component(alarm2)

    
        ical.add_component(calEvent)

 
    print("Updload to iCloud")
    calendar.add_event(ical.to_ical())
    print("Updload to iCloud...Done")

def create_qr_code(title: str, url: str):

    print("Create QR-Code for ", title)
    
    filename = f"QR {title}.png".replace(' ','_')
    qrcode = segno.make_qr(url)
    qrcode.save(filename, scale = 8)
    print(f"QR-Code created successfully: {filename}")  

    print("Add sub-title to QR-Code")
    font = ImageFont.truetype("Arial.ttf", 30)

    image = Image.open(filename)
    image_width, image_height = image.size

    new_image = Image.new("RGBA", (image_width, image_height + 20), (255, 255, 255, 255))
    new_image.paste(image, (0, 0))

    draw = ImageDraw.Draw(new_image)
    text_width, text_height = draw.textbbox((0, 0), title, font=font)[2:]
    text_x = (image_width - text_width) // 2
    text_y = image_height - text_height + 10
    draw.text((text_x, text_y), title, fill="black", font=font)

    new_image.save(filename)

# Main ----------------------------------------------------------------------

events = get_ical_events_from_kepler(user1, passwd1)
for event in events:
    print(f"Event: {event.uid}  --> {event.name}")
add_to_ical("KA-Kepi-6c", events)
create_qr_code("KA Kepi 6c", KA_Kepi_6c_url)
print("Events added successfully!")

events = get_ical_events_from_kepler(user2, passwd2)
for event in events:
    print(f"Event: {event.uid}  --> {event.name}")
add_to_ical("KA-Kepi-8c", events)
create_qr_code("KA Kepi 8c", KA_Kepi_8c_url)
print("Events added successfully!")






create_qr_code("KA Kepi 8c", KA_Kepi_8c_url)

