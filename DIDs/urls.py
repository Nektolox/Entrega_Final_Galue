from django.urls import path
from .views import InicioView, DIDListView, DIDCreateView, TarifaSearchView, TarifaCreateView, CompaniaSearchView, CompaniaUpdateView, CompaniaDeleteView, CompaniaCreateView, DIDCompanySearchView, DIDUpdateView, DIDDeleteView, TarifaUpdateView, TarifaDeleteView,TicketListView, TicketDetailView, TicketCreateView, EditCommentView, DeleteCommentView, EditTicketView

urlpatterns = [
    path('Inicio/', InicioView.as_view(), name="Inicio"),
    path('BuscarDIDs/', DIDListView.as_view(), name="BusDIDs"),
    path('UD_DIDs/', DIDCompanySearchView.as_view(), name='BusDIDsByCompany'),
    path('UpdateDIDs/<int:pk>/', DIDUpdateView.as_view(), name='UpdateDID'),
    path('DeleteDIDs/<int:pk>/', DIDDeleteView.as_view(), name='DeleteDID'),
    path('RegistrarDIDs/', DIDCreateView.as_view(), name="RegDIDs"),
    path('BuscarTarifa/', TarifaSearchView.as_view(), name="BusTar"),
    path('tarifa/update/<int:pk>/', TarifaUpdateView.as_view(), name='UpdateTarifa'), 
    path('tarifa/delete/<int:pk>/', TarifaDeleteView.as_view(), name='DeleteTarifa'),
    path('RegistrarTarifa/', TarifaCreateView.as_view(), name="RegTar"),
    path('BuscarComp/', CompaniaSearchView.as_view(), name="BusComp"),
    path('compania/update/<int:pk>/', CompaniaUpdateView.as_view(), name='UpdateCompania'), 
    path('compania/delete/<int:pk>/', CompaniaDeleteView.as_view(), name='DeleteCompania'),
    path('RegistrarComp/', CompaniaCreateView.as_view(), name="RegComp"),
    path('Tickets/', TicketListView.as_view(), name='ticket_list'),
    path('Tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('Tickets/new/', TicketCreateView.as_view(), name='ticket_create'),
    path('Ticket/Edit/<int:pk>/', EditTicketView.as_view(), name='edit_ticket'),
    path('Comment/Edit/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('Comment/Delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
]





