from mysite.utils.image_utils import ImageUtils


class PhotoService:
    def __init__(self, plot_bound_service, plot_cutter_service):
        self.plot_bound_service = plot_bound_service
        self.plot_cutter_service = plot_cutter_service

    def process_image(self, image):
        photo = ImageUtils.convert_inmemory_file_to_cv2_image(image)

        plot = self.plot_cutter_service.get_plot(photo)

        top, bottom, ratio = self.plot_bound_service.get_plot_bound_ratio(plot)

        result_photo = ImageUtils.convert_cv2_image_to_bytes_io(plot)

        return (result_photo, top, bottom, ratio)
