from django.utils import timezone
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Society, Board, Committee, Senate, Activity, Contact
from festivals.models import Festival
from oauth.models import UserProfile
from .forms import ContactForm
from .mixins import NavigationMixin
from photologue.models import Gallery
from events.models import Event
from news.models import News
from .utils import MaintenanceMixin
from decouple import config


class MaintenanceAndNavigationMixin(MaintenanceMixin, NavigationMixin):
    pass


class HomeView(MaintenanceAndNavigationMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        carousel = Gallery.objects.filter(title='HomePageCarousel').filter(is_public=True).first()
        events = Event.objects.filter(society=None)[:5]
        news = News.objects.filter(society=None)[:5]
        festivals = Festival.objects.all()
        gallery = Gallery.objects.filter(title='Home Page Gallery').filter(is_public=True).first()
        context['carousel'] = carousel
        context['event_list'] = events
        context['news_list'] = news
        context['festival_list'] = festivals
        context['gallery'] = gallery
        return context


class BoardView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/board.html'
    model = Board

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        raw = self.object.society_set.filter(published=True)
        societies = raw.filter(stype='S')
        teams = raw.filter(stype='T')
        committee = raw.filter(ctype='C')
        events = Event.objects.filter(society__board=self.object).filter(published=True).filter(
            date__gte=timezone.now())[:5]
        news = News.objects.filter(society__board=self.object)[:5]
        context['society_list'] = societies
        context['team_list'] = teams
        context['committee_list'] = committee
        context['event_list'] = events
        context['news_list'] = news
        return context


class SenateView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/senate.html'
    model = Senate

    def get_context_data(self, **kwargs):
        context = super(SenateView, self).get_context_data(**kwargs)
        return context


class SocietyView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/society.html'
    model = Society

    def get_context_data(self, **kwargs):
        context = super(SocietyView, self).get_context_data(**kwargs)
        events = Event.objects.filter(society=self.object).filter(published=True).filter(date__gte=timezone.now())[:5]
        activities = Activity.objects.filter(society=self.object)
        news = News.objects.filter(society=self.object)[:5]
        members = self.object.core_members.all()
        context['event_list'] = events
        context['activity_list'] = activities
        context['news_list'] = news
        context['member_list'] = members
        return context


class CommitteeView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/committee.html'
    model = Committee

    def get_context_data(self, **kwargs):
        context = super(CommitteeView, self).get_context_data(**kwargs)
        events = Event.objects.filter(committee=self.object).filter(published=True).filter(date__gte=timezone.now())[:5]
        activities = Activity.objects.filter(committee=self.object)
        news = News.objects.filter(committee=self.object)[:5]
        members = self.object.members.all()
        context['event_list'] = events
        context['activity_list'] = activities
        context['news_list'] = news
        context['member_list'] = members
        return context


class ContactView(MaintenanceAndNavigationMixin, CreateView):
    template_name = 'main/contact.html'
    form_class = ContactForm


class ContactListView(MaintenanceAndNavigationMixin, ListView):
    template_name = 'main/contact_list.html'
    model = Contact
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class OfficeView(MaintenanceAndNavigationMixin, TemplateView):
    template_name = 'main/office.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeView, self).get_context_data(**kwargs)
        secretary_roll_no = config('GENERAL_SECRETARY_ROLL', cast=str, default='')
        current_year = str(timezone.now().year)
        context.update({
            'general_secretary': UserProfile.objects.filter(
                roll=secretary_roll_no).first() if UserProfile.objects.filter(
                roll=secretary_roll_no).exists() else None,
            'societies': Society.objects.filter(year=current_year),
            'senate_secretary': Senate.objects.filter(year=current_year).first().senatemembership_set.filter(
                role='SECY').first().userprofile if Senate.objects.filter(
                year=current_year).exists() else None
        })
        return context
