import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sign from "./pages/sigin.jsx";
// import Check from "./pages/check.jsx";
import DistrictPlaces from "./pages/place.jsx";

function App() { 
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Sign />} />
          {/* <Route path="/check" element={<Check/>}/> */}
          <Route path="/district/:name" element={<DistrictPlaces />} />
          
        </Routes>
      </Router>
    </>
  )
}
export default App
