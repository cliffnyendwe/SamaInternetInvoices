from django.contrib.auth.decorators import login_required
from . models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from . forms import *
from django.urls import reverse_lazy
import csv
import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

from .filters import ProjectsFilter, AgentFilter, InvoiceFilter
# Create your views here.
def export_invoices_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="approved-invoices.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Invoices')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Agent', 'ISP Name', 'Monthly Subscription', 'Date Due', 'Status', 'Date Submitted',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Invoice.objects.filter(approved=True).values_list('agent', 'isp_name', 'monthly_subscription', 'due_date', 'status', 'date_submitted')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

    users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for user in users:
        writer.writerow(user)

    return response

def export_payments_due_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments-due.csv"'

    writer = csv.writer(response)
    writer.writerow(['Agent', 'ISP Name', 'Monthly Subscription', 'Date Due'])

    invoices = Invoice.objects.filter(approved=True).values_list('agent', 'isp_name', 'monthly_subscription', 'due_date')
    for invoice in invoices:
        writer.writerow(invoice)

    return response

def export_filtered_invoices(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="filtered-invoices-due.csv"'

	writer = csv.writer(response)
	writer.writerow(['Agent', 'ISP Name', 'Monthly Subscription', 'Date Due'])

	invoices = Invoice.objects.filter(Q(agent__ssdc_number__icontains=q) |Q(project__title__icontains=q) | Q(status__icontains=q) | Q(due_date__icontains=q)).values_list('agent', 'isp_name', 'monthly_subscription', 'due_date')
	for invoice in invoices:
	    writer.writerow(invoice)

	return response

@login_required(login_url="/login/")
def home(request):
	return render(request, "index.html")

@login_required(login_url="/login/")
def TeamLeaders(request):
	team_leaders = TeamLeader.objects.all()
	template_name = "app/team-leaders.html"
	return render(request, template_name, {"team_leaders": team_leaders})

class NewTeamLeader(CreateView):
	model = TeamLeader
	form_class = AddTeamLeaderForm
	template_name = "app/new-team-leader.html"

@login_required(login_url="/login/")
def Agents(request):
	context = {}
	filtered_agents = AgentFilter(
		request.GET,
		queryset=Agent.objects.all()
	)
	context['filtered_agents'] = filtered_agents

	template_name = "app/agents.html"
	return render(request, template_name, context=context)

class NewAgent(CreateView):
	model = Agent
	form_class = AddAgentForm
	template_name = "app/new-agent.html"


def all_projects(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	filtered_projects = Project.objects.filter(Q(title__icontains=q))
	context = {
		"filtered_projects": filtered_projects
	}
	"""
	filtered_projects = ProjectsFilter(
		request.GET,
		queryset=Project.objects.all()
	)
	context['filtered_projects'] = filtered_projects
	"""
	return render(request, "app/projects.html", context)


class NewProject(CreateView):
	model = Project
	fields = "__all__"
	template_name = "app/new-project.html"

@login_required(login_url="/login/")
def Invoices(request):
	invoices = Invoice.objects.all()
	template_name = "app/invoices.html"
	return render(request, template_name, {"invoices": invoices})

class NewInvoice(CreateView):
	model = Invoice
	form_class = AddInvoiceForm
	template_name = "app/new-invoice.html"

	def form_valid(self, form):
		form.instance.project = self.request.user.agent.project
		return super().form_valid(form)

class InvoiceDetails(DetailView):
	model = Invoice
	template_name = "app/invoice.html"

def agent_profile(request):
	agent = Agent.objects.filter(user=request.user)
	print("Agent is: ",agent)
	context = {
		"agent": agent
	}
	return render(request, "agent-profile.html", context)

def agent_invoices(request):
	agent = Agent.objects.filter(user=request.user)
	agent_invoices = Invoice.objects.filter(agent=request.user.agent)

	context = {
		"agent": agent,
		"agent_invoices": agent_invoices
	}
	return render(request, "app/agent-invoices.html", context)

class ApproveInvoice(UpdateView):
	model = Invoice
	fields = ["approved", "reason_declined"]
	template_name = "app/approve-invoice.html"
	success_url = reverse_lazy("tl-invoices")

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Agent

@login_required(login_url="/login/")
def index(request):
    agents = Agent.objects.all()
    return render(request, 'index.html', {'agents':agents})


def my_agents(request):
	context = {}
	filtered_agents = AgentFilter(
		request.GET,
		queryset=Agent.objects.all()
	)
	context['filtered_agents'] = filtered_agents

	return render(request, "app/my-agents.html", context=context)

class AgentDetails(DetailView):
	model = Agent
	template_name = "app/agent-details.html"

def tl_invoices(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	filtered_invoices = Invoice.objects.filter(Q(agent__ssdc_number__icontains=q) |Q(project__title__icontains=q) | Q(status__icontains=q) | Q(due_date__icontains=q))
	context = {
		"filtered_invoices": filtered_invoices
	}
	return render(request, "app/tl-invoices.html", context)

class ChangeInvoiceStatus(UpdateView):
	model = Invoice
	fields = ["status"]
	template_name = "app/change-invoice-status.html"
	success_url = reverse_lazy("admin-invoices")

class UpdateProject(UpdateView):
	model = Project
	fields = "__all__"
	template_name = "app/update-project.html"


def ApprovedInvoices(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	"""
	filtered_invoices = InvoiceFilter(
		request.GET,
		queryset=Invoice.objects.filter(approved=True)
	)
	context['filtered_invoices'] = filtered_invoices
	"""
	filtered_invoices = Invoice.objects.filter(Q(agent__ssdc_number__icontains=q) | Q(project__title__icontains=q) | Q(status__icontains=q) | Q(due_date__icontains=q))
	context = {
		"filtered_invoices": filtered_invoices
	}
	return render(request, "app/admin-invoices.html", context=context)


def tl_projects(request):
	tl_projects = TeamLeader.objects.filter(te=request.user.teamleader)
	context = {
		"tl_projects": tl_projects
	}
	return render(request, "app/tl-projects.html", context)

class UpdateTL(UpdateView):
	model = TeamLeader
	form_class = UpdateTLForm
	template_name = "app/update-tl-profile.html"

class UpdateAgent(UpdateView):
	model = Agent
	form_class = UpdateAgentForm
	template_name = "app/update-agent-profile.html"

