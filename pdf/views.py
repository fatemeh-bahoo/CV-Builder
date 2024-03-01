from django.shortcuts import render
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

# Create your views here.

@csrf_exempt
def accept(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        summary = request.POST['summary']
        degree = request.POST['degree']
        school = request.POST['school']
        university = request.POST['university']
        previous_work = request.POST['previous_work']
        skills = request.POST['skills']
        website = request.POST['website']

        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills, website=website)
        profile.save()
    return render(request, 'pdf/accept.html')



def cv(request, id):
    profiles = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/cv.html')
    html = template.render({'profiles': profiles})
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    config = pdfkit.configuration(wkhtmltopdf='/wkhtmltox/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, options=options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "cv.pdf"

    return response

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})
    