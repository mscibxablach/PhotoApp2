from django import forms
import re

#TODO ma zwracać w pdf te nazwę z nie numerek
VEINS =(
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
      raise forms.ValidationError("Niepoprawna wartość pola")


def check_pesel(pesel):
    pesel_array = [int(i) for i in str(pesel)]
    check = pesel_array[0] * 1 + pesel_array[1] * 3 + pesel_array[2] * 7 + pesel_array[3] * 9 + pesel_array[4] * 1 + \
            pesel_array[5] * 3 + pesel_array[6] * 7 + pesel_array[7] * 9 + pesel_array[8] * 1 + pesel_array[9] * 3
    check_array = [int(i) for i in str(check)]
    result = 10 - check_array[2]

    if ((result != pesel_array[10]) or (pesel.isdigit()==False)):
        raise forms.ValidationError("Niepoprawna wartość pola")



class WithoutDBPhotoForm(forms.Form):
    name = forms.CharField(label='Imię', max_length=100, validators=[check_size, check_if_literal, ])
    surname = forms.CharField(label='Nazwisko', max_length=100, validators=[check_size, check_if_literal, ])
    pesel = forms.CharField(label='Pesel', max_length=11, min_length=11, validators=[check_pesel, ])
    birth_date = forms.CharField(label='Data urodzenia')
    phone = forms.CharField(label='Numer telefonu', max_length=15)
    email = forms.EmailField(label='E-mail', max_length=100)
    examination = forms.ChoiceField(label="Rozpoznanie", choices=VEINS)
    description = forms.CharField(label='Opis', max_length=100)
    photo = forms.FileField(label='Zdjęcie')