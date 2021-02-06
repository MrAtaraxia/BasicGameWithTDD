

import os
from datetime import datetime, date
import datetime
import time
now = datetime.datetime.now()
my_time = f"{now.year:04}-{now.month:02}-{now.day:02}_{now.hour:02}-{now.minute:02}-{now.second:02}"

thing1 = " auto comment"
my_commands = f"""
git add --all
git commit -m "{thing1} at {my_time}"

"""

my_location = f"pwd"

os.system(my_commands)
