from django.shortcuts import render
from account.forms import CustomUserForm
from user.forms import *
from django.contrib import messages



def find_n_winners(data, n):
    final_list = []
    product_data = data[:]
    for i in range(0, n):
        max1 = 0
        if len(product_data) == 0:
            continue
        this_winner = max(product_data, key=lambda x: x['scores'])
        # TODO: Check if None
        this = this_winner['name'] + \
            " with " + str(this_winner['scores']) + " scores"
        final_list.append(this)
        product_data.remove(this_winner)
    return ", &nbsp;".join(final_list)



def panel(request):
    positions = Position.objects.all().order_by('priority')
    product = Products.objects.all()
    person = Person.objects.all()
    scored_person = Person.objects.filter(voted=1)
    list_of_product = []
    scores_count = []
    chart_data = {}

    for position in positions:
        list_of_candidates = []
        score_count = []
        for product in Products.objects.filter(position=position):
            list_of_product.append(product.fullname)
            scores = Scores.objects.filter(product=product).count()
            scores_count.append(scores)
        chart_data[position] = {
            'product': list_of_product,
            'acores': score_count,
            'pos_id': position.id
        }

    context = {
        'position_count': positions.count(),
        'product_count': product.count(),
        'person_count': person.count(),
        'scored_person_count': scored_person.count(),
        'positions': positions,
        'chart_data': chart_data,
    }
    return render(request, "admin/home.html", context)


def person(request):
    person = Person.objects.all()
    userForm = CustomUserForm(request.POST or None)
    personForm = PersonForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': personForm,
        'person': person,
    }
    if request.method == 'POST':
        if userForm.is_valid() and personForm.is_valid():
            user = userForm.save(commit=False)
            person = personForm.save(commit=False)
            person.admin = user
            user.save()
            person.save()
            messages.success(request, "New voter created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/voters.html", context)








def viewPositions(request):
    positions = Position.objects.order_by('-priority').all()
    form = PositionForm(request.POST or None)
    context = {
        'positions': positions,
        'form1': form,
        'page_title': "Positions"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.priority = positions.count() + 1  # Just in case it is empty.
            form.save()
            messages.success(request, "New Position Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/positions.html", context)



def viewProducts(request):
    products = Products.objects.all()
    form = ProductForm(request.POST or None, request.FILES or None)
    context = {
        'products': products,
        'form1': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            messages.success(request, "New one Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "products.html", context)



def viewVotes(request):
    scores = Scores.objects.all()
    context = {
        'score': scores,
    }
    return render(request, "score.html", context)


