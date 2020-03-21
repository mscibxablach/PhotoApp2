from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate
from mysite.custom_pdf import CustomPDF
from .forms import PhotoForm, WithoutDBPhotoForm
from .models import Photo

# from PIL import Image
#import numpy as np
import cv2

from mysite.utils.image_utils import ImageUtils
from mysite.plot_cutter.plot_recognizer import PlotRecognizer
from mysite.plot_cutter.plot_cutter import PlotCutter
from mysite.services.plot_bound_service import PlotBoundService
from mysite.plot_bound_detector.ImageProcessor import ImageProcessor
from mysite.plot_bound_detector.PlotBoundDetector import PlotBoundDetector


class Home(TemplateView):
    template_name = 'home.html'


def delete_photo(request, pk):
    if request.method == 'POST':
        photo = Photo.objects.get(pk=pk)
        photo.delete()
    return redirect('photo_list')


# TO DO - ma pobierać dane z formularza i wpychać je do PDFa i potem wypluwać PDFa


def generate_pdf(request, name, surname, description, photo):
    response = HttpResponse(content_type='application/pdf')
    filename = name + "_" + surname + ".pdf"
    response['Content-Disposition'] = 'attachment; filename= "%s"' % filename

    pdf = CustomPDF()
    pdf.set_margins(left=12, top=20)

    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)

    # pdf.form(name, surname, pesel, birth_date, phone, email)
    # # TODO dodac odpiszczelowa dodatkowa
    # # TODO moze poprawic te obrazki
    # pdf.image(pdf.exam_pic(examination), x=120, y=35, w=60, h=75)
    #
    # pdf.description_of_examination(examination, description)
    # TODO ma wczytywac odpowiednio wyciete widmo przeplywu
    # buffer = BytesIO()
    # p = canvas.Canvas(buffer)
    # pic = ImageReader(photo)
    # p.drawImage(pic, 10, 10, mask='auto')
    # p.save()
    # pdf = buffer.getvalue()
    # buffer.close()
    # pdf.image(new_pic,w=120, h=55)
    # pdf.image(image, w=120, h=55)

    pdf.image("test.png", w=120, h=55, type='', link=None, file=photo)
    # pdf.image(photo, w=120, h=55)

    # pdf_result = pdf.output(dest='S').encode('latin-1')
    response.write(pdf_result)
    return response

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def upload_photo_without_DB(request):
    context = {}
    if request.method == 'POST':     # if this is a POST request we need to process the form data
        form = WithoutDBPhotoForm(request.POST, request.FILES)     # create a form instance and populate it with data from the request:
        if form.is_valid():

            photo_bytes = form.cleaned_data['photo'].read()
            photo = ImageUtils.convert_inmemory_file_to_cv2_image(photo_bytes)
            plot_recgonizer = PlotRecognizer()

            plot_cutter = PlotCutter(plot_recgonizer)
            image_processor = ImageProcessor()
            plot_bound_detector = PlotBoundDetector(image_processor)
            plot_bound_service = PlotBoundService(plot_bound_detector)

            result = plot_cutter.cut_plot(photo)

            top, bottom, ratio = plot_bound_service.get_plot_bound_ratio(result)

            result_photo = ImageUtils.convert_cv2_image_to_bytes_io(result)

            return generate_pdf(request, form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['description'], result_photo)

    else:
        form = WithoutDBPhotoForm()
    return render(request, 'upload_photo_without_DB.html', {
        'form': form
    })


