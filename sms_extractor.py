import xml.etree.ElementTree as ET
import datetime
from tqdm import tqdm

def unix_to_readable(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')

# File path to your XML data
xml_file_path = '/home/bscholer/Downloads/sms-20240122181046.xml'

# Define your target date
target_date = '2024-01-01'

messages = []
message_count = 0
interval = 1000

for event, elem in tqdm(ET.iterparse(xml_file_path, events=('end',))):
    print(elem.tag)
    # this is potentially stupid if the file changes format, but it should do the trick #regrets 
    if elem.tag != 'sms':
        break

    if elem.tag == 'sms':
        message_count += 1
        if message_count % interval == 0:
            print(f"Processed {message_count} messages")
        sms_date = unix_to_readable(elem.attrib['date'])
        if sms_date == target_date:
            contact_name = elem.attrib.get('contact_name', '(Unknown)')
            body = elem.attrib.get('body', '')
            messages.append((contact_name, body))
        elem.clear()

print(messages)

# Sort messages by contact name
messages.sort(key=lambda x: x[0])

# Print formatted messages
for name, message in messages:
    print(f"[[{name}]]: {message}")
