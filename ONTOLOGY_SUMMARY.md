# Ontology Structure Summary

## 1. CROP TYPES AND VARIETIES

### Available Crops (Classes)
- **Maize** - with variety class `Maize_Variety`
- **Cacao** (Cocoa) - with variety class `Cacao_Variety`
- **Cassava** - with variety class `Cassava_Variety`
- **Plantain** - with variety class `Plantain_Variety`

### Variety Structure
Each crop has a corresponding variety subclass with restrictions that ensure:
- Varieties are strictly associated with their parent crop (`isVarietyOf` property)
- Disjointness between different crop varieties

### Variety Properties
Crop varieties have the following attributes:
- `hasCycleDuration` (integer) - duration of growth cycle
- `hasOriginRegion` (string) - geographical origin
- `hasSeedRate` (float) - seed rate for planting
- `hasYield` (float) - expected yield
- `isImprovedVariety` (boolean) - whether it's an improved variety
- `resistantTo` (string) - disease/pest resistance description
- `hasResistanceLevel` (string) - level of resistance
- `adaptedToSoil` (Soil reference) - adapted soil types
- `adaptedToClimate` (Climate reference) - adapted climate conditions

### Growth Stages
- **VegetativeStage** - early growth phase
- **FloweringStage** - reproductive phase
- Generic `GrowthStage` class with `precedes` and `follows` properties for temporal relationships

### Nutrient System
**Nutrients (Classes):**
- `Nutrient` - base nutrient class
- `Micronutrient` - micronutrient subclass

**Nutrient Requirements:**
- `NutrientRequirement` class with properties:
  - `appliesAtGrowthStage` - which growth stage
  - `concernsNutrient` - which nutrient
  - `hasMinRequirement` (integer) - minimum amount
  - `hasMaxRequirement` (integer) - maximum amount
  - `hasRequiredAmount` (integer) - target amount
  - `hasStageSpecificAmount` (float) - stage-specific amount
  - `hasUnit` (string) - unit of measurement (e.g., kg/ha)
  - `dependsOnSoil` - soil property dependency
  - `dependsOnClimate` - climate dependency

**Nutrient Levels:**
- `NitrogenLevel` - nitrogen availability classification
- `PhosphorusLevel` - phosphorus availability classification
- `PotassiumLevel` - potassium availability classification

### Crop Temperature Requirements
- `TemperatureRequirement` class with properties:
  - `hasMinTemp` (float) - minimum temperature (°C)
  - `hasMaxTemp` (float) - maximum temperature (°C)
  - `hasOptimalMinTemp` (float) - optimal minimum temperature
  - `hasOptimalMaxTemp` (float) - optimal maximum temperature

---

## 2. SOIL PROPERTIES AND TYPES

### Soil Base Classes
- **`Soil`** - main soil entity class
- **`SoilProperty`** - general soil property category
- **`SoilTexture`** - soil texture classification
- **`SoilPH`** - pH level classification
- **`OrganicMatter`** - organic matter content
- **`CEC`** - Cation Exchange Capacity

### Soil Data Properties
- `hasSoilPH` (float) - pH value (0-14 scale)
- `hasOrganicMatter` (float) - percentage of organic matter
- `hasCEC` (float) - Cation Exchange Capacity value

### Nutrient Level Classification

#### Nitrogen Levels (3 classes)
- **LowNitrogen** - insufficient nitrogen
- **MediumNitrogen** - adequate nitrogen
- **HighNitrogen** - excess nitrogen

#### Phosphorus Levels (3 classes)
- **LowPhosphorus** - insufficient phosphorus
- **MediumPhosphorus** - adequate phosphorus
- **HighPhosphorus** - excess phosphorus

#### Potassium Levels (3 classes)
- **LowPotassium** - insufficient potassium
- **MediumPotassium** - adequate potassium
- **HighPotassium** - excess potassium

### Soil Fertility Status (SoilFertilityStatus)
Classification of overall soil health:
- **PoorNitrogenSoil** - low nitrogen fertility
- **RichNitrogenSoil** - high nitrogen fertility
- **PoorPhosphorusSoil** - low phosphorus fertility
- **RichPhosphorus** - high phosphorus fertility
- **PoorPotassiumSoil** - low potassium fertility
- **RichPotassium** - high potassium fertility

### NutrientLevel Class
- `hasValue` (float) - numeric value of nutrient
- `hasUnit` (string) - unit of measurement (e.g., mg/kg, ppm)
- `concernsNutrient` - links to specific nutrient
- Properties: `hasNitrogenLevel`, `hasPhosphorusLevel`, `hasPotassiumLevel` (subproperties of `hasNutrientLevel`)

---

## 3. CLIMATE PARAMETERS AND RANGES

### Main Climate Parameters (ClimateParameter subclasses)
- **Temperature** - air temperature measurements
- **Precipitation** - rainfall amount
- **Humidity** - atmospheric moisture content
- **CloudCover** - cloud coverage percentage
- **Wind** - wind speed and direction
- **Pressure** - atmospheric pressure
- **Rainfall** - alternative precipitation measurement
- **SolarRadiation** - solar energy received

### Climate Parameter Data Properties
- `hasValue` (float) - numeric value of parameter
- `hasUnit` (string) - unit of measurement

### Wind-specific Properties
- `hasSpeed` (float) - wind speed (m/s or km/h)
- `hasDirection` (float) - wind direction (degrees)

### CloudCover-specific Properties
- `hasCloudiness` (float) - cloudiness percentage (0-100%)

### Temperature Level Categories
- **OptimalTemperature** - ideal temperature range
- **HighTemperature** - elevated temperature
- **LowTemperature** - reduced temperature

### Precipitation/Rainfall Level Categories
- **OptimalPrecipitation** - ideal rain amount
- **HighPrecipitation** - excessive rainfall (> 10 units)
- **LowPrecipitation** - insufficient rainfall
- **HighRainfall** - heavy rainfall (SWRL rule: value > 10)
- **ModerateRainfall** (SWRL rule: value >= 2 AND < 10)
- **LowRainfall** - light rainfall

### Humidity Level Categories
- **OptimalHumidity** - ideal humidity range
- **HighHumidity** - high moisture levels
- **LowHumidity** - low moisture levels

### Wind Level Categories
- **OptimalWind** - ideal wind conditions
- **HighWind** - strong winds
- **LowWind** - calm conditions

### Other Levels
- **PressureLevel** - atmospheric pressure classification
- **CoudCoverLevel** (note: typo in ontology - "Coud" instead of "Cloud")

### SWRL Rules
The climate ontology includes SWRL (Semantic Web Rule Language) rules that automatically classify rainfall:
- **HighRainfall rule**: If Precipitation.hasValue > 10, then classify as HighRainfall
- **ModerateRainfall rule**: If Precipitation.hasValue >= 2 AND < 10, then classify as ModerateRainfall

---

## 4. AGRICULTURAL PRACTICES

### Main Practice Categories (subclasses of AgriculturalPractice)

#### Irrigation
- **`Irrigation`** - base irrigation class
  - **`DripIrrigation`** - targeted drip irrigation
  - **`SprinklerIrrigation`** - overhead sprinkler system

#### Fertilization
- **`Fertilization`** - base fertilization class
  - **`NitrogenFertilization`** - nitrogen application (e.g., NitrogenFertilization_1 instance)
  - **`PhosphorusFertilization`** - phosphorus application
  - **`PotassiumFertilization`** - potassium application
  - **`OrganicFertilization`** - organic fertilizer application

#### Soil Amendment
- **`SoilAmendment`** - base soil amendment class
  - **`Liming`** - pH adjustment with lime
  - **`OrganicMatterAddition`** - compost/organic matter addition

#### Other Practices
- **`Drainage`** - water drainage management
- **`PestControl`** - pest management
- **`CropManagement`** - general crop management
- **`FungicideTreatment`** - fungicide application

### Agricultural Practice Properties
- `hasApplicationRate` (float) - rate of application per area
- `hasFrequency` (string) - frequency (e.g., "weekly", "monthly")
- `hasMinDose` (float) - minimum dosage/amount
- `hasMaxDose` (float) - maximum dosage/amount
- `hasRecommendedDose` (float) - recommended dosage
- `hasMethod` (string) - application method description
- `hasUnit` (string) - unit of measurement (e.g., kg/ha, L/ha)

### Practice Requirements Classes
Structures for specifying when practices are needed:
- **`PracticeRequirement`** - base requirement class
- **`IrrigationRequirement`** - specifies irrigation needs (via `hasPractice`)
- **`FertilizationRequirement`** - specifies fertilization needs
- **`DrainageRequirement`** - specifies drainage needs
- **`TreatmentRequirement`** - specifies treatment/pesticide/fungicide needs

All requirements link to their corresponding practices via `hasPractice` object property.

### Practice Relationships
- Practices can be linked to crop varieties through nutrient and soil requirements
- Practices are recommended based on:
  - Current soil fertility status
  - Climate conditions
  - Crop growth stage
  - Nutrient deficiency/excess levels

---

## 5. CROSS-ONTOLOGY RELATIONSHIPS

### Crop ↔ Soil
- Varieties are `adaptedToSoil` (specific soil types)
- Nutrient requirements `dependsOnSoil` (soil properties)
- Soil fertility status determines fertilization practices

### Crop ↔ Climate
- Varieties are `adaptedToClimate`
- Nutrient requirements `dependsOnClimate`
- Growth stages have temperature requirements
- Weather-dependent practices (irrigation during low rainfall, fungicides in high humidity)

### Practices ↔ Soil & Climate
- Fertilization practices correct soil nutrient deficiencies
- Irrigation responds to precipitation levels
- Drainage manages excess moisture
- Liming adjusts soil pH
- Pest/fungicide treatments respond to climate conditions

### Nutrient Cycle
```
Crop Variety
  ├─ hasNutrientRequirement → NutrientRequirement
  │   ├─ concernsNutrient → Nutrient (N, P, K, micronutrients)
  │   ├─ appliesAtGrowthStage → GrowthStage
  │   ├─ dependsOnSoil → SoilProperty
  │   └─ dependsOnClimate → Climate
  └─ Soil has NutrientLevel
      ├─ HighNitrogen/LowNitrogen etc.
      └─ determines → Fertilization practice required
```

---

## 6. CURRENT INSTANCES/INDIVIDUALS

The ontology currently defines minimal instances:
- **crop#Maize** - Maize crop individual
- **Soil#LowNitrogen** - Low nitrogen soil condition individual
- **practice#NitrogenFertilization_1** - A specific nitrogen fertilization practice

Most content is organized as classes awaiting instantiation with real-world data.

---

## 7. KEY DESIGN PATTERNS

1. **Hierarchical Classification**: Three-level hierarchy for nutrients (Low/Medium/High)
2. **Stage-based Requirements**: Nutrient and input needs vary by growth stage
3. **Multi-factor Dependencies**: Recommendations depend on crop + soil + climate
4. **SWRL Rules**: Automated classification of climate parameters based on thresholds
5. **Disjointness**: Crop varieties are mutually exclusive from different crops
6. **Cardinality Constraints**: Each variety belongs to exactly one crop

---

## 8. MEASUREMENT UNITS

The ontology uses `hasUnit` properties to store units as strings. Common units in use:
- **Nutrients**: mg/kg, ppm, kg/ha, %
- **Climate**: °C, mm, %, m/s, hPa
- **Practices**: kg/ha, L/ha, number of applications
- **Soil**: %, cmol/kg, pH units

