import React from "react";
import { useNavigate } from "react-router-dom";
import "../css/district.css";

const Districts = ({ results }) => {

  const navigate = useNavigate();

  const handleViewPlaces = (district) => {

    // Save complete district information
    localStorage.setItem(
      "selectedDistrict",
      JSON.stringify(district)
    );

    navigate(
      `/district/${district.district}`,
      {
        state: {
          district: district.district,

          // Recommended places
          places: district.places,

          // One-line recommendation reason
          reason: district.reason,

          // Weather + AI information
          districtInfo: district.district_info
        }
      }
    );
  };


  return (
    <div className="district-container">

      {results.map((district, i) => (

        <div
          key={i}
          className="district-card"
        >

          {/* District Name */}
          <h2>
            {district.district}
          </h2>


          {/* Recommendation Reason */}
          <p className="district-reason">

            {district.reason ||
              "A good match for your travel preferences."}

          </p>


          {/* View Places */}
          <button
            onClick={() =>
              handleViewPlaces(district)
            }
          >
            View Places
          </button>

        </div>

      ))}

    </div>
  );
};

export default Districts;