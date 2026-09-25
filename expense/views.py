from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from expense.serializers import UserSerializer,ExpenseSerializer
from expense.models import Expenses
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Sum    
from django.utils import timezone
# Create your views here.

class RegisterView(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)  #performn pakaram useyynee aan
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        expense_list=Expenses.objects.filter(owner=request.user)
        ser=ExpenseSerializer(expense_list,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)
    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"deleted!!"})
    def update(self,request,pk=0):
        expense_obj=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=expense_obj)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self,request,pk=0):
        expense_obj=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=expense_obj,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseSummeryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cur_date=timezone.now()
        # print(cur_date)
        cur_month=cur_date.month
        cur_year=cur_date.year
        print(cur_month,cur_year)
        data=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        category_summery=data.values('category').annotate(Sum('amount'))
        cat_summery=[summery for summery in category_summery]
        for i in cat_summery:
            print(i)
        total_expense=data.values('amount').aggregate(total=Sum('amount'))
        print(total_expense)
        # ser=ExpenseSerializer(qs,many=True)
        context={
            "total_expense":total_expense,
            "category_summery":cat_summery
        }
        return Response(data={"msg":"context"})

