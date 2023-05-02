import os
from natsort import os_sorted

#The directory sorted like your file browser might show
somelist = os_sorted(os.listdir())

approved = ['.xlsx']

somelist[:] = [url for url in somelist if any(sub in url for sub in approved)]

print(somelist)
