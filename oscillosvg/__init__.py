#!/usr/bin/env python

import svgwrite
from svgwrite import cm, mm

class oscilloSVG(object):

    def __init__(self, width=1200.0, style='black'):
        """
        width in px, height and font size will scale automatically
        """
        self.style = style
        self.x_dimensions_svg, self.y_dimensions_svg = width, width*0.5
        self.border = 0.05*width
        self.border_top = 2 * self.border
        self.w_screen, self.h_screen = self.x_dimensions_svg - 2*self.border, self.y_dimensions_svg - self.border - self.border_top
        self.x_offset_screen, self.y_offset_screen = self.border, self.border_top
        self.dwg = svgwrite.Drawing(size=(self.x_dimensions_svg, self.y_dimensions_svg))

    def draw_title(self, title='Oscilloscope Screen'):
        self.dwg.add(self.dwg.text(title, x=[self.x_dimensions_svg/2], y=[self.border_top*2/3], text_anchor='middle'))
    
    def draw_frame(self):
        if self.style == 'black':
            bgcolor = 'black'
        else:
            bgcolor = 'none'
        self.dwg.add(self.dwg.rect((self.x_offset_screen, self.y_offset_screen), (self.w_screen, self.h_screen), stroke='gray', stroke_width=3, fill=bgcolor))

    def draw_channel_data(self, channel1=None, channel2=None, triggerlevel=0.0):
        assert type(channel1) in [type(None), list, zip]
        assert type(channel2) in [type(None), list, zip]
        if channel1:
            channel1 = list(channel1)
            xvals = [point[0] for point in channel1]
            yvals = [point[1] for point in channel1]
            #data = zip(*list(channel1))
            #xvals = data[0]
            #yvals = data[1]
            # thinning
            xvals = xvals[::5]
            yvals = yvals[::5]
            # rescaling
            xfrom, xto = self.x_offset_screen, self.w_screen + self.x_offset_screen
            xmin, xmax = min(xvals), max(xvals)
            scaling = float(xto-xfrom) / float(xmax-xmin)
            xvals = [(val - xmin) * scaling + xfrom for val in xvals]
            yfrom, yto = self.y_offset_screen, self.h_screen + self.y_offset_screen
            ymin, ymax = min(yvals), max(yvals)
            scaling = float(yto-yfrom) / float(ymax-ymin)
            yvals = [(val - ymin) * scaling + yfrom for val in yvals]
            data = zip(xvals, yvals)
            self.dwg.add(self.dwg.polyline(data, stroke='yellow', stroke_width=1, fill='none'))
            tlevel = triggerlevel
            tlevel = (tlevel - ymin) * scaling + yfrom
            self.dwg.add(self.dwg.line((xfrom, tlevel), (xto, tlevel), stroke_dasharray='5,5', stroke='gray', stroke_width="2"))
        if channel2:
            raise NotImplemented('channel 2 not yet implemented')

    def get_svg(self)
        return self.dwg.tostring()

