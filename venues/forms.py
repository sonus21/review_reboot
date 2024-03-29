from django import forms
from django_countries.widgets import CountrySelectWidget
from restaurant.utils import get_client_ip
from venues.models import Restaurant, Review, Note, Report, VenueUser, ReportType, Cuisine, Sect, Masjid


class CommonForm(forms.ModelForm):
    """
    this is CommonForm for CommonModel,
    make sure to provide request argument to make it work
    """

    def __init__(self, *args, **kwargs):
        """
        make sure to provide request argument when contruction form
        """
        self.request = kwargs.pop('request', None)
        super(CommonForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        extending base save method for allowing request tracking
        """
        if self.request:
            if self.instance.pk is None:
                self.instance.created_by = self.request.user
            else:
                self.instance.modified_by = self.request.user

            self.instance.modified_ip = get_client_ip(self.request)

        return super(CommonForm, self).save(commit)


class RestaurantForm(CommonForm):
    def clean(self):
        cleaned_data = super(RestaurantForm, self).clean()
        cuisines = cleaned_data.get('cuisines')
        return cleaned_data

    cuisines = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,
        queryset=Cuisine.objects.all(),error_messages={'required': 'Please select a cuisine'})

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'cuisines','about', 'catering', 'delivery', 'alcoholFree',
                  'porkFree', 'muslimOwner', 'location', 'menu', 'city', 'country', 'website', 'address_note',
                  'shop_number']
        widgets = {
            'menu': forms.RadioSelect(),
            'alcoholFree': forms.RadioSelect(),
            'porkFree': forms.RadioSelect(),
            'muslimOwner': forms.RadioSelect(),
            'catering': forms.RadioSelect(),
            'delivery': forms.RadioSelect(),
            'cuisines': forms.Select(),
        }





class AddressForm(forms.Form):
    address = forms.CharField(required=False)
    cuisine = forms.CharField(required=False)
    name = forms.CharField(required=False)


class ReviewForm(CommonForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']


class NoteForm(CommonForm):
    class Meta:
        model = Note
        fields = ['text']


class ReportForm(CommonForm):
    report_type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,
        queryset=ReportType.objects.all())
    class Meta:
        model = Report
        fields = ['report_type', 'note']


class VenueUserForm(CommonForm):
    username = forms.RegexField(max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': 'This value may contain only letters, numbers and '
                         '@/./+/-/_ characters.'})

    class Meta:
        model = VenueUser
        exclude = ('user', 'social_profile')

class ProfileForm(forms.ModelForm):

    username = forms.RegexField(label='Username', max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text='Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.',
        error_messages={
            'invalid': 'This value may contain only letters, numbers and '
                         '@/./+/-/_ characters.'})
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = VenueUser
        fields = (
            'username', 'first_name', 'last_name',
            'sex', 'university', 'info',
        )
        exclude = ('user',)



class MasjidForm(CommonForm):
    def clean(self):
        cleaned_data = super(MasjidForm, self).clean()
        return cleaned_data

    # sect = forms.RadioSelect(queryset=Sect.objects.all())

    class Meta:
        model = Masjid
        fields = ['name', 'address', 'phone', 'sect', 'location', 'city', 'country',  'address_note']

