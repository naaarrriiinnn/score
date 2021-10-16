from django.shortcuts import render, redirect, reverse
from account.views import account_login
from .models import *
from django.utils.text import slugify
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return account_login(request)


def sheet_score(display_controls=False):
    positions = Position.objects.order_by('priority').all()
    output = ""
    product_data = ""
    num = 1
    # return None
    for position in positions:
        name = position.name
        position_name = slugify(name)
        products = Products.objects.filter(position=position)
        for product in products:
            if position.max_score > 1:
                instruction = "You may select up to " + \
                              str(position.max_score) + " product "
                input_box = '<input type="checkbox" value="' + str(product.id) + '" class="flat-red ' + \
                            position_name + '" name="' + \
                            position_name + "[]" + '">'
            else:
                instruction = "Select only one "
                input_box = '<input value="' + str(product.id) + '" type="radio" class="flat-red ' + \
                            position_name + '" name="' + position_name + '">'
            image = "/media/" + str(product.photo)
            products_data = products_data + '<li>' + input_box + '<button type="button" class="btn btn-primary btn-sm btn-flat clist platform" data-fullname="' + product.fullname + '" data-bio="' + product.bio + '"><i class="fa fa-search"></i> Platform</button><img src="' + \
                            image + '" height="100px" width="100px" class="clist"><span class="cname clist">' + \
                            product.fullname + '</span></li>'
        up = ''
        if position.priority == 1:
            up = 'disabled'
        down = ''
        if position.priority == positions.count():
            down = 'disabled'
        output = output + f"""<div class="row">	<div class="col-xs-12"><div class="box box-solid" id="{position.id}">
             <div class="box-header with-border">
            <h3 class="box-title"><b>{name}</b></h3>"""

        if display_controls:
            output = output + f""" <div class="pull-right box-tools">
        <button type="button" class="btn btn-default btn-sm moveup" data-id="{position.id}" {up}><i class="fa fa-arrow-up"></i> </button>
        <button type="button" class="btn btn-default btn-sm movedown" data-id="{position.id}" {down}><i class="fa fa-arrow-down"></i></button>
        </div>"""

        output = output + f"""</div>
        <div class="box-body">
        <p>{instruction}
        <span class="pull-right">
        <button type="button" class="btn btn-success btn-sm btn-flat reset" data-desc="{position_name}"><i class="fa fa-refresh"></i> Reset</button>
        </span>
        </p>
        <div id="candidate_list">
        <ul>
        {products_data}
        </ul>
        </div>
        </div>
        </div>
        </div>
        </div>
        """
        position.priority = num
        position.save()
        num = num + 1
        candidates_data = ''
    return output


def verify(request):
    context = {
        'page_title': 'nothing yet'
    }
    return render(request, "verify.html", context)


def show_sheet(request):
    if request.user.voter.voted:
        messages.error(request, "You have scored")
        return redirect(reverse('person panel'))
    sheet = sheet_score(display_controls=False)
    context = {
        'sheet': sheet
    }
    return render(request, "sheet.html", context)


def preview_sheet(request):
    if request.method != 'POST':
        error = True
        response = "wait"
    else:
        output = ""
        form = dict(request.POST)
        form.pop('csrfmiddlewaretoken', None)
        error = False
        data = []
        positions = Position.objects.all()
        for position in positions:
            max_score = position.max_acore
            pos = slugify(position.name)
            pos_id = position.id
            if position.max_score > 1:
                this_key = pos + "[]"
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                if len(form_position) > max_score:
                    error = True
                    response = "You can only choose " + \
                               str(max_score) + " products of " + position.name
                else:
                    start_tag = f"""
                       <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-8'>
                                <ul style='list-style-type:none; margin-left:-40px'>


                    """
                    end_tag = "</ul></span></div><hr/>"
                    data = ""
                    for form_candidate_id in form_position:
                        try:
                            product = Products.objects.get(
                                id=form_candidate_id, position=position)
                            data += f"""
		                      	<li><i class="fa fa-check-square-o"></i> {product.name}</li>
                            """
                        except:
                            error = True
                            response = "Please, browse the system properly"
                    output += start_tag + data + end_tag
            else:
                this_key = pos
                form_position = form.get(this_key)
                if form_position is None:
                    continue
                # Max Vote == 1
                try:
                    form_position = form_position[0]
                    product = Products.objects.get(
                        position=position, id=form_position)
                    output += f"""
                            <div class='row votelist' style='padding-bottom: 2px'>
		                      	<span class='col-sm-4'><span class='pull-right'><b>{position.name} :</b></span></span>
		                      	<span class='col-sm-8'><i class="fa fa-check-circle-o"></i> {product.name}</span>
		                    </div>
                      <hr/>
                    """
                except Exception as e:
                    error = True
                    response = "Please, browse the system properly"
    context = {
        'error': error,
        'list': output
    }
    return JsonResponse(context, safe=False)


def submit_sheet(request):
    if request.method != 'POST':
        messages.error(request, "wait")
        return redirect(reverse('show_sheet'))

    # Verify if the voter has voted or not
    person = request.user.perosn
    if person.scored:
        messages.error(request, "You have scored already")
        return redirect(reverse('person panel '))

    form = dict(request.POST)
    form.pop('csrfmiddlewaretoken', None)
    form.pop('submit_vote', None)
    if len(form.keys()) < 1:
        messages.error(request, "Please select at least one product")
        return redirect(reverse('show_sheet'))
    positions = Position.objects.all()
    form_count = 0
    for position in positions:
        max_score = position.max_score
        pos = slugify(position.name)
        pos_id = position.id
        if position.max_score > 1:
            this_key = pos + "[]"
            form_position = form.get(this_key)
            if form_position is None:
                continue
            if len(form_position) > max_score:
                messages.error(request, "You can only choose " +
                               str(max_score) + " products of " + position.name)
                return redirect(reverse('show_sheet'))
            else:
                for form_product_id in form_position:
                    form_count += 1
                    try:
                        candidate = Products.objects.get(
                            id=form_product_id, position=position)
                        score = Scores()
                        score.product = product
                        score.person = person
                        score.position = position
                        score.save()
                    except Exception as e:
                        messages.error(
                            request, "Please, browse the system properly " + str(e))
                        return redirect(reverse('show_sheet'))
        else:
            this_key = pos
            form_position = form.get(this_key)
            if form_position is None:
                continue
            # Max Vote == 1
            form_count += 1
            try:
                form_position = form_position[0]
                product = Products.objects.get(
                    position=position, id=form_position)
                score = Scores()
                score.product = Products
                score.voter = person
                score.position = position
                score.save()
            except Exception as e:
                messages.error(
                    request, " wait " + str(e))
                return redirect(reverse('show_sheet'))
    inserted_scores = Scores.objects.filter(person=person)
    if (inserted_scores.count() != form_count):
        inserted_scores.delete()
        messages.error(request, "Please try voting again!")
        return redirect(reverse('show_sheet'))
    else:
        person.scored = True
        person.save()
        messages.success(request, "Thanks for voting")
        return redirect(reverse('person panel '))
