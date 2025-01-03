from django.urls import path
from .views import InicioView, DIDListView, DIDCreateView, TarifaSearchView, TarifaCreateView, CompaniaSearchView, CompaniaUpdateView, CompaniaDeleteView, CompaniaCreateView, DIDCompanySearchView, DIDUpdateView, DIDDeleteView, TarifaUpdateView, TarifaDeleteView,TicketListView, TicketDetailView, TicketCreateView, EditCommentView, DeleteCommentView, EditTicketView, AboutMeView

urlpatterns = [
    path('Inicio/', InicioView.as_view(), name="Inicio"),
    path('AboutMe/', AboutMeView.as_view(), name="AboutMe"),
    path('BuscarDIDs/', DIDListView.as_view(), name="BusDIDs"),
    path('UD_DIDs/', DIDCompanySearchView.as_view(), name='BusDIDsByCompany'),
    path('UpdateDIDs/<int:pk>/', DIDUpdateView.as_view(), name='UpdateDID'),
    path('DeleteDIDs/<int:pk>/', DIDDeleteView.as_view(), name='DeleteDID'),
    path('RegistrarDIDs/', DIDCreateView.as_view(), name="RegDIDs"),
    path('BuscarTarifa/', TarifaSearchView.as_view(), name="BusTar"),
    path('Tarifa/Update/<int:pk>/', TarifaUpdateView.as_view(), name='UpdateTarifa'), 
    path('Tarifa/Delete/<int:pk>/', TarifaDeleteView.as_view(), name='DeleteTarifa'),
    path('RegistrarTarifa/', TarifaCreateView.as_view(), name="RegTar"),
    path('BuscarComp/', CompaniaSearchView.as_view(), name="BusComp"),
    path('Compania/Update/<int:pk>/', CompaniaUpdateView.as_view(), name='UpdateCompania'), 
    path('Compania/Delete/<int:pk>/', CompaniaDeleteView.as_view(), name='DeleteCompania'),
    path('RegistrarComp/', CompaniaCreateView.as_view(), name="RegComp"),
    path('Tickets/', TicketListView.as_view(), name='ticket_list'),
    path('Tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('Tickets/New/', TicketCreateView.as_view(), name='ticket_create'),
    path('Ticket/Edit/<int:pk>/', EditTicketView.as_view(), name='edit_ticket'),
    path('Comment/Edit/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('Comment/Delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
]





