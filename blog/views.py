import json
from _operator import attrgetter
from functools import reduce
from itertools import chain
from operator import or_

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from accounts.models import Profile
from blog.decorators import ajax_required
from blog.forms import  PhotoForm, AlbumForm
from blog.models import Photo, Like,  Album


class AddPhoto(CreateView, LoginRequiredMixin):
    template_name = 'blog/photos/photo/create.html'
    form_class = PhotoForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        image = Photo()
        image.user = self.request.user
        image.image_obj = self.request.FILES.get('photo')
        if form.fields['description']:
            image.description = form.fields['description']
        image.save()
        return HttpResponseRedirect(self.success_url)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    form_class = PhotoForm
    template_name = 'blog/photos/photo/create.html'

    def get_success_url(self):
        return reverse('blog:photos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'photos'
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.get_success_url())


def photo_detail(request, id):
    photo = get_object_or_404(Photo, id=id)
    total_likes = photo.likes.count()
    return render(request,
                  'blog/photos/photo/detail.html',
                  {'section': 'photos',
                   'photo': photo,
                   'total_likes': total_likes, })


@ajax_required
@login_required
@require_POST
def photo_like(request):
    photo_id = request.POST.get('id')
    action = request.POST.get('action')
    if photo_id and action:
        try:
            photo = Photo.objects.get(id=photo_id)
            if action == 'like':
                Like.objects.create(photo=photo, user=request.user)
            else:
                Like.objects.get(photo=photo, user=request.user).delete()
            return JsonResponse({'status': 'ok'})
        except Photo.DoesNotExist:
            return JsonResponse({'status': 'ok', })
    return JsonResponse({'status': 'ok'})


@login_required
def image_list(request):
    photos = Photo.objects.all()
    paginator = Paginator(photos, 8)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        photos = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'blog/photos/photo/list_ajax.html',
                      {'section': 'photos', 'photos': photos})

    return render(request,
                  'blog/photos/photo/list.html',
                  {'section': 'photos', 'photos': photos})


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/photos/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # get user
        user = self.request.user
        # get follows
        follows = user.followers.all()
        if len(follows) > 0:
            # get follows images limit 50
            feed_post_amount = 25
            images_buddies = Photo.objects.prefetch_related('likes').filter(
                reduce(or_, [Q(user_id=c.id) for c in follows])).order_by('-posted_on')[:feed_post_amount]
        return ctx


class FollowersView(ListView):
    model = Profile
    template_name = 'blog/followers.html'
    # simple pagination
    paginate_by = 5

    def get_object(self):
        """
        Get Profile object
        :return: Profile object
        """
        return get_object_or_404(Profile, username=self.kwargs['username'])

    def get_queryset(self):
        """
        Update queryset to show profile followers.
        :return followers queryset
        """
        queryset = Profile.objects.filter(follows=self.get_object())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # put to context profile object
        user = self.get_object()
        ctx['profile'] = user
        return ctx


class FollowView(LoginRequiredMixin, View):
    """
    Method to handle follow ajax request
    """

    def post(self, request):
        status = 'OK'
        if request.is_ajax():
            username = request.POST.get('username', None)
            # session user
            curr_user = request.user
            # target user
            target_user = Profile.objects.get(username=username)
            # add to follow
            if target_user in curr_user.follows.all():
                curr_user.follows.remove(target_user)
                status = 'Removed'
            else:
                curr_user.follows.add(target_user)
                status = 'Added'
        else:
            status = 'BAD'
        data = {'status': status}
        return HttpResponse(json.dumps(data), content_type='application/json')

1


class AlbumCreateView(CreateView, LoginRequiredMixin):
    form_class = AlbumForm
    template_name = 'blog/photos/album_create.html'

    def get_success_url(self):
        return reverse('blog:photos')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return redirect(self.get_success_url())


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'blog/photos/album_detail.html'
    pk_url_kwarg = 'id'


class AlbumListView(ListView):
    model = Album
    template_name = 'blog/photos/album_list.html'