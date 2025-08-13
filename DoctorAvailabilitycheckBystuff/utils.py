from datetime import datetime, timedelta

def iter_slots(start_time, end_time, minutes):
    dt_start = datetime.combine(datetime.today().date(), start_time)
    dt_end = datetime.combine(datetime.today().date(), end_time)
    while dt_start + timedelta(minutes=minutes) <= dt_end:
        yield (dt_start.time())
        dt_start += timedelta(minutes=minutes)
