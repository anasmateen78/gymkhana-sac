from django.utils import timezone
from graphene import relay, Field
from photologue.models import Gallery, Photo

from events.models import Event
from events.schema import EventNode
from gallery.schema import ImageType
from gymkhana_sac.utils import build_image_types
from main.models import Society, Board, Activity, Committee, SacKeyPeople, Membership
from graphene_django import DjangoObjectType, DjangoConnectionField

from news.models import News
from news.schema import NewsNode


class BoardNode(DjangoObjectType):
    cover = Field(ImageType)
    upcoming_events = DjangoConnectionField(EventNode, max_limit=5)
    past_news = DjangoConnectionField(NewsNode, max_limit=5)

    class Meta:
        model = Board
        fields = (
            'name', 'slug', 'president', 'vice_president', 'description', 'society_set', 'committee_set', 'cover', 'report_link', 'constitution_link',
            'is_active',
            'gallery', 'custom_html')
        filter_fields = ('slug', 'is_active')
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))

    def resolve_committee_set(self, info, *args, **kwargs):
        return self.committee_set.filter(published=True)

    def resolve_society_set(self, info, *args, **kwargs):
        return self.society_set.filter(published=True)

    def resolve_upcoming_events(self, info, *args, **kwargs):
        return Event.objects.filter(society__board=self).filter(published=True).filter(date__gte=timezone.now())[
               :kwargs.get('first', 5)]

    def resolve_past_news(self, info, *args, **kwargs):
        return News.objects.filter(society__board=self)[:kwargs.get('first', 5)]


class SocietyNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = Society
        fields = '__all__'
        filter_fields = ('slug', 'published')
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))


class CommitteeNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = Committee
        fields = '__all__'
        filter_fields = ('slug', 'published')
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))

class MembershipNode(DjangoObjectType):
    class Meta:
        model = Membership
        fields = '__all__'
        filter_fields = ('role',)
        interfaces = (relay.Node,)

class ActivityNode(DjangoObjectType):
    class Meta:
        model = Activity
        fields = '__all__'
        interfaces = (relay.Node,)


class GalleryNode(DjangoObjectType):
    class Meta:
        model = Gallery
        exclude = ('board_set', 'society_set', 'committee_set')
        filter_fields = ('slug',)
        interfaces = (relay.Node,)


class GalleryPhoto(DjangoObjectType):
    image = Field(ImageType)

    class Meta:
        model = Photo
        exclude = ('galleries',)
        interfaces = (relay.Node,)

    def resolve_image(self, info):
        return ImageType(sizes=build_image_types(request=info.context, image=self.image, key_set='image'))


class SacKeyPeopleNode(DjangoObjectType):
    class Meta:
        model = SacKeyPeople
        fields = '__all__'
        filter_fields = ('gen_secy', 'gen_secy_sac')
        interfaces = (relay.Node,)
