from django.shortcuts import render, get_object_or_404, redirect, reverse
# from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

from .models import Aktorius, Filmas, FilmasInstance, Review
from .forms import FilmasReviewForm, UserUpdateForm, ProfilisUpdateForm, UserFilmasCreateForm


def index(request):
    num_aktoriai = Aktorius.objects.all().count()
    num_filmai = Filmas.objects.count()

    context_t = {
        'num_aktoriai_t': num_aktoriai,
        'num_filmai_t': num_filmai,
    }

    return render(request, 'index.html', context=context_t)


def aktoriai(request):
    paginator = Paginator(Aktorius.objects.all(), 6)
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
    paginate_by = 3


class FilmasDetailView(generic.DetailView):
    model = Filmas
    context_object_name = 'filmas'
    template_name = 'filmas_vienas.html'
    form_class = FilmasReviewForm

    # nurodome kur pateksime po submit mygtuko formoj paspaudimo
    def get_success_url(self):
        return reverse('filmas-one', kwargs={'pk': self.object.id})

        # post metodas formai

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        # formos custom validacija

    def form_valid(self, form):
        form.instance.filmas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


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


# Mano filmo viewsas
class LoanedFilmasByUserListView(LoginRequiredMixin, generic.ListView):
    model = FilmasInstance
    template_name = 'user_filmai.html'
    context_object_name = 'filmasinstance_list'


#    def get_queryset(self):
#        return FilmasInstance.objects.filter(reader=self.request.user).order_by('due_back')


@csrf_protect
def register(request):
    if request.method == "POST":
        # paimami duomenys iš formos
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} užimtas!")
                return redirect('register-url')  # jei užimtas nukreipiam išnaujo į formą
            else:  # tikrinam email, kai praėjo password ir username patikrinimai
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su email adresu {email} egzistuoja!")
                    return redirect('register-url')  # jei užimtas nukreipiam išnaujo į formą
                ####### patikrinimai praeiti
                else:
                    ### sukuriam naują userį
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f"Vartotojas {username} sukurtas!!!")
                    return redirect('login')



    else:
        return render(request, "registration/registration.html")


@login_required
def profilis(request):
    if request.method == "GET":
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    elif request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect('profilis-url')

    context_t = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profilis.html', context=context_t)


class FilmasByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = FilmasInstance
    # fields = ['book', 'due_back']
    success_url = '/filmai/mymovies'
    template_name = 'user_film_form.html'
    form_class = UserFilmasCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class FilmasByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                             generic.UpdateView):
    model = FilmasInstance
    fields = ['filmas']
    success_url = '/filmai/mymovies'
    template_name = 'user_film_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        filminst = self.get_object()
        return self.request.user == filminst.reader


class FilmasByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                             generic.DeleteView):
    model = FilmasInstance
    template_name = 'user_filma_delete.html'
    success_url = '/filmai/mymovies'

    def test_func(self):
        bookinst = self.get_object()
        return self.request.user == bookinst.reader


def rate(request, id):
    post = Filmas.objects.get(id=id)
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        author = request.POST.get('author')
        stars = request.POST.get('stars')
        comment = request.POST.get('comment')
        review = Review(author=author, stars=stars, comment=comment, filmas=post)
        review.save()
        return redirect('success')

    form = ReviewForm()
    context = {
        "form": form

    }
    return render(request, 'rate.html', context)

def success(request):
    return render(request, "success.html")