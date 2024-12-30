from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy 
from .models import DID, Tarifa, Compania
# Create your views here.


class InicioView(TemplateView): 
    
    template_name = 'dids/Inicio.html'


class DIDListView(TemplateView): 
    
    template_name = 'dids/DIDsSearch.html' 
        
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        numero = self.request.GET.get('numero') 
        if numero: 
            try: 
                context['resultado'] = DID.objects.get(numero=numero) 
            
            except DID.DoesNotExist: 
                context['mensaje'] = "The DID number is not registered yet." 
        
        return context    

class DIDCreateView(CreateView): 
    
    model = DID 
    template_name = 'dids/NewDIDs.html' 
    fields = ['numero', 'pais', 'empresa', 'minutos_uso'] 
    success_url = reverse_lazy('Inicio') 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['companias'] = Compania.objects.all().order_by('nombre') 
        return context 
        
    def form_valid(self, form): 
        form.instance.empresa = self.request.POST["empresa"] 
        return super().form_valid(form)
    

class DIDCompanySearchView(TemplateView):
    template_name = 'dids/UD_DIDs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companias'] = Compania.objects.all().order_by('nombre')
        
        empresa = self.request.GET.get('empresa')
        if empresa:
            context['dids'] = DID.objects.filter(empresa=empresa)
        
        return context

class DIDUpdateView(UpdateView):
    model = DID
    template_name = 'dids/UpdateDIDs.html'
    fields = ['empresa', 'minutos_uso']
    success_url = reverse_lazy('BusDIDsByCompany')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companias'] = Compania.objects.all().order_by('nombre')
        return context

class DIDDeleteView(DeleteView):
    model = DID
    template_name = 'dids/DeleteDIDs.html'
    success_url = reverse_lazy('BusDIDsByCompany')


class TarifaSearchView(TemplateView):
    template_name = 'dids/PriceSearch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarifas'] = Tarifa.objects.all().order_by('pais')
        pais = self.request.GET.get('pais')
        if pais:
            context['tarifa'] = get_object_or_404(Tarifa, pais=pais)
        return context

class TarifaUpdateView(UpdateView):
    model = Tarifa
    template_name = 'dids/UpdatePrice.html'
    fields = ['trafico_entrante', 'trafico_saliente', 'precio_por_numero']
    success_url = reverse_lazy('BusTar')

class TarifaDeleteView(DeleteView):
    model = Tarifa
    template_name = 'dids/DeletePrice.html'
    success_url = reverse_lazy('BusTar')


class TarifaCreateView(CreateView): 
    
    model = Tarifa 
    template_name = 'dids/NewPrice.html' 
    fields = ['trafico_entrante', 'trafico_saliente', 'precio_por_numero', 'pais'] 
    success_url = reverse_lazy('Inicio')

class CompaniaSearchView(TemplateView):
    template_name = 'dids/CompanySearch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companias'] = Compania.objects.all().order_by('nombre')
        nombre = self.request.GET.get('nombre')
        if nombre:
            context['compania'] = get_object_or_404(Compania, nombre=nombre)
        return context

class CompaniaUpdateView(UpdateView):
    model = Compania
    template_name = 'dids/UpdateCompany.html'
    fields = ['nombre', 'direccion', 'codigo_postal', 'persona_contacto', 'NOCemail']
    success_url = reverse_lazy('BusComp')

    def form_valid(self, form):
        # Obtener el objeto antes de aplicar el formulario de actualización
        self.object = self.get_object()
        old_nombre = self.object.nombre
        response = super().form_valid(form)
        new_nombre = form.cleaned_data['nombre']
        # Actualizar el campo empresa de todos los DIDs que tenían el nombre anterior
        DID.objects.filter(empresa=old_nombre).update(empresa=new_nombre)
        return response


class CompaniaDeleteView(DeleteView):
    model = Compania
    template_name = 'dids/DeleteCompany.html'
    success_url = reverse_lazy('BusComp')


class CompaniaCreateView(CreateView): 
    
    model = Compania 
    template_name = 'dids/NewCompany.html' 
    fields = ['direccion', 'codigo_postal', 'nombre', 'persona_contacto', 'NOCemail'] 
    success_url = reverse_lazy('Inicio')