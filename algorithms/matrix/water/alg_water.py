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
     
            # numpy.rand выдает число в [0,1], добавим больше донышек
            if a[gi,gj] < 0.2:
                a[gi,gj] = 0
            
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
    
if __name__ == '__main__':
    
    a = numpy.array([ [0,2,1,0,1,1,1],
                      [2,0,5,0,1,0,1],
                      [0,5,0,5,1,1,1],
                      [0,1,5,0,1,0,1]
                      ])
    
    global_value = alg_fill_bottom(a)
    print "="*10
    print "Result: ", global_value
     
    a = numpy.random.rand(1000,1000)
     
    global_value = alg_fill_bottom(a)
    print "="*10
    print "Result: ", global_value
    
    a = numpy.zeros((1000,1000))
     
    global_value = alg_fill_bottom(a)
    print "="*10
    print "Result: ", global_value
 
    
    
