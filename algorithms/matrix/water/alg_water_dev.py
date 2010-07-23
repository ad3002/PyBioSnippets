#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 20.07.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 
 
import numpy

 
def get_volume(a):
    '''
    @param a: any array or list
    '''

    if not a.__class__ is numpy.ndarray:
        a = numpy.asarray(a)

    # print "\n",a

    N,M = a.shape
    
    right_border = M-1
    bottom_border = N-1 
    
    global_value = 0
    
    # print"Size: ", N, M
    # preprocessing: compute all heights
    
    avaliable_heights = set()
    for gi in range(0,N):
        for gj in range(0,M):
            avaliable_heights.add(a[gi,gj])
    
    avaliable_heights = list(avaliable_heights)
    avaliable_heights.sort()
    min_height = avaliable_heights[0] - 1
    
    # print"Heights: ", len(avaliable_heights)
    
    for H in avaliable_heights[:-1]:
     
        # print "height cheking: ", H
     
        checked = set()
#        added_floors = set()
        
        global_leak_cells = set()
        
        
         
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
         
                floors = set()
                floors.add((gi,gj))
         
                local_number_floors = []
#                added_floors.add((gi,gj))
                borders = {}
         
                while floors:
         
                    p = floors.pop()
                    
                    
                    # print"floor checking: ", p
         
                    i = p[0]
                    j = p[1]
                    
                    local_number_floors.append((i,j))
                    
                    checked.add((i, j))
         
                    # проверяем утечки
                    
                    # print global_leak_cells
                    
                    if (i,j-1) in global_leak_cells or\
                       (i,j+1) in global_leak_cells or\
                       (i-1,j) in global_leak_cells or\
                       (i+1,j) in global_leak_cells:
                        # print "  neib. leak added"
                        borders[0] = H
         
                    # дальше завливаем по четырем направлениям
                    # пока не уткнемся в границу или не выйдем за границы матрицы
                    # новый донышки добавляем к группе текущего
                    # и их тоже заливаем
         
                    # влево
         
                    k = 0
                    while True:
                        
                        k += 1
                        # print"  check left: ", i, j-k
                        
                        if a[i,j-1] == H:
                            # print"   pass zero"
                            if i == 0 or j-1 == 0 or i == bottom_border or j-1 == right_border:
                                borders[0] = H
                                # print"    +zero border:", i, j-1 
                            break
                        
                        if (i,j-k) in checked:
                            # print"   pass checked"
                            continue
                        elif j-k < 0:
                            borders[0] = H
                            # print"   left leak added"
                            break
                        elif a[i, j-k] > H:
                            borders[(i, j-k)] = a[i,j-k]
                            # print"   left border added"
                            break
                        else:
                            if not (i, j-k) in floors:
                                # print"   left cell added"
                                floors.add((i, j-k))
#                                added_floors.add((i, j-k))
         
                    # вправо
         
                    k = 0
                    while True:
                        k += 1
                        
                        # print"  check right: ", i, j+k
                        if a[i,j-1] == H:
                            # print"   pass zero"
                            if i == 0 or j-1 ==0 or i == bottom_border or j-1 == right_border:
                                borders[0] = H
                                # print"    +zero border", i, j-1
                            break
                        
                        if (i,j+k) in checked:
                            # print"   pass checked"
                            continue
                        elif j+k == M:
                            borders[0] = H
                            # print"   right leak added"
                            break
                        elif a[i, j+k] > H:
                            borders[(i, j+k)] = a[i,j+k]
                            # print"   right border added"
                            break
                        else:
                            if not (i, j+k) in floors:
                                # print"   right cell added"
                                floors.add((i, j+k))
#                                added_floors.add((i, j+k))
         
                    # вверх
         
                    k = 0
                    while True:
                        k += 1
                        # print"  check top: ", i-k, j
         
                        if a[i-1,j] == H:
                            # print"   pass zero"
                            if i-1 == 0 or j ==0 or i-1 == bottom_border or j == right_border:
                                borders[0] = H
                                # print"    +zero border", i-1, j
                            break
         
                        if (i-k,j) in checked:
                            # print"   pass checked"
                            continue
                        elif i-k < 0:
                            borders[0] = H
                            # print"   top leak added"
                            break
                        elif a[i-k, j] > H:
                            borders[(i-k, j)] = a[i-k,j]
                            # print"   top border added"
                            break
                        else:
                            if not (i-k, j) in floors:
                                # print"   top cell added"
                                floors.add((i-k, j))
#                                added_floors.add((i-k, j))
                            # print "oops"
         
                    # вниз
         
                   
         
                    k = 0
                    while True:
                        k += 1
                        # print"  check bottom: ", i+k, j
         
                        if a[i-1,j] == H:
                            if i-1 == 0 or j ==0 or i-1 == bottom_border or j == right_border:
                                borders[0] = H
                                # print"    +zero border", i-1, j
                            break
         
                        if (i+k,j) in checked:
                            # print"   pass checked"
                            continue
                        elif i+k == N:
                            borders[0] = H
                            # print"   bottom leak added"
                            break
                        elif a[i+k, j] > H:
                            borders[(i+k, j)] = a[i+k,j]
                            # print"   bottom border added"
                            break
                        else:
                            if not (i+k, j) in floors:
                                # print"   bottom cell added"
                                floors.add((i+k, j))
#                                added_floors.add((i+k, j))
                                
                    
                    
                if borders:
                    height = min( [ b for b in borders.values()] )
                    value = (height-H)*len(local_number_floors)
                    
                    if value > 0:
                        global_value += value
                
                    else:
                        # мы не считаем ячейки из которых выливается за границу
                        for item in local_number_floors:
                            global_leak_cells.add(item)
                                
                    
                    # print"="*10
                    # print "borders: ", borders
                    # print "value: ", value
                    # print "n: ", local_number_floors
                    # print"="*10
    
        min_height = H
    
    # print global_value
    
    return global_value
    

if __name__ == '__main__':
    pass
    
       