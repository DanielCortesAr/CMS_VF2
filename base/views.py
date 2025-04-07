from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.db.models import Q, Count
from .models import Vehiculo

from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
 
def exit(request):
    logout(request)
    return redirect('login') 

def lista_vehiculos(request):
    # Obtener todos los vehículos de la base de datos
    vehiculos = Vehiculo.objects.all()
    
    # Pasar los vehículos a la plantilla
    return render(request, 'base/index.html', {'vehiculos': vehiculos})

def grafica_vehiculos(request):
    # Contar el número de los diferentes modelos de los vehiculos
    data_modelo = Vehiculo.objects.values('modelo').annotate(total=Count('id'))
    
    # Contar el número de vehiculos de x año
    data_año = Vehiculo.objects.values('año').annotate(total=Count('id'))
    

    return JsonResponse({
        'modelo': {
            'labels': [item['Modelo'] for item in data_modelo],
            'values': [item['total'] for item in data_modelo],
        },
        'año': {
            'labels': [item['año'] for item in data_año],
            'values': [item['total'] for item in data_año],
        },
    })

def graficas(request):
    return render(request, 'base/graficas.html')


"""def generar_pdf_vehiculos(queryset):
    # Crear la respuesta HTTP con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="vehiculos.pdf"'

    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Ancho y alto de la página
    
    # Definir un estilo global para las tablas
    def get_table_style():
        custom_blue = colors.Color(red=21/255, green=47/255, blue=74/255)  # Color personalizado #152F4A
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), custom_blue),  # Color de fondo para el encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color del texto del encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación centrada
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para el encabezado
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Borde de la tabla
        ])

    # Función auxiliar para dividir texto largo en múltiples líneas
    def wrap_text(text, max_width, font_name, font_size):
        """"""
        lines = []
        words = text.split(' ')
        current_line = ''

        for word in words:
            # Verificar si la línea actual + la palabra caben en el ancho máximo
            if p.stringWidth(current_line + word, font_name, font_size) <= max_width:
                current_line += word + ' '
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        lines.append(current_line.strip())  # Agregar la última línea
        return lines

    for estadoFuerza in queryset:
        # Eliminar el título principal y ajustar la posición inicial
        y = height - 40  # Nueva posición inicial sin el título

        # Imagen (si existe)
        if Vehiculo.fotografia_vehiculo:
            try:
                imagen = ImageReader(Vehiculo.fotografia.path)
                p.drawImage(imagen, 100, y - 90, width=100, height=100)
            except Exception as e:
                p.drawString(100, y - 90, "Imagen no disponible")

        # Datos del vehiculo
        p.drawString(220, y , f"Placa: {Vehiculo.placa}")
        p.drawString(220, y - 20, f"Marca: {Vehiculo.marca}")
        p.drawString(220, y - 40, f"Modelo: {Vehiculo.modelo}")
        
        # Manejo de direcciones largas
        direccion = estadoFuerza.direccion
        max_width = 240  # Ancho máximo permitido para la dirección
        font_name = "Helvetica"
        font_size = 12
        wrapped_lines = wrap_text(direccion, max_width, font_name, font_size)

        # Dibujar cada línea de la dirección
        line_height = 15  # Altura entre líneas
        x_position = 220  # Posición horizontal fija para el campo "Dirección"
        y_position = y - 60  # Posición vertical inicial

        for i, line in enumerate(wrapped_lines):
            if i == 0:
                p.drawString(x_position, y_position, f"Dirección: {line}")
            else:
                p.drawString(x_position, y_position - (i * line_height), line)

        # Separador azul
        y -= 110  # Dejar un margen entre los datos y el separador
        p.setLineWidth(1)  # Grosor de 1 punto
        p.setStrokeColorRGB(21/255, 47/255, 74/255)  # Color azul personalizado
        p.line(100, y, width - 60, y)  # Línea horizontal

        # Título de la adscripción
        p.drawString(260, y - 20, "Datos de la Adscripción")
        y -= 20

        # Datos de la adscripción
        p.drawString(100, y - 20, f"Adscripción Actual: {estadoFuerza.adscripcion_actual}")
        p.drawString(100, y - 40, f"Sección: {estadoFuerza.seccion}")
        p.drawString(100, y - 60, f"Fiscalía: {estadoFuerza.fiscalia.nombre_fiscalia if estadoFuerza.fiscalia else 'N/A'}")

        # Crear una tabla para los datos del vehículo
        data_vehiculo = [
            ["Vehículo", "Modelo", "Placas"],
            [estadoFuerza.vehiculo.marca if estadoFuerza.vehiculo else "", 
            estadoFuerza.vehiculo.modelo if estadoFuerza.vehiculo else "", 
            estadoFuerza.vehiculo.placas if estadoFuerza.vehiculo else ""]
        ]
        table_vehiculo = Table(data_vehiculo, colWidths=[150, 150, 150])  # Ancho de las columnas
        table_vehiculo.setStyle(get_table_style())  # Aplicar el estilo global
        table_vehiculo.wrapOn(p, width, height)
        table_vehiculo.drawOn(p, 100, y - 120)  # Dibujar la tabla en la posición deseada

        # Crear una tabla para los datos del arma larga
        data_arma_larga = [
            ["Arma Larga", "Modelo", "Matrícula"],
            [estadoFuerza.arma_larga.marca_armaLarga if estadoFuerza.arma_larga else "", 
            estadoFuerza.arma_larga.modelo_armaLarga if estadoFuerza.arma_larga else "", 
            estadoFuerza.arma_larga.matricula_armaLarga if estadoFuerza.arma_larga else ""]
        ]
        table_arma_larga = Table(data_arma_larga, colWidths=[150, 150, 150])  # Ancho de las columnas
        table_arma_larga.setStyle(get_table_style())  # Aplicar el estilo global
        table_arma_larga.wrapOn(p, width, height)
        table_arma_larga.drawOn(p, 100, y - 180)  # Dibujar la tabla en la posición deseada

        # Crear una tabla para los datos del arma corta
        data_arma_corta = [
            ["Arma Corta", "Modelo", "Matrícula"],
            [estadoFuerza.arma_corta.marca_armaCorta if estadoFuerza.arma_corta else "", 
            estadoFuerza.arma_corta.modelo_armaCorta if estadoFuerza.arma_corta else "", 
            estadoFuerza.arma_corta.matricula_armaCorta if estadoFuerza.arma_corta else ""]
        ]
        table_arma_corta = Table(data_arma_corta, colWidths=[150, 150, 150])  # Ancho de las columnas
        table_arma_corta.setStyle(get_table_style())  # Aplicar el estilo global
        table_arma_corta.wrapOn(p, width, height)
        table_arma_corta.drawOn(p, 100, y - 240)  # Dibujar la tabla en la posición deseada

        # Formaciones y otros datos booleanos
        p.drawString(290, y - 280, "Formaciones")
        y -= 300  # Ajustar posición inicial para estos datos
        espaciado = 20  # Espaciado entre líneas

        if estadoFuerza.formacion_c3:
            p.drawString(100, y, f"Formación C3: ✔")
            y -= espaciado  # Decrementar solo si se imprime
        if estadoFuerza.formacion_inicial:
            p.drawString(100, y, f"Formación Inicial: ✔")
            y -= espaciado
        if estadoFuerza.cuip:
            p.drawString(100, y, f"CUIP: ✔")
            y -= espaciado
        if estadoFuerza.competencias_basicas:
            p.drawString(100, y, f"Competencias Básicas: ✔")
            y -= espaciado
        if estadoFuerza.evaluacion_desempeno:
            p.drawString(100, y, f"Evaluación de Desempeño: ✔")
            y -= espaciado
        if estadoFuerza.cup:
            p.drawString(100, y, f"CUP: ✔")
            y -= espaciado

        p.drawString(100, y, f"Fecha de Vigencia C3: {estadoFuerza.fecha_vigencia_c3}")

        # Separador azul
        y -= 10  # Dejar un margen entre los datos y el separador
        p.setLineWidth(1)  # Grosor de 1 punto
        p.setStrokeColorRGB(21/255, 47/255, 74/255)  # Color azul personalizado
        p.line(100, y, width - 60, y)  # Línea horizontal

        # Crear una tabla para los datos de los folios
        data_folios = [
            ["No.Oficio", "Curp", "Cuip"],
            [estadoFuerza.folios.no_oficio if estadoFuerza.folios else "", 
            estadoFuerza.folios.curp if estadoFuerza.folios else "", 
            estadoFuerza.folios.cuip if estadoFuerza.folios else "",]
        ]
        table_folios = Table(data_folios, colWidths=[150, 150, 150])  # Ancho de las columnas
        table_folios.setStyle(get_table_style())  # Aplicar el estilo global
        table_folios.wrapOn(p, width, height)
        table_folios.drawOn(p, 100, y - 70)  # Dibujar la tabla en la posición deseada

        # Crear una tabla para los datos de los folios
        data_folios2 = [
            ["Credencial", "Taza", "Seguro social"],
            [estadoFuerza.folios.folio_credencial if estadoFuerza.folios else "",
            estadoFuerza.folios.taza if estadoFuerza.folios else "",
            estadoFuerza.folios.seguro_social if estadoFuerza.folios else "",]
        ]
        table_folios = Table(data_folios2, colWidths=[150, 150, 150])  # Ancho de las columnas
        table_folios.setStyle(get_table_style())  # Aplicar el estilo global
        table_folios.wrapOn(p, width, height)
        table_folios.drawOn(p, 100, y - 120)  # Dibujar la tabla en la posición deseada

        # Finalizar la página
        p.showPage()

    # Guardar el PDF
    p.save()
    return response

def generar_pdf_individual(request, pk):
    # Obtener el objeto EstadoFuerza por su ID
    estadoFuerza = get_object_or_404(EstadoFuerza, pk=pk)

    # Generar un queryset con un solo objeto
    queryset = EstadoFuerza.objects.filter(pk=pk)

    # Llamar a la función genérica de generación de PDF
    return generar_pdf_estado_fuerza(queryset)

def generar_pdf_estado_fuerza_personalizado(queryset, opciones):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="estados_fuerza.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    def get_table_style():
        custom_blue = colors.Color(red=21/255, green=47/255, blue=74/255)
        return TableStyle([
            ('BACKGROUND', (0,0), (-1,0), custom_blue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])

    def wrap_text(text, max_width, font_name, font_size):
        lines = []
        words = text.split(' ')
        current_line = ''
        for word in words:
            if p.stringWidth(current_line + word, font_name, font_size) <= max_width:
                current_line += word + ' '
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        lines.append(current_line.strip())
        return lines

    for estadoFuerza in queryset:
        # Eliminar el título principal y ajustar la posición inicial
        y = height - 40  # Nueva posición inicial sin el título

        # Columna izquierda (Fotografía)
        if opciones.get('include_fotografia') and estadoFuerza.fotografia:
            x_data = 220  # Columna derecha si hay foto
            try:
                imagen = ImageReader(estadoFuerza.fotografia.path)
                p.drawImage(imagen, 100, y - 90, width=100, height=100)
            except:
                p.drawString(100, y - 100, "Imagen no disponible")
            y_photo = y - 120
        else:
            x_data = 100  # Columna izquierda si no hay foto
            y_photo = y  # No se reserva espacio para foto

        # Columna derecha (Datos personales y dirección)
        y_data = y

        if opciones.get('include_datos_personales'):
            p.drawString(x_data, y_data, f"Nombre: {estadoFuerza.nombre}")
            p.drawString(x_data, y_data - 20, f"Teléfono: {estadoFuerza.telefono}")
            p.drawString(x_data, y_data - 40, f"Género: {estadoFuerza.genero}")
            y_data -= 60

        if opciones.get('include_direccion'):
            direccion = estadoFuerza.direccion
            wrapped = wrap_text(direccion, 240, 'Helvetica', 12)
            for i, line in enumerate(wrapped):
                p.drawString(x_data, y_data - (i*15), f"Dirección: {line}" if i == 0 else line)
            y_data -= (len(wrapped)*15 + 10)

        # Sincronizar posición vertical
        y = min(y_photo, y_data - 20)

        # Datos de adscripción
        if opciones.get('include_adscripcion'):
            p.setStrokeColorRGB(21/255, 47/255, 74/255)
            p.line(100, y, width-60, y)
            y -= 20

            p.drawString(260, y, "Datos de la Adscripción")
            p.drawString(100, y - 20, f"Adscripción Actual: {estadoFuerza.adscripcion_actual}")
            p.drawString(100, y - 40, f"Sección: {estadoFuerza.seccion}")
            p.drawString(100, y - 60, f"Fiscalía: {estadoFuerza.fiscalia.nombre_fiscalia if estadoFuerza.fiscalia else 'N/A'}")
            y -= 80

        # Tabla de vehículo
        if opciones.get('include_vehiculo') and estadoFuerza.vehiculo:
            data = [
                ["Vehículo", "Modelo", "Placas"],
                [estadoFuerza.vehiculo.marca, estadoFuerza.vehiculo.modelo, estadoFuerza.vehiculo.placas]
            ]
            table = Table(data, colWidths=150)
            table.setStyle(get_table_style())
            table.wrapOn(p, width, height)
            table.drawOn(p, 100, y - 60)
            y -= 60

        # Tabla de arma larga
        if opciones.get('include_arma_larga') and estadoFuerza.arma_larga:
            data = [
                ["Arma Larga", "Modelo", "Matrícula"],
                [estadoFuerza.arma_larga.marca_armaLarga, 
                 estadoFuerza.arma_larga.modelo_armaLarga,
                 estadoFuerza.arma_larga.matricula_armaLarga]
            ]
            table = Table(data, colWidths=150)
            table.setStyle(get_table_style())
            table.wrapOn(p, width, height)
            table.drawOn(p, 100, y - 60)
            y -= 60

        # Tabla de arma corta
        if opciones.get('include_arma_corta') and estadoFuerza.arma_corta:
            data = [
                ["Arma Corta", "Modelo", "Matrícula"],
                [estadoFuerza.arma_corta.marca_armaCorta, 
                 estadoFuerza.arma_corta.modelo_armaCorta,
                 estadoFuerza.arma_corta.matricula_armaCorta]
            ]
            table = Table(data, colWidths=150)
            table.setStyle(get_table_style())
            table.wrapOn(p, width, height)
            table.drawOn(p, 100, y - 60)
            y -= 80

        # Separador 
        if opciones.get('include_formaciones'):
            p.setStrokeColorRGB(21/255, 47/255, 74/255)
            p.line(100, y, width-60, y)
            y -= 20

            p.drawString(290, y, "Formaciones")
            y -= 20
            espaciado = 20
            if estadoFuerza.formacion_c3:
                p.drawString(100, y, "Formación C3: ✔")
                y -= espaciado
            if estadoFuerza.formacion_inicial:
                p.drawString(100, y, "Formación Inicial: ✔")
                y -= espaciado
            if estadoFuerza.cuip:
                p.drawString(100, y, "CUIP: ✔")
                y -= espaciado
            if estadoFuerza.competencias_basicas:
                p.drawString(100, y, "Competencias Básicas: ✔")
                y -= espaciado
            if estadoFuerza.evaluacion_desempeno:
                p.drawString(100, y, "Evaluación de Desempeño: ✔")
                y -= espaciado
            if estadoFuerza.cup:
                p.drawString(100, y, "CUP: ✔")
                y -= espaciado
            if estadoFuerza.fecha_vigencia_c3:
                p.drawString(100, y, f"Fecha de Vigencia C3: {estadoFuerza.fecha_vigencia_c3}")
                y -= 20

        # Folios
        if opciones.get('include_folios'):
            p.setStrokeColorRGB(21/255, 47/255, 74/255)
            p.line(100, y, width-60, y)  # Separador
            y -= 20

            # Crear una tabla para los datos de los folios
            data_folios = [
                ["No.Oficio", "Curp", "Cuip"],
                [
                    estadoFuerza.folios.no_oficio if estadoFuerza.folios else "",
                    estadoFuerza.folios.curp if estadoFuerza.folios else "",
                    estadoFuerza.folios.cuip if estadoFuerza.folios else "",
                ]
            ]

            # Crear la tabla y aplicar el estilo
            table_folios = Table(data_folios, colWidths=[150, 150, 150])  # Ancho de las columnas
            table_folios.setStyle(get_table_style())  # Aplicar el estilo global

            # Dibujar la tabla en la posición deseada
            table_folios.wrapOn(p, width, height)
            table_folios.drawOn(p, 100, y - 50)  # Ajusta la posición vertical
            y -= 50  # Ajusta la posición vertical después de dibujar la tabla

            data_folios = [
                ["Credencial", "Taza", "Seguro social"],
                [
                    estadoFuerza.folios.folio_credencial if estadoFuerza.folios else "",
                    estadoFuerza.folios.taza if estadoFuerza.folios else "",
                    estadoFuerza.folios.seguro_social if estadoFuerza.folios else "",
                ]
            ]

            # Crear la tabla y aplicar el estilo
            table_folios = Table(data_folios, colWidths=[150, 150, 150])  # Ancho de las columnas
            table_folios.setStyle(get_table_style())  # Aplicar el estilo global

            # Dibujar la tabla en la posición deseada
            table_folios.wrapOn(p, width, height)
            table_folios.drawOn(p, 100, y - 50)  # Ajusta la posición vertical
            y -= 50  # Ajusta la posición vertical después de dibujar la tabla

        p.showPage()
    p.save()
    return response

def generar_pdf_individual_p(request, pk):
    estadoFuerza = get_object_or_404(EstadoFuerza, pk=pk)

    if request.method == 'POST':
        opciones = {
            'include_fotografia': 'include_fotografia' in request.POST,
            'include_datos_personales': 'include_datos_personales' in request.POST,
            'include_direccion': 'include_direccion' in request.POST,
            'include_adscripcion': 'include_adscripcion' in request.POST,
            'include_vehiculo': 'include_vehiculo' in request.POST,
            'include_arma_larga': 'include_arma_larga' in request.POST,
            'include_arma_corta': 'include_arma_corta' in request.POST,
            'include_formaciones': 'include_formaciones' in request.POST,
            'include_folios': 'include_folios' in request.POST,
        }

        queryset = EstadoFuerza.objects.filter(pk=pk)
        return generar_pdf_estado_fuerza_personalizado(queryset, opciones)

    return render(request, 'base/pdf_personalizado.html', {'estadoFuerza': estadoFuerza})
 """

""" def es_admin_o_mando(user):
    return user.is_superuser or user.groups.filter(name='Mando').exists()

@login_required
@user_passes_test(es_admin_o_mando)
def graficas(request):
    return render(request, 'base/graficas.html') """