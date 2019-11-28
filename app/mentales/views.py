from django.shortcuts import render
from django.shortcuts import redirect
from app.mentales.models import Modulo
from django.contrib import messages

def index(request):
    enfermedades2 = Modulo.objects.all()
    return render(request,'index.html',{'enfermedades': enfermedades2})

def diagnostico_general(request):
    enfermedades = Modulo.objects.all().values_list('enfermedad','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15')
    if request.method == 'POST':
        usuario = request.POST.getlist('usuario[]')
        for x in range(0,15):
            usuario[x] = int(usuario[x])
        cruce = []
        tempo = []
        umbral = 25
        mayor = {'enfermedad':'','total':0}
        res = []
        for i in range(0,10):
            tempo.append(enfermedades[i][0])
            for x in range(1,16):
                tempo.append(min(enfermedades[i][x],usuario[x-1]))
            cruce.append(tempo)
            tempo = []
        
        for enfermedad in cruce:
            suma = 0
            for i in range(1,16):
                suma += enfermedad[i]
            if suma > umbral:
                if suma > mayor['total']:
                    res = []
                    mayor['enfermedad'] = enfermedad[0]
                    mayor['total'] = suma          
                    res.append(mayor)
                    
                elif mayor['total'] == suma:
                    aux ={}
                    aux['enfermedad'] = enfermedad[0]
                    aux['total'] = suma
                    res.append(aux)
            
        if len(res) >= 1:
            request.session['resultado'] = res
        else:
            try:
                del request.session['resultado']
            except:
                pass
        return redirect('/resultado/')
    return render(request,'preguntas.html')

def resultados(request):
    try: 
        resultado = request.session['resultado']
        return render(request,'results.html',{'resultados':resultado})
    except:
        return render(request,'results.html',{'resultados':'no'})

enfermedades = []
def transtornos(request):
    if request.method == 'POST':
        global enfermedades
        transtornos = request.POST.getlist('transtornos[]')
        for x in range(0,len(transtornos)):
            enfermedades += (Modulo.objects.filter(enfermedad =transtornos[x]).values_list('enfermedad','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15'))
        if len(transtornos) >= 2:
            return redirect('/diagnostico_especifico/')
        else:
            messages.error(request,'1')
    return render(request,'especifico.html')



def diagnostico_especifico(request):
    global enfermedades
    # print(enfermedades)
    # union = []
    # for i in range(0,15):
    #     tempo = []
    #     for x in range(len(enfermedades)):
    #         tempo.append(enfermedades[x][i])
    #     union.append(max(tempo))
    if request.method == 'POST':
        usuario = request.POST.getlist('usuario[]')
        for x in range(0,15):
            usuario[x] = int(usuario[x])
        cruce = []
        tempo = []
        umbral = 25
        mayor = {'enfermedad':'','total':0}
        res = []
        for i in range(0,len(enfermedades)):
            tempo.append(enfermedades[i][0])
            for x in range(1,16):
                tempo.append(min(enfermedades[i][x],usuario[x-1]))
            cruce.append(tempo)
            tempo = []
        for enfermedad in cruce:
            suma = 0
            for i in range(1,16):
                suma += enfermedad[i]
            if suma > umbral:
                if suma > mayor['total']:
                    res = []
                    mayor['enfermedad'] = enfermedad[0]
                    mayor['total'] = suma
                    res.append(mayor)
                elif mayor['total'] == suma:
                    aux ={}
                    aux['enfermedad'] = enfermedad[0]
                    aux['total'] = suma
                    res.append(aux)
            
        enfermedades = []
        if len(res) >= 1:
            request.session['resultado'] = res
        else:
            try:
                del request.session['resultado']
            except:
                pass
        return redirect('/resultado/')
    return render(request,'preguntas.html')