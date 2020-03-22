from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import datetime

from .forms import WithoutDBPhotoForm

from mysite.utils.image_utils import ImageUtils
from mysite.plot_cutter.plot_recognizer import PlotRecognizer
from mysite.plot_cutter.plot_cutter import PlotCutter
from mysite.services.plot_bound_service import PlotBoundService
from mysite.plot_bound_detector.ImageProcessor import ImageProcessor
from mysite.plot_bound_detector.PlotBoundDetector import PlotBoundDetector

from mysite.generate_pdf.generate_pdf import CustomPDF

#TODO dodac polska czcionke

date = datetime.date.today().__str__()


class Home(TemplateView):
    template_name = 'home.html'


def create_pdf(name, surname, pesel, birth_date, phone, email, examination, description, photo):
    filename = name + "_" + surname + ".pdf"
    pdf = CustomPDF()
    pdf.set_margins(left=12, top=20)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.form(name, surname, pesel, birth_date, phone, email)

    # TODO moze poprawic te obrazki
    pdf.image(pdf.exam_pic(examination), x=120, y=35, w=60, h=75)

    pdf.description_of_examination(examination, description)
    pdf.image("pdf.png", w=120, h=55, type='', link=None, file=photo)
    pdf_result = pdf.output(filename, dest='S')
    return pdf_result


def send_email(mail, pdf):
    email = EmailMessage(
        'Wynikia badnia ultrasonograficznego',
        'Badanie z dnia ' + date,
        'mscibxablach@gmail.com',
        [mail]
    )
    email.attach('test.pdf', pdf, 'application/pdf')
    email.send(fail_silently=False)


def save_pdf_to_response(pdf_result, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "%s"' % filename
    response.write(pdf_result)
    return response


def photo_functions(photo):
    photo_bytes = photo.read()
    photo = ImageUtils.convert_inmemory_file_to_cv2_image(photo_bytes)
    plot_recgonizer = PlotRecognizer()

    plot_cutter = PlotCutter(plot_recgonizer)
    image_processor = ImageProcessor()
    plot_bound_detector = PlotBoundDetector(image_processor)
    plot_bound_service = PlotBoundService(plot_bound_detector)

    result = plot_cutter.cut_plot(photo)

    top, bottom, ratio = plot_bound_service.get_plot_bound_ratio(result)

    result_photo = ImageUtils.convert_cv2_image_to_bytes_io(result)
    return result_photo


def upload_photo_without_DB(request):
    context = {}
    if request.method == 'POST':     # if this is a POST request we need to process the form data
        form = WithoutDBPhotoForm(request.POST, request.FILES)     # create a form instance and populate it with data from the request:
        if form.is_valid():
            result = photo_functions(form.cleaned_data['photo'])
            pdf_saved = create_pdf(form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['pesel'], form.cleaned_data['birth_date'], form.cleaned_data['phone'], form.cleaned_data['email'], form.cleaned_data['examination'], form.cleaned_data['description'], result)
            #TODO nie pobiera wygenerowanego pdfa tylko na sztywno wpisany. Ma pobierac wygenerowanego
            send_email(form.cleaned_data['email'], pdf_saved)
            return save_pdf(pdf_saved, 'test.pdf')
    else:
        form = WithoutDBPhotoForm()
    return render(request, 'upload_photo_without_DB.html', {
        'form': form
    })


