from mysite.plot_cutter.plot_cutter import PlotCutter


class PlotCutterService:
    def __init__(self, plot_cutter):
        self.plot_cutter = plot_cutter

    def get_plot(self, image_path):

        image = PlotCutter.cut_plot(image_path)

        return image

