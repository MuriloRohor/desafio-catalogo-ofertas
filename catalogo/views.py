from django.shortcuts import render
from django.http import JsonResponse
from scrapper.ml_scrapper import ScrapperML
from catalogo.models import Product
from django.db.models import Case, When, F
from django.db import models

from django.shortcuts import render
from catalogo.models import Product

from django.db.models import Case, When, F

def produto(request):
    frete_gratis = request.GET.get('frete_gratis', 'false') == 'true'
    entrega_full = request.GET.get('entrega_full', 'false') == 'true'
    produtos = Product.objects.all()

    if frete_gratis:
        produtos = produtos.filter(freight_free=True)
    if entrega_full:
        produtos = produtos.filter(freight_full=True)

    ordenar_por = request.GET.get('ordenar_por', 'preco')
    if ordenar_por == 'preco':
        produtos = produtos.annotate(
            price_to_order=Case(
                When(price_with_discount__gt=0, then=F('price_with_discount')),
                default=F('price')
            )
        ).order_by('-price_to_order')
    
    elif ordenar_por == 'menor_preco':
        produtos = produtos.annotate(
            price_to_order=Case(
                When(price_with_discount__gt=0, then=F('price_with_discount')),
                default=F('price')
            )
        ).order_by('price_to_order')
    
    elif ordenar_por == 'maior_desconto':
        produtos = produtos.order_by('-percentual_discount')

    # Maior preço
    maior_preco = produtos.annotate(
        price_to_order=Case(
            When(price_with_discount__gt=0, then=F('price_with_discount')),
            default=F('price')
        )
    ).order_by('-price_to_order').first()

    # Menor preço
    menor_preco = produtos.annotate(
        price_to_order=Case(
            When(price_with_discount__gt=0, then=F('price_with_discount')),
            default=F('price')
        )
    ).order_by('price_to_order').first()


    context = {
        "produtos": produtos,
        "maior_preco": maior_preco,
        "menor_preco": menor_preco,
        "frete_gratis": frete_gratis,
        "entrega_full": entrega_full,
        "ordenar_por": ordenar_por
    }
    return render(request, 'produtos.html', context=context)







def scrape_products(request):
    scraper = ScrapperML(arguments=[
        "--headless"
    ])
    products = scraper.list_products()
    for i, product in enumerate(products):
        print(f"item {i}")
        existing_product = Product.objects.filter(cod_ml=product['cod_ml']).first()
        if existing_product:
            existing_product.name = product['name']
            existing_product.price = product['price']
            existing_product.image_url = product['image_url']
            existing_product.url = product['url']
            existing_product.installment_options = product['installment_options']
            existing_product.price_with_discount = product['price_with_discount']
            existing_product.percentual_discount = product['percentual_discount']
            existing_product.freight_free = product['freight_free']
            existing_product.freight_full = product['freight_full']
            existing_product.save()
        else:
            Product.objects.create(
                cod_ml=product['cod_ml'],
                name=product['name'],
                price=product['price'],
                image_url=product['image_url'],
                url=product['url'],
                installment_options=product['installment_options'],
                price_with_discount=product['price_with_discount'],
                percentual_discount=product['percentual_discount'],
                freight_free=product['freight_free'],
                freight_full=product['freight_full']
            )
    return JsonResponse({"message": "Scraping completed successfully", "status": "success"})
