# from ctransformers import AutoModelForCausalLM
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Query, InputSentence
from .serializers import QuerySerializer, InputSentenceSerializer

import json
from tensorflow.keras.models import load_model
import numpy as np
import os

# Llama Model
# llm = AutoModelForCausalLM.from_pretrained("./", model_file="llama-2-7b-chat.Q3_K_L.gguf", model_type="llama")

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

# From this line, for server testing.
# Linear Regression Model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'my_model.h5')
loaded_model = load_model(model_path)

def index_basic(request):
    return render(request, 'index_basic.html')

def index_rest(request):
    return render(request, 'index_rest.html')

@csrf_exempt
def submit_text(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        input_text = data.get('text', '')
        input_data = np.array([list(map(int, input_text.split()))])
        prediction = loaded_model.predict(input_data)

        response_data = {
            'input_text': input_text,
            'prediction': prediction.tolist()[0][0]
        }
        print(response_data)
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def submit_text(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        input_text = data.get('text', '')
        input_data = np.array([list(map(int, input_text.split()))])
        prediction = loaded_model.predict(input_data)

        response_data = {
            'input_text': input_text,
            'prediction': prediction.tolist()[0][0]
        }
        print(response_data)
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

class PredictSentence(APIView):
    @csrf_exempt
    def get(self, request):
        query = InputSentence.ojects.all()
        print(query)
        serializer = InputSentenceSerializer(query, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            input_text = request.data.get('text', '')
            print(input_text)

            # Save input text to the database
            input_sentence = InputSentence(sentence=input_text)
            input_sentence.save()

            # Load the model
            loaded_model = load_model(model_path)

            input_data = np.array([list(map(int, input_text.split()))])

            # Make a prediction using the loaded model
            prediction = loaded_model.predict(input_data)

            # Format the response (adjust as needed)
            response_data = {
                'input_text': input_text,
                'prediction': prediction.tolist()[0],  # Convert to list for JSON serialization
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception for debugging
            print(f"Exception: {e}")

            # Return a generic error response
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)