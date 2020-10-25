
from collections import defaultdict # Для построения словаря обратного индекса.

from Search import search
from ClearFiles import clear_data

if __name__ == "__main__":

    cites, word_set = clear_data('dataset/')                      # Словарь вида {url сайта: список слов на сайте}
    term_to_id = {word: i for i, word in enumerate(word_set)}     # -//- {слово: id слова} (нумерация с 0 до ~300k)
    url_to_docid = {url: i for i, url in enumerate(cites.keys())} # -//- {url: id сайта} (нумерация с 0 до ~9k)
    docid_to_url = {i: url for i, url in enumerate(cites.keys())} # -//- {id сайта: url}
    
    
    reversed_index = defaultdict(list)                            # Словарь обратных индексов вида
    for i, (url, word_list) in enumerate(cites.items()):          #  {id слова: все id сайтов, на которых оно есть}
        for word in word_list:
            reversed_index[term_to_id[word]].append(url_to_docid[url]) # Already sorted                            
    
    query = input()
    for i, url in enumerate(search(query, url_to_docid, docid_to_url, term_to_id, reversed_index)):
        print("%i: " % i, url) 
