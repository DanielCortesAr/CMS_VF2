from django import forms
from .models import EstadoFuerza
from .models import ContactoEmergencia, Vehiculos, ArmaLarga, ArmaCorta, Folios

class EstadoFuerzaForm(forms.ModelForm):

    nuevo_contacto_nombre = forms.CharField(
        required=False,
        label="Nombre del Nuevo Contacto",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_contacto_telefono = forms.CharField(
        required=False,
        label="Teléfono del Nuevo Contacto",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_contacto_relacion = forms.CharField(
        required=False,
        label="Relación del Nuevo Contacto",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Campos adicionales para agregar un nuevo vehículo
    nuevo_vehiculo_marca = forms.CharField(
        required=False,
        label="Marca del Nuevo Vehículo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_vehiculo_modelo = forms.CharField(
        required=False,
        label="Modelo del Nuevo Vehículo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_vehiculo_placas = forms.CharField(
        required=False,
        label="Placa del Nuevo Vehículo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Campos adicionales para agregar una nueva arma larga
    nueva_armaLarga_marca = forms.CharField(
        required=False,
        label="Marca del Arma",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nueva_armaLarga_modelo = forms.CharField(
        required=False,
        label="Modelo del Arma",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nueva_armaLarga_matricula = forms.CharField(
        required=False,
        label="Matricula del Arma",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Campos adicionales para agregar una nueva arma larga
    nueva_armaCorta_marca = forms.CharField(
        required=False,
        label="Marca del Arma 2",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nueva_armaCorta_modelo = forms.CharField(
        required=False,
        label="Modelo del Arma 2",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nueva_armaCorta_matricula = forms.CharField(
        required=False,
        label="Matricula del Arma 2",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Campos adicionales para agregar un nuevo folio
    nuevo_folio_seguro_social = forms.CharField(
        required=False,
        label="Seguro Social",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_folio_curp = forms.CharField(
        required=False,
        label="Curp",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_folio_cuip = forms.CharField(
        required=False,
        label="Cuip",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_folio_folio_credencial = forms.CharField(
        required=False,
        label="Folio de Credencial",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_folio_taza = forms.CharField(
        required=False,
        label="Taza",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nuevo_folio_no_oficio = forms.CharField(
        required=False,
        label="N. Oficio",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = EstadoFuerza
        fields = '__all__'
        widgets = {
            'fecha_alta': forms.DateInput(attrs={'type': 'date'}),
            'fecha_actual_adscripcion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vigencia_c3': forms.DateInput(attrs={'type': 'date'}),
            'genero': forms.RadioSelect,
        }
    
        def save(self, commit=True):
            # Guardar el formulario normalmente
            estado_fuerza = super().save(commit=False)

            if commit:
                estado_fuerza.save()    
            return estado_fuerza
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos relacionados opcionales en el formulario
        self.fields['vehiculo'].required = False
        self.fields['arma_larga'].required = False
        self.fields['arma_corta'].required = False
        self.fields['folios'].required = False

class ContactoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['nombre_contactoEmergencia', 'telefono_contactoEmergencia', 'parentesco']
        widgets = {
            'nombre_contactoEmergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contactoEmergencia': forms.TextInput(attrs={'class': 'form-control'}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = ['marca', 'modelo', 'placas']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'placas': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ArmaLargaForm(forms.ModelForm):
    class Meta:
        model = ArmaLarga
        fields = ['marca_armaLarga', 'modelo_armaLarga', 'matricula_armaLarga']
        widgets = {
            'marca_armaLarga': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_armaLarga': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula_armaLarga': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ArmaCortaForm(forms.ModelForm):
    class Meta:
        model = ArmaCorta
        fields = ['marca_armaCorta', 'modelo_armaCorta', 'matricula_armaCorta']
        widgets = {
            'marca_armaCorta': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_armaCorta': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula_armaCorta': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FolioForm(forms.ModelForm):
    class Meta:
        model = Folios
        fields = ['seguro_social', 'curp', 'cuip', 'folio_credencial', 'taza', 'no_oficio']
        widgets = {
            'seguro_social': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
            'cuip': forms.TextInput(attrs={'class': 'form-control'}),
            'folio_credencial': forms.TextInput(attrs={'class': 'form-control'}),
            'taza': forms.TextInput(attrs={'class': 'form-control'}),
            'no_oficio': forms.TextInput(attrs={'class': 'form-control'}),
        }