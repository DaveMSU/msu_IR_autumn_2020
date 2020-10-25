def clear_data(dirname):
    
    # Для того, чтобы почистить url от сиволов типа \x*
    #
    def __cleaned(dirty_url):
    
        ord_th = 46

        buf = ""

        for c in dirty_url:

            buf += c

            if len(buf) == 4:
                if buf != "http":
                    buf = buf[1:]      

            if (ord(buf[-1]) < ord_th) and ('http' in buf):
                    return buf[:-1]
        return buf[:-1]

    
    # Получаем из всех не предобработанных
    # файлов список из слов.
    #
    data = []
    for i in range(1,8+1,1):

        filename = "file_" + str(i) + ".gz"
        with gzip.open(dirname + filename) as f:
            data.extend(f.read().decode("utf-8", errors="ignore").lower().split())
            
    # Формируем словарь вида - {url: list of word}
    # И множество (set) всех слов в корпусе.
    #
    buffer = []
    cites  = dict()
    word_set = set(data)

    for word in data:

        if 'http' in word:
            if len(buffer) > 2:
                cites[__cleaned(buffer[0])] = buffer[1:]
                word_set.remove(buffer[0])
            buffer = []
        buffer.append(word)
            
    return cites, word_set
