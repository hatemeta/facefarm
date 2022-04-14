from bs4 import BeautifulSoup
from faker import Faker
import requests


class faceFarm():
    def __init__(self) -> None:
        super(faceFarm, self).__init__()
        self.requests = requests.Session()
        pass

    def request(self, method, url, **kwargs):
        try:
            return self.requests.request(method, url, timeout=(10, 30), **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            return e

    def identifyEmail(self, email):
        url = "https://m.facebook.com/login/identify/"
        page = self.request("GET", url, params={
            "ctx": "recover",
            "c": "/login/",
            "search_attempts": "1",
            "ars": "facebook_login",
            "alternate_search": "0",
            "show_friend_search_filtered_list": "0",
            "birth_month_search": "0",
            "city_search": "0"
        })
        soup = BeautifulSoup(page.text, "html.parser")
        lsd = soup.find("input", {"name": "lsd"})["value"]
        jazoest = soup.find("input", {"name": "jazoest"})["value"]

        page = self.request("POST", url, params={
            "ctx": "recover",
            "c": "/login/",
            "search_attempts": "1",
            "ars": "facebook_login",
            "alternate_search": "0",
            "show_friend_search_filtered_list": "0",
            "birth_month_search": "0",
            "city_search": "0"
        }, data={
            "lsd": lsd,
            "jazoest": jazoest,
            "email": email,
            "did_submit": "Cari"
        })
        soup = BeautifulSoup(page.text, "html.parser")
        login_identify_search_error_msg = soup.find(
            "div", {"id": "login_identify_search_error_msg"})
        if not login_identify_search_error_msg:
            status = soup.find("title").get_text()
            print(
                "[*] Email Address : {}\n[*] Status : {}\n[+] Saved to 'vuln.txt'.\n".format(email, status))
            with open("vuln.txt", "a", encoding="utf-8") as fp:
                fp.write(email + "\n")
        else:
            status = soup.find("title").get_text()
            detail_status = login_identify_search_error_msg.get_text()
            print("[*] Email Address : {}\n[*] Status : {}\n[*] Detail Status : {}\n".format(
                email, status, detail_status))
            pass


if __name__ == "__main__":
    faceFarmASCII = """    __             ___               
  / _|__ _ __ ___| __|_ _ _ _ _ __  
 |  _/ _` / _/ -_) _/ _` | '_| '  \ 
 |_| \__,_\__\___|_|\__,_|_| |_|_|_|
faceFarm - Email Detector for Facebook    
    """
    print(faceFarmASCII)
    faceFarm = faceFarm()
    while True:
        fake = Faker()
        emailAddr = fake.email().split("@")[0] + "@yopmail.com"
        faceFarm.identifyEmail(emailAddr)
