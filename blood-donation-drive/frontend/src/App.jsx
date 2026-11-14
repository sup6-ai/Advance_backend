import { useState, useEffect } from "react";

import Donate from "./components/Donate";
import Drive_desk from "./components/Drive_desk";
import Blood_bank from "./components/Blood_bank";


const API_URL = "http://127.0.0.1:8001";

function App() {
    const [rollNo, setRollNo] = useState("");
    const [donors, setDonors] = useState([]);
    const [donor, setDonor] = useState(null);
    const [units, setUnits] = useState({});
 
  function refreshAll() {
    fetch(API_URL + "/donors")
      .then((res) => res.json())
      .then((data) => setDonors(data));
    fetch(API_URL + "/appointments/status/units")
      .then((res) => res.json())
      .then((data) => setUnits(data));
     if (donor !== null) {
      fetch(API_URL + "/donors/" + donor.roll_no)
        .then((res) => res.json())
        .then((data) => setDonor(data));
    }
  }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

useEffect(() => {
  refreshAll();
}, []);

  return (
   
    <div>
      <h1>Blood Donation Drive</h1>


      <input
        placeholder="Enter Roll No: AUXXX"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

     <Donate API_URL={API_URL} rollNo={rollNo} donor={donor} onDonate={refreshAll} setDonor={setDonor} />
      <Drive_desk API_URL={API_URL} onMark={refreshAll} />
      <Blood_bank API_URL={API_URL} donors={donors} units={units} setDonors={setDonors} />
    </div>
  );
}

export default App;