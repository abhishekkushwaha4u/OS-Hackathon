import json
import random
import uuid

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
import hashlib

from .token import token_encode, decode
from .models import Otp, UserNotification, UserCategory, BulkMessageIssuer, TokenIssuer
from .otp import otpsender, otpverify, bulk_message
from .serializers import UserSerializer, BulkMessageSerializer

trial_message = "Use {} as your one time password which will be valid for next 5 minutes."


def hash_password(password):

    hash_pass = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return hash_pass


def generate_otp():
    number = random.randint(100000, 999999)
    print(number)
    return number


class CreateUser(APIView):
    params = ['mobile', 'password']
    number = ''
    password = ''
    user = ''

    def check_user_existence(self, number):
        user = UserNotification.objects.filter(
            mobile=self.number, verified=True)
        if user:
            return True
        else:
            return False

    def check_parameters(self, request):
        errors = {}
        for i in self.params:
            if i not in request.data:
                print(i)
                errors[i] = '{} must be supplied'.format(i)
        if errors:
            Response.status_code = 400
            return Response({"status": "error", "message": "Parameters missing"})
        else:
            self.password = hash_password(request.data.get('password'))
            print(self.password)
            self.number = request.data.get('mobile')

    def check_parameters_integrity(self):

        errors = {}
        try:
            num = int(self.number)
        except ValueError:
            errors['number'] = 'Provide a proper number'
        if errors:
            Response.status_code = 400
            return Response({"status": "error", "message": "Supply a proper phone number"})

    def post(self, request):
        """Checking if all the essential parameters are supplied or not"""
        check = self.check_parameters(request)

        if check:
            return check
        print("Checked parameters for presence of required fields")
        """Checking if all the supplied value data types are valid or not"""
        integrity = self.check_parameters_integrity()
        if integrity:
            return integrity

        print("Checked integrity of the constraints")
        """Checking user existence, returning error message if user already exists and is verified"""
        user_existence = self.check_user_existence(self.number)
        if user_existence:
            Response.status_code = 403
            return Response({"status": "error", "message": "User is already verified"})
        print("Checked unique user correspondence")

        unique_id = uuid.uuid4()
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=False)
        user_serializer.save(
            id=unique_id, mobile=self.number, password=self.password)
        print("Saved a temporary unverified user")
        otp = generate_otp()
        """Main code, sending OTP to the requested user"""
        json_response = otpsender(
            otp, trial_message.format(otp), self.number, expiry=5)
        print("Sent request to msg91 api, waiting for response")
        otp_status = json.loads(json_response)
        print(otp_status)
        """Using response sent by msg91 to return appropriate message back to the app"""
        if otp_status['type'] == "success":
            # Otp.objects.filter(mobile=self.number, verified=False).delete()
            user = UserNotification.objects.get(id=unique_id)
            Otp.objects.create(otp=otp, user=user)
            Response.status_code = 200
            return Response({"status": "success", "message": "OTP sent successfully"})
        else:
            error_msg = otp_status['message']
            Response.status_code = 400
            return Response({"status": "error", "message": error_msg})


class OTPVerify(APIView):
    params = ['otp', 'phone']
    otp = ''
    phone = ''

    def check_parameters(self, request):
        errors = {}
        for i in self.params:
            if i not in request.data:
                print(i)
                errors[i] = '{} must be supplied'.format(i)
        if errors:
            Response.status_code = 400
            return Response({"status": "error", "message": "Parameters missing"})
        else:
            self.otp = request.data.get('otp')
            self.phone = request.data.get('phone')

    def post(self, request):
        """Checking if all necessary parameters are provided"""
        check = self.check_parameters(request)
        if check:
            return check
        """Verifying if the supplied OTP and phone number are correct or not"""
        otp_verify = otpverify(self.phone, self.otp)
        server_response = json.loads(otp_verify)

        """Returning appropriate response according to the type of status given by server"""
        if server_response['type'] == 'error':
            Response.status_code = 406
            return Response({"status": "error", "message": server_response['message']})
        else:
            unverified_user = Otp.objects.filter(otp=self.otp)
            print(unverified_user)
            user = unverified_user[0].user
            """Filtering , updating the user verified part to True and returning back his unique id"""
            UserNotification.objects.filter(id=user.id).update(verified=True)

            parameters = {"number": self.phone, "password": user.password}
            token = token_encode(parameters).decode('utf-8')
            login_object = TokenIssuer.objects.filter(active_user=user)

            if login_object:
                login_object.update(token=token)
            else:
                TokenIssuer.objects.create(active_user=user, token=token)
            Response.status_code = 200
            return Response({"status": "success", "message": "Successfully verified", "token": token})


class Login(APIView):
    number = ''
    password = ''

    def parameters_check(self, request):
        try:
            self.number = request.data.get('mobile')
            self.password = hash_password(request.data.get('password'))

        except Exception as e:
            print(e)
            Response.status_code = 400
            return Response({"status": "Parameters missing"})

    def post(self, request):
        check = self.parameters_check(request)
        if check:
            return check
        try:
            account = UserNotification.objects.get(
                mobile=self.number, password=self.password)
        except ObjectDoesNotExist:
            Response.status_code = 403
            return Response({"status": "error", "message": "No user found with the given set of credentials"})
        except MultipleObjectsReturned:
            Response.status_code = 500
            return Response({"status": "error", "message": "Multiple objects returned"})

        jwt_token = token_encode(
            {"number": self.number, "password": self.password}).decode('utf-8')
        login_object = TokenIssuer.objects.filter(active_user=account)

        if login_object:
            login_object.update(token=jwt_token)
        else:
            TokenIssuer.objects.create(active_user=account, token=jwt_token)
        Response.status_code = 200
        return Response({"status": "success", "message": "Verification successful", "token": jwt_token})


class UserCategoryNotification(APIView):
    params = ['choice', 'message']
    choice = ''
    message = ''
    token = ''
    permissible_choices = ['DISABLED', 'SENIOR']

    def check_parameters(self, request):
        errors = {}
        for i in self.params:
            if i not in request.data:
                print(i)
                errors[i] = '{} must be supplied'.format(i)
        if errors:
            print(errors)
            Response.status_code = 400
            return Response({"status": "error", "message": "Parameters missing"})
        else:
            self.choice = request.data.get('choice')
            self.message = request.data.get('message')

    def check_headers(self, request):
        if 'Authorization' not in request.headers:
            Response.status_code = 403
            return Response({"status": "error", "message": "Authentication credentials not provided"})
        else:
            self.token = request.headers.get('Authorization')

    def check_parameters_integrity(self, request):

        errors = {}
        if self.choice not in self.permissible_choices:
            print("Error is: ", self.choice)
            errors['choice'] = 'Choices can only be DISABLED or SENIOR'

        if errors:
            Response.status_code = 400
            return Response({"status": "error", "message": "Choices can only be DISABLED or SENIOR"})

    def post(self, request):
        """Checking if all essential headers are supplied in this format"""
        check_headers = self.check_headers(request)
        if check_headers:
            return check_headers
        print(self.token)

        token_identity = TokenIssuer.objects.filter(token=self.token)
        if not token_identity:
            Response.status_code = 403
            return Response({"status": "error", "message": "Token not valid for current user"})

        """Checking if all essential parameters are supplied in the request"""
        check = self.check_parameters(request)
        if check:
            return check
        """Checking if all the parameters have correct data type"""
        integrity = self.check_parameters_integrity(request)

        if integrity:
            return integrity
        """This part is for checking if the user whose id we are supplying is valid and verified or not"""

        payload = decode(self.token)
        if not payload:
            Response.status_code = 401
            return Response({"status": "error", "message": "Invalid token"})
        print(payload)
        mobile = payload['payload']['number']
        password = payload['payload']['password']

        issuer = UserNotification.objects.filter(
            mobile=mobile, password=password, verified=True)
        if not issuer:
            Response.status_code = 403
            return Response({"status": "error", "message": "User not verified"})
        else:
            issuer = issuer[0]

        """This part is for finding recipients to send the message according to the choice in request parameters"""
        queryset = UserCategory.objects.filter(status=self.choice)

        """If no recipients, displaying an error message"""
        if queryset:
            response = json.loads(bulk_message(queryset, self.message))
        else:
            Response.status_code = 406
            return Response({"status": "error", "message": "No recipients to send messages"})
        print(response)

        """If messages are sent and msg91 gives a success response, then storing the person who issued the messages"""
        if response['type'] == 'success':
            BulkMessageIssuer.objects.create(
                issuer=issuer, message=self.message, category=self.choice)
            Response.status_code = 200
            return Response({"status": "success", "message": "notifications sent successfully"})
        else:
            Response.status_code = 406
            print(response)
            return Response({"status": "error", "message": "error in sending notifications"})


class ClearDb(APIView):
    """Clears the DB of all other contacts and makes a new set of """

    def get(self, request):
        UserNotification.objects.all().delete()
        mobile = ['7530000626', '8789569059',
                  '9841062377', '7980674536', '9003483275']
        first_name = ['Ayush1', 'Ayush2', 'Yashwant', 'Abhishek1', 'Abhishek2']
        last_name = ['Senior1', 'Senior2', 'Android', 'Kushwaha', 'Kushwaha']
        status = ['DISABLED', 'SENIOR', 'DISABLED', 'SENIOR', 'DISABLED']
        for i in range(len(mobile)):
            UserNotification.objects.create(
                mobile=mobile[i], password=hash_password(mobile[i]), verified=True)
            user = UserNotification.objects.get(
                mobile=mobile[i], password=hash_password(mobile[i]))
            Otp.objects.create(user=user, otp='123456')
            UserCategory.objects.create(first_name=first_name[i],
                                        last_name=last_name[i],
                                        user=user,
                                        status=status[i])
        Response.status_code = 200
        return Response({"status": "success", "message": "Cleared DB successfully and retained default contacts"})


class CreateUserCategoriesMessageSender(APIView):

    def post(self, request):
        try:
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            user_id = request.data.get('id')
            status = request.data.get('status')
        except Exception as e:
            print(e)
            Response.status_code = 500
            return Response({"status": "error", "message": "Unable to process request"})

        UserCategory.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    user=UserNotification.objects.get(
                                        id=user_id),
                                    status=status)
        Response.status_code = 200
        return Response({"status": "success", "message": "Successfully added recipients"})


class MessagesUploadedByUser(APIView):
    token = ''

    def check_headers(self, request):
        if 'Authorization' not in request.headers:
            Response.status_code = 403
            return Response({"status": "error", "message": "Authentication credentials not provided"})
        else:
            self.token = request.headers.get('Authorization')

    def get(self, request):
        headers_check = self.check_headers(request)

        if headers_check:
            return headers_check

        token_identity = TokenIssuer.objects.filter(token=self.token)
        print(token_identity)
        if not token_identity:
            Response.status_code = 403
            return Response({"status": "error", "message": "Token not valid for current user"})

        payload = decode(self.token)
        if not payload:
            Response.status_code = 401
            return Response({"status": "error", "message": "Invalid token"})

        mobile = payload['payload']['number']
        password = payload['payload']['password']

        queryset = BulkMessageIssuer.objects.filter(
            issuer__mobile=mobile, issuer__password=password)

        data = BulkMessageSerializer(queryset, many=True)
        Response.status_code = 200
        return Response(data.data)
