import platform
import time
import webbrowser
from datetime import datetime
import exceptions
import re
import pyautogui
from urllib.parse import quote


WIDTH, HEIGHT = pyautogui.size()


def close_tab(wait_time: int = 2) -> None:
    time.sleep(wait_time)
    _system = platform.system().lower()
    if _system in ("windows", "linux"):
        pyautogui.hotkey("ctrl", "w")
    elif _system == "darwin":
        pyautogui.hotkey("command", "w")
    else:
        raise Warning(f"{_system} not supported!")
    pyautogui.press("enter")


def clickTextBox() -> None:
    location = pyautogui.locateOnScreen(f"./smile1.png")
    try:
        try:
            pyautogui.moveTo(location[0] + 150, location[1] + 5)
        except Exception as e:
            if str(e) == "NoneType' object is not subscriptable":
                raise exceptions.WhatsAppNotFoundException(
                    "Seems the WhatsApp Web Window was closed or moved to another Tab!"
                )
        pyautogui.click()
    except Exception:
        location = pyautogui.locateOnScreen(f"./smile.png")
        try:
            pyautogui.moveTo(location[0] + 150, location[1] + 5)
        except Exception as e:
            if str(e) == "NoneType' object is not subscriptable":
                raise exceptions.WhatsAppNotFoundException(
                    "Seems the WhatsApp Web Window was closed or moved to another Tab!"
                )
        pyautogui.click()


def check_number(number: str) -> bool:
    return "+" in number or "_" in number


def _web(receiver: str, message: str) -> None:
    if check_number(number=receiver):
        webbrowser.open(
            "https://web.whatsapp.com/send?phone="
            + receiver
            + "&text="
            + quote(message)
        )
    else:
        webbrowser.open("https://web.whatsapp.com/accept?code=" + receiver)


def send_message(message: str, receiver: str, wait_time: int) -> None:
    _web(receiver=receiver, message=message)
    time.sleep(7)
    pyautogui.click(WIDTH / 2, HEIGHT / 2 + 15)
    time.sleep(wait_time - 7)
    if not check_number(number=receiver):
        for char in message:
            if char == "\n":
                pyautogui.hotkey("shift", "enter")
            else:
                pyautogui.typewrite(char)
    clickTextBox()
    pyautogui.press("enter")


def sendwhatmsg(
        phone_no: str,
        message: str,
        time_hour: int = None,
        time_min: int = None,
        time_sec: int = 0,
        wait_time: int = 15,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    if not check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not re.fullmatch(r'^\+?[0-9]{2,4}\s?[0-9]{9,15}', phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    if time_hour == None and time_min == None:
        webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
        time.sleep(4)
        pyautogui.click(WIDTH / 2, HEIGHT / 2 + 15)
        time.sleep(wait_time - 4)
        clickTextBox()
        pyautogui.press("enter")
        if tab_close:
            close_tab(wait_time=close_time)
        return

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:{time_sec}", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    if wait_time < 7:
        raise exceptions.WaitTimeException(
            "Wait Time must be Greater than 7 Seconds!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!{' The window will be closed in {wait_time} after Message Delivery!' if tab_close else ''}"
    )
    time.sleep(sleep_time)
    send_message(message=message, receiver=phone_no, wait_time=wait_time)
    if tab_close:
        close_tab(wait_time=close_time)


phone = input("Enter the Recipient Number (include the country code). Ex. +8801*********\n>>> ")
message = input("Enter the message\n>>> ")
isInstant = input("Do you want to send the message instantly? Options: Yes/No\n>>> ")
if isInstant.lower() not in ['yes', 'no']:
    raise exceptions.UserInputException(
        "Invalid Choice! Answer must be \"Yes\" or \"No\"."
    )
if isInstant.lower() == "no":
    desired_time = input("Enter the desired time in 24 Hours. Format: HH:MM:SS (Seconds are Optional)\n>>> ")
    try:
        hour, minute, *second= desired_time.split(":", 2)
    except:
        raise exceptions.UserInputException(
            "Unable to identify Hour, Minute and Second! Please use the format: HH:MM:SS (Seconds are Optional)"
        )
    hour = int(hour) if not str(hour).startswith("0") else int(str(hour).replace("0", "", 1))
    minute = int(minute) if not str(minute).startswith("0") else int(str(minute).replace("0", "", 1))
    if second != []:
        second = second[0]
        second = int(second) if not str(second).startswith("0") else int(str(second).replace("0", "", 1))
        sendwhatmsg(phone_no=phone, message=message, time_hour=hour, time_min=minute, time_sec=second, tab_close=True, close_time=5)
    else:
        sendwhatmsg(phone_no=phone, message=message, time_hour=hour, time_min=minute, tab_close=True, close_time=5)
else:
    sendwhatmsg(phone_no=phone, message=message, tab_close=True, close_time=5)
