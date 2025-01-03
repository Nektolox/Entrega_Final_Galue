from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy,  reverse
from .models import DID, Tarifa, Compania, TroubleTicket, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        context['user'] = self.request.user
        
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
        self.object = self.get_object()
        old_nombre = self.object.nombre
        response = super().form_valid(form)
        new_nombre = form.cleaned_data['nombre']
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


class TicketListView(ListView):
    model = TroubleTicket
    template_name = 'dids/TicketList.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets_with_last_comment = []
        for ticket in TroubleTicket.objects.all():
            last_comment = ticket.comments.order_by('-created_at').first()
            tickets_with_last_comment.append({
                'ticket': ticket,
                'last_comment': last_comment
            })
        context['tickets_with_last_comment'] = tickets_with_last_comment
        return context


class TicketDetailView(View):
    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(TroubleTicket, pk=kwargs['pk'])
        comments = Comment.objects.filter(ticket=ticket)
        return render(request, 'dids/TicketDetail.html', {'ticket': ticket, 'comments': comments})

    def post(self, request, *args, **kwargs):
        ticket = get_object_or_404(TroubleTicket, pk=kwargs['pk'])

        if 'content' in request.POST:
            # Añadir un nuevo comentario
            content = request.POST.get('content')
            if content:
                comment = Comment(content=content, ticket=ticket, author=request.user)
                comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
        
        elif 'edit_comment' in request.POST:
            # Redirigir a la página de editar comentario
            comment_id = request.POST.get('edit_comment')
            return redirect('edit_comment', pk=comment_id)
        
        elif 'delete_comment' in request.POST:
            # Redirigir a la página de eliminar comentario
            comment_id = request.POST.get('delete_comment')
            return redirect('delete_comment', pk=comment_id)
        
        comments = Comment.objects.filter(ticket=ticket)
        return render(request, 'dids/TicketDetail.html', {'ticket': ticket, 'comments': comments})

class TicketCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dids/NewTicket.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        content = request.POST.get('content')
        if title and content:
            ticket = TroubleTicket(title=title, subtitle=subtitle, content=content, author=request.user)
            ticket.save()
            return redirect('ticket_list')
        return render(request, 'dids/NewTicket.html')
    
class EditTicketView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TroubleTicket
    fields = ['content']
    template_name = 'dids/TicketEdit.html'
    context_object_name = 'ticket'

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.author

    def get_success_url(self):
        return reverse('ticket_detail', kwargs={'pk': self.object.pk})


class EditCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return render(request, 'dids/CommentEdit.html', {'comment': comment})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            return redirect('ticket_detail', pk=comment.ticket.pk)
        return render(request, 'dids/CommentEdit.html', {'comment': comment})


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'dids/CommentDelete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object.ticket
        return context

    def get_success_url(self):
        ticket_pk = self.object.ticket.pk
        return reverse('ticket_detail', kwargs={'pk': ticket_pk})





