import os
import time
import threading
import urllib.request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ping_app(url, interval_seconds):
    """Pings the given URL at regular intervals."""
    while True:
        try:
            time.sleep(interval_seconds)
            logger.info(f"Pinging {url} to keep alive...")
            req = urllib.request.Request(url, headers={'User-Agent': 'KeepAlive-Bot'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    logger.info("Ping successful.")
                else:
                    logger.warning(f"Ping returned status code: {response.getcode()}")
        except Exception as e:
            logger.error(f"Ping failed: {e}")

def start_keep_alive():
    """Starts the background keep-alive thread if on Render or configured."""
    # Render provides RENDER_EXTERNAL_URL automatically.
    # Alternatively, you can set APP_URL manually.
    app_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("APP_URL")
    
    if not app_url:
        logger.info("No RENDER_EXTERNAL_URL or APP_URL found. Keep-alive thread not started.")
        return

    # Interval: 5 minutes (300 seconds). Render sleeps after 15 mins of inactivity.
    interval = 300 
    
    # Check if thread is already running (Streamlit sometimes re-runs scripts)
    for thread in threading.enumerate():
        if thread.name == "KeepAliveThread":
            return # Already running

    logger.info(f"Starting keep-alive thread for URL: {app_url} every {interval}s")
    thread = threading.Thread(target=ping_app, args=(app_url, interval), name="KeepAliveThread", daemon=True)
    thread.start()
