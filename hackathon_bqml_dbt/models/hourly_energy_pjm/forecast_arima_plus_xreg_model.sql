{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}


SELECT 'AEP' as utility, * FROM ({{ forecast_arima_plus_xreg_model('AEP') }})
UNION ALL
SELECT 'COMED' as utility, * FROM ({{ forecast_arima_plus_xreg_model('COMED') }})
UNION ALL
SELECT 'DAYTON' as utility, * FROM ({{ forecast_arima_plus_xreg_model('DAYTON') }})
