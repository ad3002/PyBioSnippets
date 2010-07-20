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
    
    right_border = M-1
    bottom_border = N-1 
    
    global_value = 0
    
    # print "Size: ", N, M
    # preprocessing: compute all heights
    
    avaliable_heights = set()
    for gi in range(0,N):
        for gj in range(0,M):
            avaliable_heights.add(a[gi,gj])
    
    avaliable_heights = list(avaliable_heights)
    avaliable_heights.sort()
    
    min_height = avaliable_heights[0] - 1
    
    print "Heights: ", len(avaliable_heights)
    
    for H in avaliable_heights[:-1]:
     
        checked = set()
        added_floors = set()
        
        global_leak_cells = []
        
        # print "  height: ", H, len(global_calculated_cells)
         
        # края нам не интересны
        for gi in range(1,bottom_border):
            for gj in range(1,right_border):
         
                # нам интересны только донышки
                if a[gi,gj] > H :
                    continue
                # нам не интересны донышки, которые мы залили водой на пред. итерации
                if a[gi,gj] <= min_height:
                    continue
                
                if (gi, gj) in global_leak_cells:
                    continue
                
                # донышки которые уже смотрели скипим
                if (gi,gj) in checked:
                    continue
         
                floors = []
                floors.append([gi,gj])
         
                local_number_floors = []
                added_floors.add((gi,gj))
                borders = {}
         
                while floors:
         
                    p = floors.pop()
                    
                    
                    # print "floor checking: ", p
         
                    i = p[0]
                    j = p[1]
                    
                    local_number_floors.append((i,j))
                    
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
                        
                        if a[i,j-1] == H:
                            # print "   pass zero"
                            if i == 0 or j-1 == 0 or i == bottom_border or j-1 == right_border:
                                borders[0] = H
                                # print "    +zero border:", i, j-1 
                            break
                        
                        if (i,j-k) in checked:
                            # print "   pass checked"
                            break
                        elif j-k < 0:
                            borders[0] = H
                            # print "   left leak added"
                            break
                        elif a[i, j-k] > H:
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
                        if a[i,j-1] == H:
                            # print "   pass zero"
                            if i == 0 or j-1 ==0 or i == bottom_border or j-1 == right_border:
                                borders[0] = H
                                # print "    +zero border", i, j-1
                            break
                        
                        if (i,j+k) in checked:
                            # print "   pass checked"
                            break
                        elif j+k == M:
                            borders[0] = H
                            # print "   right leak added"
                            break
                        elif a[i, j+k] > H:
                            borders[(i, j+k)] = a[i,j+k]
                            # print "   right border added"
                            break
                        else:
                            if not (i, j+k) in added_floors and j+k!=right_border :
                                # print "   right cell added"
                                floors.append((i, j+k))
                                added_floors.add((i, j+k))
         
                    # вверх
         
                    k = 0
                    while True:
                        k += 1
                        # print "  check top: ", i-k, j
         
                        if a[i-1,j] == H:
                            # print "   pass zero"
                            if i-1 == 0 or j ==0 or i-1 == bottom_border or j == right_border:
                                borders[0] = H
                                # print "    +zero border", i-1, j
                            break
         
                        if (i-k,j) in checked:
                            # print "   pass checked"
                            break
                        elif i-k < 0:
                            borders[0] = H
                            # print "   top leak added"
                            break
                        elif a[i-k, j] > H:
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
         
                        if a[i-1,j] == H:
                            if i-1 == 0 or j ==0 or i-1 == bottom_border or j == right_border:
                                borders[0] = H
                                # print "    +zero border", i-1, j
                            break
         
                        if (i+k,j) in checked:
                            # print "   pass checked"
                            break
                        elif i+k == N:
                            borders[0] = H
                            # print "   bottom leak added"
                            break
                        elif a[i+k, j] > H:
                            borders[(i+k, j)] = a[i+k,j]
                            # print "   bottom border added"
                            break
                        else:
                            if not (i+k, j) in added_floors and i+k != bottom_border:
                                # print "   bottom cell added"
                                floors.append((i+k, j))
                                added_floors.add((i+k, j))
                                
                    
                    
                if borders:
                    height = min( [ b for b in borders.values()] )
                    value = (height-H)*len(local_number_floors)
                    
                    if value > 0:
                        global_value += value
                
                    else:
                        # мы не считаем ячейки из которых выливается за границу
                        for item in local_number_floors:
                            global_leak_cells.append(item)
                                
                    
                    # print "="*10
#                    print "borders: ", borders
#                    print "value: ", value
#                    print "n: ", local_number_floors
                    # print "="*10
    
        min_height = H
    
    
    return global_value
    
    
def test(a):
    return alg_fill_bottom(a)
  
def get_circle(k):
    
     a = numpy.ones((k,k))
     
     N,M = a.shape
     
     x = 1
     y = 1
     
     for i in range(x,N-x):
         a[y,i] = 0
     for i in range(y, M-y):
         a[i,M-x-1] = 0
     for i in range(N-x-1, x-1, -1):
         a[M-y-1,i] = 0
     for i in range(M-y-1, y, -1):
         a[i,x] = 0
         
     return a
    
def get_spiral():
    
    from PIL import Image
    
    i = Image.open("spiral.png")
    a = numpy.asarray(i)  
    
    return a
    

def gen_grebenka(N,M):
    s = [M+N+M+N] * M
    res = []
    for i in xrange(N):
        res += [s[:]]
    for y in xrange(1, M-1, 2):
        for x in xrange(N-2):
            res[x][y] = y
    for y in xrange(1,M-1):
        res[N-2][y] = 0
    return numpy.asarray(res)
    
if __name__ == '__main__':
    
    from timeit import Timer
    
    a = get_circle(10)
    assert test(a) == 28
    a = get_circle(100)
    assert test(a) == 388
    a = get_circle(1000)
    assert test(a) == 3988 
    
    a2 = numpy.array([ [0,2,1,0,1,1,1],
                      [2,0,5,0,1,0,1],
                      [0,5,0,5,1,1,1],
                      [0,1,5,0,1,0,1]
                      ])
    
    assert test(a2) == 8 
    t = Timer("test(a2)", "from __main__ import test; from __main__ import a2")
    print "Simple case: ", t.timeit(number=1)
    
    a2 = numpy.array([ [0,2,1,0,1,1,1],
                      [2,1,5,0,1,0,1],
                      [0,5,0,5,1,1,1],
                      [0,1,5,0,1,0,1]
                      ])
    
    assert test(a2) == 7 
    t = Timer("test(a2)", "from __main__ import test; from __main__ import a2")
    print "Simple case: ", t.timeit(number=1)
     
    a2 = numpy.array([[0,3,3,3,3,3,0],
                      [0,3,1,1,1,3,1],
                      [0,3,1,0,1,3,1],
                      [0,3,1,1,1,3,1],
                      [0,3,3,3,3,3,1]
                      ])
    
    assert test(a2) == 19 
    t = Timer("test(a2)", "from __main__ import test; from __main__ import a2")
    print "Simple case: ", t.timeit(number=1)
     
    
#    gr = gen_grebenka(1000,1000)
#    t = Timer("test(gr)", "from __main__ import test; from __main__ import gr")
#    print "Grebenka 1000x1000 case: ", t.timeit(number=1)
    
    # тестим зависимость от количества высот
#    for k in range(0,11):
#        a = numpy.random.rand(100,100)
#        
#        N,M = a.shape
#        
#        for i in range(0,N):
#            for j in range(0,M):
#                a[i,j] = round(a[i,j], 1) 
#        
#        t = Timer("test(a)", "from __main__ import test;from __main__ import a")
#        print "Random 1000x1000, %s proc of zeros: " % (10*k), t.timeit(number=1)   
#
#    s = get_spiral()
#    t = Timer("test(s)", "from __main__ import test; from __main__ import s")
#    print "Spiral case 1000x1000: ", t.timeit(number=1)

    
    
    # тестим зависимость от размера
    
    
   
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