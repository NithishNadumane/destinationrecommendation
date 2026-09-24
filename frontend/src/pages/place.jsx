import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../css/place.css";

const DistrictPlaces = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // -----------------------------------------
  // Data from previous page
  // -----------------------------------------

  const places = location.state?.places || [];
  const district = location.state?.district || "";
  const districtInfo = location.state?.districtInfo || null;

  // -----------------------------------------
  // Safe weather values
  // -----------------------------------------

  const temperature = districtInfo?.temperature;
  const humidity = districtInfo?.humidity;
  const rain = districtInfo?.precipitation;
  const wind = districtInfo?.wind_speed;

  // -----------------------------------------
  // Navigate to place
  // Works in local + production
  // -----------------------------------------

  const handlePlaceNavigation = (place) => {
    navigate(
      `/destination/${place.district_slug}/${place.place_slug}`
    );
  };

  return (
    <div className="district-page">

      {/* =========================================
          DISTRICT HEADER
      ========================================= */}

      <section className="district-header">

        <div className="district-heading">

          <span className="district-label">
            TRAVEL DESTINATION
          </span>

          <h1>{district}</h1>

          <p>
            Explore recommended places and useful
            travel information for your trip.
          </p>

        </div>

      </section>


      {/* =========================================
          DISTRICT INFORMATION
      ========================================= */}

      {districtInfo && (

        <section className="district-information">

          <div className="info-title">

            <div>

              <span className="section-label">
                DISTRICT INSIGHTS
              </span>

              <h2>
                Today's Travel Information
              </h2>

            </div>

          </div>


          {/* =====================================
              WEATHER FEATURES
          ===================================== */}

          <div className="weather-grid">


            {/* Temperature */}

            <div className="weather-card">

              <div className="weather-icon temperature-icon">
                🌡️
              </div>

              <div className="weather-content">

                <span>
                  Temperature
                </span>

                <strong>
                  {temperature !== undefined &&
                  temperature !== null
                    ? `${temperature}°C`
                    : "--"}
                </strong>

              </div>

            </div>


            {/* Humidity */}

            <div className="weather-card">

              <div className="weather-icon humidity-icon">
                💧
              </div>

              <div className="weather-content">

                <span>
                  Humidity
                </span>

                <strong>
                  {humidity !== undefined &&
                  humidity !== null
                    ? `${humidity}%`
                    : "--"}
                </strong>

              </div>

            </div>


            {/* Rain */}

            <div className="weather-card">

              <div className="weather-icon rain-icon">
                🌧️
              </div>

              <div className="weather-content">

                <span>
                  Rain
                </span>

                <strong>
                  {rain !== undefined &&
                  rain !== null
                    ? `${rain} mm`
                    : "--"}
                </strong>

              </div>

            </div>


            {/* Wind */}

            <div className="weather-card">

              <div className="weather-icon wind-icon">
                💨
              </div>

              <div className="weather-content">

                <span>
                  Wind
                </span>

                <strong>
                  {wind !== undefined &&
                  wind !== null
                    ? `${wind} km/h`
                    : "--"}
                </strong>

              </div>

            </div>

          </div>


          {/* =====================================
              AI TRAVEL INFORMATION
          ===================================== */}

          <div className="travel-insight">

            <div className="insight-icon">
              ✨
            </div>

            <div>

              <span>
                TRAVEL INSIGHT
              </span>

              <p>
                {districtInfo.summary ||
                  districtInfo.description ||
                  "A good destination to explore based on the current conditions."}
              </p>

            </div>

          </div>


          {/* =====================================
              BEST TIME
          ===================================== */}

          {districtInfo.best_time && (

            <div className="best-time-card">

              <div className="best-time-icon">
                ☀️
              </div>

              <div>

                <span>
                  BEST TIME FOR OUTDOOR ACTIVITIES
                </span>

                <p>
                  {districtInfo.best_time}
                </p>

              </div>

            </div>

          )}

        </section>

      )}


      {/* =========================================
          PLACES SECTION
      ========================================= */}

      <section className="places-section">

        <div className="places-heading">

          <div>

            <span className="section-label">
              RECOMMENDED PLACES
            </span>

            <h2>
              Places to Explore
            </h2>

          </div>

          <span className="place-count">
            {places.length} places
          </span>

        </div>


        {/* =====================================
            PLACE CARDS
        ===================================== */}

        <div className="results">

          {places.map((place, i) => (

            <div
              key={i}
              className="result-card"
              onClick={() =>
                handlePlaceNavigation(place)
              }
            >

              {/* =================================
                  IMAGE
              ================================= */}

              <div className="card-image">

                <img
                  src={place.image_url}
                  alt={place.name}
                  onError={(e) => {
                    e.target.style.display = "none";
                  }}
                />

                <div className="overlay"></div>


                {/* Rating */}

                <div className="rating">

                  ⭐{" "}

                  {Number(
                    place.rating || 0
                  ).toFixed(1)}

                </div>


                {/* Place Name */}

                <div className="place-name">

                  <h2>
                    {place.name}
                  </h2>

                  <p>
                    📍 {place.district}
                  </p>

                </div>

              </div>


              {/* =================================
                  CARD CONTENT
              ================================= */}

              <div className="content">

                <div className="details">


                  {/* Distance */}

                  <div className="detail-box">

                    <div className="detail-icon">
                      📍
                    </div>

                    <span>
                      Distance
                    </span>

                    <strong>
                      {Number(
                        place.distance || 0
                      ).toFixed(1)}{" "}
                      km
                    </strong>

                  </div>


                  {/* Category */}

                  <div className="detail-box">

                    <div className="detail-icon">
                      🌲
                    </div>

                    <span>
                      Category
                    </span>

                    <strong>
                      {place.category || "Travel"}
                    </strong>

                  </div>


                  {/* Rating */}

                  <div className="detail-box">

                    <div className="detail-icon">
                      ⭐
                    </div>

                    <span>
                      Rating
                    </span>

                    <strong>
                      {Number(
                        place.rating || 0
                      ).toFixed(1)}
                    </strong>

                  </div>

                </div>


                {/* =================================
                    EXPLORE BUTTON
                ================================= */}

                <button
                  className="explore-btn"
                  onClick={(e) => {

                    // Prevent card click
                    e.stopPropagation();

                    handlePlaceNavigation(place);

                  }}
                >

                  Explore Place

                  <span>
                    →
                  </span>

                </button>

              </div>

            </div>

          ))}

        </div>

      </section>

    </div>
  );
};

export default DistrictPlaces;