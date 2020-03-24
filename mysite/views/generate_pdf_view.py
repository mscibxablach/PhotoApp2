from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import datetime
from mysite.services.email_service import SendEmailService
from mysite.core.forms import WithoutDBPhotoForm

from mysite.utils.image_utils import ImageUtils
from mysite.plot_cutter.plot_recognizer import PlotRecognizer
from mysite.plot_cutter.plot_cutter import PlotCutter
from mysite.services.plot_bound_service import PlotBoundService
from mysite.plot_bound_detector.ImageProcessor import ImageProcessor
from mysite.plot_bound_detector.PlotBoundDetector import PlotBoundDetector
from mysite.services.plot_cutter_service import PlotCutterService
from mysite.generate_pdf.generate_pdf import CustomPDF
from mysite.services.photo_service import PhotoService

# TODO dodac polska czcionke

date = datetime.date.today().__str__()


class GeneratePDFForm(View):
    template_name = 'upload_photo_without_DB.html'
    form_class = WithoutDBPhotoForm

    def __init__(self):
        image_processor = ImageProcessor()
        plot_bound_detector = PlotBoundDetector(image_processor)
        plot_recognizer = PlotRecognizer()
        plot_cutter = PlotCutter(plot_recognizer)
        plot_bound_service = PlotBoundService(plot_bound_detector)
        plot_cutter_service = PlotCutterService(plot_cutter)

        self.email_service = SendEmailService()
        self.photo_service = PhotoService(plot_bound_service, plot_cutter_service)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            photo_bytes = form.cleaned_data['photo'].read()
            result_photo, top, bottom, ratio = self.photo_service.process_image(photo_bytes)

            pdf_saved = self.create_pdf(form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['pesel'],
                                   form.cleaned_data['birth_date'], form.cleaned_data['phone'],
                                   form.cleaned_data['email'], form.cleaned_data['examination'],
                                   form.cleaned_data['description'], result_photo)

            self.email_service.send_email(form.cleaned_data['email'], pdf_saved)

            return self.save_pdf_to_response(pdf_saved,
                                        form.cleaned_data['name'] + "_" + form.cleaned_data['surname'] + ".pdf")

        return render(request, self.template_name, {'form': form})

    def create_pdf(self, name, surname, pesel, birth_date, phone, email, examination, description, photo):
        filename = name + "_" + surname + ".pdf"
        pdf = CustomPDF()
        pdf.set_margins(left=12, top=20)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.form(name, surname, pesel, birth_date, phone, email)
        pdf.description_of_examination(description)
        pdf.description_of_diagnosis(examination)

        # TODO moze poprawic te obrazki
        pdf.image(pdf.exam_pic(examination), x=140, y=195, w=60, h=75)
        pdf.image("pdf.png", y=195, w=120, h=55, type='', link=None, file=photo)
        pdf_result = pdf.output(filename, dest='S')
        return pdf_result


    def save_pdf_to_response(self, pdf_result, filename):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename= "%s"' % filename
        response.write(pdf_result)
        return response