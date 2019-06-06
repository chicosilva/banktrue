from django.shortcuts import render, redirect, reverse
from core.decorators import access_required
from core import list_paginator, list_filter, search_filter
from django.contrib import messages
from .models import Categoria
from django.db.models import Q
from .forms import CategoriaForm


@access_required('lojista_pk', 'lojistas:login')
def lista(request):
    
    lojista = request.lojista.obj_responsavel()

    kwargs = list_filter(['nome', ], request, data_inicio='created_at__gte', data_fim='created_at__lte')
    
    kwargs['lojista'] = lojista
    
    nome = search_filter('nome', request)
    
    object_list = Categoria.objects.filter(**kwargs).\
        filter(Q(**nome)).order_by('nome')

    dados = {
        'categorias': list_paginator(request, object_list, 50),
    }
    
    return render(request, 'categorias/lista.html', dados)


@access_required('lojista_pk', 'lojistas:login')
def novo(request):
    
    lojista = request.lojista.obj_responsavel()

    if request.method == 'POST':
    
        form = CategoriaForm(request.POST)
        
        if form.is_valid():

            form.save()

            messages.success(request, 'Cadastrado com sucesso!')
            return redirect(reverse('categorias:lista'))
        
    else:
        form = CategoriaForm()

    return render(request, 'categorias/novo.html', {'form': form})



@access_required('lojista_pk', 'lojistas:login')
def editar(request, id):
    
    categoria = Categoria.objects.get(uuid=id)

    if request.method == 'POST':
    
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():

            form.save()
            
            messages.success(request, 'Atualizado com sucesso!')
            return redirect(reverse('categorias:lista'))
        
    else:
        form = CategoriaForm(instance=categoria)

    dados = {'form': form, 'categoria': categoria}
    return render(request, 'categorias/novo.html', dados)


@access_required('lojista_pk', 'lojistas:login')
def remover(request, id):
    
    obj = Categoria.objects.get(uuid=id)

    if request.method == 'POST':
        
        obj.cancela_registro().save()
        messages.success(request, 'Removido com sucesso!')
        return redirect(reverse('categorias:lista'))

    url = reverse('categorias:remover', kwargs={'id': obj.uuid})
    return render(request, 'core/remover.html', {'obj': obj, 'url_remocao': url})
