#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy


class ay7aga(scrapy.Spider):

    link ="https://www.filgoal.com/matches/256575/coverage/%D9%85%D8%A8%D8%A7%D8%B1%D8%A7%D8%A9-%D9%88%D9%84%D9%81%D8%B1%D9%87%D8%A7%D9%85%D8%A8%D8%AA%D9%88%D9%86-%D9%85%D8%A7%D9%86%D8%B4%D8%B3%D8%AA%D8%B1-%D9%8A%D9%88%D9%86%D8%A7%D9%8A%D8%AA%D8%AF-%D9%81%D9%8A-%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D9%8A-%D8%A7%D9%84%D8%A5%D9%86%D8%AC%D9%84%D9%8A%D8%B2%D9%8A/#id=0"
    name = "plan"
    start_urls = [
        link
    ]

    def parse(self, response):
        plan_1 = response.css("#mfm_num div.f::text").extract()  # scraping data
        plan_2 = response.css("#mfm_num div.s::text").extract()  # btkoon 3la form ()-()-()-()
        plan_1 = plan_1[1].replace(' ', '').replace('\r\n', '')  # extracting date from list and removing trash
        plan_2 = plan_2[1].replace(' ', '').replace('\r\n', '')
        tsh_1 = response.css(".mfm_block li div.f a::text").extract()
        tsh_2 = response.css(".mfm_block li div.s a::text").extract()  # قائمة لاعبين كل فريق 18 list
        p_1 = self.tashkeel(plan_1, tsh_1)
        p_2 = self.tashkeel(plan_2, tsh_2)
        print(p_1, p_2)

    def tashkeel(self, plan, tsh):  # الدالة اللى هتعمل التقسيمة من التشكيلة طبقا للخطة
        p = {"goal": tsh[0]}
        x = plan.replace('-', '')  # 4-2-4
        z = int(x[0]) + 1  # 4+1
        back = tsh[1:z]  # 1====>4
        c = int(x[1]) + z  # 2+5=7
        mid = tsh[z:c]  # 5=====>6
        v = int(x[2]) + c  # 4+7=11
        wing = tsh[c:v]  # 7=====>10= 4 players
        dekkah = tsh[v:]
        attack = []

        if len(x) == 4:
            b = int(x[3]) + v
            attack = tsh[v:b]
            dekkah = tsh[b:]
        p['back'] = back
        p['mid-field'] = mid
        p['wing'] = wing
        p['attack'] = attack
        p['dekkah'] = dekkah
        return p