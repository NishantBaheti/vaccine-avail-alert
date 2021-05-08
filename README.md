# vaccine-avail-alert

- create a .env file with two things 
    
    SENDER_EMAIL=<your_email>
    SENDER_PASSWD=<password>

- run it as a cron job or a triggered service in you system 
- params are 

        python main.py --pin-code 311001 --min-age 45 --rec-email email_id_1,email_id_2
                            
                            CITY PIN CODE     MIN AGE             COMMA SEP EMAIL ID's

