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
        for i in range(len(links)):
            links[i] = urllib.parse.unquote(links[i])
            page = "https://kk.wikipedia.org" + links[i]
            if page not in deep_levels:
                q.put((page, lvl + 1))
                deep_levels[page] = lvl + 1
    return

if __name__ == "__main__":
    MAXLVL = 2
    number_of_sites = [0] * (MAXLVL + 1)
    max_words = 0
    biggest_site = ""
    deep_levels = {}
    if len(sys.argv) != 3:
        print("python3 wiki_kz.py https://kk.wikipedia.org https://kk.wikipedia.org/wiki/")
        exit(1)
    start_page = sys.argv[1]
    template = sys.argv[2]
    q = Queue()
    q.put((start_page, 0))
    template =  r"/wiki/%[a-zA-Z\.0-9/%]+"
    make(q)
    pprint(deep_levels)
    print("Самый большой сайт " + biggest_site + f" количество символов на этом сайте {max_words}")
    print(f"Общее количество сайтов: {len(deep_levels)}")
    for i in range(MAXLVL + 1):
        print(f"На {i}-м уровне глубины {number_of_sites[i]} сайтов")
