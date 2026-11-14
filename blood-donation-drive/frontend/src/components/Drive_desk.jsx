import { useState } from "react";

function Drive_desk({API_URL, onMark}) {
    const [date, setDate] = useState("")
    const[appointments, setAppointments] = useState([]);
    const[msg, setMsg] = useState("");

    function Onapoint(){
        fetch(API_URL+"/appointments?drive_date="+date)
        .then((responce)=> responce.json())
        .then((data)=> setAppointments(data));
             
    }

    function mark_apoint(id,status){
        fetch(API_URL +"/appointments/"+id+"/status?status="+status,
            {method: "PATCH"})
            .then((responce)=> responce.json())
            .then((data)=> {
                if(data.detail){
                    setMsg(data.detail);
                }else{
                   Onapoint();
                   onMark();
                   }
                  });
    }
    return (
        <div>
            <h3>Drive Desk</h3>
            <input type ="date" value={date} onChange={(d)=> setDate(d.target.value)}/>
            <button onClick ={Onapoint}>Get Appointments</button>
            {msg && <p>{msg}</p>}
            <h4>Morning</h4>

            <ul>
               {appointments.filter((a)=> a.slot ==="morning").map((a)=>
                  (
                      <li>
                      <p>Name : {a.name}</p>
                      <p> blood group : {a.blood_group}</p>
                      <p>Status :{a.status}</p>
                        <button onClick={()=> mark_apoint(a.id,"donated")}>donated</button>
                        <button onClick={()=> mark_apoint(a.id,"no_show")}>no show</button>
                      </li>
                    ))}                                                
            </ul>
            <h4>Afternoon</h4>
            <ol>
               {appointments.filter((a)=> a.slot ==="afternoon").map((a)=>
                  (
                      <li>
                        <p>Name : {a.name}</p>
                        <p> blood group : {a.blood_group}</p>
                        <p>Status :{a.status}</p>
                        <button onClick={()=> mark_apoint(a.id,"donated")}>donated</button>
                        <button onClick={()=> mark_apoint(a.id,"no_show")}>no show</button>
                      </li>
                    ))}
            </ol>
        </div>
    )
}

export default Drive_desk;