from django.shortcuts import render, get_object_or_404, redirect, render_to_response

from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
import math
from django.conf import settings

from .models import Data
from .forms import DataForm
import pandas as pd

# Create your views here.


def file_upload(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)
        #print(data_form)
        if data_form.is_valid():
            print("valid")
            datasave = data_form.save(commit= False)
            if 'file_name' in request.FILES:
                data_form.file_name = request.FILES['file_name']
            data_form.save()
            print (settings.MEDIA_ROOT+"Files/"+str(data_form.file_name))
            filepath = str(settings.MEDIA_ROOT+"/Files/"+str(data_form.file_name))
            request.session['filepath'] = filepath
            return redirect('analytics:index')# TODO: redirect url

        else:
            print(data_form.errors)
            return render(request, 'analytics/error.html')

    else:
        data_form = DataForm()
        return render(request, 'analytics/file_upload.html',{'data_form':data_form})

def index(request):
    filepath = request.session['filepath']
    df = pd.read_csv(filepath)
    if request.method == "GET" :
        columns = df.columns
        data = df.head()
        data = data.to_html()
        return render_to_response('analytics/index.html',{'columns':columns, 'data':data})

    elif request.method == "POST" :
        filepath = request.session['filepath']
        domain  = request.POST['domain'].split()
        eqn     = request.POST['equation']
        domain = range( int(domain[0]), int(domain[1]) )
        y = [ eval(eqn) for x in domain ]
        title = 'y = ' + eqn

        plot = figure(title= title , x_axis_label= 'X-Axis', y_axis_label= 'Y- Axis', plot_width =400, plot_height =400)
        plot.line(domain, y, legend= 'f(x)', line_width = 2)
        script, div = components(plot)

        return render_to_response( 'analytics/index.html', {'script' : script , 'div' : div} )


    else:
        pass



def uploaded(request):
    return render(request, 'analytics/uploaded.html')
