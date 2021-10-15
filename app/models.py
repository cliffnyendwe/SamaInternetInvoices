from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from authentication.models import User


class Project(models.Model):
    title = models.CharField(max_length=500, unique=True)
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects")


PAY_METHODS = (
    ('Pay Bill', 'Pay Bill'),
    ('Till Number', 'Till Number'),
)

STATUS_CHOICES = (
    ("Paid", "Paid"),
    ("Payment Pending", "Payment Pending"),
    ("Not Paid", "Not Paid"),
)

class TeamLeader(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150, default='tl name')
    ssdc_number = models.CharField(max_length=100, default='tl ssdc number')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team-leader-profile")

class Agent (models.Model):
    name = models.CharField(max_length=150, default='agent name')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ssdc_number = models.CharField(max_length=100, default='agent ssdc number')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="projects")
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.SET_NULL, null=True)
    installation = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=200, choices=PAY_METHODS, default="m-pesa")
    till_or_paybill_number = models.CharField(max_length=20, default="000000000")
    acc_number = models.CharField(max_length=200, default="123456789")
    date_joined = models.DateField(default=timezone.now)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("agent-profile")

class Invoice(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    isp_name = models.CharField(max_length=100, default='isp name')
    monthly_subscription = models.IntegerField(default='monthly subscription')
    invoice_file = models.FileField(upload_to="invoices")
    due_date = models.DateField(default=timezone.now)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Payment Pending")
    date_submitted = models.DateField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    reason_declined = models.TextField(blank=True, null=True, default="The invoice was accepted!")

    def __str__(self):
        return str(self.agent) + " Invoice"

    def get_absolute_url(self):
        return reverse("agent-invoices")

    def invoice_approved(self):
        if self.approved:
            return "Yes"
        else: return "No"