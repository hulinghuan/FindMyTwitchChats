# FindMyTwitchChats

For some reasons I need to find my twitch chats (what I said, and when I said) in an archieved Twitch video.
If you want to do the same thing, this script can help you.

# Examples:

Example 1: Directly fetch the twitch chats and search your messages:
```bash
➜ python findmychat.py -u https://www.twitch.tv/videos/160499333 -n grimlinzbot -s grimmmz
➜ At 01 Hour, 11 Minute, 26 Second: Twitch Prime is a premium experience on Twitch that is included with an Amazon Prime membership. ➜ A FREE CHANNEL SUBSCRIPTION EVERY 30 DAYS TO BE USED ON ANY PARTNERED CHANNEL, ad-free viewing on Twitch, exclusive emotes, and chat badge.
➜ At 01 Hour, 58 Minute, 29 Second: If Grimmz misses something, he doesn't use chat to go back for it
➜ At 04 Hour, 32 Minute, 15 Second: https://multistre.am/grimmmz/anthony_kongphan/layout3/
➜ ...
```

Example 2: Load the fetched chat from a file and search your message:
```bash
➜ python findmychat.py -u https://www.twitch.tv/videos/160499333 -n grimlinzbot -l grimmmz
➜ At 01 Hour, 11 Minute, 26 Second: Twitch Prime is a premium experience on Twitch that is included with an Amazon Prime membership. ➜ A FREE CHANNEL SUBSCRIPTION EVERY 30 DAYS TO BE USED ON ANY PARTNERED CHANNEL, ad-free viewing on Twitch, exclusive emotes, and chat badge.
➜ At 01 Hour, 58 Minute, 29 Second: If Grimmz misses something, he doesn't use chat to go back for it
➜ At 04 Hour, 32 Minute, 15 Second: https://multistre.am/grimmmz/anthony_kongphan/layout3/
➜ ...
```

# Commands:
* -u: specify the archived Twitch video URL
* -n: the name of the twitch user
* -s: save the chat log fetched from server
* -l: load the chat log from local file

# Known Issues:

I do know sometimes the script is froze doing the chat log fetching phase, and being not responsive.
This might be because one of the threads cannot get the response from the Twitch API.

In the next release, I will find out the real cause. The worst scenario is adding a timeout for the script.

# To Do List:

1. Progress Bar:
So far, each thread has its own progress bar. I tried to use lock to implement universal progress bar, but 
it drops the performance significantly.
