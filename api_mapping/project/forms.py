


from django import forms
from .models import Project_team, Type_color, Subtype

class ProjectForm(forms.ModelForm):
    api = forms.CharField(required=False)  # Add api field
    mapping = forms.CharField(required=False)  # Add mapping field
    mapping_type = forms.ChoiceField(choices=[('single_input', 'Single Input'), ('excel_file', 'Excel File')], required=True)
    source_type = forms.ModelChoiceField(queryset=Type_color.objects.all(), required=True)
    source_subtype = forms.ModelChoiceField(queryset=Subtype.objects.none(), required=False)
    destination_type = forms.ModelChoiceField(queryset=Type_color.objects.all(), required=True)
    destination_subtype = forms.ModelChoiceField(queryset=Subtype.objects.none(), required=False)
    excel_file = forms.FileField(required=False) 
    flow_num=forms.CharField(required=True)
    class Meta:
        model = Project_team
        fields = ['project_name', 'project_manager', 'mapping_type', 'source_type', 'source_subtype', 'destination_type', 'destination_subtype', 'api', 'mapping', 'excel_file','flow_num']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        if 'mapping_type' in self.data:
            mapping_type = self.data.get('mapping_type')
            if mapping_type == 'single_input':
                self.fields['source_type'].required = True
                self.fields['destination_type'].required = True
                
            elif mapping_type == 'excel_file':
                self.fields['excel_file'].required = True
                self.fields['source_type'].required = False
                self.fields['destination_type'].required = False


        if 'source_type' in self.data:
            try:
                type_id = int(self.data.get('source_type'))
                self.fields['source_subtype'].queryset = Subtype.objects.filter(type_id=type_id).order_by('subtype')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['source_subtype'].queryset = Subtype.objects.filter(type=self.instance.source_type).order_by('subtype')

        if 'destination_type' in self.data:
            try:
                type_id = int(self.data.get('destination_type'))
                self.fields['destination_subtype'].queryset = Subtype.objects.filter(type_id=type_id).order_by('subtype')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['destination_subtype'].queryset = Subtype.objects.filter(type=self.instance.destination_type).order_by('subtype')

    def clean(self):
        cleaned_data = super().clean()
        mapping_type = cleaned_data.get('mapping_type')

        if mapping_type == 'single_input':
            if not cleaned_data.get('source_type'):
                self.add_error('source_type', 'This field is required for single input.')
            if not cleaned_data.get('destination_type'):
                self.add_error('destination_type', 'This field is required for single input.')
        elif mapping_type == 'excel_file':
            if not self.files.get('excel_file'):
                self.add_error('excel_file', 'This field is required for excel file input.')

        return cleaned_data




# forms.py
from django import forms
from .models import Type_color, Subtype

# class UpdateNodeForm(forms.Form):
#     current_name = forms.CharField(label='Current Name', max_length=100)
#     new_name = forms.CharField(label='New Name', max_length=100)
#     new_type = forms.ModelChoiceField(queryset=Type_color.objects.all(), label='New Type')
#     new_subtype = forms.ModelChoiceField(queryset=Subtype.objects.all(), label='New Subtype')
