import os
import time
from datetime import datetime, timedelta
from parser_html import DataExtractor
from parser_html import send_message_list
from data import get_html_file
from cleaner_html import html_cleaner

def run():
    data_extractor = DataExtractor()
    while True:
        now = datetime.now()
        if now.hour == 6 and now.minute == 0:
            html_cleaner()
            get_html_file()
            if not data_extractor.is_file_loaded():
                time.sleep(300)
                continue
            new_future_divs, new_past_divs = data_extractor.compare_files()
            if len(new_future_divs) == 0 and len(new_past_divs) == 0:
                os.remove(data_extractor.latest_file)
            else:
                target_time = (now + timedelta(hours=2)).replace(minute=0, second=0, microsecond=0)
                while datetime.now() < target_time:
                    time.sleep(1)
                if len(new_future_divs) > 0:
                    # get_divs(new_future_divs)
                    send_message_list()
                # if len(new_past_divs) > 0:
                    # get_divs(new_past_divs)
        time.sleep(3600)

if __name__ == '__main__':
    run()
