# Calls a Python script. The output of the print statement is saved in a Variable.
# Parameters:
#   $-py - Python script file name includes location.
#   $-params - Parameters pass through into Python script.

param (
    [string]$py=$(throw "-py is required."),
    [string]$params
)

# location of the Python executable
$pythonProgramPath = "C:/Users/wei_li/AppData/Local/Programs/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe"

$pythonArray = @($py) + $params.Split(" ")
#$py_params = $($paramArray -join ",")
#$py_params
#foreach ($param in $paramArray) {
#    $param
#}

# echo $pythonProgramPath
# echo $pythonScriptPath
#$testps = 'C:\Users\wei_li\source\repos\scripts\arg_parse_test.py','-k','QQQ','-v','110'
#$testps

$pythonOutput = & $pythonProgramPath $pythonArray
$pythonOutput