import sys
import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import importlib.util
import os
from vulnerability_analysis.VA import VA
import uuid



@api_view(['POST'])
def file_save(request):
	if request.method == "POST":
		file_ext = request.POST.get('ext')
		file_contents = request.POST.get("contents")
		folder_name = "/home/parrot/Desktop/fyp/projects/"+str(uuid.uuid4())
		os.makedirs(folder_name, exist_ok=True)
		file_path = os.path.join(folder_name,f"code.{file_ext}")
		with open(file_path,"w") as file:
			file.write(file_contents)
		print(file_path)
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

		if analysis_type == 'symbolic':
			return JsonResponse({"result": result[0], 'code': result[1]})

		if analysis_type == 'symbolic2':
			return JsonResponse({"result": result[0], 'segments': result[1]})

		if analysis_type == 'asan':
			return JsonResponse({"result": result[0], 'code': result[1], 'seeds': result[2]})

		# return render(request, "run_analysis.html", {"result": result})
		return JsonResponse({"result": result})

	# return render(request, "run_analysis.html")
	return JsonResponse({"error": "Invalid request method"}, status=400)

