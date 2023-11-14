from ctransformers import AutoModelForCausalLM
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Query
from .serializers import QuerySerializer

llm = AutoModelForCausalLM.from_pretrained("./", model_file="llama-2-7b-chat.Q3_K_L.gguf", model_type="llama")

class ChatView(APIView):
    def get(self, request):
        all_query = Query.objects.all()
        serilizer = QuerySerializer(all_query, many=True)
        return Response({
            "Query" : serilizer.data
        })
      
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            query_text = serializer.validated_data['question']
            return Response(self.fetchResponseFromModel(request, query_text),)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def fetchResponseFromModel(self, request, query_text):
        prompt = "Q: " + query_text + "? A:"
        response = llm(prompt)
        query = Query(question=query_text, response=response)
        query.save()
        return {
            'question': query.question,
            'response': response
        }
    