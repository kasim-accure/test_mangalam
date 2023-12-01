from django.shortcuts import render
from orders.serializers import ProductListSerializer, OrderItemSerializer
from carts.models import OrderItem
from report import serializers as report_serializer
from rest_framework.response import Response
from admin_panel.permissions import IsAdminUser
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from rest_framework import generics,status
from django.db.models import Sum
from django.utils import timezone
import calendar
from rest_framework.pagination import PageNumberPagination
from datetime import timedelta,datetime
from dateutil.relativedelta import relativedelta


class DailySaleReportView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    # serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]
    def get_daily_sales(self, date):
        # Filter orders for the given date and calculate total sales price
        start_date = date - timedelta(days=6)  # Get the start date for the last 6 days
        end_date = date  # Current date
        daily_sales = OrderItem.objects.filter(
            order__order_date__date__range=[start_date, end_date]
        ).values('order__order_date__date').annotate(total_sales=Sum('price'))
        

        formatted_daily_sales = {
            (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0
            for i in range((end_date - start_date).days + 1)
        }

        # Update sales values for existing dates
        for entry in daily_sales:
            date_key = entry['order__order_date__date'].strftime('%Y-%m-%d')
            formatted_daily_sales[date_key] = entry['total_sales']

        return formatted_daily_sales

    def list(self, request, *args, **kwargs):
        current_date = timezone.now().date()
        daily_sales_report = self.get_daily_sales(current_date)
        return Response({"status": True, "daily_report": daily_sales_report})
    



class WeeklyReportView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    # serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination
    page_size = 10  # Set your desired page size

    def get_weekly_sales(self, start_date, end_date):
        # Filter orders within the given week and calculate total sales price
        weekly_sales = OrderItem.objects.filter(
            order__order_date__date__range=[start_date, end_date]
        ).aggregate(total_sales_price=Sum('price'))['total_sales_price'] or 0
        return weekly_sales

    def get_weekly_sales_summary(self):
        # Get the current date
        current_date = timezone.now()

        # Get the number of days in the current month
        _, num_days_in_month = calendar.monthrange(current_date.year, current_date.month)

        # Initialize variables to store weekly sales summary
        weekly_sales_summary = {}

        # Calculate weekly sales for each week in the month
        for day in range(1, num_days_in_month + 1):
            date = current_date.replace(day=day)
            week_number = date.isocalendar()[1]  # Get ISO week number

            # Calculate start and end dates for the week
            start_date = date - timezone.timedelta(days=date.weekday())
            end_date = start_date + timezone.timedelta(days=6)

            # Calculate the week label (e.g., 'week_1', 'week_2', etc.)
            week_label = f'week_{week_number}'

            # Calculate weekly sales and add to summary
            if week_label not in weekly_sales_summary:
                weekly_sales_summary[week_label] = self.get_weekly_sales(start_date, end_date)

        return weekly_sales_summary

    def list(self, request, *args, **kwargs):
        weekly_sales_summary = self.get_weekly_sales_summary()
        page = self.paginate_queryset([{'week': week, 'sales': sales} for week, sales in weekly_sales_summary.items()])
        if page is not None:
            return self.get_paginated_response(page)
        return Response({"status":True,"weekly_report":weekly_sales_summary})


class MonthlyReportView(generics.ListAPIView):
    # serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]

    def get_monthly_sales_summary(self):
        current_date = timezone.now()
        months_range = range(1, 13)
        monthly_sales_summary = (
            OrderItem.objects
            .filter(order__order_date__year=current_date.year)
            .annotate(month=ExtractMonth('order__order_date', 'month'))
            .values('month')
            .annotate(total_sales=Sum('price'))
            .order_by('month')
        )
        month_names = {i: calendar.month_name[i] for i in range(1, 13)}
        formatted_summary = {
            month_names[month]: 0 for month in months_range
        }

        # Update sales values for existing months
        for entry in monthly_sales_summary:
            month_number = int(entry['month'])
            formatted_summary[month_names[month_number]] = entry['total_sales']

        return formatted_summary

    def list(self, request, *args, **kwargs):
        monthly_sales_summary = self.get_monthly_sales_summary()
        return Response({"status":True,"monthly_report":monthly_sales_summary})

    
class DailyReportListView(generics.ListAPIView):
    serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        current_date = timezone.now().date()
        start_date = current_date - timedelta(days=6)  # Get the start date for the last 6 days
        end_date = current_date  # Current date
        return OrderItem.objects.filter(order__order_date__date__range=[start_date, end_date])
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"status": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)


class WeeklyReportListView(generics.ListAPIView):
    serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        current_date = timezone.now().date()
        _, num_days_in_month = calendar.monthrange(current_date.year, current_date.month)
        
        # Calculate start and end dates for the current month
        start_date = current_date.replace(day=1)
        end_date = current_date.replace(day=num_days_in_month)

        return OrderItem.objects.filter(order__order_date__date__range=[start_date, end_date])
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"status": True, "data": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


class MonthlyReportListView(generics.ListAPIView):

    serializer_class = report_serializer.OrderReportSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        current_date = timezone.now().date()
        
        # Calculate start and end dates for the current year
        start_date = current_date.replace(month=1, day=1)
        end_date = current_date.replace(month=12, day=31)

        return OrderItem.objects.filter(order__order_date__date__range=[start_date, end_date])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True, "data": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


class YearlySalelistView(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        current_datetime_utc = timezone.now()
        current_datetime_in_specific_timezone = current_datetime_utc.astimezone(timezone.get_current_timezone())
        current_date = current_datetime_in_specific_timezone.date()
        # start_of_week = current_date - timedelta(days=current_date.weekday())  # day starts from Monday as 0
        start_date = current_date - timedelta(days=365 * 5)
        queryset = OrderItem.objects.filter(order__order_date__date__range=[start_date, current_date + timedelta(days=1)])
        # Filter orders for the current week up to the current day
        # queryset = OrderItem.objects.filter(order__order_date__date__range=[start_of_week, current_date + timedelta(days=1)])
        
        return queryset

    def list(self, request, *args, **kwargs):
        current_datetime_utc = timezone.now()
        current_datetime_in_specific_timezone = current_datetime_utc.astimezone(timezone.get_current_timezone())
        current_date = current_datetime_in_specific_timezone.date()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate yearly sales for the last five years
        current_year = datetime.now().year
        yearly_sales = {}
        for year in range(current_year, current_year - 5, -1):
            start_of_year = datetime(year, 1, 1).date()
            end_of_year = datetime(year, 12, 31).date()
            total_sales = OrderItem.objects.filter(order__order_date__date__range=[start_of_year, end_of_year]).aggregate(total_sales=Sum('price'))['total_sales'] or 0
            yearly_sales[str(year)] = total_sales

        response_data = [yearly_sales]
        # response_data = [{"yearly_sales": yearly_sales}]
        return Response(response_data, status=status.HTTP_200_OK)

class YearlyReportListView(generics.ListAPIView):

    serializer_class = report_serializer.OrderReportSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        # current_date = timezone.now().date()
        # # Calculate start date for the last five years
        # start_date = current_date - relativedelta(years=5)
        # return OrderItem.objects.filter(order__order_date__date__range=[start_date, current_date])
        return OrderItem.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True, "data": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
