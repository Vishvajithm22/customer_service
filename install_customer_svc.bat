@echo off

echo Installing Customer Service...

helm install customer-service customer-service-0.1.0.tgz -f customer-service\values-local.yaml

echo.
echo Installation completed.
pause