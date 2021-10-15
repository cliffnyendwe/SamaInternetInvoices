from django.urls import path, re_path
from . import views
from . views import *

urlpatterns = [
	path('', views.home, name='home'),
	path("agents/", views.Agents, name="agents"),
	path("new-agent/", NewAgent.as_view(), name="new-agent"),
	path("team-leaders/", views.TeamLeaders, name="team-leaders"),
	path("new-team-leader/", NewTeamLeader.as_view(), name="new-team-leader"),
	path("team-leader-profile/", views.team_leader_profile, name="team-leader-profile"),
	path("my-agents/", views.my_agents, name="my-agents"),
	path("projects/", views.all_projects, name="projects"),
	path("new-project/", NewProject.as_view(), name="new-project"),
	path("invoices/", views.Invoices, name="invoices"),
	path("new-invoice/", NewInvoice.as_view(), name="new-invoice"),
	path("agent-profile/", views.agent_profile, name="agent-profile"),
	path("agent-invoices/", views.agent_invoices, name="agent-invoices"),
	path("agent-details/<int:pk>/", AgentDetails.as_view(), name="agent-details"),
	path("approve-invoice/<int:pk>/", ApproveInvoice.as_view(), name="approve-invoice"),
	path("invoice-payment-status/<int:pk>/", ChangeInvoiceStatus.as_view(), name="invoice-payment-status"),
	path("admin-invoices/", views.ApprovedInvoices, name="admin-invoices"),
	path("declined-invoices/", views.DeclinedInvoices, name="declined-invoices"),
	path("paid-invoices/", views.PaidInvoices, name="paid-invoices"),
	path("tl-invoices/", views.tl_invoices, name="tl-invoices"),
	path('export/csv/', views.export_users_csv, name='export_users_csv'),
	path('export-payments-due-csv/', views.export_payments_due_csv, name='export-payments-due-csv'),
	path("export-filtered-invoices/", views.export_filtered_invoices, name="export-filtered-invoices"),
	#path("tl-projects/", views.tl_projects, name="tl-projects"),
	path("update-tl/<int:pk>/", UpdateTL.as_view(), name="update-tl"),
	path("update-agent/<int:pk>/", UpdateAgent.as_view(), name="update-agent"),
	path("update-project/<int:pk>/", UpdateProject.as_view(), name="update-project"),
]

