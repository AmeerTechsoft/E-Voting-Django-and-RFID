from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
import logging
from .models import RFIDData

# Create your views here.

logger = logging.getLogger(__name__)


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voterDashboard"))

    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("adminDashboard"))
            else:
                return redirect(reverse("voterDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            user.save()
            voter.save()
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))



@csrf_exempt
def get_rfid_data(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            # Extract RFID data from the POST request body
            request_data = json.loads(request.body.decode('utf-8'))
            rfid_data = request_data.get('rfid_data', '')
            
            # Log the received RFID data
            logger.info(f"Received RFID Data: {rfid_data}")

            # Your further processing logic here...
            # For example, you can save the RFID data to a database or perform other actions
            # Save RFID data in the model

            RFIDData.objects.create(uid=rfid_data)
            # Return a JSON response (you can customize this based on your requirements)
            response_data = {'status': 'success', 'message': f'Received RFID Data: {rfid_data}'}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in the request body'})
        except Exception as e:
            logger.error(f"Error processing RFID data: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'})
    else:
        # Return a response for other HTTP methods (GET, etc.)
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method. Only POST requests are allowed.'})
@csrf_exempt
def get_latest_rfid_data(request):
    try:
        latest_rfid = RFIDData.objects.latest('uid')
        response_data = {'success': True, 'rfid_data': latest_rfid.uid}
        return JsonResponse(response_data)
    except RFIDData.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No RFID data available'})
    except Exception as e:
        logger.error(f"Error fetching RFID data: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Unknown error'})