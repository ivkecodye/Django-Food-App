from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
from django.template import loader
from .forms import ItemForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

# Create your views here.


class IndexClassView(ListView):
    model = Item
    template_name = "foodapp/index.html"
    context_object_name = "item_list"


def item(request):
    return HttpResponse("Welcome to Items page!")


class FoodDetail(DetailView):
    model = Item
    template_name = "foodapp/detail.html"


class CreateItem(CreateView):
    model = Item
    fields = ["item_name", "item_desc", "item_price", "item_image"]
    template_name = "foodapp/item-form.html"

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


def update_item(request, id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect("foodapp:index")
    return render(request, "foodapp/item-form.html", {"form": form, "item": item})


def delete_item(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect("foodapp:index")
    return render(request, "foodapp/item-delete.html", {"idem": item})
