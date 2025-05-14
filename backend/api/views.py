import sys
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import importlib.util
from vulnerability_analysis.VA import VA
from vulnerability_analysis.patch import PatchGenerator
import uuid
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, PentestVulnerabilitySerializer, PentestExploitSerializer, PentestPatchSerializer
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from .models import (
    Code,
    Vulnerability,
    Patch,
    Exploit,
    Report,
    PentestProject,
    PentestVulnerability,
    PentestExploit,
    PentestPatch,
    VulnerabilityNames,
    PentestReport
)
from django.contrib.auth.decorators import login_required
from pentest.pentest import Pentest
from pentest.exploit import PentestExploitAI
from .utils import read_file_content, read_segments, read_seeds, extract_vuln_names
import re
import ast


@api_view(["POST"])
def register_user(request):
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"message": "User registered successfully"})

@api_view(["POST"])
def login_user(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return JsonResponse({"message": "Login successful", 'user': serializer.data})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)

@api_view(["GET"])
def is_authenticated(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return JsonResponse({'is_authenticated': True, 'message': 'User is authenticated', 'user': serializer.data})
        else:
            return JsonResponse({'is_authenticated': False, 'message': 'User is not authenticated', 'user': None})
    else:
        return JsonResponse({'error': 'Invalid method. GET required.'}, status=400)

@api_view(["GET"])
def logout_user(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			logout(request)
			return JsonResponse({'message': 'Successfully logged out!'}, status=200)
	else:
		return JsonResponse({'error': 'Invalid method. GET required.'}, status=400)

@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            password = data.get('password')
            new_password = data.get('new_password')

            if not password or not new_password:
                return JsonResponse({'success': False, 'message': 'Password not provided.', 'user': None})

            user = authenticate(request, username=request.user.username, password=password)

            if not user:
                return JsonResponse({'success': False, 'message': 'Old password not correct.', 'user': None})

            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)

            serializer = UserSerializer(user)

            return JsonResponse({'success': True, 'message': 'Password changed.', 'user': serializer.data})
        else:
            return JsonResponse({'success': False, 'message': 'User is not authenticated', 'user': None})
    else:
        return JsonResponse({'error': 'Invalid method. GET required.'}, status=400)


@login_required
@api_view(['POST'])
def file_save(request):
	if request.method == "POST":
		id = uuid.uuid4()

		file_ext = request.POST.get('ext')
		file_contents = request.POST.get("contents")
		name = request.POST.get('name')
		folder_name = "/home/parrot/Desktop/fyp/projects/"+str(id)
		os.makedirs(folder_name, exist_ok=True)
		file_path = os.path.join(folder_name,f"code.{file_ext}")
		with open(file_path,"w") as file:
			file.write(file_contents)
		print(file_path)

		Code.objects.create(id=id, name=name, code=file_contents, language=file_ext, submittedBy=request.user)

		return JsonResponse({"result":True, "file_path":file_path})
			

@api_view(['POST'])
def run_analysis(request):
	if request.method == "POST":
		file_path = request.POST.get("file_path") 
		analysis_type = request.POST.get("analysis_type")
		print(file_path)
		print(analysis_type)
		folder_path = os.path.dirname(file_path)
		va = VA(file_path, folder_path)
		va.setupEnv()
		result = va.startAnalysis(analysis_type)

		code_id = folder_path.split("/")[-1]
		code = Code.objects.get(id=code_id)

		if analysis_type == 'symbolic':
			Vulnerability.objects.create(cweId="", vuln_names=str(result[1]), description=result[0], code=code, analysis_type=analysis_type)
			vuln_names = result[1]
			for name in vuln_names:
				vuln = VulnerabilityNames.objects.filter(name=name).first()
				if vuln:
					vuln.count += 1
					vuln.save()
				else:
					VulnerabilityNames.objects.create(name=name)
			return JsonResponse({"result": result[0], 'code': result[2]})

		if analysis_type == 'symbolic2':
			Vulnerability.objects.create(cweId="", vuln_names=str(result[1]), description=result[0], code=code, analysis_type=analysis_type)
			vuln_names = result[1]
			for name in vuln_names:
				vuln = VulnerabilityNames.objects.filter(name__iexact=name).first()
				if vuln:
					vuln.count += 1
					vuln.save()
				else:
					VulnerabilityNames.objects.create(name=name)
			return JsonResponse({"result": result[0], 'segments': result[2]})

		if analysis_type == 'asan':
			Vulnerability.objects.create(cweId="", vuln_names=str(result[1]), description=result[0], code=code, analysis_type=analysis_type)
			vuln_names = result[1]
			for name in vuln_names:
				vuln = VulnerabilityNames.objects.filter(name__iexact=name).first()
				if vuln:
					vuln.count += 1
					vuln.save()
				else:
					VulnerabilityNames.objects.create(name=name)
			return JsonResponse({"result": result[0], 'code': result[2], 'seeds': result[3]})

		# return render(request, "run_analysis.html", {"result": result})
		Vulnerability.objects.create(cweId="", description=result, code=code, analysis_type=analysis_type)
		return JsonResponse({"result": result})

	# return render(request, "run_analysis.html")
	return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def apply_patch(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')

        folder_path = os.path.dirname(file_path)
        code_id = folder_path.split("/")[-1]
        code = Code.objects.get(id=code_id)

        vulnerabilities = Vulnerability.objects.filter(code=code)

        vulns = []
        for obj in vulnerabilities:
            vulns.append(obj.description)

        patch = PatchGenerator(code.code, str(vulns))
        patch.setupEnv()

        patched_code = patch.generate_patched_code()
        description = patch.patch_descriptor(patched_code)

        Patch.objects.create(patchedCode=patched_code, code=code, description=description)

        return JsonResponse({"result": {'code': patched_code, 'description': description}})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def generate_exploit_path(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')

        folder_path = os.path.dirname(file_path)
        code_id = folder_path.split("/")[-1]
        code = Code.objects.get(id=code_id)

        vulnerabilities = Vulnerability.objects.filter(code=code)

        vulns = []
        for obj in vulnerabilities:
            vulns.append(obj.description)

        patch = PatchGenerator(code.code, str(vulns))
        patch.setupEnv()

        exploit_path = patch.generate_exploit_path()

        Exploit.objects.create(description=exploit_path, code=code)

        return JsonResponse({"result": exploit_path})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def pentest_scan(request):
    if request.method == "POST":
        ssh_host = request.POST.get('host')
        ssh_user = request.POST.get('username')
        ssh_pass = request.POST.get('password')
        option = request.POST.get('option')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

    if not ssh_host or not ssh_user or not ssh_pass:
        return JsonResponse({'error': 'Missing SSH connection details'}, status=400)

    if not option:
        return JsonResponse({'error': 'Missing Option'}, status=400)

    pentest = Pentest(ssh_host, ssh_user, ssh_pass)

    try:
        pentest.connect()
        if pentest.ssh_client is None:
            return JsonResponse({'error': 'SSH connection failed'}, status=500)

        pentest.run_enum_scripts(option, ssh_pass)
        pentest.download_file("/tmp/enum_results.txt", "enum_results.txt")
        pentest.setupEnv()
        result = pentest.analyze_vulns("enum_results.txt")

        project = PentestProject.objects.create(
            host=ssh_host, username=ssh_user, password=ssh_pass, scan_type=option, submittedBy=request.user
        )

        vulnerabilties = [
            PentestVulnerability(
                name=vuln['vulnerability_name'], description=vuln['description'], location=vuln['location'], cve=vuln['cve'], project=project
            ) for vuln in result
        ]

        final_vulns = PentestVulnerability.objects.bulk_create(vulnerabilties)

        vuln_serializer = PentestVulnerabilitySerializer(final_vulns, many=True)

        return JsonResponse({'result': vuln_serializer.data, 'id': project.id})

    except Exception as e:
        pentest.disconnect()
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def pentest_scan_exploit(request):
    if request.method == 'POST':
        id = request.POST.get('id')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    vulnerability = PentestVulnerability.objects.filter(id=id).first()

    if not vulnerability:
        return JsonResponse({'error': 'Id not valid'}, status=400)

    pentest = PentestExploitAI('vuln_analysis.json')
    pentest.setupEnv()

    vuln_serializer = PentestVulnerabilitySerializer(vulnerability)

    try:
        result = pentest.run(vuln_serializer.data)

        exploit = PentestExploit.objects.create(description=result, vulnerability=vulnerability)
        serializer = PentestExploitSerializer(exploit)

        return JsonResponse({'result': serializer.data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def pentest_scan_patch(request):
    if request.method == 'POST':
        id = request.POST.get('id')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    vulnerability = PentestVulnerability.objects.filter(id=id).first()

    if not vulnerability:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    exploit = vulnerability.exploits.filter().first()

    if not exploit:
        return JsonResponse({'error': 'Run the exploit first'}, status=400)

    pentest = PentestExploitAI('vuln_analysis.json')
    pentest.setupEnv()

    try:
        result = pentest.generate_patch(exploit.description, vulnerability)

        patch = PentestPatch.objects.create(description=result, vulnerability=vulnerability)
        serializer = PentestPatchSerializer(patch)

        return JsonResponse({'result': serializer.data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
def fetch_projects(request):
    pentest_projects = PentestProject.objects.filter(submittedBy=request.user)
    projects = Code.objects.filter(submittedBy=request.user)

    pentest_projects_data = [{
        'id': project.id,
        'title': str(project),
        'time': project.createdAt.strftime("%b %d, %Y @ %H:%M:%S")
    } for project in pentest_projects]

    projects_data = [{
        'id': project.id,
        'title': str(project),
        'time': project.createdAt.strftime("%b %d, %Y @ %H:%M:%S"),
        'language': {'c': 'C', 'cpp': 'C++'}[project.language]
    } for project in projects]

    return JsonResponse({
        'result': {
            'pentestProjects': pentest_projects_data,
            'projects': projects_data
        }
    })

@api_view(['GET'])
def load_pentest_project(request):
    id = request.query_params.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = PentestProject.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    vulnerabilities = PentestVulnerability.objects.filter(project=project)

    exploits = {}
    patches = {}

    for index in range(len(vulnerabilities)):
        vulnerability = vulnerabilities[index]

        exploit = PentestExploit.objects.filter(vulnerability=vulnerability).first()
        if exploit:
            exploit_serializer = PentestExploitSerializer(exploit)
            exploits[str(index)] = exploit_serializer.data

        patch = PentestPatch.objects.filter(vulnerability=vulnerability).first()
        if patch:
            patch_serializer = PentestPatchSerializer(patch)
            patches[str(index)] = patch_serializer.data

    vulnerabilities_serializer = PentestVulnerabilitySerializer(vulnerabilities, many=True)

    return JsonResponse({
        'result': {
            'pentest': {
                'host': project.host,
                'username': project.username,
                'option': project.scan_type,
                'id': project.id,
                'result': vulnerabilities_serializer.data
            },
            'pentestExploit': exploits,
            'pentestPatch': patches
        }
    })

@api_view(['GET'])
def load_project(request):
    id = request.query_params.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = Code.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)

    project_folder = f'{os.path.dirname(os.getcwd())}/projects/{project.id}'

    file_path = f'{project_folder}/code.{project.language}'
    file_content = project.code

    klee_result = Vulnerability.objects.filter(code=project, analysis_type='symbolic').first()
    klee_result_obj = None
    if klee_result:
        klee_result_obj = { 'analysis': klee_result.description, 'code': read_file_content(f'{project_folder}/code_klee.{project.language}') }
    
    advanced_klee_result = Vulnerability.objects.filter(code=project, analysis_type='symbolic2').first()
    advanced_klee_result_obj = None
    if advanced_klee_result:
        advanced_klee_result_obj = { 'analysis': advanced_klee_result.description, 'segments': read_segments(project_folder, project.language) }

    fuzzer_result = Vulnerability.objects.filter(code=project, analysis_type='asan').first()
    fuzzer_result_obj = None
    if fuzzer_result:
        fuzzer_result_obj = { 
            'analysis': eval(fuzzer_result.description),
            'code': read_file_content(f'{project_folder}/code_fuzz.{project.language}'),
            'seeds': read_seeds(project_folder)
        }

    rules_result = Vulnerability.objects.filter(code=project, analysis_type='rules').first()
    rules_result_obj = None
    if rules_result:
        try:
            rules_result_obj = eval(rules_result.description)
        except Exception:
            rules_result_obj = rules_result.description

    exploit_result = Exploit.objects.filter(code=project).first()
    exploit_result_obj = None
    if exploit_result:
        exploit_result_obj = { 'result': exploit_result.description }

    patch_result = Patch.objects.filter(code=project).first()
    patch_result_obj = None
    if patch_result:
        patch_result_obj = { 'code': patch_result.patchedCode }

    result_obj = {
        'filePath': file_path,
        'fileContent': file_content
    }

    if klee_result_obj is not None:
        result_obj['kleeResult'] = klee_result_obj
    if advanced_klee_result_obj is not None:
        result_obj['advancedKleeResult'] = advanced_klee_result_obj
    if fuzzer_result_obj is not None:
        result_obj['fuzzerResult'] = fuzzer_result_obj
    if rules_result_obj is not None:
        result_obj['rulesResult'] = rules_result_obj
    if exploit_result_obj is not None:
        result_obj['exploitResult'] = exploit_result_obj
    if patch_result_obj is not None:
        result_obj['patchResult'] = patch_result_obj

    return JsonResponse({'result': result_obj})

@api_view(['GET'])
def get_pentest_report(request):
    id = request.query_params.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = PentestProject.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    # Load existing report
    
    report = PentestReport.objects.filter(project=project).first()
    if report:
        return HttpResponse(report.content, content_type='text/html')
    
    # Or else
    
    vulnerabilities = PentestVulnerability.objects.filter(project=project)

    # Data Loaded, now to build the template.

    scan_types = {
        'system_information': 'System Information',
        'container': 'Container',
        'cloud': 'Cloud',
        'procs_crons_timers_srvcs_sockets': 'Procs Crons Timers and Sockets',
        'network_information': 'Network Information',
        'users_information': 'Users Information',
        'software_information': 'Software Information',
        'interesting_perms_files': 'File Permissions',
        'interesting_files': 'Interesting Files',
        'api_keys_regex': 'API Keys'
    }

    try:
        with open('api/reports/pentest-report-template.html', 'r') as template_file:
            with open('api/reports/pentest-report-vuln-template.html', 'r') as vuln_template_file:
                vuln_template = vuln_template_file.read()

            vuln_templates = []
            for vulnerability in vulnerabilities:
                exploit = PentestExploit.objects.filter(vulnerability=vulnerability).first()
                patch = PentestPatch.objects.filter(vulnerability=vulnerability).first()

                exploit_exists = exploit is not None
                patch_exists = patch is not None

                new_vuln_template = vuln_template.replace('###NAME###', vulnerability.name)\
                                                 .replace('###DESCRIPTION###', vulnerability.description)\
                                                 .replace('###EXPLOIT###', exploit.description.replace('`', '\`') if exploit_exists else '')\
                                                 .replace('###PATCH###', patch.description.replace('`', '\`') if patch_exists else '')
                
                vuln_templates.append(new_vuln_template)

            template = template_file.read()

            template = template.replace('###TITLE###', f'ACRS - Pentest Report - {project.host} ({scan_types[project.scan_type]})')\
                    .replace('###DATE###', project.createdAt.strftime('%d/%m/%Y'))\
                    .replace('###HOST###', project.host)\
                    .replace('###USERNAME###', project.username)\
                    .replace('###SCAN_TYPE###', scan_types[project.scan_type])\
                    .replace('###VULNERABILITIES###', ''.join(vuln_templates))
            
            PentestReport.objects.create(content=template, project=project)
            
            return HttpResponse(template, content_type='text/html')
    except Exception:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
@api_view(['GET'])
def get_report(request):
    id = request.query_params.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = Code.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    # Load existing report
    
    report = Report.objects.filter(code=project).first()
    if report:
        return HttpResponse(report.content, content_type='text/html')
    
    # Or else

    project_folder = f'{os.path.dirname(os.getcwd())}/projects/{project.id}'
    
    vulnerabilities = Vulnerability.objects.filter(code=project)
    
    exploit = Exploit.objects.filter(code=project).first()
    patch = Patch.objects.filter(code=project).first()

    # Data Loaded, now to build the template.
    
    analysis_types_options = {
        'rules': 'Static Rules',
        'symbolic': 'Symbolic Execution',
        'symbolic2': 'Prioritize code paths',
        'asan': 'Fuzz'
    }
    
    vuln_names = []
    analysis_types = []
    
    for vuln in vulnerabilities:
        if vuln.analysis_type != 'rules':
            vuln_names.extend(extract_vuln_names(vuln.description))
        if vuln.analysis_type not in analysis_types:
            analysis_types.append(analysis_types_options[vuln.analysis_type])

    try:
        with open('api/reports/report-template.html', 'r') as template_file:
            # All Vulnerabilties
            with open('api/reports/report-vuln-template.html', 'r') as vuln_template_file:
                vuln_template = vuln_template_file.read()
                
            vuln_templates = []
            for vuln in vuln_names:
                new_vuln_template = vuln_template.replace('###NAME###', vuln)
                vuln_templates.append(new_vuln_template)
                
            analysis_type_templates = []
            for analysis_type in analysis_types:
                analysis_type_templates.append(f'"{analysis_type}", ')
            
            rules = []
            klee_friendly_code = ''
            klee_analysis = ''
            advanced_klee_segments = []
            advanced_klee_analysis = ''
            fuzzer_code = ''
            fuzzer_seeds = ''
            fuzzer_analysis = []
            for vuln in vulnerabilities:
                # Rules
                if vuln.analysis_type == 'rules':
                    with open('api/reports/report-semgrep-template.html', 'r') as rules_template_file:
                        rules_template = rules_template_file.read()
                        
                        try:
                            rules_result = ast.literal_eval(vuln.description)
                            
                            for result in rules_result:
                                new_template = rules_template.replace('###CODE_SNIPPET###', result['snippet'])
                                new_template = new_template.replace('###ANALYSIS###', result['ai_analysis'].replace('`', '\`'))
                                rules.append(new_template)
                                
                        except Exception:
                            pass
                        
                # Klee
                if vuln.analysis_type == 'symbolic':
                    klee_friendly_code = read_file_content(f'{project_folder}/code_klee.{project.language}').replace('\\', '\\\\')
                    klee_analysis = vuln.description.replace('`', '\`')
                    
                # Advanced Klee
                if vuln.analysis_type == 'symbolic2':
                    segments = read_segments(project_folder, project.language)
                    for segment in segments:
                        segment = segment.replace('\\', '\\\\')
                        advanced_klee_segments.append(f'`{segment}`, ')
                    advanced_klee_analysis = vuln.description.replace('`', '\`')
                    
                # Fuzzer
                if vuln.analysis_type == 'asan':
                    fuzzer_code = read_file_content(f'{project_folder}/code_fuzz.{project.language}').replace('\\', '\\\\')
                    seeds = read_seeds(project_folder).splitlines()
                    for index in range(len(seeds)):
                        seed = seeds[index]
                        if seed.strip() != '':
                            fuzzer_seeds += f'{{ name: "Seed {index + 1}", content: "{seed}" }}, '
                    analysis = eval(vuln.description)
                    for each_analysis in analysis:
                        each_analysis = each_analysis.replace('`', '\`')
                        pattern = r'\[\*\] ((?:LLM )?Analysis for id:[^:]+:.*?)\s*\**Explanation:\**\s*(.*)'
                        match = re.search(pattern, each_analysis, re.DOTALL)
                        if match:
                            heading = match.group(1).strip()
                            explanation = match.group(2).strip()
                        else:
                            heading = ''
                            explanation = each_analysis
                        fuzzer_analysis.append(f'{{ title: `{heading}`, content: `{explanation}` }}, ')
                        
            template = template_file.read()

            template = template.replace('###TITLE###', f'ACRS - Code Analysis Report')\
                    .replace('###DATE###', project.createdAt.strftime('%d/%m/%Y'))\
                    .replace('###ORIGINAL_CODE###', project.code.replace('\\', '\\\\'))\
                    .replace('###EXPLOIT_PATH###', exploit.description.replace('`', '\`') if exploit else '')\
                    .replace('###PATCH_SUGGESTION###', patch.description.replace('`', '\`') if patch else '')\
                    .replace('###PATCH_CODE###', patch.patchedCode.replace('\\', '\\\\'))\
                    .replace('###VULNERABILITIES###', ''.join(vuln_templates))\
                    .replace('###ANALYSIS_TYPES###', ''.join(analysis_type_templates))\
                    .replace('###RULES###', ''.join(rules))\
                    .replace('###KLEE_FRIENDLY_CODE###', klee_friendly_code)\
                    .replace('###KLEE_ANALYSIS###', klee_analysis)\
                    .replace('###ADVANCED_KLEE_SEGMENTS###', ''.join(advanced_klee_segments))\
                    .replace('###ADVANCED_KLEE_ANALYSIS###', advanced_klee_analysis)\
                    .replace('###FUZZER_CODE###', fuzzer_code)\
                    .replace('###FUZZER_SEEDS###', fuzzer_seeds)\
                    .replace('###FUZZER_ANALYSIS###', ''.join(fuzzer_analysis))
                    
            print(project.id)
                    
            Report.objects.create(content=template, code=project)
            
            return HttpResponse(template, content_type='text/html')
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

@api_view(['GET'])
def load_dashboard_stats(request):
	vuln_names = VulnerabilityNames.objects.order_by('-count')[:5]

	vuln_names_obj = None

	if len(vuln_names) != 0:
		vuln_names_obj = []
		for vuln in vuln_names:
			vuln_names_obj.append([vuln.name, vuln.count])

	pentest_projects = PentestProject.objects.count()
	pentest_vulns = PentestVulnerability.objects.count()
	pentest_exploits = PentestExploit.objects.count()
	pentest_patches = PentestPatch.objects.count()

	result_obj = {
		'pentestProjects': pentest_projects,
		'pentestVulns': pentest_vulns,
		'pentestExploits': pentest_exploits,
		'pentestPatches': pentest_patches,
	}

	if vuln_names_obj:
		result_obj['vulnerabilities'] = vuln_names_obj

	return JsonResponse({'result': result_obj})

@api_view(['GET'])
def fetch_reports(request):
    pentest_reports = PentestReport.objects.filter(project__submittedBy=request.user)
    reports = Report.objects.filter(code__submittedBy=request.user)

    pentest_reports_data = [{
        'id': report.project.id,
        'title': str(report.project),
        'time': report.createdAt.strftime("%b %d, %Y @ %H:%M:%S")
    } for report in pentest_reports]

    reports_data = [{
        'id': report.code.id,
        'title': str(report.code),
        'time': report.createdAt.strftime("%b %d, %Y @ %H:%M:%S")
    } for report in reports]

    return JsonResponse({
        'result': {
            'pentestReports': pentest_reports_data,
            'reports': reports_data
        }
    })
    
@api_view(['DELETE'])
def delete_report(request):
    id = request.data.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = Code.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    Report.objects.filter(code__id=id).delete()
    
    return JsonResponse({'result': 'Report Deleted!'})

@api_view(['DELETE'])
def delete_pentest_report(request):
    id = request.data.get('id')

    if not id:
        return JsonResponse({'error': 'Id not provided'}, status=400)
    
    project = PentestProject.objects.filter(id=id).first()

    if not project:
        return JsonResponse({'error': 'Id not valid'}, status=400)
    
    PentestReport.objects.filter(project__id=id).delete()
    
    return JsonResponse({'result': 'Report Deleted!'})