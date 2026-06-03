CREATE DATABASE tw_weather_db;
\c tw_weather_db;
CREATE TABLE IF NOT EXISTS tw_cities (
    city_name VARCHAR(20) PRIMARY KEY,
    latitude NUMERIC(8, 4) NOT NULL,
    longitude NUMERIC(7, 4) NOT NULL,
    timezone_offset INT NOT NULL DEFAULT (28800)
);

CREATE TABLE IF NOT EXISTS weather_daily_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    city_name VARCHAR(20) REFERENCES tw_cities(city_name) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    temp_day NUMERIC(5, 2),
    temp_min NUMERIC(5, 2),
    temp_max NUMERIC(5, 2),
    pressure INT,
    humidity INT,
    rain_volume NUMERIC(6, 2) DEFAULT 0.0,
    CONSTRAINT unique_location_date UNIQUE (city_name, forecast_date)
);
CREATE INDEX IF NOT EXISTS idx_forecast_date ON weather_daily_forecasts(forecast_date);
INSERT INTO tw_cities (city_name, latitude, longitude, timezone_offset) VALUES
('Taichung', 24.1477, 120.7360, 28800),
('Taipei', 25.0330, 121.5654, 28800),
('New Taipei', 25.0170, 121.4626, 28800),
('Kaohsiung', 22.6273, 120.3014, 28800),
('Taoyuan', 24.9937, 121.3010, 28800),
('Tainan', 22.9997, 120.2270, 28800),
('Hsinchu City', 24.8138, 120.9675, 28800),
('Hsinchu County', 24.8267, 121.0117, 28800),
('Keelung', 25.1283, 121.7419, 28800),
('Chiayi City', 23.4801, 120.4491, 28800),
('Chiayi County', 23.4518, 120.2554, 28800),
('Changhua', 24.0517, 120.5161, 28800),
('Nantou', 23.9155, 120.6865, 28800),
('Yunlin', 23.7092, 120.4313, 28800),
('Miaoli', 24.5601, 120.8214, 28800),
('Pingtung', 22.5516, 120.5488, 28800),
('Yilan', 24.7021, 121.7377, 28800),
('Hualien', 23.9872, 121.6016, 28800),
('Taitung', 22.7972, 121.1244, 28800),
('Penghu', 23.5711, 119.5793, 28800),
('Kinmen', 24.4489, 118.3731, 28800),
('Lienchiang', 26.1519, 119.9311, 28800)
ON CONFLICT (city_name) DO NOTHING;