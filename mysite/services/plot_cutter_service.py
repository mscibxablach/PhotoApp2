from mysite.plot_cutter.plot_cutter import PlotCutter


class PlotCutterService:
    def __init__(self, plot_cutter):
        self.plot_cutter = plot_cutter

    def get_plot(self, image):

        result = self.plot_cutter.cut_plot_from_memory(image)

        return result

