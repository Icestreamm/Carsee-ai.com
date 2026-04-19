# PowerShell script to download assets from CarSee website
$baseUrl = "https://cdn.prod.website-files.com/6055bfb0e78764e755d62b69"
$assetsUrl = "https://assets.website-files.com/6055bfb0e78764e755d62b69"

# Create directories
New-Item -ItemType Directory -Force -Path "assets/images", "assets/icons", "assets/logos" | Out-Null

# Logo
$logoUrl = "$assetsUrl/6055d1824dfc7f7a3f7d6d93_Group%2017.svg"
Invoke-WebRequest -Uri $logoUrl -OutFile "assets/logos/carsee-logo.svg" -UseBasicParsing

# Icons
$icons = @(
    @{url="$baseUrl/633edb1509924978d844133b_icon-check.svg"; file="assets/icons/icon-check.svg"},
    @{url="$baseUrl/639338f1bf66968301b429ea_iconmonstr-marketing-20-240.webp"; file="assets/icons/marketing-icon.webp"},
    @{url="$baseUrl/6345807ee6dcae5dcda515a0_close-icon-white.svg"; file="assets/icons/close-icon-white.svg"},
    @{url="$baseUrl/623b327581f77708d7630631_iconmonstr-x-mark-1-240.webp"; file="assets/icons/x-mark.webp"},
    @{url="$baseUrl/63b55e02dd4f8877a9dc3b22_noun-data-1703027-1ADF6D%20(1).webp"; file="assets/icons/data-acquisition.webp"},
    @{url="$baseUrl/63b55edef6d39008d832697b_noun-technology-4039991-1ADF6D%20(1).webp"; file="assets/icons/data-treatment.webp"},
    @{url="$baseUrl/63b55f6e41b3ad0b7a2fbcf7_noun-cloud-data-4366760-1ADF6D.webp"; file="assets/icons/data-delivery.webp"}
)

foreach ($icon in $icons) {
    try {
        Invoke-WebRequest -Uri $icon.url -OutFile $icon.file -UseBasicParsing
        Write-Host "Downloaded: $($icon.file)"
    } catch {
        Write-Host "Failed to download: $($icon.url)"
    }
}

# Partner logos
$partnerLogos = @(
    @{url="$baseUrl/633ed340127a728b10036a5f_meilleure-reprise-logo%205.svg"; file="assets/logos/meilleure-reprise.svg"},
    @{url="$baseUrl/62387bc4497aeb92fb370089_Aramis.webp"; file="assets/logos/aramis-auto.webp"},
    @{url="$baseUrl/64be3ae5a7cb1c7fd483fa60_Logo%20de%20Toyota%20France.webp"; file="assets/logos/toyota.webp"},
    @{url="$baseUrl/62b1d5cae71c989e698fbf69_logo-groupe-mary.svg"; file="assets/logos/groupe-mary.svg"},
    @{url="$baseUrl/62387bc4497aeb22dd37008d_Avis.webp"; file="assets/logos/avis-budget.webp"},
    @{url="$baseUrl/62387bc4497aeb7fc137009d_SENGER.webp"; file="assets/logos/senger.webp"},
    @{url="$baseUrl/62387bc4497aeb0f7e370097_fastlease.webp"; file="assets/logos/fast-lease.webp"},
    @{url="$baseUrl/64b7ec453818735960171b7e_TFS.webp"; file="assets/logos/toyota-financial.webp"}
)

foreach ($logo in $partnerLogos) {
    try {
        Invoke-WebRequest -Uri $logo.url -OutFile $logo.file -UseBasicParsing
        Write-Host "Downloaded: $($logo.file)"
    } catch {
        Write-Host "Failed to download: $($logo.url)"
    }
}

# Partner/Mentor logos
$partnersMentors = @(
    @{url="$baseUrl/63aaf1e590b0ca6a41e5ae47_partner_logo_demeter.webp"; file="assets/logos/demeter.webp"},
    @{url="$baseUrl/63aaf1e3805633d73098b65d_partner_logo_turenne-capital.webp"; file="assets/logos/turenne-capital.webp"},
    @{url="$baseUrl/63aaf1e2d827c501002e193c_partner_logo_ces.webp"; file="assets/logos/ces.webp"},
    @{url="$baseUrl/63aaf1e208d0986a8f1f51bf_partner_logo_turenne-groupe.webp"; file="assets/logos/turenne-groupe.webp"},
    @{url="$baseUrl/63aaf1e2c753bdeb43644c48_partner_logo_viva-technology.webp"; file="assets/logos/viva-technology.webp"},
    @{url="$baseUrl/63aaf1e027ff6d1cf5c53148_partner_logo_region-sud.webp"; file="assets/logos/region-sud.webp"},
    @{url="$baseUrl/644103356b79b5bd510f75fa_FEDER_-_REACT_EU_COMMUNICATION_beneficiaires.webp"; file="assets/logos/eu-feder.webp"},
    @{url="$baseUrl/63aaf1dfaba7a896f884be97_partner_logo_reseau-entreprendre.webp"; file="assets/logos/reseau-entreprendre.webp"},
    @{url="$baseUrl/63aaf1dec73ddf63eafac1d9_partner_logo_region-sud-invest.webp"; file="assets/logos/region-sud-invest.webp"},
    @{url="$baseUrl/63aaf1de08d09807341f5175_partner_logo_credit-agricole-aples-provence.webp"; file="assets/logos/credit-agricole.webp"}
)

foreach ($partner in $partnersMentors) {
    try {
        Invoke-WebRequest -Uri $partner.url -OutFile $partner.file -UseBasicParsing
        Write-Host "Downloaded: $($partner.file)"
    } catch {
        Write-Host "Failed to download: $($partner.url)"
    }
}

# Solution images
$solutionImages = @(
    @{url="$baseUrl/6346932c2f835463f70a4949_Sans%20titre%20(47).webp"; file="assets/images/remote-trade-in.webp"},
    @{url="$baseUrl/634691f164a47c6a12956524_Sans%20titre%20(44).webp"; file="assets/images/on-site-trade-in.webp"},
    @{url="$baseUrl/6343f4eee8067d10a144af95_feature-background-image.webp"; file="assets/images/remarketing.webp"},
    @{url="$baseUrl/6343f4f1bfc2e7c07575efd7_feature-inspection-image.webp"; file="assets/images/inspection-api.webp"}
)

foreach ($img in $solutionImages) {
    try {
        Invoke-WebRequest -Uri $img.url -OutFile $img.file -UseBasicParsing
        Write-Host "Downloaded: $($img.file)"
    } catch {
        Write-Host "Failed to download: $($img.url)"
    }
}

# Professional images
$professionalImages = @(
    @{url="$baseUrl/634560b822e815294ebe8653_car-dealership-image.webp"; file="assets/images/car-dealership.webp"},
    @{url="$baseUrl/634560b4ff90d505a5d6d372_car-marketplace-image.webp"; file="assets/images/car-marketplace.webp"},
    @{url="$baseUrl/634560d2c2a4ec71414cc2c4_oem-image.webp"; file="assets/images/oem.webp"},
    @{url="$baseUrl/63c02a0514c79245479d2c06_image_software-publishers.webp"; file="assets/images/software-publishers.webp"},
    @{url="$baseUrl/634560b7fe84b3094f8fceac_car-rental-image.webp"; file="assets/images/car-rental.webp"},
    @{url="$baseUrl/634560d225b2bb39097629a8_carsharing-image.webp"; file="assets/images/carsharing.webp"},
    @{url="$baseUrl/634560b8b4c8942c27392f33_car-insurer-image.webp"; file="assets/images/car-insurer.webp"}
)

foreach ($img in $professionalImages) {
    try {
        Invoke-WebRequest -Uri $img.url -OutFile $img.file -UseBasicParsing
        Write-Host "Downloaded: $($img.file)"
    } catch {
        Write-Host "Failed to download: $($img.url)"
    }
}

# Footer logo
$footerLogo = "$baseUrl/633ef275cbe353d2b6edf3fb_tchek-logo-white.webp"
Invoke-WebRequest -Uri $footerLogo -OutFile "assets/logos/carsee-logo-white.webp" -UseBasicParsing

Write-Host "`nAsset download complete!"
