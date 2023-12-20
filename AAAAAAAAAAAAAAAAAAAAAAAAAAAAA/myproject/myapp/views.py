# myapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CamionetaForm
from .models import Camioneta
import sqlite3



def ver_estados(request):

    # Lista de pares de datos (patente, estado)
    datos_camionetas = [
        #("ABC123", "Disponible"),
        #("XYZ789", "En arriendo"),
        # Agrega más datos según sea necesario
    ]

    con = sqlite3.connect("DBcamioneta.db")
    cur = con.cursor()
    cur.execute("SELECT Patente, Estado FROM Camioneta;")
    for row in cur.fetchall():
        #print(row[0])
        datos_camionetas.append((row[0],row[1]))
        
    con.commit()
    con.close()


    return render(request, 'myapp/ver_estados.html', {'datos_camionetas': datos_camionetas})

def arrendar_camioneta(request):
    if request.method == 'POST':
        form = CamionetaForm(request.POST)
        if form.is_valid():
            patente = form.cleaned_data['patente']
            try:
                #query para verificar que este la patente y el auto disponibles
                con = sqlite3.connect("DBcamioneta.db")
                cur = con.cursor()
                cur.execute("SELECT Patente FROM Camioneta WHERE Patente = '"+ patente+ "';")
                if len(cur.fetchall()) == 0:
                    print("ERROR:Revise que el vehiculo esta disponible(len=0)")
                else:
                    #Hacer query para cambiar estado a Arrendado (2)
                    try:
                        con = sqlite3.connect("DBcamioneta.db")

                        cur = con.cursor()
                        cur.execute("UPDATE Camioneta SET Estado = 2 WHERE Patente = '"+patente+"';")
                        con.commit()
                        con.close()

                       
                        return redirect('arrendar_camioneta')
                    except:
                        print("ERROR: hubo problemas con su arriendo intente denuevo")
                    
            except:
                print("ERROR:Revise que el vehiculo esta disponible(except)")

            
            
        else:
            return HttpResponse("La camioneta no está disponible para arrendar.")
    else:
        form = CamionetaForm()

    return render(request, 'myapp/arrendar_camioneta.html', {'form': form})

def entregar_camioneta(request):
    if request.method == 'POST':
        form = CamionetaForm(request.POST)
        if form.is_valid():
            patente = form.cleaned_data['patente']
            try:
                #query para verificar que este la patente 
                con = sqlite3.connect("DBcamioneta.db")
                cur = con.cursor()
                cur.execute("SELECT Patente FROM Camioneta WHERE Patente = '"+ patente+ "';")
                if len(cur.fetchall()) == 0:
                    print("ERROR:Revise que el vehiculo esta disponible(len=0)")
                else:
                    #Hacer query para cambiar estado a DISPONIBLE (1)
                    try:
                        con = sqlite3.connect("DBcamioneta.db")

                        cur = con.cursor()
                        cur.execute("UPDATE Camioneta SET Estado = 1 WHERE Patente = '"+patente+"';")
                        con.commit()
                        con.close()

                       
                        return redirect('entregar_camioneta')
                    except:
                        print("ERROR: hubo problemas con su ENTREGA intente denuevo")
                    
            except:
                print("ERROR:Revise que el vehiculo esta disponible(except)")

            
            
        else:
            return HttpResponse("La camioneta no está disponible para arrendar.")
    else:
        form = CamionetaForm()

    return render(request, 'myapp/entregar_camioneta.html', {'form': form})

def mantenimiento_camioneta(request):
    if request.method == 'POST':
        form = CamionetaForm(request.POST)
        if form.is_valid():
            patente = form.cleaned_data['patente']
            try:
                #query para verificar que este la patente y el auto disponibles
                con = sqlite3.connect("DBcamioneta.db")
                cur = con.cursor()
                cur.execute("SELECT Patente FROM Camioneta WHERE Patente = '"+ patente+ "';")
                if len(cur.fetchall()) == 0:
                    print("ERROR:Revise que el vehiculo esta disponible(len=0)")
                else:
                    #Hacer query para cambiar estado a Arrendado (2)
                    try:
                        con = sqlite3.connect("DBcamioneta.db")

                        cur = con.cursor()
                        cur.execute("UPDATE Camioneta SET Estado = 0 WHERE Patente = '"+patente+"';")
                        con.commit()
                        con.close()

                       
                        return redirect('mantenimiento_camioneta')
                    except:
                        print("ERROR: hubo problemas con su arriendo intente denuevo")
                    
            except:
                print("ERROR:Revise que el vehiculo esta disponible(except)")

            
            
        else:
            return HttpResponse("La camioneta no está disponible para arrendar.")
    else:
        form = CamionetaForm()

    return render(request, 'myapp/mantenimiento_camioneta.html', {'form': form})
