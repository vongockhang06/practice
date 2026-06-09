from flask import Flask, render_template, request, abort
from config import get_db_session
from models import WeatherDailyForecasts
from datetime import datetime

app = Flask(__name__)

@app.template_filter('format_date')
def format_date(value):
    if isinstance(value, str):
        try:
            # Change "2026-06-04" into object datetime
            value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return value
    return value.strftime("%b %d, %Y")

@app.route('/')
def main_page():
    session = get_db_session()
    try:
        # Take parameter from filter 
        selected_city = request.args.get('city', '').strip()
        selected_date = request.args.get('date', '').strip()
        
        # City list not duplicate for search
        distinct_cities = (
            session.query(WeatherDailyForecasts.city_name)
            .distinct()
            .order_by(WeatherDailyForecasts.city_name.asc())
            .all()
        )
        city_list = [c[0] for c in distinct_cities]
        
        # Dynamic Query
        query = session.query(WeatherDailyForecasts)
        if selected_city:
            query = query.filter(WeatherDailyForecasts.city_name == selected_city)
        if selected_date:
            query = query.filter(WeatherDailyForecasts.forecast_date == selected_date)
            
        forecasts = query.order_by(WeatherDailyForecasts.forecast_date.asc()).all()

        return render_template(
            'dashboard.html', 
            forecasts=forecasts,
            city_list=city_list,
            selected_city=selected_city,
            selected_date=selected_date
        )
    except Exception as e:
        app.logger.error(f"Lỗi truy vấn giao diện: {e}")
        return "Internal Server Error", 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)