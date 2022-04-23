from calendar import month, week
import re
from nwb import db
from sqlalchemy.dialects.postgresql import JSON


class NWBDATA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(100), nullable=False)
    json_nwb = db.Column(JSON)

    def __repr__(self):
        return 'NWB Month of ' + str(self.month)

class POSTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nwb = db.Column(JSON)

    def __repr__(self):
        return 'NWB Month of ' + str(self.nwb)

def add_data(data:dict):
    data1 = NWBDATA(month=str(data['month']), json_nwb=data)
    db.session.add(data1)
    db.session.commit()
    print(data1," done")

def get_data(month_text):
    data = NWBDATA.query.all()
    data_cleaned = []
    for d in data:
        h = re.match("{month_text}".format(month_text=month_text), d.month)
        print(h)
        if h:
            data_cleaned.append(d)
    return data_cleaned