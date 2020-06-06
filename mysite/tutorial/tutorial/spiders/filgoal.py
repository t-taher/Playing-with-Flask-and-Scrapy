# import sys
import scrapy
import time
from ..items import TutorialItem


def date():
    # getting link to scrape
    date = time.localtime()
    yr = date[0]
    mon = date[1]
    dy = date[2] - 0
    link = "https://www.filgoal.com/matches/?date={0}-{1}-{2}".format(yr, mon, dy)
    return link


lnk = date()
# done

# start using scrapy


class filgolspider(scrapy.Spider):

    name = "filgoal"
    start_urls = [
        lnk
    ]

    def parse(self, response):
        global tme, std, channel
        items = TutorialItem()

        all_blocks = response.css("div.mc-block div.mc-block")
        m = ""
        for block in all_blocks:
            league = block.css("h1 span::text").extract()
            all_mtches = block.css("div.cin_cntnr")
            for match in all_mtches:
                team_1 = match.css("div.f strong::text").extract()
                team_2 = match.css("div.s strong::text").extract()
                info = match.css("span::text").extract()
                rslt_1 = match.css("div.f b::text").extract()
                rslt_2 = match.css("div.s b::text").extract()
                rslt = [rslt_1[0], rslt_2[0]]
                # print(team_2,team_1)
                del info[1]
                n = len(info)
                if n == 4:
                    std = info[1]
                    channel = info[2]
                    tme = info[3]

                elif n == 3:
                    std = info[1]
                    channel = ""
                    tme = info[2]

                elif n == 2:
                    std = ""
                    channel = ""
                    tme = info[1]
                elif n == 5:
                    std = info[1]
                    channel = info[2], info[3]
                    tme = info[4]

                items['league'] = league
                items['team_1'] = team_1
                items['team_2'] = team_2
                items['state'] = info[0]
                items['channel'] = channel
                items['tme'] = tme
                items['std'] = std.replace('  ', '')  # removing extra spaces
                items['rslt'] = rslt
                yield items
                m += str(items)
        m = m.replace("}{", "},{")
        g = open("info.txt", "w")
        g.write(m)
        g.close()

