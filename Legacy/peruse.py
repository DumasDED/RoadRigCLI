import config
import facebook


def events(handle):
    event_list = facebook.get_attr(handle, 'events', fields=config.app_fields_events)
    print "%i events found for %s:" % (len(event_list), handle)
    for event in event_list[:24]:
        print event['name']
