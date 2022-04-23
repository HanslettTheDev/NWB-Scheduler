import json, asyncio

from nwb.scrapper import JWIZARD

class UTILS:
    def scrap_data(self,end_point,start_point=1):
        weeklist=[i for i in range(start_point, end_point)]
        basepath="https://wol.jw.org/wes-x-pgw/wol/meetings/r429/lp-pgw/2022/{num}"
        jwizard = JWIZARD(basepath=basepath,weeklist=weeklist)
        asyncio.run(jwizard.main())
        return "done"

    def update_time(self, preaching_time, middle_time):
        default_time = 2
        default_middle_time = 21
        pt_time = []
        mt_time = []
        for p in preaching_time:
            h = int(p)
            default_time += h
            print(default_time)
            pt_time.append(default_time)
        for m in middle_time:
            h = int(m)
            default_middle_time += h
            mt_time.append(default_middle_time) 
        return pt_time,mt_time
    
    def get_json_data(self, dict_id:str):
        with open('meeting.json') as f:
            data = json.load(f)
        items = [d for d in data[dict_id]]
        return items