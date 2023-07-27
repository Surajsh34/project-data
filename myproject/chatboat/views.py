from django.shortcuts import render
import openai
from .utill.gsheets import  read_a_spreadsheet




# Create your views here.
openai.api_key = "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"


def question_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        prompt = request.POST.get('question')
        response = openai.Completion.create(
        model="text-davinci-002", prompt=prompt, temperature=0.6, max_tokens=500, n=1, stop=None
          )
        ans = response.choices[0].text.strip()
        return render(request, 'response.html', {'name': name, 'question': prompt, 'ans': ans})
    
    return render(request, 'index.html')







# def text_input_view(request):
#     spreadsheet_id = "1cirjGAr7Iz4tMwaJfwI7XMZ1bdO9PCcuX5PR-pspNLk"
#     sheet_name = "Call Transcripts"
#     if request.method == 'POST':

#         data=read_a_spreadsheet(spreadsheet_id, sheet_name)

#         return render(request, 'response.html', {'response_text': data})

#     return render(request, 'index.html')

