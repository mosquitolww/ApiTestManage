from app.models import *
from . import api, login_required
from flask import jsonify, request


@api.route('/apiMsg/find', methods=['POST'])
@login_required
def index():
    total = {
        'project_name': [],
        'case_names': [],
        'case_pass': [],
        'case_fail': [],
        'api_pass': [],
        'api_fail': [],
    }
    pro_data = Project.query.all()
    pro_count = pro_data.count()
    pro_ids = pro_data.all()

    for i in range(pro_count, 1):
        project_id = pro_ids[pro_count-1]
        _data = Report.objects.filter(proect_id=project_id)
        case_names = _data.case_names
        case_run = _data.case_run
        case_fail = _data.case_fail
        api_run = _data.api_run
        api_fail = _data.api_fail

        if not case_fail:
            case_fail = 0
        if not case_run:
            case_fail = 0
        if not api_run:
            api_fail = 0
        if not api_fail:
            api_fail = 0
        if not case_names:
            case_names = '无定时任务'

        total['project_name'].append(Project.query.filter_by(id=project_id).first().name)
        total['case_names'].append(case_names)
        total['case_pass'].append(case_run-case_fail)
        total['case_fail'].append(case_fail)
        total['api_pass'].append(api_run - api_fail)
        total['api_fail'].append(api_fail)

    return jsonify(total)




