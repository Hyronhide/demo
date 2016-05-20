# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalogo.apps.home.forms import contact_form, Login_form, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage #paginator
from django.contrib.auth.models import User 
##
from django.core.mail import EmailMultiAlternatives
from catalogo.apps.ventas.forms import add_product_form
from catalogo.apps.ventas.forms import add_brant_form
from catalogo.apps.ventas.models import Producto,Marca,Categoria
from django.db.models import Sum,Max

#def base_view (request):
#	return render_to_response('home/base.html' , context_instance = RequestContext(request) )
def about_view (request):
	return render_to_response('home/about.html' , context_instance = RequestContext(request) )
def index_view (request):
	return render_to_response('home/index.html' , context_instance = RequestContext(request) )	

def contacto_view(request):
	info_enviado = False 
	email = ""
	title = ""
	text = ""
	if request.method == "POST":
		formulario = contact_form(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['correo']
			title = formulario.cleaned_data['titulo']
			text = formulario.cleaned_data['texto']
			''' Bloque configuracion de envio por GMAIL '''
			to_admin = 'david-b60@hotmail.com'
			html_content = "Informacion recibida de %s <br> ---Mensaje--- <br> %s"%(email,text)
			msg = EmailMultiAlternatives('correo de contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html')
			msg.send()
			''' Fin del Bloque '''
	else:		
		formulario = contact_form()
	ctx = {'form':formulario,'email':email,'title':title,'text':text,'info_enviado':info_enviado}
	return render_to_response('home/contacto.html',ctx,context_instance = RequestContext(request))	

def single_product_view(request, id_prod): 
	prod = Producto.objects.get(id = id_prod)#SELECT * from Producto WHERE Producto.id = id_prod 	
	ctx={'producto':prod}
	return render_to_response('home/single_producto.html',ctx,context_instance = RequestContext(request))

def productos_view(request,pagina): 
	#lista_prod = Producto.objects.filter(status = True)
	#lista_prod = Producto.objects.filter(marca_id = 3)
	#lista_prod = Producto.objects.all().order_by('nombre')
	#lista_prod = Producto.objects.all().order_by('nombre').reverse()
	#lista_prod = Producto.objects.filter(nombre =  'rizadas').update(nombre = 'RIZADAS')
	#lista_prod = Producto.objects.all()[:5]
	#lista_prod = Producto.objects.all()[3:5]
	#lista_prod = Producto.objects.filter(id__in = [13 , 9 ,6])
	#lista_prod = Producto.objects.filter(id__gt = 3)
	#lista_prod = Producto.objects.filter(nombre__startswith='a')
	#lista_prod = Producto.objects.filter(nombre__endswith='a')
	#lista_prod = Producto.objects.order_by('nombre').all()[:5]
	#lista_prod = Producto.objects.exclude(nombre__startswith='a')
	#lista_prod = Producto.objects.exclude(nombre__startswith='a').all()[:5]
	#lista_prod = Producto.objects.exclude(nombre__endswith='a').all()[3:7]
	#lista_prod = Producto.objects.filter(marca__nombre='pepsi').count()
	#lista_prod = Producto.objects.get(id__exact='4')
	#lista_prod = Producto.objects.get(nombre__iexact='cocosette')
	#lista_prod = Producto.objects.all().aggregate(Max('precio'))

	#lista_prod = Producto.objects.exclude(marca__nombre='Margarita') #Muestra todo los productos que no sean de la marca margarita
	#lista_prod = Producto.objects.select_related().filter(marca__nombre='Pepsi') #Muestra todos los productos relacionados con la marca "Pepsi"
	#lista_prod = Producto.objects.get(id__exact='5') #Muestra el producto con el id 5 por coincidencias exactas
	#lista_prod = Producto.objects.filter(nombre__iexact='BEBIDA1') #Muestra el producto con el nombre bebida1 sin distinguir mayusculas de minusculas por coincidencias exactas
	#lista_prod = Producto.objects.filter(nombre__contains='bebida') #Muestra el/los producto(s) con la subcadena bebida distinguiendo mayusculas de minusculas
	#lista_prod = Producto.objects.filter(nombre__icontains='BEBIDA') #Muestra el/los producto(s) con la subcadena bebida sin distinguir mayusculas de minusculas
	#lista_prod = Producto.objects.filter(nombre__startswith='beb') #Muestra los productos que comiencen y coincidan con el pefijo beb 
	#lista_prod = Producto.objects.filter(nombre__endswith='1') #Muestra los productos coincidan y terminen con el sufijo "1" 
	#lista_prod = Producto.objects.filter(id__gt='5') #Muestra los productos con un id mayor a 5
	#lista_prod = Producto.objects.filter(id__gte='5') #Muestra los productos con un id mayor o igual a 5
	#lista_prod = Producto.objects.filter(id__lt='5') #Muestra los productos con un id menor a 5
	#lista_prod = Producto.objects.filter(id__lte='5') #Muestra los productos con un id menor o igual a 5
	#lista_prod = Producto.objects.filter(id__in=[1,2,5]) #Se Aplica un flitro para mostrar los productos con id 1,2,5
	#lista_prod = Producto.objects.filter(stock__range=(20,40)) #Muestra los productos con stock entre 20 y 40
	#lista_prod = Producto.objects.count() #Calcula el numero de productos existentes
	#lista_prod = Producto.objects.all().aggregate(Sum('precio'))#Calcula la suma de todos los precios de los productos
	#lista_prod = Producto.objects.all().aggregate(Max('precio'))#Devuelve el valor máximo de los precios de los productos
	#lista_prod = Producto.objects.all().aggregate(Min('precio'))#Devuelve el valor minimo de los precios de los productos
	#lista_prod = Producto.objects.filter(categorias__nombre='bebidas') #Muestras todos los productos de la categoria "bebidas"
	#lista_prod = Producto.objects.filter(categorias__nombre='bebidas')


	lista_prod = Producto.objects.filter(status = True)#SELECT * from Producto WHERE status= True
	paginator = Paginator(lista_prod, 3) 
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)

	ctx={'productos':productos}
	return render_to_response('home/productos.html',ctx,context_instance = RequestContext(request))	

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():#verificacmos si el usuario ya esta authenticado o logueado
		return HttpResponseRedirect('/')#si esta logueado lo redirigimos a la pagina principal
	else: #si no esta authenticado 
		if request.method == "POST":
			formulario = Login_form(request.POST) #creamos un objeto de Loguin_form
			if formulario.is_valid(): #si la informacion enviada es correcta		
				usu= formulario.cleaned_data['usuario'] #guarda informacion ingresada del formulario
				pas= formulario.cleaned_data['clave'] #guarda informacion ingresada del formulario
				usuario = authenticate(username = usu,password = pas)#asigna la autenticacion del usuario
				if usuario is not None and usuario.is_active:#si el usuario no es nulo y esta activo
					login(request,usuario)#se loguea al sistema con la informacion de usuario
					return HttpResponseRedirect('/')#redirigimos a la pagina principal
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = Login_form() #creamos un formulario nuevo limpio
		ctx = {'form':formulario, 'mensaje':mensaje}#variable de contexto para pasar info a login.html
		return render_to_response('home/login.html',ctx, context_instance = RequestContext(request))

def logout_view(request):
	logout(request)# funcion de django importda anteriormente
	return HttpResponseRedirect('/')# redirigimos a la pagina principal

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()# Guarda el objeto
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:		
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))