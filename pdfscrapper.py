import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/2022/18").content, "html5lib")

WeekItems = soup.find("div", {"class":"todayItems"})

SectionX0 = WeekItems.select(".itemData #p1")
SectionX4 = WeekItems.select(".bodyTxt #section4")

print()