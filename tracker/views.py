from django.shortcuts import render, redirect
from .forms import ExcelUploadForm, CivilPackForm
from .models import App, CivilPack
import pandas as pd
from datetime import datetime
import json
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from collections import Counter

# Civil Packs page
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse

def civil_packs(request):
    message = ''
    if request.method == 'POST':
        form = CivilPackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pack = CivilPack(
                ss_number=data['ss_number'],
                substation_number=data['substation_number'],
                job_code=data['job_code'],
                scheme_reference=data['scheme_reference'],
                wayleave_number=data['wayleave_number'],
                passed_date=data['passed_date'],
                road_level_number=data['road_level_number'],
                plot_number=data['plot_number'],
                substation_tx_count=data['substation_tx_count'],
                waylvb_count=data['waylvb_count'],
                tx_size=data['tx_size']
            )
            pack.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'pack': {
                        'id': str(pack.id),
                        'ss_number': pack.ss_number,
                        'substation_number': pack.substation_number,
                        'job_code': pack.job_code,
                        'scheme_reference': pack.scheme_reference,
                        'wayleave_number': pack.wayleave_number,
                        'passed_date': pack.passed_date.strftime('%Y-%m-%d') if pack.passed_date else '',
                        'road_level_number': pack.road_level_number,
                        'plot_number': pack.plot_number,
                        'substation_tx_count': pack.substation_tx_count,
                        'waylvb_count': pack.waylvb_count,
                        'tx_size': pack.tx_size,
                    }
                })
            message = 'Civil Pack added successfully!'
            form = CivilPackForm()  # reset form
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid form data.'})
            message = 'Please correct the errors below.'
    else:
        form = CivilPackForm()
    packs = CivilPack.objects.order_by('-id')
    return render(request, 'tracker/civil_packs.html', {'form': form, 'packs': packs, 'message': message})

from bson import ObjectId

def export_civil_packs(request):
    import pandas as pd
    packs = CivilPack.objects()
    data = []
    for pack in packs:
        data.append({
            'SS Number': pack.ss_number,
            'Substation Number': pack.substation_number,
            'Job Code': pack.job_code,
            'Scheme Reference': pack.scheme_reference,
            'Wayleave Number': pack.wayleave_number,
            'Passed Date': pack.passed_date.strftime('%Y-%m-%d') if pack.passed_date else '',
            'Road Level Number': pack.road_level_number,
            'Plot Number': pack.plot_number,
            'Substation TX Count': pack.substation_tx_count,
            'Way LVB Count': pack.waylvb_count,
            'TX Size': pack.tx_size,
        })
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Civil Packs')
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="civil_packs.xlsx"'
    return response

@csrf_exempt
def edit_civil_pack(request, pack_id):
    from django.http import JsonResponse, HttpResponse
    pack = CivilPack.objects(id=ObjectId(pack_id)).first()
    if not pack:
        return JsonResponse({'success': False, 'error': 'Civil Pack not found.'})
    if request.method == 'POST':
        # Update fields from POST data
        pack.ss_number = request.POST.get('ss_number', pack.ss_number)
        pack.substation_number = request.POST.get('substation_number', pack.substation_number)
        pack.job_code = request.POST.get('job_code', pack.job_code)
        pack.scheme_reference = request.POST.get('scheme_reference', pack.scheme_reference)
        pack.wayleave_number = request.POST.get('wayleave_number', pack.wayleave_number)
        passed_date = request.POST.get('passed_date')
        if passed_date:
            try:
                pack.passed_date = datetime.strptime(passed_date, '%Y-%m-%d')
            except Exception:
                pass
        pack.road_level_number = request.POST.get('road_level_number', pack.road_level_number)
        pack.plot_number = request.POST.get('plot_number', pack.plot_number)
        pack.substation_tx_count = request.POST.get('substation_tx_count', pack.substation_tx_count)
        pack.waylvb_count = request.POST.get('waylvb_count', pack.waylvb_count)
        pack.tx_size = request.POST.get('tx_size', pack.tx_size)
        pack.save()
        return JsonResponse({'success': True})
    # GET: return current values
    return JsonResponse({
        'ss_number': pack.ss_number,
        'substation_number': pack.substation_number,
        'job_code': pack.job_code,
        'scheme_reference': pack.scheme_reference,
        'wayleave_number': pack.wayleave_number,
        'passed_date': pack.passed_date.strftime('%Y-%m-%d') if pack.passed_date else '',
        'road_level_number': pack.road_level_number,
        'plot_number': pack.plot_number,
        'substation_tx_count': pack.substation_tx_count,
        'waylvb_count': pack.waylvb_count,
        'tx_size': pack.tx_size,
    })

# Main dashboard view

@csrf_exempt
def edit_app(request, app_id):
    from django.http import JsonResponse, HttpResponse
    app = App.objects(id=app_id).first()
    if not app:
        return JsonResponse({'success': False, 'error': 'App not found.'})
    if request.method == 'POST':
        # Update fields from POST data
        app.current_stage = request.POST.get('current_stage', app.current_stage)
        for field in ['wayleave_date', 'in_design_date', 'usp_date', 'passed_date']:
            val = request.POST.get(field)
            app[field] = val if val else None
        app.remarks = request.POST.get('remarks', app.remarks)
        app.save()
        return JsonResponse({'success': True})
    # GET: return current values
    return JsonResponse({
        'app_name': app.app_name,
        'customer': app.customer,
        'wayleave_date': app.wayleave_date.strftime('%Y-%m-%d') if app.wayleave_date else '',
        'in_design_date': app.in_design_date.strftime('%Y-%m-%d') if app.in_design_date else '',
        'usp_date': app.usp_date.strftime('%Y-%m-%d') if app.usp_date else '',
        'passed_date': app.passed_date.strftime('%Y-%m-%d') if app.passed_date else '',
        'current_stage': app.current_stage,
        'remarks': app.remarks,
    })

@csrf_exempt
def delete_app(request, app_id):
    from django.http import JsonResponse, HttpResponse
    app = App.objects(id=app_id).first()
    if not app:
        return JsonResponse({'success': False, 'error': 'App not found.'})
    app.delete()
    return JsonResponse({'success': True})

def admin_dashboard(request):
    apps = App.objects()
    total_apps = apps.count()
    stage_counts = Counter(app.current_stage for app in apps)
    now = datetime.now()
    delayed_in_design = 0
    delayed_gis = 0
    for app in apps:
        if app.current_stage == 'in_design' and app.in_design_date:
            delta = (now - app.in_design_date).days
            if delta > 3:
                delayed_in_design += 1
        if app.current_stage == 'gis' and hasattr(app, 'gis_date') and app.gis_date:
            delta = (now - app.gis_date).days
            if delta > 3:
                delayed_gis += 1
    stage_labels = list(stage_counts.keys())
    stage_values = list(stage_counts.values())
    stage_counts_list = list(stage_counts.items())
    return render(request, 'tracker/admin_dashboard.html', {
        'total_apps': total_apps,
        'stage_counts': stage_counts,
        'stage_counts_list': stage_counts_list,
        'stage_labels': json.dumps(stage_labels),
        'stage_values': json.dumps(stage_values),
        'delayed_in_design': delayed_in_design,
        'delayed_gis': delayed_gis,
    })

def dashboard(request):
    from django.urls import reverse
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                df = pd.read_excel(excel_file)
                # Expected columns: app_name, customer, wayleave_date, in_design_date, usp_date, passed_date, current_stage, remarks
                for _, row in df.iterrows():
                    app = App.objects(app_name=str(row['app_name'])).first()
                    if app:
                        continue  # Skip updating existing apps
                    app = App(app_name=str(row['app_name']))
                    app.customer = str(row.get('customer', '')) if pd.notnull(row.get('customer', '')) else ''
                    # Handle date fields
                    for field in ['wayleave_date', 'in_design_date', 'usp_date', 'passed_date']:
                        val = row.get(field)
                        setattr(app, field, pd.to_datetime(val) if pd.notnull(val) and val != '' else None)
                    # Validate current_stage
                    valid_stages = ['wayleave', 'in_design', 'usp', 'passed']
                    stage = str(row.get('current_stage', '')).strip().lower() if pd.notnull(row.get('current_stage', '')) else ''
                    app.current_stage = stage if stage in valid_stages else ''
                    # Remarks as string
                    app.remarks = str(row.get('remarks', '')) if pd.notnull(row.get('remarks', '')) else ''
                    app.save()
                messages.success(request, 'Excel data imported successfully.')
            except Exception as e:
                messages.error(request, f'Error importing Excel: {e}')
        return redirect(reverse('dashboard'))
    else:
        form = ExcelUploadForm()
    apps = App.objects()
    # Statistics
    total_apps = apps.count()
    from collections import Counter
    stage_counts = Counter(app.current_stage for app in apps)
    # Delayed: in_design > 3 days, gis > 3 days
    now = datetime.now()
    delayed_in_design = 0
    delayed_gis = 0
    delayed_app_ids = set()
    for app in apps:
        if app.current_stage == 'in_design' and app.in_design_date:
            delta = (now - app.in_design_date).days
            if delta > 3:
                delayed_in_design += 1
                delayed_app_ids.add(str(app.id))
        if app.current_stage == 'gis' and hasattr(app, 'gis_date') and app.gis_date:
            delta = (now - app.gis_date).days
            if delta > 3:
                delayed_gis += 1
                delayed_app_ids.add(str(app.id))
    return render(request, 'tracker/weeklyApps.html', {
        'form': form,
        'apps': apps,
        'total_apps': total_apps,
        'stage_counts': stage_counts,
        'delayed_in_design': delayed_in_design,
        'delayed_gis': delayed_gis,
        'delayed_app_ids': delayed_app_ids,
    })
