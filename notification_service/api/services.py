from datetime import datetime


def get_time_start_currect_finish(mailing):
    time_start = mailing.date_time_start
    time_now = datetime.now()
    time_finish = mailing.date_time_finish

    return time_start, time_now, time_finish
