#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 20.07.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 
 
import numpy
from copy import copy

 
def get_volume(a):
    '''
    @param a: any array or list
    '''

    # print "\n",a

    N = len(a)
    M = len(a[0])
    
    right_border = M-1
    bottom_border = N-1 
    global_value = 0
    
    # print"Size: ", N, M
    
    avaliable_heights = set()
    points = {}
    
    for i in xrange(0,N):
        for j in xrange(0,M):
            avaliable_heights.add(a[i][j])
            points.setdefault(a[i][j], [])
            if 0<i<bottom_border and 0<j<right_border:
                points[a[i][j]].append((i,j))
    
    avaliable_heights = list(avaliable_heights)
    avaliable_heights.sort()
    global_checked = set()
    
    for H in avaliable_heights[:-1]:
        
#        # print "height cheking: ", H

        checked = set()
 
        for gi,gj in points[H]:
        
            if (gi,gj) in checked or (gi, gj) in global_checked:
                continue
            
            local_number_floors = set()
            
     
            i = gi
            j = gj
            
            borders = [avaliable_heights[-1]]
            
            
            def check_line(i,j):
                # print "  checking: ",i,j
                
                if a[i][j] == H:
                    if i == 0 or j == 0 or i == bottom_border or j == right_border:  
                        borders[0] = H
                        checked.add((i,j))
                        # print "    leak found: ",i,j
                        return
                    if not (i, j) in local_number_floors:
                        local_number_floors.add((i, j))
                        checked.add((i,j))
                        # print "    new cell: ",i,j
                        if not (i-1,j) in checked:
                            check_line(i-1,j)
                        if not (i+1,j) in checked:
                            check_line(i+1,j)
                        if not (i,j+1) in checked:
                            check_line(i,j+1)
                        if not (i,j-1) in checked:
                            check_line(i,j-1)
                        return
                    return
                elif a[i][j] > H:
                    # print "    new border: ",i,j
                    borders[0] = min(borders[0], a[i][j])
                    checked.add((i,j))
                    
                    return
                else:
                    if not (i, j) in local_number_floors:
                        local_number_floors.add((i,j))
                        checked.add((i,j))
                        # print "    new old cell: ",i,j
                        if not (i-1,j) in checked:
                            check_line(i-1,j)
                        if not (i+1,j) in checked:
                            check_line(i+1,j)
                        if not (i,j+1) in checked:
                            check_line(i,j+1)
                        if not (i,j-1) in checked:
                            check_line(i,j-1)
                return
                    
                
            if not (i,j) in checked:
                check_line(i,j)
           
            if borders[0] > H:
                value = (borders[0]-H)*len(local_number_floors)
                
                if value > 0:
                    global_value += value
                else:
                    global_checked.update(local_number_floors)
              

    
    return global_value

