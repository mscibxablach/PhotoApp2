import datetime
from email.message import EmailMessage


class SendEmailService:

    def send_email(self, mail, pdf):
        date = datetime.date.today().__str__()
        email = EmailMessage(
            'Wynikia badnia ultrasonograficznego',
            'Badanie z dnia ' + date,
            'mscibxablach@gmail.com',
            [mail]
        )
        email.attach('test.pdf', pdf, 'application/pdf')
        email.send(fail_silently=False)