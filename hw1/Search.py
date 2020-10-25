import random
from math import trunc

def search(query, url_to_docid, docid_to_url, term_to_id, reversed_index):
    """
    Основная функция.
    
    input: запрос заданный в виде бульевого запроса
    
    output: список сайтов, удовлетворяющих ему.
    """
    
    def get_formula(query):    
        """
        Вспомогательная функция.
        
        input: строка - запрос в формате бульевого запроса.
        
        output: список строк - где каждый объект
         либо операция,
         либо операнд,
         либо скобка
         в бульевом запросе.
        """

        lizt, buf = [], ""

        for c in query.lower():

            if not c.isalpha():

                if buf.strip():
                    lizt.append(buf)

                if c.strip():
                    lizt.append(c)
                buf = ""

            else:    
                buf += c
        if buf.strip():
            lizt.append(buf)  

        return lizt    

    
    def get_polish_notation(formula):
        """
        Вспомогательная функция.
        
        Input: список строк - выход функции get_formula(query) (инфексная запись формулы)
        
        Output: список строк - та же формула, но в порядке обратной польской записи.
        """

        prior = {'!': 3, '&': 2, '|': 1, '(': 0}
        polskRecord = []
        stack = []

        def condition(stack, elem):

            if len(stack) > 0:
                if prior[stack[-1]] >= prior[elem]:
                    return True
            return False


        for elem in formula:

            if elem == '(':
                stack.append(elem)

            elif elem == ')':
                while stack[-1] != '(':
                    polskRecord.append(stack[-1])
                    del stack[-1]
                del stack[-1]

            elif elem in prior.keys():
                while condition(stack, elem):            
                    polskRecord.append(stack[-1])
                    del stack[-1]
                stack.append(elem)

            else:
                polskRecord.append(elem)

        polskRecord.extend(stack[::-1])

        return polskRecord
    


    class getPtr:
        """
        Класс функтор, который позволяет
         получить указатель-адрес вершины дерева.
        """
        def __init__(self):     
            """
            Чтобы не было разных вершин с одним адресом.
            """
            self.all_ptr = set()


        def __call__(self):        
            """
            При вывозове, возвращает 
             новый уникальный указатель.
            """
            tmp = random.randint(0, 10000)

            while tmp in self.all_ptr:
                tmp = random.randint(0, 10000)
            self.all_ptr.add(tmp)

            return tmp
        


    get_ptr = getPtr()
    binTree = dict()

    
    def find_intersection_by_streaming_passage(bin_tree, head_ptr, reversed_index, term_to_id):
  
        def bin_search(arr, key, l=0, r=-100):
            """
            Функция бинарного поиска,
             позволяет при потоковом обходе
             быстрее находить следующий id в списке в листе,
             ограниченный сверху docId.
            """

            if r == -100:
                r = len(arr) - 1

            if l == len(arr) - 1:
                return len(arr) - 1

            if l > r:
                return l

            m = trunc((r + l) / 2)    

            if   arr[m] > key:
                return bin_search(arr, key, l,   m-1)

            elif arr[m] < key:
                return bin_search(arr, key, m+1, r)

            else:
                return m               

        docId = -1 # Главный счётчик текущего инедкса.
        res = []

        def _run(cur_ptr, docId):
            """
            Функция, позволяющая 
             произвоть потоковый проход
             по дереву рекурсивно.
            """

            cur_node = bin_tree[cur_ptr]

            if cur_node[0] == 'BIN_OPERATION':
                if   cur_node[1] == '&':
                    return max(_run(cur_node[2], docId),
                               _run(cur_node[3], docId))

                elif cur_node[1] == '|':
                    return min(_run(cur_node[2], docId),
                               _run(cur_node[3], docId))

                else:
                    raise "error1"

            elif cur_node[0] == 'UN_OPERATION':
                if cur_node[1] == '!':
                    tmp = _run(cur_node[2], docId)
                    if tmp == docId:
                        return tmp+1
                    else:
                        return docId
                else:
                    raise "error3"

            elif cur_node[0] == 'OPERAND':
                doc_list = reversed_index[cur_node[1]]

                cur_node[2] = bin_search(doc_list, docId, l=cur_node[2])

                if   cur_node[2] == len(doc_list)-1:
                    return float("inf")

                elif doc_list[cur_node[2]] >= docId:
                    return doc_list[cur_node[2]]

                else:
                    print(doc_list)
                    print(cur_node)
                    print(docId)
                    raise "error4"

            else:
                raise "error5"                    


        while docId < max_docId:

            query_result = _run(head_ptr, docId)        
            if docId == query_result:
                res.append(docId)
                docId += 1
            else:
                if docId < query_result:
                    docId = query_result
                else:
                    raise "error6"

        return res     
            
        
        
    def make_node(elem, stack, this_type):
        """
        Вспомогательная функция, которая формирует дерево.
        """
        ptr = get_ptr()

        if this_type == 'OPERAND':
            node = {ptr: ['OPERAND', elem, 0]}

        elif this_type == 'UN_OPERATION':
            node = {ptr: ['UN_OPERATION', elem, stack[-1]]}
            del stack[-1]

        elif this_type == 'BIN_OPERATION':
            node = {ptr: ['BIN_OPERATION', elem, stack[-2], stack[-1]]}
            del stack[-2:]

        else:
            raise "error"

        stack.append(ptr)
        binTree.update(node)

        return stack 
    
    # Основоне тело функции search:
    
    # Переводим запрос в список смысловых елементов (слова, скобки, символы &/|/!).
    #
    formula = get_formula(query) 
    
    # Первеодим формулу в польскую запись.
    #
    polishRecord = get_polish_notation(formula)
    
    # Формализуем множество используемых символов-операций.
    #
    operations = {'&', '|', '!'}
    stack = []

    # Итерируемся по формуле, записанной в польской записи
    #  и формируем дерево бинарного поиска.
    #
    for elem in polishRecord:

        if elem in {'&', '|'}:
            stack = make_node(elem, stack, 'BIN_OPERATION')
        elif elem == '!':
            stack = make_node(elem, stack, 'UN_OPERATION')        
        else:
            stack = make_node(term_to_id[elem], stack, 'OPERAND')
            
    # В стеке, находится корень.
    #
    head_ptr = stack[0]
    
    # Запоминаем максимульное значние индекса url'ов.
    #
    max_docId = max(url_to_docid.values())

    # Получаем список из docid, сайтов удовлетворяющих запросу.
    #
    list_of_docid = find_intersection_by_streaming_passage(binTree, head_ptr, reversed_index, term_to_id)
    
    # По docid'шникам получаем сами url'ы.
    #
    needed_urls = []
    for docid in list_of_docid:
        needed_urls.append(docid_to_url[docid])
        
    return needed_urls
