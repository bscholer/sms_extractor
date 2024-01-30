import xml.etree.ElementTree as ET
import datetime
from tqdm import tqdm
import requests
import os

def unix_to_readable(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')

# File path to your XML data
xml_file_path = '/home/bscholer/Downloads/sms-20240122181046.xml'

# today
# target_date = '2024-01-01'
# target_date = datetime.datetime.now().strftime('%Y-%m-%d')

api_path = "http://localhost:11435/api/generate"
model = "llama2"

dates = {}

for event, elem in tqdm(ET.iterparse(xml_file_path, events=('end',))):
    # this is potentially stupid if the file changes format, but it should do the trick #regrets 
    if elem.tag != 'sms':
        break

    if elem.tag == 'sms':
        sms_date = unix_to_readable(elem.attrib['date'])

        address = elem.attrib.get('address', '')
        contact_name = elem.attrib.get('contact_name', f"Unknown-{address}")
        body = elem.attrib.get('body', '')
        incoming = True if elem.attrib.get('type', 0) == '1' else False
        # messages.append((contact_name, body, incoming))

        if sms_date not in dates:
            dates[sms_date] = [(contact_name, body, incoming)]
        else:
            dates[sms_date].append((contact_name, body, incoming))

        elem.clear()

for date, messages in dates.items():
    messages_by_contact = {}
    for name, message, incoming in messages:
        if name not in messages_by_contact:
            messages_by_contact[name] = []
        messages_by_contact[name].append((message, incoming))

    summaries = {}

    for name, messages in messages_by_contact.items():
        system_message = f"you are a text message summarizer bot. I am Ben. This is a log of my text messages to {name} for the day. your job is to summarize the messages. Do not summarize texts with 2 factor codes, and sign in codes.do not include any extra notes, or anything that isn't a key point of the note. Write each key point with bullet points (-). Be concise. Do not simply rewrite the notes, you must summarize them. Do not include a title or description at the top."
        prompt = ""
        for message, incoming in messages:
            prompt += f"\n\n{'from' if incoming else 'to'} {name}: {message}"

        res = requests.post(api_path, json={"model": model, "prompt": prompt, "stream": False, "system": system_message})
        summary = res.json()['response']
        # Make an Obsidian link for the contact
        summaries[name] = f"\n# [[{name}]]\n" + summary 

    year = date[:4]
    month = date[5:7] + '-' + datetime.datetime.strptime(date[5:7], '%m').strftime('%B')
    print(date)
    path = f'/home/bscholer/bens-brain/⏱️ Timestamps/{year}/{month}/{date} 💬 Texts.md'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        for name, summary in summaries.items():
            f.write(summary + '\n\n')

