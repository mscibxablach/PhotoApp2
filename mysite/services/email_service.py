import datetime
from django.core.mail import EmailMessage


class SendEmailService:
    def send_email(self, mail, pdf, filename):
        date = datetime.date.today().__str__()
        email = EmailMessage(
            'Wynikia badnia ultrasonograficznego',
            'Badanie z dnia ' + date,
            'mscibxablach@gmail.com',
            [mail]
        )
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)