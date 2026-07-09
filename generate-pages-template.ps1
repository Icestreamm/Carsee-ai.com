# Template-based page generator
$baseTemplate = @'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <meta name="description" content="{{DESCRIPTION}}">
    <link rel="stylesheet" href="{{CSS_PATH}}">
    <link rel="stylesheet" href="{{CSS_PATH_RESPONSIVE}}">
</head>
<body>
    <!-- Header and Footer will be added -->
    <script src="{{JS_PATH}}"></script>
</body>
</html>
'@

Write-Host "Template created. Use this to generate pages programmatically."
