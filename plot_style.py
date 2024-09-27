import ROOT as rt
import matplotlib.pyplot as plt

# Plot display/adjustments.
# This sets a bunch of colors, for both PyROOT and matplotlib.
class PlotStyle:
    def __init__(self, mode = 'dark'):
        if(mode != 'dark'): mode = 'light'

        if(mode == 'light'):
            self.main  = rt.kBlack
            self.canv  = rt.kWhite
            self.text  = rt.kBlack
            self.curve = rt.kBlue
            self.palette = rt.kCool

            self.text_plt = 'xkcd:black'
            self.canv_plt = 'xkcd:white'
            self.main_plt = 'xkcd:black'
            self.grid_plt = '0.65'
            self.curve_plt = 'xkcd:blue'

        elif(mode == 'dark'):
            self.main  = rt.TColor.GetColor(52,165,218)
            self.canv  = rt.TColor.GetColor(34,34,34)
            self.text  = rt.kWhite
            self.curve = rt.TColor.GetColor(249,105,4)
            self.palette = rt.kBlackBody

            self.text_plt = 'xkcd:white'
            self.canv_plt = '#222222' # dark grey
            self.main_plt = '#34a5da' # light blue
            self.grid_plt = '0.65'
            self.curve_plt = '#f96904' # orange

        # list of matplotlib colors
        self.colors = [
            'xkcd:medium purple', # first pass through rainbow
            'xkcd:periwinkle blue',
            'xkcd:aqua blue',
            'xkcd:electric lime',
            'xkcd:kelly green',
            'xkcd:tangerine',
            'xkcd:wheat',
            'xkcd:bordeaux',
            'xkcd:bright red',
            'xkcd:baby purple', # second pass through rainbow
            'xkcd:dark teal',
            'xkcd:true blue',
            'xkcd:very light green',
            'xkcd:macaroni and cheese',
            'xkcd:burnt orange',
            'xkcd:brick red',
            'xkcd:salmon'
         ]
        #self.colors.reverse() # put the reds first -- purple can be comparitively hard to see on dark background

        # list of matplotlib linestyles
        self.linestyles = [
            '-',
            ':',
            '-.'
        ]

    def SetStyle(self):
        rt.gStyle.SetAxisColor(self.main,'xyz')
        rt.gStyle.SetGridColor(self.main)
        rt.gStyle.SetLineColor(self.main)
        rt.gStyle.SetFrameLineColor(self.main)

        rt.gStyle.SetPadColor(self.canv)
        rt.gStyle.SetCanvasColor(self.canv)
        rt.gStyle.SetLegendFillColor(self.canv)

        rt.gStyle.SetTitleTextColor(self.text)
        rt.gStyle.SetTitleColor(self.text, 'xyz')
        rt.gStyle.SetLabelColor(self.text, 'xyz')
        rt.gStyle.SetStatTextColor(self.text)
        rt.gStyle.SetTextColor(self.text)

        rt.gStyle.SetPalette(self.palette)

    def SetStylePlt(self, ax):

        # canvas color
        ax.set_facecolor(self.canv_plt)

        # tick colors (marks, then tick labels)
        ax.tick_params(axis='both',colors=self.main_plt, which='major')
        ax.tick_params(axis='both',colors=self.text_plt, which='minor')
        plt.setp(ax.get_xticklabels(), color=self.text_plt)
        plt.setp(ax.get_yticklabels(), color=self.text_plt)

        # axis spines
        for spine in ['bottom','top','left','right']:
            ax.spines[spine].set_color(self.main_plt)

        # axis titles
        ax.xaxis.label.set_color(self.text_plt)
        ax.yaxis.label.set_color(self.text_plt)

        # plot title
        ax.title.set_color(self.text_plt)

        # grid color
        ax.grid()

        # face color
        ax.set_facecolor(self.canv_plt)