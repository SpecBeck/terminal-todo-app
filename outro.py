import time

from rich.live import Live
from rich.panel import Panel

script = ["Thanks to the CS50P team", "For this awesome course and",
          "This was specbeck", "Goodbye :)"]

for line in script:
    with Live(Panel.fit(line), refresh_per_second=4):  # update 4 times a second to feel fluid
        time.sleep(2)  # arbitrary delay
