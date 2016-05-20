from catalogo.apps.ventas.models import Producto 
from catalogo.apps.ventas.models import Marca 
from django import forms

class add_product_form( forms.ModelForm ):
	class Meta:
		model = Producto
		#se excluye el status por que en el modelo lo ponemos default=True
		exclude = {'status',}

class add_brant_form( forms.ModelForm ):
	class Meta:
		model = Marca 
		exclude = {'status',}	
		