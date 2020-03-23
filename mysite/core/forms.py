from django import forms
import re
from dobwidget import DateOfBirthWidget

# TODO ma zwracać w pdf te nazwę z nie numerek
VEINS = (
    ("1", "Żyła odpiszczelowa - I st."),
    ("2", "Żyła odpiszczelowa - II st."),
    ("3", "Żyła odpiszczelowa - III st."),
    ("4", "Żyła odpiszczelowa - IV st."),
    ("5", "Żyła odstrzałkowa - I st."),
    ("6", "Żyła odstrzałkowa - II st."),
    ("7", "Żyła odstrzałkowa - III st."),
)


def check_size(value):
    if len(value) < 2:
        raise forms.ValidationError("Niepoprawna wartość pola.")


def check_if_literal(string):
    string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (any(char.isdigit() for char in string) or (string_check.search(string) != None)):
        raise forms.ValidationError("Niepoprawna wartość pola.")


def check_if_digits(string):
    string_check = re.compile('^[0-9]*$')

    if ((string_check.search(string) == None)):
        raise forms.ValidationError("Niepoprawna wartość pola.")


def check_pesel(pesel):
    string_check = re.compile('^[0-9]*$')

    if ((string_check.search(pesel) == None)):
        raise forms.ValidationError("Niepoprawna wartość pola.")
    pesel_array = [int(i) for i in str(pesel)]
    check = pesel_array[0] * 1 + pesel_array[1] * 3 + pesel_array[2] * 7 \
            + pesel_array[3] * 9 + pesel_array[4] * 1 + pesel_array[5] * 3 + pesel_array[6] * 7 + pesel_array[7] * 9 + \
            pesel_array[8] * 1 + pesel_array[9] * 3
    check_array = [int(i) for i in str(check)]
    result = 10 - check_array[2]

    if ((result != pesel_array[10])):
        raise forms.ValidationError("Niepoprawna wartość pola.")


def check_phone(number):
    number_check = re.compile(r'^(([+]\d{2})|\d{4}){0,1}[-|\s]{0,1}\d{3}[-|\s]{0,1}\d{3}[-|\s]{0,1}\d{3}$')

    if ((number_check.search(number) == None)):
        raise forms.ValidationError(
            "Niepoprawna wartość pola. Numer powinien być w postaci '(+48/0048)-xxx-xxx-xxx' lub '(+48/0048) xxx xxx xxx' lub '(+48/0048)xxxxxxxxx'.")


class WithoutDBPhotoForm(forms.Form):
    name = forms.CharField(label='Imię', max_length=100, validators=[check_size, check_if_literal], required=True)
    surname = forms.CharField(label='Nazwisko', max_length=100, validators=[check_size, check_if_literal], required=True)
    pesel = forms.CharField(label='Pesel', max_length=11, min_length=11, validators=[check_pesel], required=True)
    birth_date = forms.CharField(label='Data urodzenia', widget=DateOfBirthWidget(order='DMY'), required=True)
    phone = forms.CharField(label='Numer telefonu', max_length=16, validators=[check_phone], required=True)
    email = forms.EmailField(label='E-mail', max_length=100, required=True)
    examination = forms.ChoiceField(label="Rozpoznanie", choices=VEINS, required=True)
    description = forms.CharField(label='Opis', max_length=520, widget=forms.Textarea, required=False)
    photo = forms.FileField(label='Zdjęcie', required=True)
