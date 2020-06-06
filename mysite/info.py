import os
# print(path+"dah el e7na 3awzino")
import time


def Run_spdr(name, path):
    time.sleep(1)
    os.chdir(f"{path}/mysite/tutorial")
    os.system(f"scrapy crawl {name}")
    os.chdir(path)


def y_t():
    import time
    path = os.getcwd()
    Run_spdr(name="yesterday", path=path)
    Run_spdr(name="tomorrow", path=path)
    r = time.localtime()
    x = (24 - r.tm_hour - 1)*3600 + (60 - r.tm_min - 1)*60 + (60 - r.tm_sec)
    time.sleep(x)

    while True:
        if time.localtime().tm_mday == r.tm_mday+1:
            for i in range(0, 1):
                Run_spdr("yesterday")
                Run_spdr("tomorrow")
                r = time.localtime()
                time.sleep(86400)
