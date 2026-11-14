import { useState } from "react";
const GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

function Blood_bank({ API_URL, donors, units, setDonors}) {
  const [bloodGroup, setBloodGroup] = useState("");
  const [blood, setBlood] = useState("");
  const [msg, setMsg] = useState("");
  const [eligible, setEligible] = useState([]);

  function filterDonors() {
    let api_url = API_URL + "/donors";
    if (bloodGroup !== "") {
      api_url = API_URL + "/donors?blood_group=" + bloodGroup;
    }
    fetch(api_url)
      .then((res) => res.json())
      .then((data) => setDonors(data));
  }

  function whoCanDonate() {
    fetch(API_URL + "/donors/eligible?blood_group=" + blood)
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setMsg(data.detail);
           setEligible([]);
        } else {
          setMsg("");
          setEligible(data);
        }
      });
  }

  return (
    <div>
      <h2>Blood Bank</h2>
      <p >{msg}</p>
      <h3>Units collected</h3>
      <ul>
        {GROUPS.map((g) => (
          <li>
           {g} = {units[g]}
          </li>
        ))}
      </ul>

      <h3>All donors</h3>
      <select value={bloodGroup} onChange={(b) => setBloodGroup(b.target.value)}>
        <option value="">ALL</option>
        <option value="A%2B">A+</option>
        <option value="A-">A-</option>
        <option value="B%2B">B+</option>
        <option value="B-">B-</option>
        <option value="AB%2B">AB+</option>
        <option value="AB-">AB-</option>  
        <option value="O%2B">O+</option>
        <option value="O-">O-</option>
      </select>
      <button onClick={filterDonors}>Filter</button>
      <ul>
        {donors.map((d) => (
        <li>
        <p>Name: {d.name}</p>
        <p>Roll NO: {d.roll_no}</p>
        <p>Blood Group: {d.blood_group}</p> 
        <p>Weight KG: {d.weight_kg }</p>  
        </li>
        ))}
      </ul>

      <h3>Who can donate?</h3>
      <select value={blood} onChange={(b) => setBlood(b.target.value)}>
        <option value="">BloodGroups Donate </option>
        <option value="A%2B">A+</option>
        <option value="A-">A-</option>
        <option value="B%2B">B+</option>
        <option value="B-">B-</option>
        <option value="AB%2B">AB+</option>
        <option value="AB-">AB-</option>  
        <option value="O%2B">O+</option>
        <option value="O-">O-</option>
      </select> 
      <button onClick={whoCanDonate}>Who can donate?</button>
      <ul>
  {eligible.map((d) => (
    <li key={d.id}>
        <p>Name: {d.name}</p>
        <p>Roll NO: {d.roll_no}</p>
        <p>Blood Group: {d.blood_group}</p> 
        <p>Weight KG: {d.weight_kg }</p> 
    </li>
  ))}
</ul>
     </div>
  );
}

export default Blood_bank;