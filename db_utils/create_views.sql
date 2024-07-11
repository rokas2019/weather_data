CREATE OR REPLACE VIEW daily_temp_stats_today AS
SELECT
    city,
    MAX(temp_celsius) AS max_temp,
    MIN(temp_celsius) AS min_temp,
    STDDEV_SAMP(temp_celsius) AS stddev_temp
FROM city_hourly_weather
WHERE date = CURRENT_DATE
GROUP BY city;


CREATE OR REPLACE VIEW daily_temp_stats_yesterday AS
SELECT
    city,
    MAX(temp_celsius) AS max_temp,
    MIN(temp_celsius) AS min_temp,
    STDDEV_SAMP(temp_celsius) AS stddev_temp
FROM city_hourly_weather
WHERE date = CURRENT_DATE - INTERVAL '1 day'
GROUP BY city;


CREATE OR REPLACE VIEW weekly_temp_stats AS
SELECT
    city,
    MAX(temp_celsius) AS max_temp,
    MIN(temp_celsius) AS min_temp,
    STDDEV_SAMP(temp_celsius) AS stddev_temp
FROM city_hourly_weather
WHERE date >= DATE_TRUNC('week', CURRENT_DATE)
GROUP BY city;


CREATE OR REPLACE VIEW last_seven_days_temp_stats AS
SELECT
    city,
    MAX(temp_celsius) AS max_temp,
    MIN(temp_celsius) AS min_temp,
    STDDEV_SAMP(temp_celsius) AS stddev_temp
FROM city_hourly_weather
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY city;


CREATE OR REPLACE VIEW hourly_temp_status_today AS
WITH HourlyMax AS (
    SELECT
        date, hour, city, MAX(temp_celsius) AS max_temp
    FROM city_hourly_weather
    WHERE date = CURRENT_DATE
    GROUP BY date, hour, city
),
HourlyMin AS (
    SELECT
        date, hour, city, MIN(temp_celsius) AS min_temp
    FROM city_hourly_weather
    WHERE date = CURRENT_DATE
    GROUP BY date, hour, city
)
SELECT
    hw.city,
    hw.date,
    hw.hour,
    hw.temp_celsius,
    CASE
        WHEN hw.temp_celsius = hm.max_temp THEN 'Highest'
        WHEN hw.temp_celsius = hl.min_temp THEN 'Lowest'
    END AS temp_status
FROM city_hourly_weather hw
LEFT JOIN HourlyMax hm ON hw.date = hm.date AND hw.hour = hm.hour AND hw.city = hm.city AND hw.temp_celsius = hm.max_temp
LEFT JOIN HourlyMin hl ON hw.date = hl.date AND hw.hour = hl.hour AND hw.city = hl.city AND hw.temp_celsius = hl.min_temp
WHERE hw.date = CURRENT_DATE;


CREATE OR REPLACE VIEW daily_temp_status_last_seven_days AS
WITH DailyMax AS (
    SELECT
        date, MAX(avgtemp_c) AS max_temp
    FROM city_daily_weather
    WHERE date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY date
),
DailyMin AS (
    SELECT
        date, MIN(avgtemp_c) AS min_temp
    FROM city_daily_weather
    WHERE date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY date
)
SELECT
    dw.city,
    dw.date,
    dw.avgtemp_c,
    CASE
        WHEN dw.avgtemp_c = dm.max_temp THEN 'Highest'
        WHEN dw.avgtemp_c = dl.min_temp THEN 'Lowest'
    END AS temp_status
FROM city_daily_weather dw
LEFT JOIN DailyMax dm ON dw.date = dm.date AND dw.avgtemp_c = dm.max_temp
LEFT JOIN DailyMin dl ON dw.date = dl.date AND dw.avgtemp_c = dl.min_temp
WHERE dw.date >= CURRENT_DATE - INTERVAL '7 days';


CREATE OR REPLACE VIEW weekly_temp_status AS
WITH WeeklyMax AS (
    SELECT
        city, MAX(avgtemp_c) AS max_temp
    FROM city_daily_weather
    WHERE date >= DATE_TRUNC('week', CURRENT_DATE)
    GROUP BY city
),
WeeklyMin AS (
    SELECT
        city, MIN(avgtemp_c) AS min_temp
    FROM city_daily_weather
    WHERE date >= DATE_TRUNC('week', CURRENT_DATE)
    GROUP BY city
)
SELECT
    city,
    max_temp,
    min_temp
FROM (
    SELECT
        wm.city,
        wm.max_temp,
        wmin.min_temp,
        ROW_NUMBER() OVER (ORDER BY wm.max_temp DESC) AS rank_max,
        ROW_NUMBER() OVER (ORDER BY wmin.min_temp) AS rank_min
    FROM WeeklyMax wm
    JOIN WeeklyMin wmin ON wm.city = wmin.city
) ranked
WHERE rank_max = 1 OR rank_min = 1;


CREATE OR REPLACE VIEW hours_rained_last_day AS
SELECT
    city,
    COUNT(*) AS hours_rained
FROM city_hourly_weather
WHERE date = CURRENT_DATE - INTERVAL '1 day' AND will_it_rain = TRUE
GROUP BY city;


CREATE OR REPLACE VIEW hours_rained_last_week AS
SELECT
    city,
    COUNT(*) AS hours_rained
FROM city_hourly_weather
WHERE date >= CURRENT_DATE - INTERVAL '7 days' AND will_it_rain = TRUE
GROUP BY city;
