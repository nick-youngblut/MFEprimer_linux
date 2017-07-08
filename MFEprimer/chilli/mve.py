#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division

__version__ = '1.0'
__author__  = 'Wubin Qu <quwubin@gmail.com>'
__license__ = 'GPL v3'

import os
import time
import CairoNumberWidth as CNW
import cairo
import GelMobility

def draw_title(ctx, height, width):
    '''Draw title'''
    title = 'Virtual Electrophotogram'

    title_length = 0
    for i in range(len(title)):
        title_length = title_length + CNW.font30[title[i]]

    ctx.move_to(width/2 - title_length/2, 50)
    ctx.set_source_rgb(0, 0, 237)
    ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL)
    ctx.set_font_size(30)
    ctx.show_text(title)

    ISOTIMEFORMAT = '%Y-%m-%d %X'
    title = 'Created by VE @ %s' % time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

    title_length = 0
    for i in range(len(title)):
        title_length = title_length + CNW.font20[title[i]]

    ctx.move_to(width/2 - title_length/2, 80)
    ctx.set_source_rgb(0, 0, 237)
    ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL)
    ctx.set_font_size(20)
    ctx.show_text(title)

    ctx.stroke()

    return ctx

def draw_foot(ctx, height, width, agarose, product_number):
    '''Draw title'''
    title = 'M: Marker DL2000, %s%% agarose gel' % agarose

    title_length = 0
    for i in range(len(title)):
        title_length = title_length + CNW.font20[title[i]]

    ctx.move_to(width/2 - title_length/2, 715)
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL)
    ctx.set_font_size(20)
    ctx.show_text(title)

    ctx.stroke()

    title = '1-%s: PCR amplicons' % (product_number)
    title_length = 0
    for i in range(len(title)):
        title_length = title_length + CNW.font20[title[i]]

    ctx.move_to(width/2 - title_length/2, 738)
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL)
    ctx.set_font_size(20)
    ctx.show_text(title)

    ctx.stroke()

    return ctx

def draw_virtual_elec(ctx, height, width, idname_size, agarose, product_number, size_matrix):
    '''Draw'''
    # Draw slot
    ctx.select_font_face("Times", cairo.FONT_SLANT_NORMAL)
    x = 30 + 80
    y = 160
    for i in range(product_number + 1):
	ctx.set_source_rgba(0, 0, 0, 1.0)
	ctx.rectangle(x, y, 70, 500)
	ctx.fill()
	x = x + 90

    x = 30 + 80
    y = 160
    for i in range(product_number + 1):

	if i == 0:
	    line_title = 'M'
	else:
	    line_title = str(i)

	line_title_length = 0
	for j in range(len(line_title)):
	    line_title_length = line_title_length + CNW.font20[line_title[j]]

	ctx.move_to(x + 35 - line_title_length/2, y-10)
	ctx.set_source_rgb(1, 1, 1)
	ctx.set_font_size(20)
	ctx.show_text(line_title)

	if i == 0:
	    x = x + 90
	    continue

	for size in size_matrix[i-1][1:]:
	    id = str(size_matrix[i-1][0])
	    y1 = GelMobility.cal_mobility(size, gel_conc=agarose, ref_mobility=50, formula='Helling')
	    y1 = y1*13 - 40# 13 is just a amplificationfactor
	    ctx.move_to(x+10, y1)
	    ctx.set_line_width(6)
	    ctx.line_to(x + 60, y1)

	    '''
	    x2 = 30 + 80 + 90 * (product_number + 1) + 10
	    ctx.move_to(x2, y1)
	    ctx.set_line_width(6)
	    ctx.line_to(x2 + 50, y1)
	    ctx.stroke()
	    '''

	    x3 = 30 + 80 + 90 * (product_number + 1) 
	    ctx.move_to(x3, y1+4)
	    bp_num = str(size).rjust(4) + ' bp'
	    #bp_num = size + ' bp'
	    ctx.show_text(bp_num)
	    ctx.stroke()

	    y4 = y + 525
	    id_length = 0
	    for k in range(len(id)):
		id_length = id_length + CNW.font20[id[k]]

	    ctx.move_to(x + 35 - id_length/2, y4)
	    ctx.set_source_rgb(1, 1, 1)
	    ctx.set_font_size(20)
	    ctx.show_text(id)


	x = x + 90

    
    # Mark 2000 kb
    mark_size_list = [2000, 1000, 750, 500, 250, 100]
    mark_size_dict = {
	2000 : '2000 bp',
	1000 : '1000 bp',
	750  : '  750 bp',
	500  : '  500 bp',
	250  : '  250 bp',
	100  : '  100 bp',
    }
    
    ctx.set_source_rgb(1, 1, 1)
    for mark_size in mark_size_list:
	x = 30 + 80 + 10
	y = GelMobility.cal_mobility(mark_size, gel_conc=agarose, ref_mobility=50, formula='Helling')
	y = y*13 - 40# 13 is just a amplificationfactor

	ctx.move_to(x, y)
        #x, y = ctx.get_current_point()
        ctx.set_line_width(6)
        ctx.line_to(x + 50, y)
        ctx.stroke()

        ctx.move_to(x - 90, y+4)
	ctx.show_text(mark_size_dict[mark_size])
        ctx.stroke()	
	
    return ctx

def paint(size_matrix, agarose, pic_path):
    '''Paint the virtual electrophotogram '''
    idname_set = set()
    for size_list in size_matrix:
	for size in size_list[1:]:
	    idname_set.add(size)

    idname_size = sorted(list(idname_set))
    size_matrix.append(idname_size)

    height = 750
    # Marker line width: 80
    product_number = len(size_matrix) - 1
    width = (product_number + 2) * 90 + 80 + 60 + 80

    # Set cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Mask
    ctx.set_source_rgba(0, 0, 0, 0.9)
    ctx.rectangle(0, 100, width, height)
    ctx.fill()

    ctx = draw_title(ctx, height, width)
    ctx = draw_virtual_elec(ctx, height, width, idname_size, agarose, product_number, size_matrix)
    ctx = draw_foot(ctx, height, width, agarose, product_number)

    #output a PNG file
    try:
	surface.write_to_png(pic_path)
	return None
    except:
	return 'Virtual Electrophoresis Error'
    #name = 'a.png'
    #surface.write_to_png(name)
    #return name

def main ():
    size_matrix = [
	['1 h', 100, 140, 200, 300, 400, 600, 1500],
	['2 h', 100, 140, 200, 300, 400, 600, 1500],
	['4 h', 100, 140, 200, 600, 900, 1100, 1500],
	['8 h', 100, 140, 200, 600, 900, 1100, 1500],
	['16 h', 200, 300, 400, 600, 900, 1100, 1500],
	['32 h', 200, 300, 400, 600, 900, 1100, 1500],
	]

    agarose = 1
    pic_path = 've.png'
    paint(size_matrix, agarose, pic_path)


if __name__ == '__main__':
    main()

