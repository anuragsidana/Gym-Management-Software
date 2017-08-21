from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Batch, Member, FeeDetails, Fee

from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    # You can also specify an alternative location to redirect the user to if they are not authenticated (login_url),
    # and a URL parameter name instead of "next" to insert the current absolute path (redirect_field_name).

    login_url = 'accounts/login/'
    redirect_field_name = 'members/index.html'

    # name of template which is to be visited
    template_name = 'members/index.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_batches'

    # data that is to be passed in the template
    def get_queryset(self):
        # it will return all list items in object_list variable by default
        return Batch.objects.all()


# details of a batch
class DetailView(LoginRequiredMixin, generic.DetailView):
    # detail of which object or model u are going to write
    model = Batch
    template_name = 'members/detail.html'


# details of a batch
import datetime


class MemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Member
    template_name = 'members/member_detail.html'
    now = datetime.datetime.now()

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MemDetailView, self).get_context_data(**kwargs)

        context['current_date'] = self.now
        return context


# a view for the fee details of the gym
class FeeDetailsListView(LoginRequiredMixin, generic.ListView):
    # name of template which is to be visited
    template_name = 'members/fee_details.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_fees'

    # data that is to be passed in the template
    def get_queryset(self):
        # it will return all list items in object_list variable by default
        return FeeDetails.objects.all()


# this import to use complex queries
from django.db.models import Q


# returns all the members of a batch
class AllMembersView(LoginRequiredMixin, generic.ListView):
    # name of template which is to be visited
    template_name = 'members/all_members.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_members'

    # in case its a search query then the title of the page needs to be changed
    title = "Gym Members"

    # data that is to be passed in the template
    def get_queryset(self):
        # query passed in the search box
        query = self.request.GET.get("q")
        # if its a query then this
        if query:
            # title changed
            self.title = "Search Results"
            return Member.objects.filter(
                Q(member_name__icontains=query) |
                Q(member_date__icontains=query)

            )

        # if its a simple call to get all the objects then  it will return all list items in object_list variable by default
        return Member.objects.all()

        # this is used to pass extra context data in case of generic classes

    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(AllMembersView, self).get_context_data()

        context['page_title'] = self.title
        return context


class BatchCreate(LoginRequiredMixin, CreateView):
    # for which u wanna create a view
    model = Batch
    # the fields u wanna return
    fields = ['batch_title', 'batch_time']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(BatchCreate, self).get_context_data()

        context['page_title'] = 'Add a new Batch'
        return context


class BatchUpdate(LoginRequiredMixin, UpdateView):
    model = Batch
    fields = ['batch_title', 'batch_time']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(BatchUpdate, self).get_context_data()

        context['page_title'] = 'Update Batch'
        return context


from django.core.urlresolvers import reverse_lazy


class BatchDelete(LoginRequiredMixin, DeleteView):
    model = Batch
    # after deletion where to redirect
    success_url = reverse_lazy('members:index')


class MemberCreate(LoginRequiredMixin, CreateView):
    # for which u wanna create a view
    model = Member
    # the fields u wanna return
    fields = ['batch', 'member_name', 'member_age', 'member_email', 'member_date', 'member_pic', 'member_packageType',
              'member_discount', 'feeDetails']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(MemberCreate, self).get_context_data()

        context['page_title'] = 'Add new member'
        return context


class MemberUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['batch', 'member_name', 'member_age', 'member_email', 'member_date', 'member_pic', 'member_packageType',
              'member_discount', 'feeDetails']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(MemberUpdate, self).get_context_data()

        context['page_title'] = 'Update member details'
        return context


from django.core.urlresolvers import reverse_lazy


class MemberDelete(LoginRequiredMixin, DeleteView):
    model = Member
    # after deletion where to redirect
    success_url = reverse_lazy('members:index')


class FeeDetailsCreate(LoginRequiredMixin, CreateView):
    # for which u wanna create a view
    model = FeeDetails
    # the fields u wanna return
    fields = ['fee_update_date', 'monthly_fee', 'quater_fee', 'half_fee', 'year_fee']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(FeeDetailsCreate, self).get_context_data()

        context['page_title'] = 'Add new Fee Details '
        return context


from .forms import FeeForm
from django.shortcuts import redirect

'''
def FeeCreate(request,id):
    template_name = 'members/fee_form.html'
    if request.method == "POST":
        form=FeeForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('members:memberDetail',pk=id)
    else:
        form=FeeForm()
        form.fields['member'].queryset = Member.objects.filter(pk=id)
    return render(request, template_name, {'form': form})

'''


class FeeCreate(LoginRequiredMixin, CreateView):
    template_name = 'members/fee_form.html'

    def get(self, request, *args, **kwargs):
        form = FeeForm()
        form.fields['member'].queryset = Member.objects.filter(pk=kwargs['id'])
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)

            # code to update the fee submitted for a member
            amount = fee.fee_amount
            member = Member.objects.get(id=kwargs['id'])
            previous = member.member_fee_deposit
            member.member_fee_deposit = previous + amount

            member.save()

            fee.save()
            return redirect('members:memberDetail', pk=kwargs['id'])
        return render(request, self.template_name, {'form': form})

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(FeeCreate, self).get_context_data()

        context['page_title'] = 'Add Fee deposited'
        return context


# in update which id of form table to be passed
# n also how to manage the redirect url
class FeeUpdate(LoginRequiredMixin, UpdateView):
    model = Fee
    fields = ['member', 'fee_month', 'fee_amount']

    # this is used to pass extra context data in case of generic classes
    def get_context_data(self):
        # Call the base implementation first to get a context
        context = super(FeeUpdate, self).get_context_data()

        context['page_title'] = 'Update Fee deposited'
        return context


# in delete pass the id of the row of the fee table to be deleted
# also manage success
class FeeDelete(LoginRequiredMixin, DeleteView):
    model = Fee
    # after deletion where to redirect
    success_url = reverse_lazy('members:index')


from django.views.generic import View


# query to get new joined members
#  Member.objects.filter(member_date__month=self.today.month)
class MonthlyRevenue(LoginRequiredMixin, generic.ListView):
    # name of template which is to be visited
    template_name = 'members/monthly_revenue.html'
    # returned object stored in this  'by default its object_list'
    context_object_name = 'all_fee'
    today = datetime.datetime.now()

    # data that is to be passed in the template
    def get_queryset(self):
        # it will return all list items in object_list variable by default
        return Fee.objects.all()
        # this is used to pass extra context data in case of generic classes

    all_mem = Member.objects.all()

    # to calculate fee deposited this month
    fees = Fee.objects.all()

    #count = 0;
    # for fee in fees:
    #       if fee.fee_deposit_date.month == today.month :
    #           count=count+fee.fee_amount
    def count(self):
        count2 = 0
        for fee in self.fees:
            if fee.fee_deposit_date.month == self.today.month:
                count2 = count2 + fee.fee_amount
        return count2

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MonthlyRevenue, self).get_context_data(**kwargs)

        context['current_date'] = self.today
        context['all_members'] = self.all_mem
        context['count'] = self.count
        return context
