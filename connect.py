import database
import error


def band_to_band(band1, band2):
    print "Adding relationship between %s and %s..." % (band1, band2)
    try:
        band1 = database.get_node('band', band1)
        band2 = database.get_node('band', band2)

        database.add_relationship(band1, 'knows', band2)
    except error.types as e:
        error.handle(e)
    else:
        print "Bands connected successfully."
