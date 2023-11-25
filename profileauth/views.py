from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountInformationEditForm
from .models import User, ProfileImage
from django.views.generic.edit import FormMixin


class Profile(LoginRequiredMixin, generic.TemplateView):
    """
    Profile view that requires login.
    """
    template_name = 'profile/profile.html'


class AccountInformation(LoginRequiredMixin, generic.TemplateView):
    """
    Account information view that requires login.
    """
    template_name = 'profile/account_information.html'

    def get_context_data(self, **kwargs):
        """
        Get context data for the template.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile_images'] = user.profile_images.all()
        return context


class AccountInformationEditView(LoginRequiredMixin, generic.UpdateView, FormMixin):
    """
    Account information edit view that requires login.
    """
    model = User
    form_class = AccountInformationEditForm
    template_name = 'profile/account_information_edit.html'
    success_url = reverse_lazy('profileauth:account_information')

    def __init__(self, *args, **kwargs):
        """
        Initialize the view.
        """
        super().__init__(*args, **kwargs)
        self.object = None

    def get_object(self, queryset=None):
        """
        Get the object this view is displaying.
        """
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        self.object = self.get_object()
        form = self.get_form()
        profile_images = self.object.profile_images.all()
        return self.render_to_response(
            self.get_context_data(form=form, profile_images=profile_images)
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.save(self.request)
        response = super().form_valid(form)
        self._process_profile_images()
        return response

    def _process_profile_images(self):
        """
        Process profile images.
        """
        self._update_existing_images()
        self._add_new_images()
        self._delete_images()

    def _update_existing_images(self):
        """
        Update existing images.
        """
        for image in self.object.profile_images.all():
            alt_name = f"image_{image.id}_alt"
            if alt_name in self.request.POST:
                image.alt = self.request.POST[alt_name]
                image.save()

    def _add_new_images(self):
        """
        Add new images.
        """
        new_images = self.request.FILES.getlist('new_images')
        for image_file in new_images:
            ProfileImage.objects.create(profile=self.object, image_file=image_file)

    def _delete_images(self):
        """
        Delete images.
        """
        deleted_images = self.request.POST.getlist('deleted_images')
        for image_id in deleted_images:
            image = ProfileImage.objects.get(id=image_id)
            image.delete()
