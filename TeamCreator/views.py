import json
import logging

import django.forms
from django.shortcuts import render
from TeamCreator.teams import Student, group_students

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from TeamCreator.forms import UploadFileForm


def index(request):
    return HttpResponseRedirect('upload_file')


def validate_csv_content(all):
    lines = len(all.splitlines())
    # Including the header line.
    return 1 < lines < 422


def parse_csv_content(csv):
    all_students = []
    for line in csv.splitlines()[1:]:
        # logging.warning(line)
        fields = line.split(',')
        s = Student()
        s.ID = int(fields[0])
        s.Start_time = fields[1]
        s.Completion_time = fields[2]
        s.Email = fields[3]
        s.Name = fields[4]
        s.Student_ID = fields[5]
        s.Workshop = fields[6]
        s.Preferred_teammates = fields[7]
        s.Preferred_project_option = fields[8]
        s.Preferred_tech = fields[9]
        s.Timezone = fields[10]
        s.Preferred_week_days = fields[11]
        s.Preferred_day_night_times = fields[12]
        all_students.append(s)

    return all_students


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        logging.error("POST file")
        if form.is_valid():
            logging.error("POST file, valid")
            content = str()
            for binary_bytes in request.FILES['file'].chunks():
                text = binary_bytes.decode('utf-8')
                # logging.warning(text)
                content += text
            valid = validate_csv_content(content)
            if valid:
                request.session['csv_content'] = content
                return render(request, 'TeamCreator/upload.html', {'form': form, 'create_button_visibility': 'visible'})
            else:
                return render(request, 'TeamCreator/upload.html',
                              {'form': form, 'create_button_visibility': 'hidden',
                               'error': 'CVS file content is invalid.'})

    else:
        form = UploadFileForm()
    return render(request, 'TeamCreator/upload.html', {'form': form})


def teams_list(request):
    try:
        students = parse_csv_content(request.session['csv_content'])
        workshop_groups = group_students(students)
        total_groups = sum(len(g) for g in workshop_groups.values())
        logging.warning(f'Total groups: {total_groups}')
    except Exception as e:
        logging.error('Create team failed.')
        return render(request, 'TeamCreator/error.html', {'error': 'Create teams failed.' + str(e)})

    return render(request, 'TeamCreator/team_list.html', {'total_groups': total_groups})
