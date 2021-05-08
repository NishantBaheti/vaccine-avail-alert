import argparse
import datetime
import pandas as pd
from src.util.req import request_get
from src.util.dfops import df_to_html
from src.util.mail import send_mail
from dotenv import load_dotenv
import logging
import os
load_dotenv()

logging.basicConfig(
    filename=os.path.join(os.getcwd(),"service.log"),
    filemode="a",
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]:%(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='command line arguments')

    parser.add_argument(
        "--pin-code",
        type=int,
        default=311001
    )
    parser.add_argument(
        "--min-age",
        type=int
    )
    parser.add_argument(
        "--rec-email",
        type=str
    )

    args = parser.parse_args()

    CITY_CODE = args.pin_code
    MIN_AGE = args.min_age
    REC_EMAIL = args.rec_email

    DATE = datetime.datetime.strftime(datetime.datetime.today(), "%d-%m-%Y")
    API_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + \
        str(CITY_CODE)+"&date="+DATE

    REC_LIST = [i.strip() for i in REC_EMAIL.split(",")]

    data = request_get(API_URL)
    if data is not None and "error" not in data:
        list_of_avail_centers = data["sessions"]

        if len(list_of_avail_centers) == 0:
            logger.debug("No Centers available today. SAD")
        else:
            filtered = []
            for center_info in list_of_avail_centers:
                if center_info["min_age_limit"] <= MIN_AGE and center_info["available_capacity"] > 0:
                    filtered.append(center_info)
            if len(filtered) == 0:
                logger.debug("No results for minimum age :"+ str(MIN_AGE) +" SAD")
            else:
                logger.debug(str(len(filtered)) + "Results found")
                try:
                    df = pd.DataFrame(filtered)
                    html_str = df_to_html(df)
                    subject = "ALERT FOR VACCINATION DETAIL :" + DATE

                    for rec in REC_LIST:
                        try:
                            send_mail(subject=subject, body=html_str,
                                body_type="html", to_user=rec)
                            logger.info("MAIL SENT SUCCESSFULLY TO "+ str(rec))
                        except Exception as e:
                            logger.error(str(e))
                except Exception as e:
                    logger.error(str(e))
    else:
        logger.debug("None received from URL.")
