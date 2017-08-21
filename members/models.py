from django.db import models
import datetime
from datetime import date
from  django.core.urlresolvers import reverse


# Create your models here.
class Batch(models.Model):
    batch_title = models.CharField(max_length=500)
    batch_time = models.TimeField(default=datetime.datetime.now())

    def count(self):
        return self.member_set.count()

    def __str__(self):
        return self.batch_title

    # whenever a new batch created redirect it to its details page
    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('members:batchDetail', kwargs={'pk': self.pk})


class FeeDetails(models.Model):
    fee_update_date = models.DateField(default=date.today)
    monthly_fee = models.IntegerField(default=0)
    quater_fee = models.IntegerField(default=0)
    half_fee = models.IntegerField(default=0)
    year_fee = models.IntegerField(default=0)

    def __str__(self):
        return "FeeDetails"

    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('members:feeDetail')


class Member(models.Model):
    # def __init__(self):
    #     if self.member_packageType is 'M':
    #         self.member_fee_remaining = self.feeDetails.monthly_fee - self.member_discount
    #     elif self.member_packageType is 'Q':
    #         self.member_fee_remaining = self.feeDetails.quater_fee - self.member_discount
    #     elif self.member_packageType is 'H':
    #         self.member_fee_remaining = self.feeDetails.half_fee - self.member_discount
    #     elif self.member_packageType is 'Y':
    #         self.member_fee_remaining = self.feeDetails.year_fee - self.member_discount

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=False)
    member_name = models.CharField(max_length=250)
    member_age = models.IntegerField()
    member_email = models.EmailField(max_length=250)
    member_date = models.DateField(default=date.today)
    member_pic = models.ImageField()
    PACKAGES = (
        ('M', 'MONTHLY'),
        ('Q', 'QUATERLY'),
        ('H', 'HALF_YEAR'),
        ('Y', 'YEARLY'),
    )
    member_packageType = models.CharField(max_length=250, choices=PACKAGES, default='MONTHLY')
    member_discount = models.IntegerField(help_text='Enter discount in Rs', default=0)
    member_fee_deposit = models.IntegerField(default=0)
    member_active=models.BooleanField(default=True)

    feeDetails = models.ForeignKey(FeeDetails, on_delete=models.CASCADE, blank=False)

    # modelFeeDetails = models.OneToOneField(FeeDetails, primary_key=1)
    def getFee(self):
        if self.member_packageType is 'M':
            return self.feeDetails.monthly_fee - self.member_discount
        elif self.member_packageType is 'Q':
            return self.feeDetails.quater_fee - self.member_discount
        elif self.member_packageType is 'H':
            return self.feeDetails.half_fee - self.member_discount
        elif self.member_packageType is 'Y':
            return self.feeDetails.year_fee - self.member_discount

            # this addes another field inside member table
            # to use getFee method to assign value to this member_fee_remaining ,we have used declaration by method



    def get_member_fee_remaining(self):
        return self.getFee() - self.member_fee_deposit

    member_fee_remaining = property(get_member_fee_remaining,get_member_fee_remaining)
    # def getx(self):
    #     return self.getFee()-self.member_fee_deposit
    #
    # def setx(self, value):
    #     self._x = value
    #
    # def delx(self):
    #     del self._x
    #
    # member_fee_remaining = property(getx, setx, delx, getFee)


    def __str__(self):
        return self.member_name

    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('members:memberDetail', kwargs={'pk': self.pk})


class Fee(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=False)
    MONTHS = (
        ('JN', 'January'),
        ('FB', 'February'),
        ('MR', 'MARCH'),
        ('AP', 'APRIL'),
        ('MY', 'MAY'),
        ('JN', 'JUNE'),
        ('JL', 'JULY'),
        ('AG', 'AUGUST'),
        ('SP', 'SEPTEMBER'),
        ('OT', 'OCTOBER'),
        ('NV', 'NOVEMBER'),
        ('DC', 'DECEMBER'),
    )
    fee_month = models.CharField(max_length=50, choices=MONTHS)
    fee_amount = models.IntegerField(default=0)
    fee_deposit_date = models.DateField(default=date.today)

    def getMember(self):
        return self.member.member_name

    def __str__(self):
        return self.fee_month

    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('members:memberDetail', kwargs={'pk': self.pk})


