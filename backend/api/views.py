import sys
import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import importlib.util
import os
from vulnerability_analysis.VA import VA


@api_view(['POST'])
def run_analysis(request):
	if request.method == "POST":
		# file_path = request.POST.get("file_path")
		file_path = '/home/parrot/Desktop/fyp/backend/vulnerability_analysis/aflSetup/bank_management/bms.cpp'
		analysis_type = request.POST.get("analysis_type")

		print(analysis_type)

		va = VA(file_path)
		va.setupEnv()
		result = va.startAnalysis(analysis_type)

		if analysis_type in ['symbolic']:
			return JsonResponse({"result": result[0], 'code': result[1]})

		if analysis_type in ['asan']:
			return JsonResponse({"result": result[0], 'code': result[1], 'seeds': result[2]})

		# return render(request, "run_analysis.html", {"result": result})
		return JsonResponse({"result": result})

	# return render(request, "run_analysis.html")
	return JsonResponse({"error": "Invalid request method"}, status=400)

