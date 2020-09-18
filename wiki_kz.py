import requests
import sys
import re
import urllib.parse
from queue import Queue
from pprint import pprint

def make(q):
    global max_words, biggest_site, number_of_sites
    while not q.empty():
        page, lvl = q.get()
        number_of_sites[lvl] += 1;
        answer = requests.get(page)
        print(page + " " + str(lvl + 1))
        if len(answer.text) > max_words:
            max_words = len(answer.text)
            biggest_site = page
        if lvl == MAXLVL:
            continue
        links = re.findall(template, answer.text)
        for link in links:
            link = urllib.parse.unquote(link)
            if flag:
                link = start_page + link
            if link not in deep_levels:
                q.put((link, lvl + 1))
                deep_levels[link] = lvl + 1
    return

if __name__ == "__main__":
    MAXLVL = 2
    number_of_sites = [0] * (MAXLVL + 1)
    max_words = 0
    biggest_site = ""
    deep_levels = {}
    if len(sys.argv) != 3:
        print("python3 wiki_kz.py https://kz.wikipedia.org https://kz.wikipedia.org/wiki/")
        exit(1)
    start_page = sys.argv[1]
    template = sys.argv[2]
    flag = False
    if template.find(start_page) != -1:
        template = template[len(start_page):]
        flag = True
    q = Queue()
    q.put((start_page, 0))
    template = re.compile(template + "%[a-zA-Z\.0-9/%]+")
    make(q)
    pprint(deep_levels)
    print("Самый большой сайт " + biggest_site + f" количество символов на этом сайте {max_words}")
    print(f"Общее количество сайтов: {len(deep_levels)}")
    for i in range(MAXLVL + 1):
        print(f"На {i}-м уровне глубины {number_of_sites[i]} сайтов")
