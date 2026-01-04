###############################################################################
#  Monitoring Script
#
# (c) Stuart Miller
#
###############################################################################
from email.mime.text import MIMEText
import logging
import os
import requests
import re
import smtplib
import time


###############################################################################
#  Main
###############################################################################
def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    # Get env vars
    try:
        servers = os.environ["SERVERS"]
        sender_address = os.environ["SENDER_ADDRESS"]
        sender_password = os.environ["SENDER_PASSWORD"]
        recipients = os.environ["RECIPIENTS"]
    except KeyError as error:
        logging.error(f"Environment variable {str(error)} is required")
        exit()
    servers = [x.strip() for x in servers.split(',')]
    recipients = [x.strip() for x in recipients.split(',')]
    interval = float(os.environ.get("INTERVAL", "15"))  # minutes
    max_counter = int(os.environ.get("MAX_COUNTER", "4"))
    # Init
    counter = {}
    notified = {}
    for server in servers:
        counter[server] = 0
        notified[server] = False
    # Loop forever
    while True:
        logging.info("Running checks")
        for server in servers:
            # Check if down
            if not ping_server(server) or not request_server(server):
                counter[server] = counter[server] + 1
                if not notified[server]:
                    logging.error(
                        f"{server} did not respond ({counter[server]}/{max_counter})")
            else:
                if counter[server] > 0:
                    logging.info(f"{server} is back up")
                counter[server] = 0
                notified[server] = False
            # Notify if necessary
            if counter[server] >= max_counter and not notified[server]:
                print(
                    f"Notifying {", ".join(recipients)} that {server} is down")
                subject = f"{server} is down!"
                body = f"This is an automated message. Host {server} is down or unresponsive."
                try:
                    send_email(subject, body, sender_address,
                               recipients, sender_password)
                except:
                    logging.error("Failed to send email")
                else:
                    notified[server] = True
        # Sleep
        time.sleep(interval * 60)


###############################################################################
#  ping_server
###############################################################################
def ping_server(server):
    response = os.system(f"ping -c 1 {server} > /dev/null 2>&1")
    if response != 0:
        logging.debug(f"{server} did not response to ping")
    return response == 0


###############################################################################
#  request_server
###############################################################################
def request_server(server):
    # Correct URL to always use HTTPS
    server_corrected = "https://" + server
    server_corrected = re.sub(
        r"^([A-Za-z0-9]+\:\/{2})+", "https://", server_corrected)
    # Send HTTP request
    try:
        request = requests.get(server_corrected)
    except requests.ConnectionError:
        logging.debug(f"{server} did not respond")
        return False
    if request.status_code != 200:
        logging.debug(f"{server} responded with HTTP {request.status_code}")
        return False
    return True


###############################################################################
#  send_email
###############################################################################
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())


###############################################################################
#  (default)
###############################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
