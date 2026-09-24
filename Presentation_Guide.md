# Urban Planner - Capstone Presentation Guide


## Project Overview & Objectives

### Speaking Points
* **Introduction:** Introduce the team and the project "Urban Planner". 
* **The Problem:** Urban planning is often hindered by fragmented, static datasets. City planners struggle to overlay environmental variables (like air quality) with demographic variables (like population density) and infrastructural data (like existing buildings or airports) dynamically.
* **The Solution:** We built an interactive, scalable, data-driven urban analysis platform. It allows stakeholders to visualize spatial data seamlessly and make informed decisions on city development—specifically, where to place new "Green Spaces".
* **Key Achievements:** We successfully integrated machine learning (KNN) for spatial interpolation, developed custom scoring algorithms for land evaluation, and deployed an interactive dashboard using Plotly Dash.

### Potential Questions & Answers
* **Q:** *Why did you choose this specific problem for your capstone?*
  * **A:** As cities grow, sustainable development is critical. We wanted to bridge the gap between complex environmental data and actionable city planning.
* **Q:** *Who is the target audience for this application?*
  * **A:** Urban planners, municipal governments, environmental agencies, and real estate developers looking to assess environmental impact.

---

## Data Processing & Pipeline Architecture

### Speaking Points
* **Data Ingestion:** Our data pipeline handles multiple geographic datasets. We pull data either from local CSV files or dynamically from an AWS S3 bucket using the `boto3` library.
* **Spatial Interpolation (ML):** Because environmental data (like Carbon Monoxide, Nitrogen Dioxide) isn't available for every single coordinate, we utilized K-Nearest Neighbors (KNN) regression (`KNeighborsRegressor` with the Haversine metric for spherical distance). This allows us to predict the air quality metric at any given latitude and longitude based on surrounding sensor data.
* **Performance Optimization:** We implemented multiprocessing (`multiprocess` pool) to apply these complex geographical calculations across large dataframes concurrently, significantly speeding up the pipeline.
* **Pickling Models:** To optimize the dashboard's runtime, we serialize (pickle) our trained KNN models and upload them to AWS S3. This ensures the dashboard can retrieve predictions quickly without retraining.

### Potential Questions & Answers
* **Q:** *Why did you use KNN for spatial interpolation instead of other algorithms?*
  * **A:** KNN is highly effective for spatial data when combined with the Haversine distance metric. It intuitively estimates a point's value based on its closest geographic neighbors, which accurately reflects how air pollution disperses.
* **Q:** *What challenges did you face when processing the data?*
  * **A:** The sheer volume of geographic coordinates made calculations very slow. We overcame this by parallelizing the row operations using python's `multiprocess` module.

---

## Core Metrics & Algorithms

### Speaking Points
* **The Air Quality (AQ) Score:** We calculate a composite AQ score by normalizing five different metrics (CO, NO2, O3, SO2, and Aerosol Index). Each pollutant contributes 20% to the final score, where a lower score indicates better air quality.
* **The Green Space Score Algorithm:** This is the heart of our platform. We determine the optimal location for new parks/green spaces by evaluating:
  1. **Population Density:** Areas with higher density but lower existing greenspace per capita are prioritized.
  2. **Air Quality:** Areas with poor air quality receive a higher need for green spaces.
  3. **Distance to Existing Parks:** We use a `BallTree` algorithm to calculate the distance to the nearest 3 green spaces. Areas further away from existing parks are rewarded.
* **Land Type Penalty/Reward:** We built a contextual multiplier. For example, if a coordinate is over an airport or a water body, it's penalized heavily (score drops to 0) because we can't build a park there. If it's over an urban area, it's rewarded.

### Potential Questions & Answers
* **Q:** *How did you determine the weighting for the Green Space Score?*
  * **A:** We based our population density weighting on the World Health Organization (WHO) standard, which recommends an ideal 50m² of green space per capita. Areas falling short of this standard are weighted more heavily.
* **Q:** *How do you prevent the algorithm from recommending a park in the middle of a lake?*
  * **A:** We introduced a 'Penalty/Reward' multiplier. Water bodies and Airports have a multiplier of 0, which zeroes out the final Green Space Score for those coordinates.

---

## Dashboard & Visualization

### Speaking Points
* **UI Framework:** We built the front-end using Plotly Dash, which allows for pure Python-based reactive web applications.
* **Mapbox Integration:** We utilized Plotly Express and Figure Factory to render interactive Mapbox maps. Users can seamlessly pan, zoom, and explore the geographic data.
* **Visualization Techniques:**
  * **Hexbin Maps:** For high-density data, we used `create_hexbin_mapbox` to aggregate points into hexagons. This prevents the map from becoming cluttered and shows clear concentration zones.
  * **Scatter Maps:** For specific land types (like buildings or existing parks), we overlay point data using `scatter_mapbox` with dynamic color scales (Turbo/Carto-positron).
* **Interactivity:** The dashboard features a dropdown callback system. When a user selects a different metric (e.g., Population Density vs. AQ Ozone), the backend instantly filters the dataframe and regenerates the Plotly figure without reloading the page.

### Potential Questions & Answers
* **Q:** *Why did you choose Plotly Dash over something like React or Tableau?*
  * **A:** Dash integrates natively with our Python data science stack (Pandas, Scikit-Learn). It allowed us to keep the machine learning and the visualization in the same ecosystem, making it highly maintainable.
* **Q:** *If you had more time, how would you improve the dashboard?*
  * **A:** We would add time-series sliders to see how air quality and urban development change over years, and integrate user-drawn bounding boxes to calculate stats for a custom-selected neighborhood.
