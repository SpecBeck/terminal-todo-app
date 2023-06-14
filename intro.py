import time

from rich.live import Live
from rich.panel import Panel

script = ["hello, world!", "This is Saransh Sood", "Also known as specbeck :)",
          "From New Delhi, India", "And I present to you my final project", "Terminal TODO list application!"]

for line in script:
    with Live(Panel.fit(line), refresh_per_second=4):  # update 4 times a second to feel fluid
        time.sleep(1)  # arbitrary delay
