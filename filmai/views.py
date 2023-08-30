from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Aktorius, Filmas
def index(request):
    num_aktoriai = Aktorius.objects.all().count()
    num_filmai = Filmas.objects.count()

    context_t = {
        'num_aktoriai_t': num_aktoriai,
        'num_filmai_t': num_filmai,
    }

    return render(request, 'index.html', context=context_t)

def aktoriai(request):
    paginator = Paginator(Aktorius.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_aktoriai = paginator.get_page(page_number)
    context_t = {
        'aktoriai_visos_eilutes_t': paged_aktoriai
    }


    return render(request, 'aktoriai_visi.html', context=context_t)

def aktorius(request, aktorius_id):
    aktorius_viena_eilute = get_object_or_404(Aktorius, pk=aktorius_id)
    # print(authors)
    context_t = {
        'aktorius_viena_eilute_t': aktorius_viena_eilute
    }
    return render(request, 'aktorius_vienas.html', context=context_t)

class FilmasListView(generic.ListView):  # ListView - visos eilutės (objektai)
    model = Filmas  # modelioklasė_list -> book_list
    context_object_name = 'filmas_list'
    template_name = 'filmai_visi.html'

class FilmasDetailView(generic.DetailView):
    model = Filmas
    context_object_name = 'filmas'
    template_name = 'filmas_vienas.html'

def search(request):
    paieskos_tekstas = request.GET.get('laukelio-tekstas')
    paieskos_rezultatai = Filmas.objects.filter(
        Q(pavadinimas__icontains=paieskos_tekstas) |
        Q(aktoriusFK__vardas_pavarde__icontains=paieskos_tekstas)
    )

    context_t = {
        'paieskos_tekstas_t': paieskos_tekstas,
        'paieskos_rezultatai_t': paieskos_rezultatai
    }
    return render(request, 'paieskos-rezultatai.html', context=context_t)
