class Simple9_encoder_decoder():
    def __init__(self):

        # Формируем маски-константы.
        #
        code_9 = 0x90000000 # 1001 0000 0000 ... 0000
        code_8 = 0x80000000 # 1000 0000 0000 ... 0000
        code_7 = 0x70000000 # 0111 0000 0000 ... 0000
        code_6 = 0x60000000 # 0110 0000 0000 ... 0000
        code_5 = 0x50000000 # 0101 0000 0000 ... 0000
        code_4 = 0x40000000 # 0100 0000 0000 ... 0000
        code_3 = 0x30000000 # 0011 0000 0000 ... 0000
        code_2 = 0x20000000 # 0010 0000 0000 ... 0000
        code_1 = 0x10000000 # 0001 0000 0000 ... 0000
        
        self.encode_type = [[28, 2**1  - 1, code_9,  1],     
                            [14, 2**2  - 1, code_8,  2],
                            [ 9, 2**3  - 1, code_7,  3],
                            [ 7, 2**4  - 1, code_6,  4],
                            [ 5, 2**5  - 1, code_5,  5],
                            [ 4, 2**7  - 1, code_4,  7],
                            [ 3, 2**9  - 1, code_3,  9],
                            [ 2, 2**14 - 1, code_2, 14],
                            [ 1, 2**28 - 1, code_1, 28]
                           ]

        self.decode_type = {code_9: [28, 2**1  - 1,  1],     
                            code_8: [14, 2**2  - 1,  2],
                            code_7: [9,  2**3  - 1,  3],
                            code_6: [7,  2**4  - 1,  4],
                            code_5: [5,  2**5  - 1,  5],
                            code_4: [4,  2**7  - 1,  7],
                            code_3: [3,  2**9  - 1,  9],
                            code_2: [2,  2**14 - 1, 14],
                            code_1: [1,  2**28 - 1, 28]
                           }
        
    def encode(self, a):
        """
        Метод класса, позволяюзий КОДИРОВАТЬ
        список элементов a, по принципу Simple9.
        """

        offset    = 0        
        res       = []
        list_size = len(a)

        while offset < list_size:        

            for current_encode_type in self.encode_type:

                n     = current_encode_type[0] # Кол-во чисел которые могут поместиться на регистр.
                th    = current_encode_type[1] # Верхнее возможное число для выбранного code_x.
                code  = current_encode_type[2] # Запоминаем n (важны лишь первые 4 бита)
                shift = current_encode_type[3] # На сколько сдвигать указатель при обработке.
                 
                # В идеале менять порядок следования элементов и их запоминать,
                #  но мы обойдемся тем, что будем обрезать по максимальному.
                #
                last_n_max = max(a[offset:offset + n])

                if (offset + n <= list_size) and (last_n_max <= th):

                    tmp = a[offset]
                    for i in range(1, n): 
                        tmp |= (a[offset + i] << (shift * i))

                    res.append(tmp | code)
                    offset += n
                    break

        return res
    

    def decode(self, a):
        """
        Метод класса, позволяюзий ДЕКОДИРОВАТЬ
        список элементов a, по принципу Simple9.
        """        
        
        res = []
        for cur_num in a:

            code = cur_num & 0xf0000000 # cur_num & (1111 0000 0000 ... 0000) - маска для типа SimpleX.
            data = cur_num & 0x0fffffff # cur_num & (0000 1111 1111 ... 1111) - маска для элементов.
            info = self.decode_type[code]

            n     = info[0] # Кол-во чисел которые могут поместиться на регистр.
            bit   = info[1] # Соответствующая бинарная последовательность 1-иц.
            shift = info[2] # На сколько сдвигать указатель при обработке.

            for i in range(n):
                res.append(data & bit)            
                data >>= shift

        return res
