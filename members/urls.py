from django.conf.urls import url
from . import views

app_name = 'members'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /1/
    url(r'^batch/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="batchDetail"),
    # /1/
    url(r'^batch/(?P<pk>[0-9]+)/memberDetail/$', views.MemDetailView.as_view(), name="memberDetail"),

    # /members
    url(r'^members/$', views.AllMembersView.as_view(), name="allMembers"),

    # url for fee details of gym
    url(r'^feeDetail/$', views.FeeDetailsListView.as_view(), name="feeDetail"),

    # for batch form
    url(r'^batch/add/$', views.BatchCreate.as_view(), name='batch-add'),
    url(r'^batch/(?P<pk>[0-9]+)/update/$', views.BatchUpdate.as_view(), name='batch-update'),
    #  url(r'^batch/(?P<pk>[0-9]+)/delete/$', views.BatchDelete.as_view(), name='batch-delete'),

    # for member form
    url(r'^member/add/$', views.MemberCreate.as_view(), name='member-add'),
    url(r'^member/(?P<pk>[0-9]+)/update/$', views.MemberUpdate.as_view(), name='member-update'),
    url(r'^member/(?P<pk>[0-9]+)/delete/$', views.MemberDelete.as_view(), name='member-delete'),

    # for fee details form
    url(r'^feeDetail/add/$', views.FeeDetailsCreate.as_view(), name='feeDetails-add'),

    # for member fee for a particular month
    url(r'^member/(?P<id>[0-9]+)/fee/add/$', views.FeeCreate.as_view(), name='fee-add'),
    url(r'^member/(?P<id>[0-9]+)/fee/update/$', views.FeeUpdate.as_view(), name='fee-update'),

    # for search query
    url(r'^Search/$', views.AllMembersView.as_view(), name='member-search'),

    # url for monthly revenue
    url(r'^revenue/monthly/(?P<id>[0-9]+)/$',views.MonthlyRevenue.as_view(),name='monthly-revenue'),

    url(r'^nopage/',views.my_view,name="no_content")

]
