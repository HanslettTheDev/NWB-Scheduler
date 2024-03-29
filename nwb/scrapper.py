import json, asyncio, aiohttp, re
from nwb.models import add_data
from bs4 import BeautifulSoup

class JWIZARD:
  def __init__(self, basepath = "", weeklist=[]):
        self.basepath = basepath
        self.weeklist = weeklist
        self.pathdict = {}
        
  def get_all_urls(self):
    weeklist = self.weeklist
    for week in weeklist:
        self.pathdict[week] = self.basepath.format(num=str(week))
    return self.pathdict
          
  async def fetch_data(self,session, url):
      try:
          async with session.get(url) as response:
              print("fetching ", url)
              return await response.text()
      except Exception as error:
          print(error)
  def scrap_data(self, html):
    soup = BeautifulSoup(html, "html5lib") # If this line causes an error, run 'pip install html5lib' or install html5lib
    #soup.prettify()

    WeekItems = soup.find("div", {"class":"todayItems"})
    WeekRange = WeekItems.select(".cardTitleBlock .cardLine1 span")[0].next_sibling.strip()#[0].find("div", class_="cardLine1").select("span").next_sibling
    ###sections
    SectionX0 = WeekItems.select(".itemData #p1")
    SectionX1 = WeekItems.select(".bodyTxt #section1")
    SectionX2 = WeekItems.select(".bodyTxt #section2")
    SectionX3 = WeekItems.select(".bodyTxt #section3")
    SectionX4 = WeekItems.select(".bodyTxt #section4")
    
    SectionX5 = WeekItems.select(".itemData #p2")


    ###section1
    nwb_date = SectionX0[0].select("strong")[0].text
    reading = SectionX5[0].select("strong")[0].text

    
    OpenxSong = SectionX1[0].select("ul li strong")[0].text #last [0] removes wetin we go learn
    
    ###section2
    MessageHd = SectionX2[0].select(".pGroup ul li a")[0].text.strip() #add pa a after li to eliminate time
  
    BibleRdxs = SectionX2[0].select(".pGroup ul li .b")[-1].text.strip() #can be fine tuned to get only verse
    bible_reading_point = SectionX2[0].select(".pGroup ul li a")[-1].text.strip() 
    



    ###section3
    TypeOfItm = SectionX3[0].select(".pGroup ul li p strong") #to be passed item separetor
    # # print(TypeOfItm)
    nwb_parts = []
    for t in TypeOfItm:
      nwb_parts.append(t.text)
    # clean the data
    for l in nwb_parts:
      h = re.match(":", l)
      if ('“' in l) or ('”:' in l):
        nwb_parts.remove(l)
      if h:
        nwb_parts.remove(h.group(0))
    
    
      
    # get parts study point
    dump = []
    nwb_parts_point = []
    TypeOfItm = SectionX3[0].select(".pGroup ul li")
    for t in TypeOfItm:
      dump.append(t.text)
    
    for d in dump:
      h = re.search(r'(?<=study\D)\d+', d)
      if h:
        nwb_parts_point.append(h.group(0))
      else:
        nwb_parts_point.append("")
    



    # get parts time
    dump = []
    nwb_parts_time = []
    TypeOfItm = SectionX3[0].select(".pGroup ul li p")
    for t in TypeOfItm:
      dump.append(t.text)
    
    for d in dump:
      h = re.search(r'(?<=\()\d+', d)
      if h:
        nwb_parts_time.append(h.group(0))
      else:
        nwb_parts_point.append("")

    
    ###section4
    ChristLif = SectionX4[0].select(".pGroup ul li strong")
    nwb_lac = []
    middle_song = ChristLif[0].text
  

    for cl in ChristLif:
      nwb_lac.append(cl.text)

    for l in nwb_lac:
      if '“' in l or '”:' in l:
        nwb_lac.remove(l)
    # nwb_lac.pop()
    nwb_lac.pop(0)
    nwb_lac=nwb_lac[:-3]
    for n in nwb_lac:
      if "Congregation Bible Study:" in n:
        nwb_lac.remove(n)

    # get live as christian time
    dummy = []
    nwb_lac_time = []
    times = SectionX4[0].select(".pGroup ul li p")
    for t in times:
      dummy.append(t.text)
    
    for d in dummy:
      h = re.search(r'(?<=\()\d+', d)
      if h:
        nwb_lac_time.append(h.group(0))
      else:
        nwb_parts_point.append("")
    nwb_lac_time.pop()
    nwb_lac_time.pop()

    if nwb_lac == [] or len(nwb_lac_time) != len(nwb_lac):
      extra = SectionX4[0].select(".pGroup ul li em")
      print(extra)


    book_study = SectionX4[0].select(".pGroup ul li p a")[-2].text
    concluding_song = SectionX4[0].select(".pGroup ul li strong")[-2].text

    nwb = {
      'month': nwb_date,
      'reading': reading,
      'opening_song': OpenxSong,
      'fine_fine_lesson': MessageHd,
      'bible_reading': BibleRdxs,
      'bible_reading_point': bible_reading_point,
      'preaching': nwb_parts,
      'preaching_points': nwb_parts_point,
      'preaching_time': nwb_parts_time,
      'middle_song': middle_song,
      'middle_parts': nwb_lac,
      'middle_parts_time': nwb_lac_time,
      'book_study': book_study,
      'book_study_box': "", 
      'concluding_song': concluding_song,
    }
    add_data(nwb)
    with open("meeting.json", "w") as f:
      json.dump(nwb, f, indent=4)


  async def main(self):
    async with aiohttp.ClientSession() as session:
        tasklist = []
        
        for _ , url in self.get_all_urls().items():
            tasklist.append(self.fetch_data(session, url))
            
        htmls = await asyncio.gather(*tasklist)

        for html in htmls:
            self.scrap_data(html)

# weeklist=[x for x in range(1, 20)]
# basepath="https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/2022/{num}"
# jwizard = JWIZARD(basepath=basepath,weeklist=weeklist)
# asyncio.run(jwizard.main())