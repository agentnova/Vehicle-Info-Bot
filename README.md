# Vehicle-Info-Bot

Pluggable
[Telegram](https://telegram.org) bot based on
[Pyrogram](https://github.com/pyrogram/pyrogram).

## About the bot

>Simply the purpose of this bot is to gather all possible information about an indian vehicle registration number.
>Saves your time...:-)

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Mozilla Public License for more details.

### Installation

#### The Easy Way

Deploy it to heroku

#### The Legacy Way
Simply clone the repository and run the main file:
```sh
git clone https://github.com/agentnova/Vehicle-Info-Bot.git

cd Vehicle-Info-Bot

python3 -m venv venv

. ./venv/bin/activate

pip install -r requirements.txt

python3 main.py

```
#### Dont forget to edit the creds.py with your own variables like below with your own values
```python3
class cred():
    BOT_TOKEN = "your bot token from botfather"
    API_ID = "your api id from my.telegram.org!"       
    API_HASH = "your api hash from my.telegram.org!"   
    
```

