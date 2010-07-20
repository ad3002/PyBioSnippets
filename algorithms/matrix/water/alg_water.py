#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 20.07.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 
 
import numpy

 
def alg_fill_bottom(a):
    '''
    @param a: numpy 2d array
    '''
 
    N,M = a.shape
    # print "Size: ", N, M
     
    checked = set()
    added_floors = set()
    global_value = 0
     
    # края нам не интересны
    for gi in range(1,N-1):
        for gj in range(1,M-1):
     
            # нам интересны только донышки
            if a[gi,gj] > 0:
                continue
            # донышки которые уже смотрели скипим
            if (gi,gj) in checked:
                continue
     
     
            floors = []
            floors.append([gi,gj])
     
            number_floors = 0
            added_floors.add((gi,gj))
            borders = {}
     
            local_checked = set()
            while floors:
     
                p = floors.pop()
                number_floors += 1
                # print "floor checking: ", p
     
                i = p[0]
                j = p[1]
                checked.add((i, j))
     
                # дальше завливаем по четырем направлениям
                # пока не уткнемся в границу или не выйдем за границы матрицы
                # новый донышки добавляем к группе текущего
                # и их тоже заливаем
     
                # влево
     
                k = 0
                while True:
                    k += 1
                    # print "  check left: ", i, j-k
     
                    if (i,j-k) in checked or (i,j-k-1) in local_checked:
                        # print "   pass"
                        break
                    elif j-k < 0:
                        borders[0] = 0
                        # print "   left leak added"
                        break
                    elif a[i, j-k] > 0:
                        borders[(i, j-k)] = a[i,j-k]
                        # print "   left border added"
                        break
                    else:
                        if not (i, j-k) in added_floors and j-k > 0:
                            # print "   left cell added"
                            floors.append((i, j-k))
                            added_floors.add((i, j-k))
     
                # вправо
     
                k = 0
                while True:
                    k += 1
                    # print "  check right: ", i, j+k
     
                    if (i,j+k) in checked  or (i,j+k-1) in local_checked:
                        # print "   pass"
                        break
                    elif j+k == M:
                        borders[0] = 0
                        # print "   right leak added"
                        break
                    elif a[i, j+k] > 0:
                        borders[(i, j+k)] = a[i,j+k]
                        # print "   right border added"
                        break
                    else:
                        if not (i, j+k) in added_floors and j+k!=M-1 :
                            # print "   right cell added"
                            floors.append((i, j+k))
                            added_floors.add((i, j+k))
     
                # вверх
     
                k = 0
                while True:
                    k += 1
                    # print "  check top: ", i-k, j
     
                    if (i-k,j) in checked or (i-k-1,j) in local_checked:
                        # print "   pass"
                        break
                    elif i-k < 0:
                        borders[0] = 0
                        # print "   top leak added"
                        break
                    elif a[i-k, j] > 0:
                        borders[(i-k, j)] = a[i-k,j]
                        # print "   top border added"
                        break
                    else:
                        if not (i-k, j) in added_floors and i-j>0:
                            # print "   top cell added"
                            floors.append((i-k, j))
                            added_floors.add((i-k, j))
     
                # вниз
     
                k = 0
                while True:
                    k += 1
                    # print "  check bottom: ", i+k, j
     
                    if (i+k,j) in checked or (i+k-1,j) in local_checked:
                        # print "   pass"
                        break
                    elif i+k == N:
                        borders[0] = 0
                        # print "   bottom leak added"
                        break
                    elif a[i+k, j] > 0:
                        borders[(i+k, j)] = a[i+k,j]
                        # print "   bottom border added"
                        break
                    else:
                        if not (i+k, j) in added_floors and i+k!=N-1:
                            # print "   bottom cell added"
                            floors.append((i+k, j))
                            added_floors.add((i+k, j))
                            
                
                local_checked.add((i,j))
     
     
            height = min( [ b for b in borders.values()] )
            value = height*number_floors
            global_value += value
            # print "="*10
            # print "borders: ", borders
            # print "value: ", value
            # print "="*10
    return global_value
    
    
def test(a):
    return alg_fill_bottom(a)
  
    
if __name__ == '__main__':
    
    
    from timeit import Timer
    
    # тестим зависимость от количества нулевых элементов
    for k in range(0,11):
        a = numpy.random.rand(1000,1000)
        
        N,M = a.shape
        
        for i in range(0,N):
            for j in range(0,M):
                if a[i,j] < k*0.1:
                    a[i,j] = 0 
        
        t = Timer("test(a)", "from __main__ import test;from __main__ import a")
        print "Random 1000x1000, %s proc of zeros: " % (10*k), t.timeit(number=1)   
    
    
    # тестим зависимость от размера
    
    
#    a = numpy.array([ [0,2,1,0,1,1,1],
#                      [2,0,5,0,1,0,1],
#                      [0,5,0,5,1,1,1],
#                      [0,1,5,0,1,0,1]
#                      ])
#    
#    t = Timer("test(a2)", "from __main__ import test; from __main__ import a2")
#    print "Simple case: ", t.timeit(number=1)
#    
#    
#    b1 = numpy.random.rand(10,10)
#    t = Timer("test(b1)", "from __main__ import test; from __main__ import b1")
#    print "Random 10x10: ", t.timeit(number=1)
#    
#    b2 = numpy.random.rand(100,100)
#    t = Timer("test(b2)", "from __main__ import test; from __main__ import b2")
#    print "Random 100x100: ", t.timeit(number=1)
#    
#    b3 = numpy.random.rand(1000,1000)
#    t = Timer("test(b3)", "from __main__ import test; from __main__ import b3")
#    print "Random 1000x1000: ", t.timeit(number=1)
#    
#    d = numpy.ones((10,10))
#    t = Timer("test(d)", "from __main__ import test; from __main__ import d")
#    print "Ones 10x10: ", t.timeit(number=1)
#    
#    d1 = numpy.ones((100,100))
#    t = Timer("test(d1)", "from __main__ import test; from __main__ import d1")
#    print "Ones 100x100: ", t.timeit(number=1)
#
#    d2 = numpy.ones((1000,1000))
#    t = Timer("test(d2)", "from __main__ import test; from __main__ import d2")
#    print "Ones 1000x1000: ", t.timeit(number=1)
#
#    w = numpy.zeros((10,10))
#    t = Timer("test(w)", "from __main__ import test; from __main__ import w")
#    print "Zeros 10x10: ", t.timeit(number=1)
#    
#    w1 = numpy.zeros((100,100))
#    t = Timer("test(w1)", "from __main__ import test; from __main__ import w1")
#    print "Zeros 100x100: ", t.timeit(number=1)
#    
#    w2 = numpy.zeros((1000,1000))
#    t = Timer("test(w2)", "from __main__ import test; from __main__ import w2")
#    print "Zeros 1000x1000: ", t.timeit(number=1)
#    
#    