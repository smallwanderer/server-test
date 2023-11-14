from ctransformers import AutoModelForCausalLM
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Query
from .serializers import QuerySerializer

import json

llm = AutoModelForCausalLM.from_pretrained("./", model_file="llama-2-7b-chat.Q3_K_L.gguf", model_type="llama")

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def submit_text(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')) #데이터는 json 입력 utf-8 출력입니다.
        input_text = data.get('text', '') # input_text에 입력값이 저장됩니다.
        #input_data = np.array([list(map(int, input_text.split()))])
        #prediction = loaded_model.predict(input_data)

        response_data = {
            'input_text': input_text,
            'prediction': #prediction.tolist()[0][0]
        }
        print(response_data)
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


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
    