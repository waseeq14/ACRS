import sys
import os
from django.shortcuts import render
from django.http import JsonResponse
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
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Code, Vulnerability, Patch, Exploit
from django.contrib.auth.decorators import login_required
from pentest.pentest import Pentest
from pentest.exploit import PentestExploitAI


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
		folder_name = "/home/parrot/Desktop/fyp/projects/"+str(id)
		os.makedirs(folder_name, exist_ok=True)
		file_path = os.path.join(folder_name,f"code.{file_ext}")
		with open(file_path,"w") as file:
			file.write(file_contents)
		print(file_path)

		Code.objects.create(id=id, code=file_contents, language=file_ext, submittedBy=request.user)

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
			Vulnerability.objects.create(cweId="", description=result[0], code=code, analysis_type=analysis_type)
			return JsonResponse({"result": result[0], 'code': result[1]})

		if analysis_type == 'symbolic2':
			Vulnerability.objects.create(cweId="", description=result[0], code=code, analysis_type=analysis_type)
			return JsonResponse({"result": result[0], 'segments': result[1]})

		if analysis_type == 'asan':
			Vulnerability.objects.create(cweId="", description=result[0], code=code, analysis_type=analysis_type)
			return JsonResponse({"result": result[0], 'code': result[1], 'seeds': result[2]})

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

        Patch.objects.create(patchedCode=patched_code, code=code, description="")

        return JsonResponse({"result": patched_code})

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

    if not ssh_host or not ssh_user or not ssh_pass:
        return JsonResponse({'error': 'Missing SSH connection details'}, status=400)

    if not option:
        return JsonResponse({'error': 'Missing Option'}, status=400)

    pentest = Pentest(ssh_host, ssh_user, ssh_pass)

    try:
        pentest.connect()
        if pentest.ssh_client is None:
            return JsonResponse({'error': 'SSH connection failed'}, status=500)

        pentest.run_enum_scripts(option)
        pentest.download_file("/tmp/enum_results.txt", "enum_results.txt")
        pentest.setupEnv()
        result = pentest.analyze_vulns("enum_results.txt")
        return JsonResponse({'result': result})

    except Exception as e:
        pentest.disconnect()
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def pentest_scan_exploit(request):
    if request.method == 'POST':
        index = request.POST.get('index')

    if not index:
        return JsonResponse({'error': 'Index not provided'}, status=400)

    pentest = PentestExploitAI('vuln_analysis.json')
    pentest.setupEnv()

    try:
        result = pentest.run(int(index))
        return JsonResponse({'result': result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def pentest_scan_patch(request):
    if request.method == 'POST':
        index = request.POST.get('index')

    if not index:
        return JsonResponse({'error': 'Index not provided'}, status=400)

    pentest = PentestExploitAI('vuln_analysis.json')
    pentest.setupEnv()

    try:
        result = pentest.run(int(index))
        return JsonResponse({'result': result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
