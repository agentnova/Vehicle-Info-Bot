from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram import Client, filters
from process import check, get_captcha, sort
import os, re
from creds import cred

app = Client(
    "Vehicle-Info-Bot",
    api_id=cred.API_ID,
    api_hash=cred.API_HASH,
    bot_token=cred.BOT_TOKEN
)

@app.on_message(filters.command(["start"]))
def start(client, message):
    client.send_message(chat_id=message.chat.id,
                        text=f"`Hi` **{message.from_user.first_name}**\n`Enter the vehicle number to search`",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Help", callback_data="help"),
                                                            InlineKeyboardButton("About", callback_data="about")]]))


@app.on_callback_query()
def data(client, callback_query):
    txt = callback_query.data
    if txt == "help":
        callback_query.message.edit(
            text="**How to use?**\n\nGive me the vehicle number as plain text without(,-,/..etc\nSuppose the vehicle number is KL-18-U-1234 then you need to enter it as kl18u1234 or KL18U1234\n\nWhile sending captcha you must send it as a reply to the given image\n\n__(Nb:vehicleinfobot is not affiliated to any of the government authorities)__",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]]))
    elif txt == "close":
        callback_query.message.delete()
    elif txt == "about":
        callback_query.message.edit(
            text=f"`Bot`            : [vehicleinfobot](t.me/vehicleinfobot)\n`Creator :` [agentnova](t.me/agentnova)\n`Language:` [Python3](https://python.org)\n`Library :` [Pyrogram](https://docs.pyrogram.org/),[Selenium](https://www.selenium.dev/) \n`Server  :` [Heroku](https://herokuapp.com/)",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Give Feedback", url="t.me/agentnova")]]))


@app.on_message(filters.text)
def errr(client, message):
    msg = message.text
    isreply = message.reply_to_message
    chek = check(msg)
    if chek == "invalid" and isreply == None:
        client.send_message(chat_id=message.chat.id, text="Invalid format",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Help", callback_data="help")]]))
    elif chek == "valid" and isreply == None:
        resp = client.send_message(chat_id=message.chat.id, text="Checking...", reply_to_message_id=message.message_id)
        r_num = message.text
        temp = re.compile("([a-zA-Z]+)([0-9]+)([a-zA-Z]+)([0-9]+)")
        res = temp.match(r_num).groups()
        first_p = res[0] + res[1] + res[2]
        print(first_p)
        second_p = res[3]
        print(second_p)
        chrome_options = Options()
        chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        driver = ""
        driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver", options=chrome_options)
        driver.get("https://parivahan.gov.in/rcdlstatus")

        first = driver.find_element_by_xpath("//input[@placeholder='DL10ABC']")
        first.send_keys(first_p)
        second = driver.find_element_by_xpath("//input[@placeholder='1234']")
        second.send_keys(second_p)
        image_main = driver.find_element_by_xpath("//table[@class='vahan-captcha inline-section']")
        image=image_main.find_element_by_tag_name("img")

        location = os.path.join("./CAPCTCHA", str(message.chat.id))
        if not os.path.isdir(location):
            os.makedirs(location)
        get_captcha(driver, image, f"{location}/cap.png")
        resp.delete()
        client.send_photo(chat_id=message.chat.id, photo=f"{location}/cap.png",
                          caption="Type the capcha & reply to this message..", reply_markup=ForceReply())
        if os.path.exists(f"{location}/cap.png"):
            os.remove(f"{location}/cap.png")

    @app.on_message(filters.reply, group=3)
    def ver(client, message):
        message.reply_to_message.delete()
        repl = client.send_message(chat_id=message.chat.id, text="`checking`")
        capcha = message.text
        third = image_main.find_element_by_tag_name("input")
        third.send_keys(capcha)
        third.send_keys(Keys.RETURN)
        try:
            main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form_rcdl:rcPanel")))
            details = main.find_element_by_tag_name("table")
            lst = details.text.split("\n")
            response = sort(lst)
            message.delete()
            repl.delete()
            client.send_photo(chat_id=message.chat.id, photo="final.jpg", caption=f"{response}")
        except:
            message.delete()
            repl.edit("__Reg.no does not exist or wrong captcha entered__")
        finally:
            driver.quit()
        


app.run()
