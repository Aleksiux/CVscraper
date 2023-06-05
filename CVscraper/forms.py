from django import forms

locations = (
    ('kaunas', 'Kaunas'),
    ('vilnius', 'Vilnius'),
    ('klaipeda', 'Klaipeda'),
    ('alytus', 'Alytus'),
    ('birstonas', 'Birstonas'),
    ('jonava', 'Jonava'),
)


# class CvSearchForm(forms.Form):
#     location_select = forms.MultipleChoiceField(
#         choices=locations,
#         widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
#     )

class CvSearchForm(forms.Form):
    options = locations
    countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=options)