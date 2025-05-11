from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')

class CivilPackForm(forms.Form):
    ss_number = forms.CharField(label='SS Number', max_length=100)
    substation_number = forms.CharField(label='Substation Number', max_length=100)
    job_code = forms.CharField(label='Job Code', max_length=100)
    scheme_reference = forms.CharField(label='Scheme Reference', max_length=100)
    wayleave_number = forms.CharField(label='Wayleave Number', max_length=100)
    passed_date = forms.DateField(label='Passed Date', widget=forms.DateInput(attrs={'type': 'date'}))
    road_level_number = forms.CharField(label='Road Level Number', max_length=100)
    plot_number = forms.CharField(label='Plot Number', max_length=100)
    substation_tx_count = forms.CharField(label='How many tx is the substation', max_length=50)
    waylvb_count = forms.CharField(label='How many way LVB', max_length=50)
    tx_size = forms.CharField(label='TX Size', max_length=100)
