import { useState } from "react";
function Donate({ API_URL, rollNo,donor, onDonate,setDonor }) {
  const [name, setName] = useState("");
  const [blood_group, setBloodGroup] = useState("A%2B");
  const [weight_kg, setWeight] = useState("");
  const [drive_date, setDriveDate] = useState("");
  const [slot, setSlot] = useState("morning");
  const[msg, setMsg] = useState("");

    function register() {
    fetch(
      API_URL + "/donors?roll_no=" + rollNo + "&name=" + name +
      "&blood_group=" +blood_group+ "&weight_kg=" + weight_kg,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
         if(data.detail){
          setMsg(data.detail)
        }else{          
              onDonate()}
             });
  }
  function show() {
    fetch(API_URL + "/donors/" + rollNo)
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
            setMsg(data.detail);
        } else {
          setDonor(data);
        }
      });
  }
  function book() {
    fetch(
      API_URL + "/appointments?roll_no=" + rollNo + "&drive_date=" + drive_date + "&slot=" + slot,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
            setMsg(data.detail);
        } else {
          show();
          setDonor(data);
        }
          });
      
  }
  function cancel(id) {
    fetch(API_URL + "/appointments/" + id + "/cancel", { method: "PATCH" })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
            setMsg(data.detail);
        } else {
          show();
          setDonor(data);
        }
          });
        }
   

    return (
    <div>
      <h2>Donate</h2>
      <p>{msg}</p>
      <input placeholder="Name" onChange={(e) => setName(e.target.value)} />
       <select value={blood_group} onChange={(b) => setBloodGroup(b.target.value)}>
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
      <input placeholder="Weight" onChange={(e) => setWeight(e.target.value)} />
      <button onClick={register}>Register</button>
      <button onClick={show}>Show</button>

    {donor !== null && (
      <div>
        <p>Name: {donor.name}</p>
        <p>Blood Group: {donor.blood_group}</p>
        <p>Last Donated: {donor.last_donated_on}</p>

        <input type="date" onChange={(e) => setDriveDate(e.target.value)} />
        <select onChange={(e) => setSlot(e.target.value)}>
          <option>morning</option>
          <option>afternoon</option>
        </select>
        <button onClick={book}>Book</button>

        <ul>
          {donor.appointments.map((a) => (
            <li key={a.id}>
              <p>Drive Date: {a.drive_date}</p>
              <p>Slot: {a.slot}</p>
              <p>Status: {a.status}</p>
              <button onClick={() => cancel(a.id)}>Cancel</button>
            </li>
          ))}
        </ul>
      </div>
     )}
    </div>
  );
}

export default Donate;
