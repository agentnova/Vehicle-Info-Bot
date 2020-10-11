from PIL import Image
from re import *

def get_captcha(driver, element, path):
    location = element.location
    size = element.size
    driver.save_screenshot(path)
    image = Image.open(path)
    left = location['x'] + 1  # fromleft
    top = location['y'] + 1  # fromtop
    right = location['x'] + size['width'] + 1  # toright
    bottom = location['y'] + size['height'] + 1  # tobottom
    image = image.crop((left, top, right, bottom))
    image.save(path, 'png')

def sort(lst):
    dict={}
    dict["Registration number"]=lst[0].split(":")[1].replace("Registration Date","")
    dict["Registration Date"]=lst[0].split(":")[2]
    dict["Chasis number"]=lst[1].split(":")[1].replace("Engine No","")
    dict["Engine number"]=lst[1].split(":")[2]
    dict["Owner name"]=lst[2].split(":")[1]
    dict["Vehicle class"]=lst[3].split(":")[1].replace("Fuel Type","")
    dict["Fuel type"]=lst[3].split(":")[2]
    dict["Model"]=lst[4].split(":")[1]
    dict["Fitness upto"]=lst[5].split(":")[1].replace("Insurance Upto","")
    dict["Insurance upto"]=lst[5].split(":")[2]
    dict["Tax paid upto"]=lst[6].split(":")[2]
    respns = f"Owner name : `{dict['Owner name']}`\nRegistration number : `{dict['Registration number']}`\nRegistration date : `{dict['Registration Date']}`\nModel : `{dict['Model']}`\nVehicle class : `{dict['Vehicle class']}`\nChasis number : `{dict['Chasis number']}`\nEngine number : `{dict['Engine number']}`\nFuel type : `{dict['Fuel type']}`\nFitnes upto: `{dict['Fitness upto']}`\nInsurence upto : `{dict['Insurance upto']}`\nTax paid upto : `{dict['Tax paid upto']}`"
    return respns


def check(num):
    rule = '[a-zA-Z][a-zA-Z][0-9]{2}[a-zA-Z]*\d*'
    regno = num
    matcher = fullmatch(rule, regno)
    if not matcher == None:
        return "valid"
    else:
        return "invalid"
