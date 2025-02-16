from django import forms 

from .models import Courses, Dates 

class CourseForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Courses.objects.all(),
        widget=forms.Select(attrs={"hx-get": "/load_cities/", "hx-target": "#id_date"}))
    date = forms.ModelChoiceField(queryset=Dates.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "name" in self.data:
            courses_id = int(self.data.get("name"))
            self.fields["date"].queryset = Dates.objects.filter(courses_id=courses_id)