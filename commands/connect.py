import config
import database as db

def band_to_city(band, city):
    r = db.add_relationship(band, 'is_from', city)
    return r