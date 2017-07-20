import urllib
import urllib2
import json
import pprint
pp = pprint.PrettyPrinter(indent = 4)
import argparse
import pdb
import time
import progressbar
import threading
max_thread_count = 50
progress_counter = 0
counter_lock = threading.Lock()
from datetime import datetime, timedelta
from jsoncompare import jsoncompare

api = [
'https://rechat.twitch.tv/rechat-messages?start=',
'&video_id=v']

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def make_querry_url(time_beg, video_id):
    return api[0] + str(time_beg) + api[1] + video_id

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_video_id(url):
    return url.split("/")[-1]
    

def get_timestamps(video_id):
    query = "https://rechat.twitch.tv/rechat-messages?start=0&video_id=v"
    query += str(video_id)

    req = urllib2.Request(query)
    response = None
    try:
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        response = e.read()
    
    response = json.loads(response)
    time_beg = response['errors'][0]['detail'].split()[-3]
    time_end = response['errors'][0]['detail'].split()[-1]
    if represents_int(time_beg) and represents_int(time_end):
        return_val = {}
        return_val['time_beg'] = time_beg
        return_val['time_end'] = time_end
        return return_val

def fetch_raw_chats(video_id, timestamps):
    time_beg = int(timestamps['time_beg'])
    time_end = int(timestamps['time_end'])
    time_segs = []
    threads = []
    chats = []

    if not (time_end - time_beg) / 15 > max_thread_count:
        thread_count = (time_end - time_beg) / 15
        time_segs = range(thread_count)
    else:
        thread_count = max_thread_count
        time_segs = chunkIt(range(time_beg, time_end, 15), max_thread_count)

    # pt = threading.Thread(target=progress_counting_worker, args=(time_end-time_beg,))
    # pt.start()

    for i in range(thread_count):
        td = threading.Thread(target=chat_fetching_worker, args=(time_segs[i][0], time_segs[i][-1], chats, video_id))
        threads.append(td)
        td.start()

    for e in threads:
        e.join()
    # pt.join()

    return chats

def chat_fetching_worker(time_beg, time_end, chats, video_id):
    global progress_counter
    bar = progressbar.ProgressBar()
    with progressbar.ProgressBar(max_value=time_end-time_beg) as bar:
        for t in range(time_beg, time_end, 15):
            req = api[0] + str(t) + api[1] + video_id
            response = urllib2.urlopen(req)
            chat = json.loads(response.read())
            chats.append(chat)
            bar.update(t-time_beg)
            # counter_lock.acquire()
            # try:
            #     progress_counter += 1
            # finally:
            #     counter_lock.release()

def progress_counting_worker(total_progress):
    with progressbar.ProgressBar(max_value=total_progress) as bar:
        while progress_counter < total_progress:
            bar.update(progress_counter)

def get_my_chats(raw_chats, twitch_name = None):
    results = []
    for e in raw_chats:
        for d in e['data']:
            if not twitch_name:
                results.append(d)
            else:
                if d['attributes']['from'] == twitch_name or \
                d['attributes']['tags']['display-name'] == twitch_name:
                    results.append(d)
    return results

def print_my_chats(my_chats, timestamps):
    if my_chats:
        for e in my_chats:
            t = int(e['attributes']['timestamp'])/1000 - int(timestamps['time_beg'])
            sec = timedelta(seconds=t)
            d = datetime(1, 1, 1) + sec
            print "At {0:0>2} Hour, {1:0>2} Minute, {2:0>2} Second:  {3}".format(d.hour, d.minute, d.second, e['attributes']['message'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',  help='URL of the twitch video e.g., https://www.twitch.tv/videos/158708579')
    parser.add_argument('-n', '--name', help='the name of the twitch user')
    parser.add_argument('-s', '--save', help='save the fechted json into file')
    parser.add_argument('-l', '--load', help='load chat json')
    args = parser.parse_args()

    video_id = get_video_id(args.url)
    timestamps = get_timestamps(video_id)
    if args.load:
        with open(args.load) as f:
            raw_chats = json.load(f)
        get_my_chats(raw_chats)
    else:
        video_id = get_video_id(args.url)
        timestamps = get_timestamps(video_id)
        print "Fetching chat log..."
        raw_chats = fetch_raw_chats(video_id, timestamps)
        with open(args.save, "w") as f:
            json.dump(raw_chats, f)

    my_chats = get_my_chats(raw_chats, args.name)
    print_my_chats(my_chats, timestamps)

if __name__ == '__main__':
    main()