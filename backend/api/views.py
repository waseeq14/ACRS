import sys
import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import importlib.util
import os
from vulnerability_analysis.VA import VA


#api_view(['POST'])
def run_analysis(request):
	if request.method == "POST":
		file_path = request.POST.get("file_path")
		analysis_type = request.POST.get("analysis_type")

		va = VA(file_path)
		va.setupEnv()
		result = va.startAnalysis(analysis_type)
		return render(request, "run_analysis.html", {"result": result})
	return render(request, "run_analysis.html")

