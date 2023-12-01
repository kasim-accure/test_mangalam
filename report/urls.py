from django.urls import path,include
from report import views
app_name = "report"

urlpatterns = [
    path("daily-report/",views.DailySaleReportView.as_view(),name="DailySaleListView"),
    # path("orderitem-search/",views.OrderItemSearchView.as_view(),name=" orderItemsListView"),

    path("weekly-report/",views.WeeklyReportView.as_view(),name="weekly-report"),
    path("monthly-report/",views.MonthlyReportView.as_view(),name="monthly-report"),
    path("yearly-report/",views.YearlySalelistView.as_view(),name="yearly-report"),
    path("daily-list-report/",views.DailyReportListView.as_view(),name="daily-list"),
    path("weekly-list-report/",views.WeeklyReportListView.as_view(),name="weekly-list"),
    path("monthly-list-report/",views.MonthlyReportListView.as_view(),name="monthly-list"),
     path("yearly-list-report/",views.YearlyReportListView.as_view(),name="yearly-list"),
    
]