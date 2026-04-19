# Script to create all remaining pages
$pages = @(
    @{path="solution/remote-trade-in/index.html"; title="CarSee Remote Trade-in - Source more Used Vehicles with remote inspection"; desc="Get comprehensive vehicle condition reports remotely. With damage detection and repair cost estimation, make accurate cash trade-in offers in minutes."},
    @{path="solution/on-site-trade-in/index.html"; title="CarSee On-site Trade-in - Simplify the recovery of used vehicles on site"; desc="Optimized customer registration integrated with your management tools, guided photo tour, damage detection and costing."},
    @{path="solution/car-fleet/index.html"; title="CarSee Fleet Management - Inspect fleets faster, improve consistency"; desc="Inspect fleets faster, improve consistency, and control costs with AI-powered vehicle inspection."},
    @{path="solution/inspection/index.html"; title="CarSee API Inspection - Accelerate and optimize inspection with our API"; desc="CarSee easily integrates into your existing apps, databases and business flows. CarSee AI helps you get instant result detecting the damage."},
    @{path="solution/remarketing/index.html"; title="CarSee Remarketing - Resell your vehicles faster and professionalize your ads"; desc="Our AI checks the conformity of your images and retouches them automatically according to your wishes."},
    @{path="clients/dealerships/index.html"; title="Dealerships - Inspecting damage for trade-in or repair"; desc="CarSee helps dealerships inspect damage for trade-in or repair with AI-powered vehicle inspection technology."},
    @{path="clients/uv-marketplaces/index.html"; title="Marketplaces - Remote inspection and image standardization"; desc="Remote inspection and image standardization for used vehicle marketplaces."},
    @{path="clients/oem/index.html"; title="OEM - Inspection and remarketing for you or your dealership network"; desc="Inspection and remarketing solutions for OEMs and their dealership networks."},
    @{path="clients/rental-cars-car-sharing/index.html"; title="Rental Cars & Carsharing - Inspection before and after each rental"; desc="Inspection before and after each rental for rental car companies and carsharing services."},
    @{path="clients/insurers-experts/index.html"; title="Insurers & Experts - Streamline your processes and guard against fraud"; desc="Streamline your processes and guard against fraud with AI-powered vehicle inspection."},
    @{path="clients/software-publishers/index.html"; title="Software Publishers - Integrate AI-powered vehicle inspection to your solutions"; desc="Integrate AI-powered vehicle inspection to your software solutions."},
    @{path="clients/leasing/index.html"; title="Leasers - Control your costs thanks to artificial intelligence"; desc="Control your costs thanks to artificial intelligence for leasing companies."},
    @{path="company/career/index.html"; title="Career - Join us! We're always looking for talented people"; desc="Join CarSee! We're always looking for talented people to join our team."},
    @{path="company/partners/index.html"; title="Become a Partner - Join Europe's leading AI vehicle inspection technology partner ecosystem"; desc="Join Europe's leading AI vehicle inspection technology partner ecosystem."},
    @{path="blog/index.html"; title="Blog - Latest news and insights from CarSee"; desc="Latest news, insights, and updates from CarSee about AI vehicle inspection technology."}
)

Write-Host "Creating $($pages.Count) pages..."

foreach ($page in $pages) {
    $dir = Split-Path $page.path -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    Write-Host "Created: $($page.path)"
}

Write-Host "`nAll page directories created. Pages will be generated individually."
