#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Translations authorship:
# Arabic (ar): User:SR5
# Bengali (bn): User:Aftabuzzaman
# Catalan (ca): User:Emijrp
# French (fr): User:Pamputt
# Galician (gl): User:Emijrp
# Hebrew (he): User:Mikey641
# Romanian (ro): User:XXN
# Spanish (es): User:Emijrp
# Albanian (sq): User:Liridon
# Thanks everybody for your help!

import os
import re
import sys
import time
import urllib.parse

import pwb
import pywikibot
from wikidatafun import *

#ideas: fix politico/musico, etc for females

def main():
    #isScriptAlive(__file__) #using jstart continuous grid job
    #https://wikitech.wikimedia.org/wiki/Help:Tool_Labs/Grid#Submitting_continuous_jobs_.28such_as_bots.29_with_.27jstart.27
    #jstart -N humandesc -mem 1G /usr/bin/python3 /data/project/.../human.descriptions.py
    
    targetlangs = ['es', 'ca', 'gl', 'he', 'ar', 'fr', 'bn', 'ro', 'sq']
    site = pywikibot.Site('wikidata', 'wikidata')
    repo = site.data_repository()
    
    genders = {
        'Q6581097': 'male', 
        'Q6581072': 'female', 
    }
    genders_list = [[x, y] for x, y in genders.items()]
    genders_list.sort()
    
    #ca: https://ca.wikipedia.org/wiki/Llista_de_gentilicis#Llista_de_gentilicis_per_estat
    #en: https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations
    #es: https://es.wikipedia.org/wiki/Anexo:Gentilicios
    #fr: https://fr.wikipedia.org/wiki/Liste_de_gentil%C3%A9s
    #gl: https://web.archive.org/web/20060512203621/http://www.galegoenlinna.uvigo.es/fichasVer.asp?idFicha=132
    translationsNationalities = {
        'river': {
            'bn': { 'male': 'নদী', 'female': 'নদী' },
        },
    }
    #more occupations https://query.wikidata.org/#SELECT%20%3Foccupation%20%3FoccupationLabel%20%28COUNT%28%3Fitem%29%20AS%20%3Fcount%29%0AWHERE%20%7B%0A%09%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%20%20%3Fitem%20wdt%3AP27%20wd%3AQ142.%0A%20%20%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20.%20%7D%0A%7D%0AGROUP%20by%20%3Foccupation%20%3FoccupationLabel%0AORDER%20BY%20DESC%28%3Fcount%29
    #translations https://query.wikidata.org/#SELECT%20%3FitemDescription%20%28COUNT%28%3Fitem%29%20AS%20%3Fcount%29%0AWHERE%20%7B%0A%09%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%20%20%3Fitem%20wdt%3AP106%20wd%3AQ28389.%0A%20%20%20%20OPTIONAL%20%7B%20%3Fitem%20schema%3Adescription%20%3FitemDescription.%20FILTER%28LANG%28%3FitemDescription%29%20%3D%20%22gl%22%29.%20%20%7D%0A%09FILTER%20%28BOUND%28%3FitemDescription%29%29%0A%7D%0AGROUP%20BY%20%3FitemDescription%0AORDER%20BY%20DESC%28%3Fcount%29
    #https://query.wikidata.org/#SELECT%20%3FitemDescription%20%28COUNT%28%3Fitem%29%20AS%20%3Fcount%29%0AWHERE%0A%7B%0A%09%3Fitem%20wdt%3AP31%20wd%3AQ5%20.%0A%20%20%20%20%3Fitem%20wdt%3AP27%20wd%3AQ142%20.%0A%09OPTIONAL%20%7B%20%3Fitem%20schema%3Adescription%20%3FitemDescription.%20FILTER%28LANG%28%3FitemDescription%29%20%3D%20%22en%22%29.%20%20%7D%0A%09FILTER%20%28BOUND%28%3FitemDescription%29%29%0A%7D%0AGROUP%20BY%20%3FitemDescription%0AORDER%20BY%20DESC%28%3Fcount%29
    translationsOccupations = {
'~ in Afghanistan': {
         'bn': { 'male': 'আফগানিস্তানের ~', 'female': 'আফগানিস্তানের ~' },
},
'~ in Albania': {
         'bn': { 'male': 'আলবেনিয়ার ~', 'female': 'আলবেনিয়ার ~' },
},
'~ in Algeria': {
         'bn': { 'male': 'আলজেরিয়ার ~', 'female': 'আলজেরিয়ার ~' },
},
'~ in Andorra': {
         'bn': { 'male': 'অ্যান্ডোরার ~', 'female': 'অ্যান্ডোরার ~' },
},
'~ in Angola': {
         'bn': { 'male': 'অ্যাঙ্গোলার ~', 'female': 'অ্যাঙ্গোলার ~' },
},
'~ in Antigua and Barbuda': {
         'bn': { 'male': 'অ্যান্টিগুয়া ও বার্বুডার ~', 'female': 'অ্যান্টিগুয়া ও বার্বুডার ~' },
},
'~ in Argentina': {
         'bn': { 'male': 'আর্জেন্টিনার ~', 'female': 'আর্জেন্টিনার ~' },
},
'~ in Armenia': {
         'bn': { 'male': 'আর্মেনিয়ার ~', 'female': 'আর্মেনিয়ার ~' },
},
'~ in Australia': {
         'bn': { 'male': 'অস্ট্রেলিয়ার ~', 'female': 'অস্ট্রেলিয়ার ~' },
},
'~ in Austria': {
         'bn': { 'male': 'অস্ট্রিয়ার ~', 'female': 'অস্ট্রিয়ার ~' },
},
'~ in Azerbaijan': {
         'bn': { 'male': 'আজারবাইজানের ~', 'female': 'আজারবাইজানের ~' },
},
'~ in Bahamas': {
         'bn': { 'male': 'বাহামা দ্বীপপুঞ্জের ~', 'female': 'বাহামা দ্বীপপুঞ্জের ~' },
},
'~ in Bahrain': {
         'bn': { 'male': 'বাহরাইনের ~', 'female': 'বাহরাইনের ~' },
},
'~ in Bangladesh': {
         'bn': { 'male': 'বাংলাদেশের ~', 'female': 'বাংলাদেশের ~' },
},
'~ in Barbados': {
         'bn': { 'male': 'বার্বাডোসের ~', 'female': 'বার্বাডোসের ~' },
},
'~ in Belarus': {
         'bn': { 'male': 'বেলারুশের ~', 'female': 'বেলারুশের ~' },
},
'~ in Belgium': {
         'bn': { 'male': 'বেলজিয়ামের ~', 'female': 'বেলজিয়ামের ~' },
},
'~ in Belize': {
         'bn': { 'male': 'বেলিজের ~', 'female': 'বেলিজের ~' },
},
'~ in Benin': {
         'bn': { 'male': 'বেনিনের ~', 'female': 'বেনিনের ~' },
},
'~ in Bermuda': {
         'bn': { 'male': 'বারমুডার ~', 'female': 'বারমুডার ~' },
},
'~ in Bhutan': {
         'bn': { 'male': 'ভূটানের ~', 'female': 'ভূটানের ~' },
},
'~ in Bolivia': {
         'bn': { 'male': 'বলিভিয়ার ~', 'female': 'বলিভিয়ার ~' },
},
'~ in Bosnia and Herzegovina': {
         'bn': { 'male': 'বসনিয়া ও হার্জেগোভিনার ~', 'female': 'বসনিয়া ও হার্জেগোভিনার ~' },
},
'~ in Botswana': {
         'bn': { 'male': 'বতসোয়ানার ~', 'female': 'বতসোয়ানার ~' },
},
'~ in Brazil': {
         'bn': { 'male': 'ব্রাজিলের ~', 'female': 'ব্রাজিলের ~' },
},
'~ in Brunei': {
         'bn': { 'male': 'ব্রুনাইয়ের ~', 'female': 'ব্রুনাইয়ের ~' },
},
'~ in Bulgaria': {
         'bn': { 'male': 'বুলগেরিয়ার ~', 'female': 'বুলগেরিয়ার ~' },
},
'~ in Burkina Faso': {
         'bn': { 'male': 'বুর্কিনা ফাসোর ~', 'female': 'বুর্কিনা ফাসোর ~' },
},
'~ in Myanmar': {
         'bn': { 'male': 'মায়ানমারের ~', 'female': 'মায়ানমারের ~' },
},
'~ in Burundi': {
         'bn': { 'male': 'বুরুন্ডির ~', 'female': 'বুরুন্ডির ~' },
},
'~ in Cambodia': {
         'bn': { 'male': 'কম্বোডিয়ার ~', 'female': 'কম্বোডিয়ার ~' },
},
'~ in Cameroon': {
         'bn': { 'male': 'ক্যামেরুনের ~', 'female': 'ক্যামেরুনের ~' },
},
'~ in Canada': {
         'bn': { 'male': 'কানাডার ~', 'female': 'কানাডার ~' },
},
'~ in Cape Verde': {
         'bn': { 'male': 'কাবু ভের্দির ~', 'female': 'কাবু ভের্দির ~' },
},
'~ in Central African Republic': {
         'bn': { 'male': 'মধ্য আফ্রিকান প্রজাতন্ত্রের ~', 'female': 'মধ্য আফ্রিকান প্রজাতন্ত্রের ~' },
},
'~ in Chad': {
         'bn': { 'male': 'চাদের ~', 'female': 'চাদের ~' },
},
'~ in Chile': {
         'bn': { 'male': 'চিলির ~', 'female': 'চিলির ~' },
},
'~ in China': {
         'bn': { 'male': 'চীনের ~', 'female': 'চীনের ~' },
},
'~ in Colombia': {
         'bn': { 'male': 'কলম্বিয়ার ~', 'female': 'কলম্বিয়ার ~' },
},
'~ in Comoros': {
         'bn': { 'male': 'কোমোরোসের ~', 'female': 'কোমোরোসের ~' },
},
'~ in Congo': {
         'bn': { 'male': 'কঙ্গোর ~', 'female': 'কঙ্গোর ~' },
},
'~ in Costa Rica': {
         'bn': { 'male': 'কোস্টা রিকার ~', 'female': 'কোস্টা রিকার ~' },
},
'~ in Croatia': {
         'bn': { 'male': 'ক্রোয়েশিয়ার ~', 'female': 'ক্রোয়েশিয়ার ~' },
},
'~ in Cuba': {
         'bn': { 'male': 'কিউবার ~', 'female': 'কিউবার ~' },
},
'~ in Cyprus': {
         'bn': { 'male': 'সাইপ্রাসের ~', 'female': 'সাইপ্রাসের ~' },
},
'~ in Czech Republic': {
         'bn': { 'male': 'চেক প্রজাতন্ত্রের ~', 'female': 'চেক প্রজাতন্ত্রের ~' },
},
'~ in Denmark': {
         'bn': { 'male': 'ডেনমার্কের ~', 'female': 'ডেনমার্কের ~' },
},
'~ in Djibouti': {
         'bn': { 'male': 'জিবুতির ~', 'female': 'জিবুতির ~' },
},
'~ in Dominican Republic': {
         'bn': { 'male': 'ডোমিনিকান প্রজাতন্ত্রের ~', 'female': 'ডোমিনিকান প্রজাতন্ত্রের ~' },
},
'~ in Dominica': {
         'bn': { 'male': 'ডোমিনিকার ~', 'female': 'ডোমিনিকার ~' },
},
'~ in Ecuador': {
         'bn': { 'male': 'ইকুয়েডরের ~', 'female': 'ইকুয়েডরের ~' },
},
'~ in Egypt': {
         'bn': { 'male': 'মিশরের ~', 'female': 'মিশরের ~' },
},
'~ in El Salvador': {
         'bn': { 'male': 'এল সালভাদোরের ~', 'female': 'এল সালভাদোরের ~' },
},
'~ in Equatorial Guinea': {
         'bn': { 'male': 'বিষুবীয় গিনির ~', 'female': 'বিষুবীয় গিনির ~' },
},
'~ in Eritrea': {
         'bn': { 'male': 'ইরিত্রিয়ার ~', 'female': 'ইরিত্রিয়ার ~' },
},
'~ in Estonia': {
         'bn': { 'male': 'এস্তোনিয়ার ~', 'female': 'এস্তোনিয়ার ~' },
},
'~ in Ethiopia': {
         'bn': { 'male': 'ইথিওপিয়ার ~', 'female': 'ইথিওপিয়ার ~' },
},
'~ in Fiji': {
         'bn': { 'male': 'ফিজির ~', 'female': 'ফিজির ~' },
},
'~ in Finland': {
         'bn': { 'male': 'ফিনল্যান্ডের ~', 'female': 'ফিনল্যান্ডের ~' },
},
'~ in France': {
         'bn': { 'male': 'ফ্রান্সের ~', 'female': 'ফ্রান্সের ~' },
},
'~ in French Guiana': {
         'bn': { 'male': 'ফরাসি গায়ানার ~', 'female': 'ফরাসি গায়ানার ~' },
},
'~ in Gabon': {
         'bn': { 'male': 'গ্যাবনের ~', 'female': 'গ্যাবনের ~' },
},
'~ in Gambia': {
         'bn': { 'male': 'গাম্বিয়ার ~', 'female': 'গাম্বিয়ার ~' },
},
'~ in Georgia': {
         'bn': { 'male': 'জর্জিয়া ~', 'female': 'জর্জিয়া ~' },
},
'~ in Germany': {
         'bn': { 'male': 'জার্মানির ~', 'female': 'জার্মানির ~' },
},
'~ in Ghana': {
         'bn': { 'male': 'ঘানার ~', 'female': 'ঘানার ~' },
},
'~ in Great Britain': {
         'bn': { 'male': 'গ্রেট ব্রিটেনের ~', 'female': 'গ্রেট ব্রিটেনের ~' },
},
'~ in Greece': {
         'bn': { 'male': 'গ্রিসের ~', 'female': 'গ্রিসের ~' },
},
'~ in Grenada': {
         'bn': { 'male': 'গ্রেনাডার ~', 'female': 'গ্রেনাডার ~' },
},
'~ in Guadeloupe': {
         'bn': { 'male': 'গুয়াদলুপের ~', 'female': 'গুয়াদলুপের ~' },
},
'~ in Guatemala': {
         'bn': { 'male': 'গুয়াতেমালার ~', 'female': 'গুয়াতেমালার ~' },
},
'~ in Guinea': {
         'bn': { 'male': 'গিনির ~', 'female': 'গিনির ~' },
},
'~ in Guinea-Bissau': {
         'bn': { 'male': 'গিনি-বিসাউয়ের ~', 'female': 'গিনি-বিসাউয়ের ~' },
},
'~ in Guyana': {
         'bn': { 'male': 'গায়ানার ~', 'female': 'গায়ানার ~' },
},
'~ in Haiti': {
         'bn': { 'male': 'হাইতির ~', 'female': 'হাইতির ~' },
},
'~ in Honduras': {
         'bn': { 'male': 'হন্ডুরাসের ~', 'female': 'হন্ডুরাসের ~' },
},
'~ in Hungary': {
         'bn': { 'male': 'হাঙ্গেরির ~', 'female': 'হাঙ্গেরির ~' },
},
'~ in Iceland': {
         'bn': { 'male': 'আইসল্যান্ডের ~', 'female': 'আইসল্যান্ডের ~' },
},
'~ in India': {
         'bn': { 'male': 'ভারতের ~', 'female': 'ভারতের ~' },
},
'~ in Indonesia': {
         'bn': { 'male': 'ইন্দোনেশিয়ার ~', 'female': 'ইন্দোনেশিয়ার ~' },
},
'~ in Iran': {
         'bn': { 'male': 'ইরানের ~', 'female': 'ইরানের ~' },
},
'~ in Iraq': {
         'bn': { 'male': 'ইরাকের ~', 'female': 'ইরাকের ~' },
},
'~ in Ireland': {
         'bn': { 'male': 'আয়ারল্যান্ডের ~', 'female': 'আয়ারল্যান্ডের ~' },
},
'~ in Israel': {
         'bn': { 'male': 'ইসরায়েলের ~', 'female': 'ইসরায়েলের ~' },
},
'~ in Italy': {
         'bn': { 'male': 'ইতালির ~', 'female': 'ইতালির ~' },
},
'~ in Ivory Coast': {
         'bn': { 'male': 'কোত দিভোয়ারের ~', 'female': 'কোত দিভোয়ারের ~' },
},
'~ in Jamaica': {
         'bn': { 'male': 'জ্যামাইকার ~', 'female': 'জ্যামাইকার ~' },
},
'~ in Japan': {
         'bn': { 'male': 'জাপানের ~', 'female': 'জাপানের ~' },
},
'~ in Jordan': {
         'bn': { 'male': 'জর্দানের ~', 'female': 'জর্দানের ~' },
},
'~ in Kazakhstan': {
         'bn': { 'male': 'কাজাখস্তানের ~', 'female': 'কাজাখস্তানের ~' },
},
'~ in Kenya': {
         'bn': { 'male': 'কেনিয়ার ~', 'female': 'কেনিয়ার ~' },
},
'~ in Kosovo': {
         'bn': { 'male': 'কসোভোর ~', 'female': 'কসোভোর ~' },
},
'~ in Kuwait': {
         'bn': { 'male': 'কুয়েতের ~', 'female': 'কুয়েতের ~' },
},
'~ in Kyrgyzstan': {
         'bn': { 'male': 'কির্গিজস্তানের ~', 'female': 'কির্গিজস্তানের ~' },
},
'~ in Laos': {
         'bn': { 'male': 'লাওসের ~', 'female': 'লাওসের ~' },
},
'~ in Latvia': {
         'bn': { 'male': 'লাতভিয়ার ~', 'female': 'লাতভিয়ার ~' },
},
'~ in Lebanon': {
         'bn': { 'male': 'লেবাননের ~', 'female': 'লেবাননের ~' },
},
'~ in Lesotho': {
         'bn': { 'male': 'লেসোথোর ~', 'female': 'লেসোথোর ~' },
},
'~ in Liberia': {
         'bn': { 'male': 'লাইবেরিয়ার ~', 'female': 'লাইবেরিয়ার ~' },
},
'~ in Libya': {
         'bn': { 'male': 'লিবিয়ার ~', 'female': 'লিবিয়ার ~' },
},
'~ in Liechtenstein': {
         'bn': { 'male': 'লিশটেনস্টাইনের ~', 'female': 'লিশটেনস্টাইনের ~' },
},
'~ in Lithuania': {
         'bn': { 'male': 'লিথুয়ানিয়ার ~', 'female': 'লিথুয়ানিয়ার ~' },
},
'~ in Luxembourg': {
         'bn': { 'male': 'লুক্সেমবুর্গের ~', 'female': 'লুক্সেমবুর্গের ~' },
},
'~ in Macedonia': {
         'bn': { 'male': 'ম্যাসেডোনিয়ার ~', 'female': 'ম্যাসেডোনিয়ার ~' },
},
'~ in Madagascar': {
         'bn': { 'male': 'মাদাগাস্কারের ~', 'female': 'মাদাগাস্কারের ~' },
},
'~ in Malawi': {
         'bn': { 'male': 'মালাউইয়ের ~', 'female': 'মালাউইয়ের ~' },
},
'~ in Malaysia': {
         'bn': { 'male': 'মালয়েশিয়ার ~', 'female': 'মালয়েশিয়ার ~' },
},
'~ in Maldives': {
         'bn': { 'male': 'মালদ্বীপের ~', 'female': 'মালদ্বীপের ~' },
},
'~ in Mali': {
         'bn': { 'male': 'মালির ~', 'female': 'মালির ~' },
},
'~ in Malta': {
         'bn': { 'male': 'মাল্টার ~', 'female': 'মাল্টার ~' },
},
'~ in Martinique': {
         'bn': { 'male': 'মার্তিনিকের ~', 'female': 'মার্তিনিকের ~' },
},
'~ in Mauritania': {
         'bn': { 'male': 'মৌরিতানিয়ার ~', 'female': 'মৌরিতানিয়ার ~' },
},
'~ in Mauritius': {
         'bn': { 'male': 'মরিশাসের ~', 'female': 'মরিশাসের ~' },
},
'~ in Mayotte': {
         'bn': { 'male': 'মায়োতের ~', 'female': 'মায়োতের ~' },
},
'~ in Mexico': {
         'bn': { 'male': 'মেক্সিকোর ~', 'female': 'মেক্সিকোর ~' },
},
'~ in Moldova': {
         'bn': { 'male': 'মলদোভার ~', 'female': 'মলদোভার ~' },
},
'~ in Monaco': {
         'bn': { 'male': 'মোনাকোর ~', 'female': 'মোনাকোর ~' },
},
'~ in Mongolia': {
         'bn': { 'male': 'মঙ্গোলিয়ার ~', 'female': 'মঙ্গোলিয়ার ~' },
},
'~ in Montenegro': {
         'bn': { 'male': 'মন্টিনিগ্রোর ~', 'female': 'মন্টিনিগ্রোর ~' },
},
'~ in Morocco': {
         'bn': { 'male': 'মরক্কোর ~', 'female': 'মরক্কোর ~' },
},
'~ in Mozambique': {
         'bn': { 'male': 'মোজাম্বিকের ~', 'female': 'মোজাম্বিকের ~' },
},
'~ in Namibia': {
         'bn': { 'male': 'নামিবিয়ার ~', 'female': 'নামিবিয়ার ~' },
},
'~ in Nepal': {
         'bn': { 'male': 'নেপালের ~', 'female': 'নেপালের ~' },
},
'~ in Netherlands': {
         'bn': { 'male': 'নেদারল্যান্ডসের ~', 'female': 'নেদারল্যান্ডসের ~' },
},
'~ in New Zealand': {
         'bn': { 'male': 'নিউজিল্যান্ডের ~', 'female': 'নিউজিল্যান্ডের ~' },
},
'~ in Nicaragua': {
         'bn': { 'male': 'নিকারাগুয়ার ~', 'female': 'নিকারাগুয়ার ~' },
},
'~ in Niger': {
         'bn': { 'male': 'নাইজারের ~', 'female': 'নাইজারের ~' },
},
'~ in Nigeria': {
         'bn': { 'male': 'নাইজেরিয়ার ~', 'female': 'নাইজেরিয়ার ~' },
},
'~ in North Korea': {
         'bn': { 'male': 'উত্তর কোরিয়ার ~', 'female': 'উত্তর কোরিয়ার ~' },
},
'~ in Norway': {
         'bn': { 'male': 'নরওয়ের ~', 'female': 'নরওয়ের ~' },
},
'~ in Oman': {
         'bn': { 'male': 'ওমানের ~', 'female': 'ওমানের ~' },
},
'~ in Pakistan': {
         'bn': { 'male': 'পাকিস্তানের ~', 'female': 'পাকিস্তানের ~' },
},
'~ in Panama': {
         'bn': { 'male': 'পানামার ~', 'female': 'পানামার ~' },
},
'~ in Papua New Guinea': {
         'bn': { 'male': 'পাপুয়া নিউগিনির ~', 'female': 'পাপুয়া নিউগিনির ~' },
},
'~ in Paraguay': {
         'bn': { 'male': 'প্যারাগুয়ের ~', 'female': 'প্যারাগুয়ের ~' },
},
'~ in Peru': {
         'bn': { 'male': 'পেরুর ~', 'female': 'পেরুর ~' },
},
'~ in Philippines': {
         'bn': { 'male': 'ফিলিপাইনের ~', 'female': 'ফিলিপাইনের ~' },
},
'~ in Poland': {
         'bn': { 'male': 'পোল্যান্ডের ~', 'female': 'পোল্যান্ডের ~' },
},
'~ in Portugal': {
         'bn': { 'male': 'পর্তুগালের ~', 'female': 'পর্তুগালের ~' },
},
'~ in Puerto Rico': {
         'bn': { 'male': 'পুয়ের্তো রিকোর ~', 'female': 'পুয়ের্তো রিকোর ~' },
},
'~ in Qatar': {
         'bn': { 'male': 'কাতারের ~', 'female': 'কাতারের ~' },
},
'~ in Romania': {
         'bn': { 'male': 'রোমানিয়ার ~', 'female': 'রোমানিয়ার ~' },
},
'~ in Russian Federation': {
         'bn': { 'male': 'রাশিয়ার ~', 'female': 'রাশিয়ার ~' },
},
'~ in Rwanda': {
         'bn': { 'male': 'রুয়ান্ডার ~', 'female': 'রুয়ান্ডার ~' },
},
'~ in Saint Kitts and Nevis': {
         'bn': { 'male': 'সেন্ট কিট্‌স ও নেভিসের ~', 'female': 'সেন্ট কিট্‌স ও নেভিসের ~' },
},
'~ in Saint Lucia': {
         'bn': { 'male': 'সেন্ট লুসিয়ার ~', 'female': 'সেন্ট লুসিয়ার ~' },
},
'~ in Samoa': {
         'bn': { 'male': 'সামোয়ার ~', 'female': 'সামোয়ার ~' },
},
'~ in Sao Tome and Principe': {
         'bn': { 'male': 'সাঁউ তুমি ও প্রিন্সিপির ~', 'female': 'সাঁউ তুমি ও প্রিন্সিপির ~' },
},
'~ in Saudi Arabia': {
         'bn': { 'male': 'সৌদি আরবের ~', 'female': 'সৌদি আরবের ~' },
},
'~ in Senegal': {
         'bn': { 'male': 'সেনেগালের ~', 'female': 'সেনেগালের ~' },
},
'~ in Serbia': {
         'bn': { 'male': 'সার্বিয়ার ~', 'female': 'সার্বিয়ার ~' },
},
'~ in Seychelles': {
         'bn': { 'male': 'সেশেলের ~', 'female': 'সেশেলের ~' },
},
'~ in Sierra Leone': {
         'bn': { 'male': 'সিয়েরা লিওনের ~', 'female': 'সিয়েরা লিওনের ~' },
},
'~ in Singapore': {
         'bn': { 'male': 'সিঙ্গাপুরের ~', 'female': 'সিঙ্গাপুরের ~' },
},
'~ in Slovakia': {
         'bn': { 'male': 'স্লোভাকিয়া ~', 'female': 'স্লোভাকিয়া ~' },
},
'~ in Slovenia': {
         'bn': { 'male': 'স্লোভেনিয়ার ~', 'female': 'স্লোভেনিয়ার ~' },
},
'~ in Solomon Islands': {
         'bn': { 'male': 'সলোমন দ্বীপপুঞ্জের ~', 'female': 'সলোমন দ্বীপপুঞ্জের ~' },
},
'~ in Somalia': {
         'bn': { 'male': 'সোমালিয়ার ~', 'female': 'সোমালিয়ার ~' },
},
'~ in South Africa': {
         'bn': { 'male': 'দক্ষিণ আফ্রিকার ~', 'female': 'দক্ষিণ আফ্রিকার ~' },
},
'~ in South Korea': {
         'bn': { 'male': 'দক্ষিণ কোরিয়ার ~', 'female': 'দক্ষিণ কোরিয়ার ~' },
},
'~ in South Sudan': {
         'bn': { 'male': 'দক্ষিণ সুদানের ~', 'female': 'দক্ষিণ সুদানের ~' },
},
'~ in Spain': {
         'bn': { 'male': 'স্পেনের ~', 'female': 'স্পেনের ~' },
},
'~ in Sri Lanka': {
         'bn': { 'male': 'শ্রীলঙ্কার ~', 'female': 'শ্রীলঙ্কার ~' },
},
'~ in Sudan': {
         'bn': { 'male': 'সুদানের ~', 'female': 'সুদানের ~' },
},
'~ in Suriname': {
         'bn': { 'male': 'সুরিনামের ~', 'female': 'সুরিনামের ~' },
},
'~ in Swaziland': {
         'bn': { 'male': 'সোয়াজিল্যান্ডের ~', 'female': 'সোয়াজিল্যান্ডের ~' },
},
'~ in Sweden': {
         'bn': { 'male': 'সুইডেনের ~', 'female': 'সুইডেনের ~' },
},
'~ in Switzerland': {
         'bn': { 'male': 'সুইজারল্যান্ডের ~', 'female': 'সুইজারল্যান্ডের ~' },
},
'~ in Syria': {
         'bn': { 'male': 'সিরিয়ার ~', 'female': 'সিরিয়ার ~' },
},
'~ in Tajikistan': {
         'bn': { 'male': 'তাজিকিস্তানের ~', 'female': 'তাজিকিস্তানের ~' },
},
'~ in Tanzania': {
         'bn': { 'male': 'তানজানিয়ার ~', 'female': 'তানজানিয়ার ~' },
},
'~ in Thailand': {
         'bn': { 'male': 'থাইল্যান্ডের ~', 'female': 'থাইল্যান্ডের ~' },
},
'~ in Timor Leste': {
         'bn': { 'male': 'পূর্ব তিমুরের ~', 'female': 'পূর্ব তিমুরের ~' },
},
'~ in Togo': {
         'bn': { 'male': 'টোগোর ~', 'female': 'টোগোর ~' },
},
'~ in Trinidad and Tobago': {
         'bn': { 'male': 'ত্রিনিদাদ ও টোবাগোর ~', 'female': 'ত্রিনিদাদ ও টোবাগোর ~' },
},
'~ in Tunisia': {
         'bn': { 'male': 'তিউনিসিয়ার ~', 'female': 'তিউনিসিয়ার ~' },
},
'~ in Turkey': {
         'bn': { 'male': 'তুরস্কের ~', 'female': 'তুরস্কের ~' },
},
'~ in Turkmenistan': {
         'bn': { 'male': 'তুর্কমেনিস্তানের ~', 'female': 'তুর্কমেনিস্তানের ~' },
},
'~ in Uganda': {
         'bn': { 'male': 'উগান্ডার ~', 'female': 'উগান্ডার ~' },
},
'~ in Ukraine': {
         'bn': { 'male': 'ইউক্রেনের ~', 'female': 'ইউক্রেনের ~' },
},
'~ in United Arab Emirates': {
         'bn': { 'male': 'সংযুক্ত আরব আমিরাতের ~', 'female': 'সংযুক্ত আরব আমিরাতের ~' },
},
'~ in United States of America': {
         'bn': { 'male': 'মার্কিন যুক্তরাষ্ট্রের ~', 'female': 'মার্কিন যুক্তরাষ্ট্রের ~' },
},
'~ in Uruguay': {
         'bn': { 'male': 'উরুগুয়ের ~', 'female': 'উরুগুয়ের ~' },
},
'~ in Uzbekistan': {
         'bn': { 'male': 'উজবেকিস্তানের ~', 'female': 'উজবেকিস্তানের ~' },
},
'~ in Venezuela': {
         'bn': { 'male': 'ভেনেজুয়েলার ~', 'female': 'ভেনেজুয়েলার ~' },
},
'~ in Vietnam': {
         'bn': { 'male': 'ভিয়েতনামের ~', 'female': 'ভিয়েতনামের ~' },
},
'~ in Yemen': {
         'bn': { 'male': 'ইয়েমেনের ~', 'female': 'ইয়েমেনের ~' },
},
'~ in Zambia': {
         'bn': { 'male': 'জাম্বিয়ার ~', 'female': 'জাম্বিয়ার ~' },
},
'~ in Zimbabwe': {
         'bn': { 'male': 'জিম্বাবুয়ের ~', 'female': 'জিম্বাবুয়ের ~' },
        },
    }
    
    translations = {}
    for occupkey, occupdic in translationsOccupations.items():
        for natkey, natdic in translationsNationalities.items():
            entranslation = re.sub('~', natkey, occupkey)
            translations[entranslation] = {}
            for translang in occupdic.keys():
                if translang in natdic.keys(): #when no translation for this nationatily, skip to avoid error
                    #print(occupkey, natkey, translang)
                    translations[entranslation][translang] = {
                        'male': re.sub('~', natdic[translang]['male'], occupdic[translang]['male']), 
                        'female': re.sub('~', natdic[translang]['female'], occupdic[translang]['female']), 
                    }
                else:
                    print('Missing %s: translation for %s. Skiping...' % (translang.encode('utf-8'), natkey.encode('utf-8')))
    time.sleep(5)
    c2 = 1
    total2 = 0
    cqueries = 0
    translations_list = list(translations.keys())
    translations_list.sort()
    totalqueries = len(targetlangs) * len(genders_list) * len(translations_list)
    skiptolang = '' #'es'
    skiptogender = '' #'male'
    skiptoperson = '' #'American politician'
    for targetlang in targetlangs:
        if skiptolang:
            if skiptolang != targetlang:
                print('Skiping lang:', targetlang.encode('utf-8'))
                continue
            else:
                skiptolang = ''
        
        for genderq, genderlabel in genders_list:
            if skiptogender:
                if skiptogender != genderlabel:
                    print('Skiping gender:', genderlabel.encode('utf-8'))
                    continue
                else:
                    skiptogender = ''
            
            for translation in translations_list:
                cqueries += 1
                print(targetlang, genderlabel, translation.encode('utf-8'))
                if skiptoperson:
                    if skiptoperson != translation:
                        print('Skiping translation:', translation.encode('utf-8'))
                        continue
                    else:
                        skiptoperson = ''
                
                url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%20%7B%0A%20%20BIND%28%20STRLANG%28%20%22urllib.parse.quote%28translation%29%22%2C%20%22en%22%20%29%20AS%20%3Fdesc%20%29%20.%0A%20%20%3Fitem%20schema%3Adescription%20%3Fdesc%20.%0A%20%20MINUS%20%7B%0A%20%20%20%20%3Fitem%20schema%3Adescription%20%3Fdescription%20.%0A%20%20%20%20FILTER%28%20LANG%28%20%3Fdescription%20%29%20%3D%20%22bn%22%20%29%20.%0A%20%20%7D%0A%20%20%7D'
                url = '%s&format=json' % (url)
                sparql = getURL(url=url)
                json1 = loadSPARQL(sparql=sparql)
                total = len(json1['results']['bindings'])
                total2 += total
                c = 1
                for result in json1['results']['bindings']:
                    q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
                    print('\n== %s (%d/%d; %s; %s; %s; items %d/%d; queries %d/%d) ==' % (q, c, total, translation.encode('utf-8'), genderlabel, targetlang, c2, total2, cqueries, totalqueries))
                    c += 1
                    c2 += 1
                    item = pywikibot.ItemPage(repo, q)
                    try: #to detect Redirect because .isRedirectPage fails
                        item.get()
                    except:
                        print('Error while .get()')
                        continue
                    descriptions = item.descriptions
                    addedlangs = []
                    for lang in translations[translation].keys():
                        if not lang in descriptions.keys():
                            descriptions[lang] = translations[translation][lang][genderlabel]
                            addedlangs.append(lang)
                    data = { 'descriptions': descriptions }
                    addedlangs.sort()
                    if addedlangs:
                        summary = 'BOT - বিবরণ যোগ (%sটি ভাষা): %s' % (len(addedlangs), ', '.join(addedlangs))
                        print(summary)
                        try:
                            item.editEntity(data, summary=summary)
                        except:
                            #pywikibot.data.api.APIError: modification-failed: Item Q... already has label "..." associated with language code ..., using the same description text.
                            print('Error while saving')
                            continue
                    else:
                        print('No changes needed')
    print("Finished successfully")

if __name__ == "__main__":
    main()
