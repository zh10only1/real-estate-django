from django.shortcuts import render, redirect, get_object_or_404
from . models import Interface
from . forms import InterfaceForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator  ## For Pagination
# Create your views here.
from pages.models import Topbar

def interface(request):

    interface = Interface.objects.order_by('-created').filter(is_published=True)  ## Check or uncheck in admin area
    tb = Topbar.objects.get()
    ### Pagination Start ###
    paginator = Paginator(interface, 6)   ## how much item i want to show in each page
    page = request.GET.get('page')
    paged_interface = paginator.get_page(page)
    ### Pagination End ###

    context = {
        'interface': paged_interface,
        'tb': tb,
    }

    return render(request, 'listings/interface.html', context)


def createInterface(request):
    if request.method == 'POST':
        # print(request.POST)
        form = InterfaceForm(request.POST)
        if form.is_valid():
            interface_item = form.save(commit=False)
            interface_item.save()
            # form.save()
            return redirect('interface')
    else:
        form = InterfaceForm()
    tb = Topbar.objects.get()
    return render(request, 'listings/interface_form.html', {'form' : form, 'tb':tb})


def updateInterface(request, interface_id=None):
    interface = get_object_or_404(Interface, id=interface_id)
    form = InterfaceForm(request.POST or None, instance=interface)

    if form.is_valid():
        form.save()
        return redirect('interface')
    tb = Topbar.objects.get()
    return render(request, 'listings/interface_form.html', {'form' : form, 'tb':tb})



def interfaceDetail(request, inter_id):

    interface_details = get_object_or_404(Interface, pk=inter_id)   ## if page doesn't exist, it will show page not found(error message)
    tb = Topbar.objects.get()
    context = {
        'interface_details': interface_details,
        'tb': tb,
    }

    return render(request, 'listings/interface-detail.html', context)
