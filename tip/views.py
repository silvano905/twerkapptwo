from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import MakePostForm
from .models import MakeTip, LikeUserList, DownVoteUserList
# from comments.models import Comment
from django.db.models import Q
from accounts.models import PointsUserList, Profile
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count



User = get_user_model()


@login_required
def crate_tip(request):
    form = MakePostForm()

    if request.method == "POST":
        form = MakePostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user_tip = form.save(commit=False)
            user_tip.author = request.user
            form.save(commit=True)
            return redirect('tips:gracias')
        else:
            form = MakePostForm()

    return render(request, 'tip/maketip_form.html', {'form': form})



@login_required
def reglas_view(request):
    return render(request, 'tip/reglas.html')


@login_required
def tip_details(request, pk):
    post = get_object_or_404(MakeTip, pk=pk)
    is_liked = False
    is_down = False

    if DownVoteUserList.objects.filter(user=request.user, post=post.pk):
        is_down = True

    if LikeUserList.objects.filter(user=request.user, post=post.pk):
        is_liked = True
    context = {
        'post': post,
        # 'is_down': is_down,
        # 'is_liked': is_liked,
        # 'total_likes': post.total_likes(),
        # 'comment_list': Comment.objects.all().order_by('-created_date')
    }
    return render(request, 'tip/tip_detail.html', context)


@login_required
def like_tip(request):
    all_tipsx = MakeTip.objects.filter(author__exact=request.user)
    pksx = MakeTip.objects.filter(author__exact=request.user).values_list('id', flat=True)

    def appendTest(x):
        theList = []
        for i in x:
            theList.append(i)
        return theList

    to_be_deleted = []
    spp = appendTest(pksx)
    while spp:
        s2 = all_tipsx.get(pk=spp[-1])
        s3 = s2.total_down_votes()
        if s3 >= 105:
            to_be_deleted.append(s2.pk)
        spp.pop()
    for x in to_be_deleted:
        MakeTip.objects.filter(author__exact=request.user).get(pk=x).delete()

    is_liked = False
    tip = get_object_or_404(MakeTip, id=request.POST.get('post_id'))
    membership = LikeUserList.objects.filter(user=request.user, post=tip.pk)
    if membership:
        membership.delete()
        is_liked = False

    else:
        LikeUserList.objects.create(user=request.user, post=tip)
        is_liked = True
    return redirect(tip.get_absolute_url())


@login_required
def down_tip(request):
    is_down = False
    tip = get_object_or_404(MakeTip, id=request.POST.get('post_id'))
    membership = DownVoteUserList.objects.filter(user=request.user, post=tip.pk)
    if membership:
        membership.delete()
        is_down = False

    else:
        DownVoteUserList.objects.create(user=request.user, post=tip)
        is_down = True
    return redirect(tip.get_absolute_url())


class TipUpdateView(UpdateView, LoginRequiredMixin):
    form_class = MakePostForm
    success_url = reverse_lazy('tips:list')
    model = MakeTip


class TipDeleteView(DeleteView, LoginRequiredMixin):
    model = MakeTip
    success_url = reverse_lazy('tips:list')


class UserTips(ListView, LoginRequiredMixin):

    context_object_name = 'post_list'
    model = MakeTip
    template_name = 'tip/user_tip_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('tips').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.tips.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


def tips_list_search(request):
    notificaciones = 'none'
    if request.user.is_anonymous:
        pass

    queryset_list = '?'
    if request.method == 'GET':
        sku = request.GET.get('populares')
        sku2 = request.GET.get('comentadas')
        sku3 = request.GET.get('recientes')

        if sku:
            queryset_list = MakeTip.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sku2:
            queryset_list = MakeTip.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
        else:
            queryset_list = MakeTip.objects.all().order_by('-created_date')

    query = request.GET.get('q')
    if query is not None:
        queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(info__icontains=query))

    paginator = Paginator(queryset_list, 36)    # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        'notifications_list': notificaciones,
        "post_list": queryset
    }
    return render(request, 'tip/tip_list.html', context)


class CreateProfileBeforeSearch(TemplateView, LoginRequiredMixin):
    template_name = 'tip/create_a_profile.html'


def request_services(request):
    return render(request, 'tip/gracias.html')



# class tips_list_search(TemplateView, LoginRequiredMixin):
#     login_url = '/login/'
#     template_name = 'tip/tip_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset_list = MakeTip.objects.all()
#
#         query = self.request.GET.get('q')
#         if query is not None:
#             queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(info__icontains=query))
#
#         paginator = Paginator(queryset_list, 36)    # Show 25 contacts per page
#
#         page = self.request.GET.get('page')
#         queryset = paginator.get_page(page)
#
#         ss = self.request.GET
#         print(ss)
#         context = {
#             "post_list": queryset
#         }
#         return context





