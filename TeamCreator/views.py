import json
import logging
import os
import pandas as pd
from pathlib import Path

import django.forms
from django.shortcuts import render
from TeamCreator.teams import Student, group_students

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from TeamCreator.forms import UploadFileForm


def index(request):
    return HttpResponseRedirect('upload_file')


def validate_csv_file(file_path):
    with open(file_path, 'r') as f:
        all = f.read()
        lines = len(all.splitlines())
        # Including the header line.
        return lines > 1 and lines < 422


def parse_csv_file(file_path):
    all_students = []
    with open(file_path, 'r') as f:
        for line in f.readlines()[1:]:
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
            up_file = request.FILES['file']
            fs = FileSystemStorage()
            file = fs.save(up_file.name, up_file)
            path = os.path.join(settings.MEDIA_ROOT, file)
            if up_file.name.endswith('.xls') or up_file.name.endswith('.xlsx'):
                df = pd.read_excel(path)
                csv_path = Path(path).with_suffix('.csv').as_posix()
                df.to_csv(csv_path, sep=',', index=False)
                path = csv_path
            request.session['csv_file_path'] = path
            valid = validate_csv_file(path)
            if valid:
                request.session['csv_content'] = content
                return render(request, 'TeamCreator/upload.html', {'form': form, 'create_button_visibility': 'visible'})
            else:
                return render(request, 'TeamCreator/upload.html',
                              {'form': form, 'create_button_visibility': 'hidden',
                               'error': 'The file content is invalid.'})

    else:
        form = UploadFileForm()
    return render(request, 'TeamCreator/upload.html', {'form': form})


def teams_list(request):
    try:
        students = parse_csv_file(request.session['csv_file_path'])
        workshop_groups = group_students(students)
        total_groups = sum ( len(g) for g in workshop_groups.values())
        logging.warning(f'Total groups: {total_groups}')
    except Exception as e:
        logging.error('Create team failed.')
        return render(request, 'TeamCreator/error.html', {'error': 'Create teams failed.' + str(e)})

    return render(request, 'TeamCreator/team_list.html', {'total_groups': total_groups, 'workshop_groups':workshop_groups})