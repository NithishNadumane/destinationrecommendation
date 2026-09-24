import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/form.css";
import District from "./district";

const tripOptions = [
  { name: "Adventure", icon: "⛰️" },
  { name: "Nature", icon: "🌲" },
  { name: "Beach", icon: "🏖️" },
  { name: "Temple", icon: "🛕" },
  { name: "Heritage", icon: "🏛️" }
];

export default function TravelForm() {

  // ---------------- API URL ----------------
  const API_URL = import.meta.env.NEXT_PUBLIC_API_URL;

  // ---------------- Form ----------------
  const [form, setForm] = useState(() => {
    try {
      const saved = localStorage.getItem("travelForm");

      return saved
        ? JSON.parse(saved)
        : {
            location: "",
            max_distance: ""
          };
    } catch {
      return {
        location: "",
        max_distance: ""
      };
    }
  });

  // ---------------- Preferences ----------------
  const [preferences, setPreferences] = useState(() => {
    try {
      const saved = localStorage.getItem("preferences");

      if (saved) {
        const parsed = JSON.parse(saved);

        if (
          Array.isArray(parsed) &&
          parsed.length === tripOptions.length
        ) {
          return parsed;
        }
      }
    } catch {}

    return tripOptions.map((item) => ({
      type: item.name,
      preference: 0
    }));
  });

  // ---------------- Results ----------------
  const [results, setResults] = useState(() => {
    try {
      const saved = localStorage.getItem("results");

      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // ---------------- Save Form ----------------
  useEffect(() => {
    localStorage.setItem(
      "travelForm",
      JSON.stringify(form)
    );
  }, [form]);

  // ---------------- Save Preferences ----------------
  useEffect(() => {
    localStorage.setItem(
      "preferences",
      JSON.stringify(preferences)
    );
  }, [preferences]);

  // ---------------- Save Results ----------------
  useEffect(() => {
    localStorage.setItem(
      "results",
      JSON.stringify(results)
    );
  }, [results]);

  // ---------------- Handle Form Change ----------------
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  // ---------------- Handle Preference Change ----------------
  const handlePreferenceChange = (type, value) => {

    value = value === "" ? 0 : Number(value);

    if (value < 0 || value > 5) {
      return;
    }

    setPreferences((prev) =>
      prev.map((item) =>
        item.type === type
          ? {
              ...item,
              preference: value
            }
          : item
      )
    );
  };

  // ---------------- Submit ----------------
  const handleSubmit = async () => {

    // Check location
    if (!form.location.trim()) {
      alert("Please enter your location.");
      return;
    }

    // Check distance
    if (!form.max_distance) {
      alert("Please enter maximum travel distance.");
      return;
    }

    const payload = {
      location: form.location,
      max_distance: Number(form.max_distance),
      trip_type: preferences
    };

    console.log("Payload:", payload);
    console.log("API URL:", API_URL);

    try {

      const response = await axios.post(
        `${API_URL}api/recommend`,
        payload,
        {
          headers: {
            "Content-Type": "application/json"
          }
        }
      );

      console.log(
        "Response:",
        response.data.results
      );

      setResults(
        response.data.results || []
      );

    } catch (err) {

      console.error("Request Error:", err);

      console.log(
        "Backend Error:",
        err.response?.data
      );

      alert(
        "Failed to fetch recommendations."
      );
    }
  };

  // ---------------- Clear ----------------
  const clearData = () => {

    localStorage.removeItem("travelForm");
    localStorage.removeItem("preferences");
    localStorage.removeItem("results");

    setForm({
      location: "",
      max_distance: ""
    });

    setPreferences(
      tripOptions.map((item) => ({
        type: item.name,
        preference: 0
      }))
    );

    setResults([]);
  };

  // ---------------- UI ----------------
  return (
    <div className="container">

      <h2 className="title">
        Travel Planner
      </h2>

      {/* Location */}
      <input
        className="input"
        name="location"
        placeholder="Enter Current Location"
        value={form.location}
        onChange={handleChange}
      />

      {/* Distance */}
      <input
        className="input"
        name="max_distance"
        type="number"
        placeholder="Maximum One-way Distance (km)"
        value={form.max_distance}
        onChange={handleChange}
      />

      <h3 className="subtitle">
        Travel Preferences
      </h3>

      <p
        style={{
          fontSize: "14px",
          color: "#777",
          marginBottom: "20px",
          lineHeight: "1.7"
        }}
      >
        <strong>Preference Guide</strong>
        <br />
        1 = Highest Priority
        <br />
        2 = High Priority
        <br />
        3 = Medium Priority
        <br />
        4 = Low Priority
        <br />
        5 = Lowest Priority
        <br />
        0 or Empty = Not Preferred
      </p>

      <div className="grid">

        {tripOptions.map((item) => {

          const pref =
            preferences.find(
              (p) => p.type === item.name
            ) || {
              type: item.name,
              preference: 0
            };

          return (
            <div
              className="card"
              key={item.name}
            >

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  marginBottom: "10px"
                }}
              >

                <span className="icon">
                  {item.icon}
                </span>

                <span>
                  {item.name}
                </span>

              </div>

              <input
                className="input"
                type="number"
                min="0"
                max="5"
                placeholder="0-5"
                value={
                  pref.preference === 0
                    ? ""
                    : pref.preference
                }
                onChange={(e) =>
                  handlePreferenceChange(
                    item.name,
                    e.target.value
                  )
                }
              />

            </div>
          );
        })}

      </div>

      {/* Get Recommendations */}
      <button
        className="btn"
        onClick={handleSubmit}
      >
        Get Recommendations
      </button>

      {/* Clear */}
      <button
        className="btn"
        style={{
          marginTop: "10px",
          background: "#dc3545"
        }}
        onClick={clearData}
      >
        Clear
      </button>

      {/* Results */}
      <District results={results} />

    </div>
  );
}